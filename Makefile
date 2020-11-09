# To build with different settings (e.g. turn on character glyph copying),
# edit build.py and then "make".

all:
	fontforge -lang=py -script build.py \
	| fgrep -v 'This contextual rule applies no lookups.' \
	| fgrep -v 'Bad device table'
