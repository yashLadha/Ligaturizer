"""Minimal in-memory fakes for the fontforge/psMat API used by ligaturize.py.

This lets the rule-generation logic in LigatureCreator run (and be tested)
under plain python3, where the real fontforge module is only available
inside the fontforge binary's embedded interpreter.

Only the API surface actually used by LigatureCreator is implemented.
Fonts record every operation of interest (glyphs copied out, contextual
subtables added, paste-into merges) so tests can assert on behavior.

fontforge semantics reproduced here:
- selection.select() raises ValueError for an unknown glyph name
  (this is what copy_ligature_from_source relies on to detect missing
  source glyphs).
- copy()/paste() go through a single clipboard that is SHARED between
  fonts (copying from the source font and pasting into the target font).
"""

import sys
import types

# Global clipboard shared across all FakeFonts, like real fontforge.
_CLIPBOARD = None


class FakeGlyph(object):
    def __init__(self, name, width=0, code=None):
        self.glyphname = name
        self.width = width
        self.code = code
        self.left_side_bearing = 0
        self.right_side_bearing = 0
        self.transforms = []        # recorded psMat matrices
        self.pasted_from = None     # glyph name last pasted into this glyph
        self.references = ()        # composite references, like real fontforge
        self.unlinked = False       # set once unlinkRef() has flattened refs

    def transform(self, matrix):
        self.transforms.append(matrix)

    def unlinkRef(self, refname=None):
        # Flatten references into contours. The fake has no real outline
        # model, so just record that flattening happened and drop the refs.
        self.references = ()
        self.unlinked = True

    def addPosSub(self, subtable_name, target):
        # Recorded on the owning font by FakeFont.__getitem__ wiring.
        self._font.pos_subs.append((subtable_name, self.glyphname, target))


class FakeSelection(object):
    def __init__(self, font):
        self._font = font
        self.selected = None

    def none(self):
        self.selected = None

    def select(self, name):
        if isinstance(name, str) and name not in self._font.glyphs:
            raise ValueError('no glyph named %s' % name)
        self.selected = name


class FakeFont(object):
    def __init__(self, em=1000):
        self.em = em
        self.glyphs = {}
        self.by_code = {}
        self.selection = FakeSelection(self)
        # Recorded operations:
        self.lookups = []           # (lookup_name, lookup_type)
        self.subtables = []         # (lookup_name, subtable_name)
        self.calt_rules = []        # (lookup_name, subtable_name, spec)
        self.pos_subs = []          # (subtable_name, glyph, target)
        self.copied_from = []       # glyph names copied OUT of this font
        self.paste_into_ops = []    # (target_glyph, clipboard_glyph)

    # -- glyph management -------------------------------------------------

    def add_glyph(self, name, width=600, code=None):
        glyph = FakeGlyph(name, width=width, code=code)
        glyph._font = self
        self.glyphs[name] = glyph
        if code is not None:
            self.by_code[code] = glyph
        return glyph

    def createChar(self, code, name):
        if name not in self.glyphs:
            self.add_glyph(name, width=0, code=None if code == -1 else code)
        return self.glyphs[name]

    def removeGlyph(self, name):
        del self.glyphs[name]

    def __contains__(self, name):
        return name in self.glyphs

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.by_code[key]
        return self.glyphs[key]

    # -- clipboard --------------------------------------------------------

    def copy(self):
        global _CLIPBOARD
        name = self.selection.selected
        if name is None or name not in self.glyphs:
            raise ValueError('nothing selected to copy')
        _CLIPBOARD = {'name': name, 'width': self.glyphs[name].width}
        self.copied_from.append(name)

    def paste(self):
        name = self.selection.selected
        if name is None:
            raise ValueError('nothing selected to paste into')
        if _CLIPBOARD is None:
            raise ValueError('clipboard is empty')
        glyph = self.glyphs.get(name)
        if glyph is None:
            glyph = self.add_glyph(name, width=0)
        glyph.width = _CLIPBOARD['width']
        glyph.pasted_from = _CLIPBOARD['name']

    def pasteInto(self):
        name = self.selection.selected
        if name is None:
            raise ValueError('nothing selected to pasteInto')
        if _CLIPBOARD is None:
            raise ValueError('clipboard is empty')
        self.paste_into_ops.append((name, _CLIPBOARD['name']))

    # -- lookups ----------------------------------------------------------

    def addLookup(self, name, lookup_type, flags, features):
        self.lookups.append((name, lookup_type))

    def addLookupSubtable(self, lookup_name, subtable_name):
        self.subtables.append((lookup_name, subtable_name))

    def addContextualSubtable(self, lookup_name, subtable_name, fmt, spec):
        self.calt_rules.append((lookup_name, subtable_name, spec))


def _fake_psmat():
    mod = types.ModuleType('psMat')
    mod.scale = lambda x, y: ('scale', x, y)
    mod.translate = lambda x, y: ('translate', x, y)
    return mod


def install():
    """Install fake fontforge/psMat modules into sys.modules.

    Must be called before importing ligaturize.
    """
    sys.modules['fontforge'] = types.ModuleType('fontforge')
    sys.modules['psMat'] = _fake_psmat()
