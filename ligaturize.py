#!/usr/bin/env python
#
# usage: fontforge -lang=py ligaturize.py [options]
# Run with --help for detailed options, or use the `build.py` script to
# process lots of fonts at once.
#
# See ligatures.py for a list of all the ligatures (and, optionally, individual
# characters) that will be copied.

import fontforge
import psMat
import os
from os import path
import sys

from ligatures import ligatures, seq_families
from char_dict import char_dict

# Constants
COPYRIGHT = '''
Programming ligatures added by Ilya Skriblovsky from FiraCode
FiraCode Copyright (c) 2015 by Nikita Prokopov'''

def get_ligature_source(fontname):
    # Become case-insensitive
    fontname = fontname.lower()
    for weight in ['Bold', 'SemiBold', 'Retina', 'Medium', 'Regular', 'Light']:
        if fontname.endswith('-' + weight.lower()):
            # Exact match for one of the Fira Code weights
            return 'fonts/fira/distr/ttf/FiraCode-%s.ttf' % weight

    # No exact match. Guess based on weight keywords in the font name.
    if 'extralight' in fontname:
        return 'fonts/fira/distr/ttf/FiraCode-Light.ttf'
    if 'light' in fontname:
        return 'fonts/fira/distr/ttf/FiraCode-Light.ttf'
    if 'retina' in fontname:
        return 'fonts/fira/distr/ttf/FiraCode-Retina.ttf'
    if 'semibold' in fontname:
        return 'fonts/fira/distr/ttf/FiraCode-SemiBold.ttf'
    if 'medium' in fontname:
        return 'fonts/fira/distr/ttf/FiraCode-Medium.ttf'
    if 'bold' in fontname or 'heavy' in fontname or 'black' in fontname:
        return 'fonts/fira/distr/ttf/FiraCode-Bold.ttf'
    return 'fonts/fira/distr/ttf/FiraCode-Regular.ttf'

class LigatureCreator(object):

    def __init__(self, font, firacode,
                 scale_character_glyphs_threshold,
                 copy_character_glyphs):
        self.font = font
        self.firacode = firacode
        self.scale_character_glyphs_threshold = scale_character_glyphs_threshold
        self.should_copy_character_glyphs = copy_character_glyphs
        self._lig_counter = 0

        # Scale firacode to correct em height.
        self.firacode.em = self.font.em
        self.emwidth = self.font[ord('m')].width

    def copy_ligature_from_source(self, ligature_name):
        try:
            self.firacode.selection.none()
            self.firacode.selection.select(ligature_name)
            self.firacode.copy()
            return True
        except ValueError:
            return False

    def correct_character_width(self, glyph):
        """Width-correct copied individual characters (not ligatures!).

        This will correct the horizontal advance of characters to match the em
        width of the output font, and (depending on the width of the glyph, the
        em width of the output font, and the value of the command line option
        --scale-character-glyphs-threshold) optionally horizontally scale it.

        Glyphs that are not horizontally scaled, but which still need horizontal
        advance correction, will be centered instead.
        """

        if glyph.width == self.emwidth:
            # No correction needed.
            return

        widthdelta = float(abs(glyph.width - self.emwidth)) / self.emwidth
        if widthdelta >= self.scale_character_glyphs_threshold:
            # Character is too wide/narrow compared to output font; scale it.
            scale = float(self.emwidth) / glyph.width
            glyph.transform(psMat.scale(scale, 1.0))
        else:
            # Do not scale; just center copied characters in their hbox.
            # Fix horizontal advance first, to recalculate the bearings.
            glyph.width = self.emwidth
            # Correct bearings to center the glyph.
            glyph.left_side_bearing = int((glyph.left_side_bearing + glyph.right_side_bearing) / 2)
            glyph.right_side_bearing = int(glyph.left_side_bearing)

        # Final adjustment of horizontal advance to correct for rounding
        # errors when scaling/centering -- otherwise small errors can result
        # in visible misalignment near the end of long lines.
        glyph.width = self.emwidth


    def copy_character_glyphs(self, chars):
        """Copy individual (non-ligature) characters from the ligature font."""
        if not self.should_copy_character_glyphs:
            return
        print("    ...copying %d character glyphs..." % (len(chars)))

        for char in chars:
            self.firacode.selection.none()
            self.firacode.selection.select(char)
            self.firacode.copy()
            self.font.selection.none()
            self.font.selection.select(char)
            self.font.paste()
            self.correct_character_width(self.font[ord(char_dict[char])])

    def correct_ligature_width(self, glyph):
        """Correct the horizontal advance and scale of a ligature."""

        if glyph.width == self.emwidth:
            return

        # TODO: some kind of threshold here, similar to the character glyph
        # scale threshold? The largest ligature uses 0.956 of its hbox, so if
        # the target font is within 4% of the source font size, we don't need to
        # resize -- but we may want to adjust the bearings. And we can't just
        # center it, because ligatures are characterized by very large negative
        # left bearings -- they advance 1em, but draw from (-(n-1))em to +1em.
        scale = float(self.emwidth) / glyph.width
        glyph.transform(psMat.scale(scale, 1.0))
        glyph.width = self.emwidth

    def compose_seq_ligature(self, seq_components, ligature_name):
        """Compose a ligature from multiple .seq glyph components.

        Fira Code v6 uses .seq glyphs (start/middle/end) for arrows and other
        sequence ligatures instead of single .liga glyphs. This method tiles
        the components left-to-right and merges them into a single glyph.
        """
        n = len(seq_components)

        # Copy first component to get the glyph width (after em rescaling)
        if not self.copy_ligature_from_source(seq_components[0]):
            return False
        self.font.createChar(-1, ligature_name)
        self.font.selection.none()
        self.font.selection.select(ligature_name)
        self.font.paste()
        glyph_width = self.font[ligature_name].width

        # Shift first component into its position
        if n > 1:
            self.font[ligature_name].transform(
                psMat.translate(-(n - 1) * glyph_width, 0))

        # Overlay remaining components at their positions
        for i in range(1, n):
            if not self.copy_ligature_from_source(seq_components[i]):
                return False
            tmp = '_tmp_seq_%d' % i
            self.font.createChar(-1, tmp)
            self.font.selection.none()
            self.font.selection.select(tmp)
            self.font.paste()

            shift_x = -(n - 1 - i) * glyph_width
            if shift_x != 0:
                self.font[tmp].transform(psMat.translate(shift_x, 0))

            self.font.selection.none()
            self.font.selection.select(tmp)
            self.font.copy()
            self.font.selection.none()
            self.font.selection.select(ligature_name)
            self.font.pasteInto()
            self.font.removeGlyph(tmp)

        self.font[ligature_name].width = glyph_width
        return True

    def add_ligature(self, input_chars, firacode_ligature_name,
                     seq_components=None):
        if firacode_ligature_name is None:
            # No ligature name -- we're just copying a bunch of individual characters.
            self.copy_character_glyphs(input_chars)
            return

        self._lig_counter += 1
        ligature_name = 'lig.{}'.format(self._lig_counter)

        if seq_components:
            # Fira Code v6: compose from .seq glyph components
            if not self.compose_seq_ligature(seq_components, ligature_name):
                return
        else:
            # Traditional: copy single .liga glyph
            if not self.copy_ligature_from_source(firacode_ligature_name):
                return
            self.font.createChar(-1, ligature_name)
            self.font.selection.none()
            self.font.selection.select(ligature_name)
            self.font.paste()

        self.correct_ligature_width(self.font[ligature_name])

        self.font.selection.none()
        self.font.selection.select('space')
        self.font.copy()

        lookup_name = lambda i: 'lookup.{}.{}'.format(self._lig_counter, i)
        lookup_sub_name = lambda i: 'lookup.sub.{}.{}'.format(self._lig_counter, i)
        cr_name = lambda i: 'CR.{}.{}'.format(self._lig_counter, i)

        for i, char in enumerate(input_chars):
            self.font.addLookup(lookup_name(i), 'gsub_single', (), ())
            self.font.addLookupSubtable(lookup_name(i), lookup_sub_name(i))

            if char not in self.font:
                # We assume here that this is because char is a single letter
                # (e.g. 'w') rather than a character name, and the font we're
                # editing doesn't have glyphnames for letters.
                self.font[ord(char_dict[char])].glyphname = char

            if i < len(input_chars) - 1:
                self.font.createChar(-1, cr_name(i))
                self.font.selection.none()
                self.font.selection.select(cr_name(i))
                self.font.paste()

                self.font[char].addPosSub(lookup_sub_name(i), cr_name(i))
            else:
                self.font[char].addPosSub(lookup_sub_name(i), ligature_name)

        calt_lookup_name = 'calt.{}'.format(self._lig_counter)
        self.font.addLookup(calt_lookup_name, 'gsub_contextchain', (),
            (('calt', (('DFLT', ('dflt',)),
                       ('arab', ('dflt',)),
                       ('armn', ('dflt',)),
                       ('cyrl', ('SRB ', 'dflt')),
                       ('geor', ('dflt',)),
                       ('grek', ('dflt',)),
                       ('lao ', ('dflt',)),
                       ('latn', ('CAT ', 'ESP ', 'GAL ', 'ISM ', 'KSM ', 'LSM ', 'MOL ', 'NSM ', 'ROM ', 'SKS ', 'SSM ', 'dflt')),
                       ('math', ('dflt',)),
                       ('thai', ('dflt',)))),))
        #print('CALT %s (%s)' % (calt_lookup_name, firacode_ligature_name))
        for i, char in enumerate(input_chars):
            self.add_calt(calt_lookup_name, 'calt.{}.{}'.format(self._lig_counter, i),
                '{prev} | {cur} @<{lookup}> | {next}',
                prev = ' '.join(cr_name(j) for j in range(i)),
                cur = char,
                lookup = lookup_name(i),
                next = ' '.join(input_chars[i+1:]))

        # Add ignore rules
        self.add_calt(calt_lookup_name, 'calt.{}.{}'.format(self._lig_counter, i+1),
            '| {first} | {rest} {last}',
            first = input_chars[0],
            rest = ' '.join(input_chars[1:]),
            last = input_chars[-1])
        self.add_calt(calt_lookup_name, 'calt.{}.{}'.format(self._lig_counter, i+2),
            '{first} | {first} | {rest}',
            first = input_chars[0],
                rest = ' '.join(input_chars[1:]))

        # Add seq-aware ignore rules: block this fixed ligature when
        # preceded by a .seq glyph from the same family, so seq rules
        # take priority in active seq contexts (e.g. prevent === from
        # firing after < in <===).
        from ligatures import seq_families
        for family in seq_families:
            if input_chars[0] != family['base_char']:
                continue
            vocab = set([family['base_char']] + family['terminators']
                        + family.get('compound_terminators', []))
            if not all(c in vocab for c in input_chars):
                break
            # Collect all .seq glyphs from this family for backtrack
            family_seq = set()
            family_seq.add(family['start_seq'])
            family_seq.add(family['middle_seq'])
            for key in ('middle_lookup', 'single_term_middle_lookup',
                        'single_term_start_lookup', 'double_term_start_lookup'):
                if key in family:
                    for gn in family[key].values():
                        if gn.endswith('.seq'):
                            family_seq.add(gn)
            for seq_glyph in sorted(family_seq):
                self.add_calt(calt_lookup_name,
                    'calt.{}.{}'.format(self._lig_counter, i+3),
                    '{seq} | {first} | {rest}',
                    seq=seq_glyph,
                    first=input_chars[0],
                    rest=' '.join(input_chars[1:]))
                i += 1
            break

    def copy_seq_glyphs(self, family):
        """Copy all .seq glyphs for a seq family from Fira Code."""
        # Collect all unique glyph names from the lookup mappings
        seq_glyphs = set()
        for key in ('middle_lookup', 'end_spacer_lookup', 'single_term_middle_lookup',
                     'double_term_end_lookup', 'start_spacer_lookup',
                     'single_term_end_lookup', 'double_term_start_lookup',
                     'double_term_spacer_lookup', 'single_term_start_lookup'):
            if key in family:
                for glyph_name in family[key].values():
                    if glyph_name.endswith('.seq'):
                        seq_glyphs.add(glyph_name)

        copied = 0
        for glyph_name in sorted(seq_glyphs):
            try:
                self.firacode.selection.none()
                self.firacode.selection.select(glyph_name)
                self.firacode.copy()
                self.font.createChar(-1, glyph_name)
                self.font.selection.none()
                self.font.selection.select(glyph_name)
                self.font.paste()
                # Scale glyph horizontally to match target font's cell width.
                # After em-scaling, the glyph is sized for Fira's cell/em ratio
                # which differs from the target font's ratio. We scale to match.
                glyph = self.font[glyph_name]
                if glyph.width != self.emwidth and glyph.width > 0:
                    scale = float(self.emwidth) / glyph.width
                    glyph.transform(psMat.scale(scale, 1.0))
                glyph.width = self.emwidth
                copied += 1
            except ValueError:
                print('    Warning: .seq glyph %s not found in Fira Code' % glyph_name)
        print('    ...copied %d .seq glyphs for %s' % (copied, family['name']))

    def create_spacer_glyph(self, name):
        """Create a blank spacer glyph with the correct width."""
        if name in self.font:
            return
        self.font.createChar(-1, name)
        self.font[name].width = self.emwidth

    def _make_calt_lookup(self, tag):
        """Create a new CALT lookup and return its name."""
        self._lig_counter += 1
        name = 'calt.seq.%s.%d' % (tag, self._lig_counter)
        self.font.addLookup(name, 'gsub_contextchain', (),
            (('calt', (('DFLT', ('dflt',)),
                       ('arab', ('dflt',)),
                       ('armn', ('dflt',)),
                       ('cyrl', ('SRB ', 'dflt')),
                       ('geor', ('dflt',)),
                       ('grek', ('dflt',)),
                       ('lao ', ('dflt',)),
                       ('latn', ('CAT ', 'ESP ', 'GAL ', 'ISM ', 'KSM ', 'LSM ', 'MOL ', 'NSM ', 'ROM ', 'SKS ', 'SSM ', 'dflt')),
                       ('math', ('dflt',)),
                       ('thai', ('dflt',)))),))
        return name

    def _make_single_lookup(self, tag, mapping):
        """Create a SingleSubst lookup and return its name."""
        self._lig_counter += 1
        lk_name = 'lookup.seq.%s.%d' % (tag, self._lig_counter)
        sub_name = 'lookup.seq.sub.%s.%d' % (tag, self._lig_counter)
        self.font.addLookup(lk_name, 'gsub_single', (), ())
        self.font.addLookupSubtable(lk_name, sub_name)
        for src, dst in mapping.items():
            if src in self.font and dst in self.font:
                self.font[src].addPosSub(sub_name, dst)
        return lk_name

    def add_seq_ligature(self, family):
        """Add per-character seq substitution rules for an arrow family.

        This implements Fira Code's two-phase approach using glyph-type
        contextual rules (coverage type crashes this FontForge version).
        Phase A: Convert interior base chars to spacers
        Phase B: Convert spacers and remaining chars to positional .seq glyphs

        NOTE: FontForge reverses CALT lookup insertion order, so we add
        Phase B first (appears last in output) and Phase A second (appears
        first in output). This ensures Phase A runs before Phase B.
        """
        base = family['base_char']
        spacer = family['spacer']
        name = family['name']
        terminators = family['terminators']
        compound_terminators = family.get('compound_terminators', [])

        print('    ...adding seq ligature rules for %s' % name)

        # Ensure spacer glyphs exist
        self.create_spacer_glyph(spacer)
        for t in terminators:
            self.create_spacer_glyph('%s.spacer' % t)

        # Create all single subst helper lookups upfront.
        # Augment mappings: after Phase A converts base -> spacer, Phase B
        # needs to match the spacer glyph too. Add spacer -> seq entries.
        def augment_with_spacer(mapping):
            aug = dict(mapping)
            if base in aug:
                aug[spacer] = aug[base]
            return aug

        spacer_lk = self._make_single_lookup('%s.spacer' % name, {base: spacer})
        middle_lk = self._make_single_lookup('%s.mid' % name, augment_with_spacer(family['middle_lookup']))
        end_spacer_lk = self._make_single_lookup('%s.endspc' % name, augment_with_spacer(family['end_spacer_lookup']))
        single_term_mid_lk = self._make_single_lookup('%s.stmid' % name, augment_with_spacer(family['single_term_middle_lookup']))
        double_term_end_lk = self._make_single_lookup('%s.dtend' % name, augment_with_spacer(family['double_term_end_lookup']))
        start_spacer_lk = self._make_single_lookup('%s.stspc' % name, augment_with_spacer(family['start_spacer_lookup']))
        single_term_end_lk = self._make_single_lookup('%s.stend' % name, family['single_term_end_lookup'])
        double_term_start_lk = self._make_single_lookup('%s.dtstart' % name, family['double_term_start_lookup'])
        double_term_spacer_lk = self._make_single_lookup('%s.dtspc' % name, family['double_term_spacer_lookup'])
        single_term_start_lk = self._make_single_lookup('%s.ststart' % name, family['single_term_start_lookup'])
        start_base_lk = self._make_single_lookup('%s.basestart' % name,
            {base: family['start_seq'], spacer: family['start_seq']})

        st_idx = [0]

        def add_rule(calt, spec):
            sub_name = 'calt.seq.%s.%d.%d' % (name, self._lig_counter, st_idx[0])
            st_idx[0] += 1
            self.font.addContextualSubtable(calt, sub_name, 'glyph', spec)

        seq_glyphs = [family['start_seq'], family['middle_seq']]
        # Include start and middle .seq glyphs from lookup mappings so
        # Phase B rules fire when any active family seq glyph is in
        # backtrack context. Exclude *_end.seq glyphs: once a sequence
        # is terminated, subsequent characters must not see a live seq
        # context (matching Fira Code's backtrack behavior).
        for key in ('middle_lookup', 'single_term_middle_lookup',
                    'start_spacer_lookup', 'double_term_start_lookup',
                    'single_term_start_lookup'):
            if key in family:
                for glyph_name in family[key].values():
                    if glyph_name.endswith('.seq') and glyph_name not in seq_glyphs:
                        seq_glyphs.append(glyph_name)

        def add_seq_rules(calt, spec_template):
            for sg in seq_glyphs:
                add_rule(calt, spec_template.replace('{seq}', sg))

        # ===== PHASE B (added first so FontForge places it AFTER Phase A) =====
        # NOTE: FontForge reverses subtable order within a lookup.
        # We add rules from LEAST specific to MOST specific. After reversal,
        # most specific (with backtrack) appear first in output.
        calt_b = self._make_calt_lookup('%s.B' % name)

        # --- LEAST SPECIFIC: Start rules (no backtrack, added first -> last in output) ---

        # Start rules: match base or spacer as input (Phase A may have
        # already converted the first position to a spacer).
        start_inputs = [base, spacer]

        # Start: base/spacer followed by terminator (e.g. =>, =|)
        for si in start_inputs:
            for target in terminators + compound_terminators:
                add_rule(calt_b, '| %s @<%s> | %s' % (si, start_base_lk, target))

        # Start: base/spacer followed by base+terminator (e.g. ==>)
        for si in start_inputs:
            for target in terminators + compound_terminators:
                add_rule(calt_b, '| %s @<%s> | %s %s' % (si, start_base_lk, base, target))
                add_rule(calt_b, '| %s @<%s> | %s %s' % (si, start_base_lk, spacer, target))

        # Start: base/spacer followed by 3+ base/spacer chars
        for si in start_inputs:
            for la1 in [base, spacer]:
                for la2 in [base, spacer]:
                    add_rule(calt_b, '| %s @<%s> | %s %s %s' % (
                        si, start_base_lk, la1, la2, base))
                    add_rule(calt_b, '| %s @<%s> | %s %s %s' % (
                        si, start_base_lk, la1, la2, spacer))

        # Start: base/spacer followed by 2 base/spacer chars (3-char sequences)
        if family.get('seq_handles_triple', False):
            for si in start_inputs:
                for la1 in [base, spacer]:
                    add_rule(calt_b, '| %s @<%s> | %s %s' % (
                        si, start_base_lk, la1, base))
                    add_rule(calt_b, '| %s @<%s> | %s %s' % (
                        si, start_base_lk, la1, spacer))

        # Start: base+base+terminator patterns (e.g. ===>)
        for target in terminators + compound_terminators:
            add_rule(calt_b, '| %s @<%s> | %s %s %s' % (
                base, start_base_lk, base, base, target))
            add_rule(calt_b, '| %s @<%s> | %s %s %s' % (
                base, start_base_lk, spacer, spacer, target))
            add_rule(calt_b, '| %s @<%s> | %s %s %s' % (
                base, start_base_lk, spacer, base, target))

        # Start: single terminator
        liga_terms = set(family.get('liga_terminators', []))
        for t in terminators:
            if t in liga_terms:
                # This terminator has a .liga for the 2-char case (e.g. <=, >=).
                # Only enter seq mode when followed by base + more seq content,
                # so the fixed .liga handles the bare 2-char case.
                for la in [base, spacer] + terminators + compound_terminators:
                    add_rule(calt_b, '| %s @<%s> | %s %s' % (t, single_term_start_lk, base, la))
                    add_rule(calt_b, '| %s @<%s> | %s %s' % (t, single_term_start_lk, spacer, la))
            else:
                add_rule(calt_b, '| %s @<%s> | %s' % (t, single_term_start_lk, base))
                add_rule(calt_b, '| %s @<%s> | %s' % (t, single_term_start_lk, spacer))

        # Start: double terminator
        for t in terminators:
            t_spacer = '%s.spacer' % t
            add_rule(calt_b, '| %s @<%s> | %s %s' % (t, double_term_spacer_lk, t, base))
            add_rule(calt_b, '| %s @<%s> | %s %s' % (t, double_term_spacer_lk, t, spacer))
            add_rule(calt_b, '%s | %s @<%s> | %s' % (t_spacer, t, double_term_start_lk, base))
            add_rule(calt_b, '%s | %s @<%s> | %s' % (t_spacer, t, double_term_start_lk, spacer))

        # --- MEDIUM SPECIFIC: End/terminator rules (with seq backtrack) ---

        # Single term end: seq + t -> single_term_end
        for t in terminators:
            add_seq_rules(calt_b, '{seq} | %s @<%s> |' % (t, single_term_end_lk))

        # Double term end: seq + t.spacer + t -> double_term_end
        for t in terminators:
            t_spacer = '%s.spacer' % t
            for sg in seq_glyphs:
                add_rule(calt_b, '%s | %s @<%s> | %s' % (sg, t, start_spacer_lk, t))
            for sg in seq_glyphs:
                add_rule(calt_b, '%s %s | %s @<%s> |' % (sg, t_spacer, t, double_term_end_lk))

        # Single terminator: seq + t + base -> single_term_middle
        for t in terminators:
            add_seq_rules(calt_b, '{seq} | %s @<%s> | %s' % (t, single_term_mid_lk, base))

        # Double term: seq + t.spacer + t + base -> middle
        for t in terminators:
            t_spacer = '%s.spacer' % t
            for sg in seq_glyphs:
                add_rule(calt_b, '%s | %s @<%s> | %s %s' % (sg, t, end_spacer_lk, t, base))
            for sg in seq_glyphs:
                add_rule(calt_b, '%s %s | %s @<%s> | %s' % (sg, t_spacer, t, middle_lk, base))

        # End of run: seq + base (nothing after) -> end_spacer
        add_seq_rules(calt_b, '{seq} | %s @<%s> |' % (base, end_spacer_lk))
        add_seq_rules(calt_b, '{seq} | %s @<%s> |' % (spacer, end_spacer_lk))

        # --- MOST SPECIFIC: Interior/middle rules (with seq backtrack, added last -> first in output) ---

        # Interior: seq + compound_term + base -> middle
        for ct in compound_terminators:
            add_seq_rules(calt_b, '{seq} | %s @<%s> | %s' % (ct, middle_lk, base))
            add_seq_rules(calt_b, '{seq} | %s @<%s> | %s' % (ct, middle_lk, spacer))

        # Interior: seq + base + [base or any term] -> middle
        for input_g in [base, spacer]:
            for target in [base, spacer] + terminators + compound_terminators:
                add_seq_rules(calt_b, '{seq} | %s @<%s> | %s' % (input_g, middle_lk, target))

        # --- Ignore rules (added last, will appear BEFORE all action in output) ---
        for t in terminators:
            add_rule(calt_b, '%s | %s | %s %s' % (t, t, t, base))
            add_rule(calt_b, '%s | %s | %s' % (t, t, base))
            for sg in seq_glyphs:
                add_rule(calt_b, '%s | %s | %s %s' % (sg, t, t, t))
        # Prevent base from entering seq mode when followed by 3+ same
        # terminators (e.g. ->>> should use the fixed >>> ligature, not seq).
        for t in terminators:
            add_rule(calt_b, '| %s | %s %s %s' % (base, t, t, t))

        # ===== PHASE A (added second so FontForge places it BEFORE Phase B) =====
        # NOTE: FontForge reverses subtable order within a lookup, so we add
        # action rules FIRST and ignore rules SECOND. Output will be:
        # ignore rules first (correct), action rules second.
        calt_a = self._make_calt_lookup('%s.A' % name)

        # Action rules (added first, will appear AFTER ignore in output)
        add_rule(calt_a, '%s | %s @<%s> | %s' % (spacer, base, spacer_lk, base))
        add_rule(calt_a, '| %s @<%s> | %s %s' % (base, spacer_lk, base, base))

        # Ignore rules (added second, will appear BEFORE action in output)
        import itertools
        for ignore_char, rules in family.get('ignore_rules', {}).items():
            for rule in rules:
                bt_slots = rule.get('backtrack', [])
                la_slots = rule.get('lookahead', [])
                bt_options = [s if isinstance(s, list) else [s] for s in bt_slots]
                la_options = [s if isinstance(s, list) else [s] for s in la_slots]
                bt_combos = list(itertools.product(*bt_options)) if bt_options else [()]
                la_combos = list(itertools.product(*la_options)) if la_options else [()]
                for bt_combo in bt_combos:
                    for la_combo in la_combos:
                        parts = list(bt_combo) + ['| %s |' % ignore_char] + list(la_combo)
                        add_rule(calt_a, ' '.join(parts))

    def add_calt(self, calt_name, subtable_name, spec, **kwargs):
        spec = spec.format(**kwargs)
        #print('    %s: %s ' % (subtable_name, spec))
        self.font.addContextualSubtable(calt_name, subtable_name, 'glyph', spec)


def replace_sfnt(font, key, value):
    font.sfnt_names = tuple(
        (row[0], key, value)
        if row[1] == key
        else row
        for row in font.sfnt_names
    )

def update_font_metadata(font, new_name):
    # Figure out the input font's real name (i.e. without a hyphenated suffix)
    # and hyphenated suffix (if present)
    old_name = font.familyname
    try:
        suffix = font.fontname.split('-')[1]
    except IndexError:
        suffix = None

    # Replace the old name with the new name whether or not a suffix was present.
    # If a suffix was present, append it accordingly.
    font.familyname = new_name
    if suffix:
        font.fullname = "%s %s" % (new_name, suffix)
        font.fontname = "%s-%s" % (new_name.replace(' ', ''), suffix)
    else:
        font.fullname = new_name
        font.fontname = new_name.replace(' ', '')

    print("Ligaturizing font %s (%s) as '%s'" % (
        path.basename(font.path), old_name, new_name))

    font.copyright = (font.copyright or '') + COPYRIGHT
    replace_sfnt(font, 'UniqueID', '%s; Ligaturized' % font.fullname)
    replace_sfnt(font, 'Preferred Family', new_name)
    replace_sfnt(font, 'Compatible Full', new_name)
    replace_sfnt(font, 'Family', new_name)
    replace_sfnt(font, 'WWS Family', new_name)

def ligaturize_font(input_font_file, output_dir, ligature_font_file,
                    output_name, prefix, **kwargs):
    font = fontforge.open(input_font_file)

    if not ligature_font_file:
        ligature_font_file = get_ligature_source(font.fontname)

    if output_name:
        name = output_name
    else:
        name = font.familyname
    if prefix:
        name = "%s %s" % (prefix, name)

    update_font_metadata(font, name)

    print('    ...using ligatures from %s' % ligature_font_file)
    firacode = fontforge.open(ligature_font_file)

    creator = LigatureCreator(font, firacode, **kwargs)

    # Copy seq glyphs first (needed before any ligature processing)
    for family in seq_families:
        try:
            creator.copy_seq_glyphs(family)
        except Exception as e:
            print('Exception while copying seq glyphs: {}'.format(family['name']))
            raise

    # Add traditional fixed-length ligatures first (skip seq-handled ones).
    # FontForge reverses CALT lookup insertion order, so these end up LAST
    # in the feature, which is correct -- seq rules must fire before them.
    ligature_length = lambda lig: len(lig['chars'])
    for lig_spec in sorted(ligatures, key=ligature_length):
        if lig_spec.get('handled_by_seq'):
            continue
        try:
            creator.add_ligature(lig_spec['chars'],
                                 lig_spec['firacode_ligature_name'],
                                 lig_spec.get('seq_components'))
        except Exception as e:
            print('Exception while adding ligature: {}'.format(lig_spec))
            raise

    # Add seq rules LAST so FontForge places them FIRST in CALT feature.
    # Phase B must come before Phase A (reverse order due to FontForge).
    for family in reversed(seq_families):
        try:
            creator.add_seq_ligature(family)
        except Exception as e:
            print('Exception while adding seq family: {}'.format(family['name']))
            raise

    # Work around a bug in Fontforge where the underline height is subtracted from
    # the underline width when you call generate().
    font.upos += font.uwidth

    # Generate font type (TTF or OTF) corresponding to input font extension
    # (defaults to TTF)
    if input_font_file[-4:].lower() == '.otf':
        output_font_type = '.otf'
    else:
        output_font_type = '.ttf'

    # Generate font & move to output directory
    output_font_file = path.join(output_dir, font.fontname + output_font_type)
    print("    ...saving to '%s' (%s)" % (output_font_file, font.fullname))
    font.generate(output_font_file)


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("input_font_file",
        help="The TTF or OTF font to add ligatures to.")
    parser.add_argument("--output-dir",
        help="The directory to save the ligaturized font in. The actual filename"
             " will be automatically generated based on the input font name and"
             " the --prefix and --output-name flags.")
    parser.add_argument("--ligature-font-file",
        type=str, default='', metavar='PATH',
        help="The file to copy ligatures from. If unspecified, ligaturize will"
             " attempt to pick a suitable one from fonts/fira/distr/ttf/ based on the input"
             " font's weight.")
    parser.add_argument("--copy-character-glyphs",
        default=False, action='store_true',
        help="Copy glyphs for (some) individual characters from the ligature"
             " font as well. This will result in punctuation that matches the"
             " ligatures more closely, but may not fit in as well with the rest"
             " of the font.")
    parser.add_argument("--scale-character-glyphs-threshold",
        type=float, default=0.1, metavar='THRESHOLD',
        help="When copying character glyphs, if they differ in width from the"
             " width of the input font by at least this much, scale them"
             " horizontally to match the input font even if this noticeably"
             " changes their aspect ratio. The default (0.1) means to scale if"
             " they are at least 10%% wider or narrower. A value of 0 will scale"
             " all copied character glyphs; a value of 2 effectively disables"
             " character glyph scaling.")
    parser.add_argument("--prefix",
        type=str, default="Liga",
        help="String to prefix the name of the generated font with.")
    parser.add_argument("--output-name",
        type=str, default="",
        help="Name of the generated font. Completely replaces the original.")
    return parser.parse_args()

def main():
    ligaturize_font(**vars(parse_args()))

if __name__ == '__main__':
    main()
