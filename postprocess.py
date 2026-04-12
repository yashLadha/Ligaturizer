#!/usr/bin/env python3
"""Post-process ligaturized fonts: convert ChainContextSubst Format 1 to Format 3.

FontForge generates Format 1 (glyph-based) subtables for all CALT rules.
Fira Code uses a mix of formats:
  - Format 1: multi-rule lookups (multiple rules per coverage glyph)
  - Format 2: class-based lookups (Phase A spacer conversion)
  - Format 3: single-rule lookups with coverage sets (Phase B seq rules)

This script converts only single-rule Format 1 subtables to Format 3,
preserving multi-rule subtables as Format 1 to match Fira Code's structure.
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables


def count_rules(subtable):
    """Count total rules in a Format 1 subtable."""
    return sum(
        len(rs.ChainSubRule)
        for rs in (subtable.ChainSubRuleSet or [])
        if rs
    )


def convert_format1_to_format3(subtable):
    """Convert a single-rule ChainContextSubst Format 1 subtable to Format 3."""
    if subtable.Format != 1:
        return False
    if count_rules(subtable) != 1:
        return False

    cov_glyphs = subtable.Coverage.glyphs
    rule = None
    cov_glyph = None
    for k, rs in enumerate(subtable.ChainSubRuleSet or []):
        if rs and rs.ChainSubRule:
            rule = rs.ChainSubRule[0]
            cov_glyph = cov_glyphs[k]
            break
    if rule is None:
        return False

    def make_coverage(glyphs):
        cov = otTables.Coverage()
        cov.glyphs = list(glyphs)
        return cov

    bt_covs = [make_coverage([g]) for g in (rule.Backtrack or [])]
    inp_covs = [make_coverage([cov_glyph])]
    inp_covs.extend(make_coverage([g]) for g in (rule.Input or []))
    la_covs = [make_coverage([g]) for g in (rule.LookAhead or [])]

    subtable.Format = 3
    subtable.BacktrackCoverage = bt_covs
    subtable.BacktrackCount = len(bt_covs)
    subtable.InputCoverage = inp_covs
    subtable.InputCount = len(inp_covs)
    subtable.LookAheadCoverage = la_covs
    subtable.LookAheadCount = len(la_covs)
    subtable.SubstLookupRecord = rule.SubstLookupRecord or []
    subtable.SubstCount = rule.SubstCount

    for attr in ('Coverage', 'ChainSubRuleSet', 'ChainSubRuleSetCount'):
        if hasattr(subtable, attr):
            delattr(subtable, attr)

    return True


def postprocess(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    t = TTFont(input_path)
    gsub = t['GSUB'].table
    converted = 0
    kept_f1 = 0

    for lookup in gsub.LookupList.Lookup:
        for st in lookup.SubTable:
            actual = st
            if lookup.LookupType == 7:
                actual = st.ExtSubTable
            if not hasattr(actual, 'Format') or actual.Format != 1:
                continue
            if getattr(actual, 'ChainSubRuleSet', None) is None:
                continue
            if convert_format1_to_format3(actual):
                converted += 1
            else:
                kept_f1 += 1

    t.save(output_path)
    print("  %s: %d subtables F1->F3, %d kept as F1" % (
        output_path, converted, kept_f1))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 postprocess.py <font.ttf> [output.ttf]")
        sys.exit(1)
    postprocess(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
