# To build with different settings (e.g. turn on character glyph copying),
# edit build.py and then "make".
#
# Requires: fontforge (system package with Python bindings)
# Optional: .venv with fonttools for font inspection utilities

default: without-characters

all: without-characters with-characters

clean:
	rm -rf fonts/output/* fonts/output-with-characters/* Ligaturized*.zip

release: clean all pack

pack:
	zip -r -9 -j LigaturizedFonts.zip fonts/output/
	zip -r -9 -j LigaturizedFontsWithCharacters.zip fonts/output-with-characters/

fonts/output:
	mkdir -p fonts/output

fonts/output-with-characters:
	mkdir -p fonts/output-with-characters

without-characters: fonts/output
	fontforge -lang=py -script build.py 2>&1 \
	| grep -Fv 'This contextual rule applies no lookups.' \
	| grep -Fv 'Bad device table' \
	| grep -Fv 'Ignoring' \
	| grep -Fv 'But its name indicates'
	@echo "Post-processing fonts (Format 1 -> Format 3 conversion)..."
	@for f in fonts/output/*.ttf fonts/output/*.otf; do \
		[ -f "$$f" ] && python3 postprocess.py "$$f" || true; \
	done

with-characters: fonts/output-with-characters
	fontforge -lang=py -script build.py --copy-character-glyphs 2>&1 \
	| grep -Fv 'This contextual rule applies no lookups.' \
	| grep -Fv 'Bad device table' \
	| grep -Fv 'Ignoring' \
	| grep -Fv 'But its name indicates'
	@echo "Post-processing fonts (Format 1 -> Format 3 conversion)..."
	@for f in fonts/output-with-characters/*.ttf fonts/output-with-characters/*.otf; do \
		[ -f "$$f" ] && python3 postprocess.py "$$f" || true; \
	done

ligature-list:
	luajit name2dict.lua < fonts/fira/FiraCode.glyphs

testpattern:
	grep -F "{   #" ligatures.py \
  | grep -v absent \
  | cut -d'#' -f2 \
  | tr -d ' ' \
  | egrep '.' \
  | sed -E 's,\\,\\\\,g' \
  | xargs printf '| %6s %6s %6s %6s %6s %6s %6s %6s |\n'

.PHONY: default all clean release pack without-characters with-characters ligature-list testpattern
