# To build with different settings (e.g. turn on character glyph copying),
# edit build.py and then "make".
#
# Requires: fontforge (system package with Python bindings)
# Optional: .venv with fonttools for font inspection utilities

SHELL := /bin/bash

FIRA_TTF := fonts/fira/distr/ttf/FiraCode-Regular.ttf
FIRA_ZIP_URL := https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip

# grep -v exits 1 when it filters out every line, which is not a build failure.
LOG_FILTER := { grep -Fv \
	-e 'This contextual rule applies no lookups.' \
	-e 'Bad device table' \
	-e 'Ignoring' \
	-e 'But its name indicates' \
	; [ $$? -le 1 ]; }

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

check-fira:
	@if [ ! -f $(FIRA_TTF) ]; then \
		echo "error: $(FIRA_TTF) not found." >&2; \
		echo "The fonts/fira submodule does not ship TTFs. Run ./build-fonts.sh, or unpack" >&2; \
		echo "ttf/*.ttf from $(FIRA_ZIP_URL) into fonts/fira/distr/ttf/." >&2; \
		exit 1; \
	fi

without-characters: check-fira fonts/output
	set -o pipefail; fontforge -lang=py -script build.py 2>&1 | $(LOG_FILTER)
	@echo "Post-processing fonts (Format 1 -> Format 3 conversion)..."
	@for f in fonts/output/*.ttf fonts/output/*.otf; do \
		[ -e "$$f" ] || continue; \
		python3 postprocess.py "$$f" || exit 1; \
	done

with-characters: check-fira fonts/output-with-characters
	set -o pipefail; fontforge -lang=py -script build.py --copy-character-glyphs 2>&1 | $(LOG_FILTER)
	@echo "Post-processing fonts (Format 1 -> Format 3 conversion)..."
	@for f in fonts/output-with-characters/*.ttf fonts/output-with-characters/*.otf; do \
		[ -e "$$f" ] || continue; \
		python3 postprocess.py "$$f" || exit 1; \
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

.PHONY: default all clean release pack check-fira without-characters with-characters ligature-list testpattern
