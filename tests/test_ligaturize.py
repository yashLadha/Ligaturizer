"""Test bench for ligaturize.py rule-generation logic.

Runs under plain python3 (no fontforge needed): tests/fake_fontforge.py
provides an in-memory implementation of the fontforge API subset that
LigatureCreator uses, and records the generated lookups/rules so tests
can assert on real behavior.

Run with:
    python3 -m unittest discover -s tests -v
"""

import contextlib
import io
import os
import sys
import unittest
from unittest import mock

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TESTS_DIR)
sys.path.insert(0, TESTS_DIR)
sys.path.insert(0, ROOT)

import fake_fontforge
fake_fontforge.install()  # must happen before importing ligaturize

import ligatures
import ligaturize
from fake_fontforge import FakeFont


# ---------------------------------------------------------------------------
# Harness helpers
# ---------------------------------------------------------------------------

def make_target_font():
    font = FakeFont(em=1000)
    font.add_glyph('m', width=600, code=ord('m'))
    font.add_glyph('space', width=600, code=ord(' '))
    for name in ('less', 'equal', 'greater', 'bar', 'slash', 'colon',
                 'exclam', 'question', 'parenleft', 'bracketleft',
                 'bracketright'):
        font.add_glyph(name, width=600)
    return font


def make_creator(firacode_glyphs=()):
    """Build a LigatureCreator over fake fonts.

    firacode_glyphs: glyph names present in the fake source (Fira Code) font.
    """
    font = make_target_font()
    firacode = FakeFont(em=2000)
    for name in firacode_glyphs:
        firacode.add_glyph(name, width=1200)
    creator = ligaturize.LigatureCreator(
        font, firacode,
        scale_character_glyphs_threshold=0.1,
        copy_character_glyphs=False)
    return creator, font, firacode


def quiet(fn, *args, **kwargs):
    """Run fn while swallowing its informational prints."""
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def backtrack_tokens(spec):
    """Glyph names in the backtrack (before the first '|') of a rule spec."""
    return spec.split('|')[0].split()


def equal_arrows_family():
    (family,) = [f for f in ligatures.seq_families
                 if f['name'] == 'equal_arrows']
    return family


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        fake_fontforge._CLIPBOARD = None


# ---------------------------------------------------------------------------
# Fix 1: family_backtrack_seq_glyphs helper
# ---------------------------------------------------------------------------

SYNTH_FAMILY = {
    'name': 'synth',
    'base_char': 'equal',
    'spacer': 'equal.spacer',
    'start_seq': 'x_start.seq',
    'middle_seq': 'x_middle.seq',
    'end_seq': 'x_end.seq',
    'terminators': ['greater'],
    'liga_terminators': ['greater'],
    # A lookup key name the implementation has never seen before: the
    # helper must collect from ANY dict-valued key, not a hardcoded list.
    'novel_future_lookup': {'greater': 'novel_middle.seq'},
    'novel_end_lookup': {'greater': 'novel_end.seq', 'equal': 'x.spacer'},
    # Non-string dict values (like ignore_rules) must not crash it.
    'ignore_rules': {'equal': [{'lookahead': ['equal']}]},
}

# Independent oracle for real families: the pre-refactor inline code
# (the 5-key whitelist that lived in add_seq_ligature) expressed the
# same intent via hardcoded lookup key names. The helper must stay
# equivalent to it for every real family config, so this pins refactor
# equivalence without hardcoding glyph lists that go stale whenever
# ligatures.py is edited.
LEGACY_WHITELIST_KEYS = (
    'middle_lookup', 'single_term_middle_lookup', 'start_spacer_lookup',
    'double_term_start_lookup', 'single_term_start_lookup')


def legacy_backtrack_glyphs(family):
    expected = {family['start_seq'], family['middle_seq']}
    for key in LEGACY_WHITELIST_KEYS:
        for glyph_name in family.get(key, {}).values():
            if glyph_name.endswith('.seq'):
                expected.add(glyph_name)
    return sorted(expected)


class TestFamilyBacktrackSeqGlyphs(BaseTestCase):
    """The single source of truth for 'which .seq glyphs mean a sequence
    is still in progress'. Start/middle glyphs are live context; end
    glyphs are not (a completed ligature must not capture what follows).
    """

    def helper(self, family):
        return ligaturize.family_backtrack_seq_glyphs(family)

    def test_includes_start_and_middle_seq(self):
        result = self.helper(SYNTH_FAMILY)
        self.assertIn('x_start.seq', result)
        self.assertIn('x_middle.seq', result)

    def test_excludes_end_seq_glyphs(self):
        result = self.helper(SYNTH_FAMILY)
        self.assertNotIn('x_end.seq', result)
        self.assertNotIn('novel_end.seq', result)

    def test_collects_from_any_dict_valued_key(self):
        # Key-name independence: a lookup key added in the future must be
        # picked up without editing a whitelist.
        self.assertIn('novel_middle.seq', self.helper(SYNTH_FAMILY))

    def test_ignores_non_seq_and_non_string_values(self):
        result = self.helper(SYNTH_FAMILY)
        self.assertNotIn('x.spacer', result)  # spacers are not seq context

    def test_all_real_families_match_legacy_whitelist_behavior(self):
        for family in ligatures.seq_families:
            with self.subTest(family=family['name']):
                self.assertEqual(self.helper(family),
                                 legacy_backtrack_glyphs(family))


class TestSeqRuleBacktrackBehavior(BaseTestCase):
    """Behavior pin for commit 7d56be2: generated Phase B rules must never
    use an *_end.seq glyph as backtrack context. Guards the helper
    refactor against regressions.
    """

    def test_no_end_seq_glyph_in_any_backtrack(self):
        creator, font, firacode = make_creator()
        quiet(creator.add_seq_ligature, equal_arrows_family())
        seq_backtracks = [tok for (_, _, spec) in font.calt_rules
                         for tok in backtrack_tokens(spec)
                         if tok.endswith('.seq')]
        self.assertTrue(seq_backtracks,
                        'expected some rules with .seq backtrack context')
        end_glyphs = [g for g in seq_backtracks if g.endswith('_end.seq')]
        self.assertEqual(end_glyphs, [])


# ---------------------------------------------------------------------------
# Fix 2: prefer the pre-drawn .liga glyph over seq_components composition
# ---------------------------------------------------------------------------

class TestLigaGlyphPriority(BaseTestCase):
    """add_ligature dispatch: firacode_ligature_name is authoritative
    artwork; seq_components is only a fallback for glyphs Fira Code v6
    dropped. A stale seq_components field must be harmless when the
    .liga glyph exists (the <= bug fixed in commit 38e54fb).
    """

    LIGA = 'less_equal.liga'
    SEQ_COMPONENTS = ['less_equal_start.seq', 'equal_end.seq']

    def add(self, creator, seq_components):
        quiet(creator.add_ligature,
              ['less', 'equal'], self.LIGA, seq_components)

    def lig_glyphs(self, font):
        return [g for name, g in font.glyphs.items() if name.startswith('lig.')]

    def test_prefers_liga_when_present_even_with_seq_components(self):
        creator, font, firacode = make_creator(
            firacode_glyphs=[self.LIGA] + self.SEQ_COMPONENTS)
        self.add(creator, self.SEQ_COMPONENTS)

        (lig,) = self.lig_glyphs(font)
        self.assertEqual(lig.pasted_from, self.LIGA,
                         'ligature glyph must come from the pre-drawn .liga')
        self.assertEqual(font.paste_into_ops, [],
                         'seq composition must not run when .liga exists')

    def test_falls_back_to_seq_components_when_liga_missing(self):
        creator, font, firacode = make_creator(
            firacode_glyphs=self.SEQ_COMPONENTS)  # no .liga in source
        self.add(creator, self.SEQ_COMPONENTS)

        (lig,) = self.lig_glyphs(font)
        self.assertEqual(lig.pasted_from, self.SEQ_COMPONENTS[0],
                         'ligature glyph must be composed from seq parts')
        self.assertTrue(font.paste_into_ops,
                        'composition must overlay the remaining components')

    def test_skips_ligature_when_source_has_neither(self):
        creator, font, firacode = make_creator(firacode_glyphs=[])
        self.add(creator, self.SEQ_COMPONENTS)

        self.assertEqual(self.lig_glyphs(font), [])
        self.assertEqual(font.calt_rules, [])

    def test_plain_liga_entry_still_works(self):
        # Entries without seq_components (the traditional path).
        creator, font, firacode = make_creator(firacode_glyphs=[self.LIGA])
        self.add(creator, None)

        (lig,) = self.lig_glyphs(font)
        self.assertEqual(lig.pasted_from, self.LIGA)
        self.assertTrue(font.calt_rules)


# ---------------------------------------------------------------------------
# Fix 3: family loop must consider every family (continue, not break)
# ---------------------------------------------------------------------------

FAMILY_ONE = {
    'name': 'family_one',
    'base_char': 'equal',
    'spacer': 'equal.spacer',
    'start_seq': 'f1_start.seq',
    'middle_seq': 'f1_middle.seq',
    'end_seq': 'f1_end.seq',
    'terminators': ['greater'],  # vocab: equal/greater -- no 'bar'
}

FAMILY_TWO = {
    'name': 'family_two',
    'base_char': 'equal',
    'spacer': 'equal.spacer',
    'start_seq': 'f2_start.seq',
    'middle_seq': 'f2_middle.seq',
    'end_seq': 'f2_end.seq',
    'terminators': ['bar'],      # vocab: equal/bar -- matches =|
}


class TestSeqIgnoreRuleFamilyLoop(BaseTestCase):
    """add_ligature adds seq-aware ignore rules per matching family so
    fixed ligatures don't fire inside an active seq context. A vocab
    mismatch on one family must not stop later families from being
    considered (the latent break-instead-of-continue bug).
    """

    LIGA = 'equal_bar.liga'

    def specs_for(self, seq_glyph, font):
        return [spec for (_, _, spec) in font.calt_rules if seq_glyph in spec]

    def add_equal_bar(self, font_families):
        creator, font, firacode = make_creator(firacode_glyphs=[self.LIGA])
        with mock.patch.object(ligatures, 'seq_families', font_families), \
             mock.patch.object(ligaturize, 'seq_families', font_families):
            quiet(creator.add_ligature, ['equal', 'bar'], self.LIGA, None)
        return font

    def test_later_family_not_skipped_by_earlier_vocab_mismatch(self):
        # '=|' is not in family_one's vocab but is in family_two's.
        # family_two must still get its ignore rules.
        font = self.add_equal_bar([FAMILY_ONE, FAMILY_TWO])
        self.assertTrue(self.specs_for('f2_start.seq', font),
                        'family_two ignore rules missing: earlier family '
                        'vocab mismatch aborted the loop')

    def test_mismatched_family_adds_no_rules(self):
        font = self.add_equal_bar([FAMILY_ONE, FAMILY_TWO])
        self.assertEqual(self.specs_for('f1_start.seq', font), [])

    def test_matching_family_rules_present_when_it_is_first(self):
        # Sanity: with family_two alone, its rules are added (proves the
        # positive case does not depend on the fix).
        font = self.add_equal_bar([FAMILY_TWO])
        self.assertTrue(self.specs_for('f2_start.seq', font))


# ---------------------------------------------------------------------------
# Disable the bare 2-char '=<' ligature while keeping <=, =<<, =>
# ---------------------------------------------------------------------------

class TestDisableEqualLessLigature(BaseTestCase):
    """The equal_arrows family lists 'less' as a terminator, which makes
    '=' + '<' ligate into an arrow-like glyph that reads poorly. We disable
    only the bare 2-char '=<' by listing 'less' in the family's
    no_short_terminators: the base->start.seq conversion must not fire for a
    lone trailing terminator, but must still fire when it is part of a longer
    sequence ('=<<') and for other terminators ('=>').
    """

    def start_base_rules(self, font):
        """(input_glyph, lookahead_tokens) for every base->start.seq rule.

        These are the equal_arrows Phase B 'start' rules, identified by the
        'basestart' single-subst lookup they invoke. The recorded spec has
        the form 'backtrack | input @<lookup> | lookahead'.
        """
        rules = []
        for (_lookup, _sub, spec) in font.calt_rules:
            if 'basestart' not in spec:
                continue
            parts = spec.split('|')
            if len(parts) < 3:
                continue
            input_glyph = parts[1].split()[0]
            lookahead = parts[2].split()
            rules.append((input_glyph, lookahead))
        return rules

    def rules(self):
        creator, font, firacode = make_creator()
        quiet(creator.add_seq_ligature, equal_arrows_family())
        return self.start_base_rules(font)

    def test_bare_equal_less_does_not_enter_seq(self):
        rules = self.rules()
        self.assertNotIn(('equal', ['less']), rules,
            "bare '=<' must not convert '=' to a seq start glyph")
        self.assertNotIn(('equal.spacer', ['less']), rules,
            "bare '=<' must not convert a spacer '=' to a seq start glyph")

    def test_equal_greater_still_enters_seq(self):
        # '=>' is unaffected: greater is not a no_short_terminator.
        self.assertIn(('equal', ['greater']), self.rules(),
            "'=>' regressed: '=' no longer enters seq mode before '>'")

    def test_equal_less_less_still_enters_seq(self):
        # '=<<' must still ligate: '=' enters seq mode when 'less' is
        # followed by more sequence content.
        self.assertIn(('equal', ['less', 'less']), self.rules(),
            "'=<<' regressed: '=' no longer enters seq mode before '<<'")


if __name__ == '__main__':
    unittest.main()
