# Euclid's Elements - Unicode XeLaTeX/LuaLaTeX Version

This branch contains Euclid's Elements with corrected Unicode Greek text,
suitable for compilation with XeLaTeX or LuaLaTeX.

## Features
- ✅ Corrected Unicode Greek (no spacing issues)
- ✅ Compatible with XeLaTeX and LuaLaTeX
- ✅ Modern font support via fontspec
- ✅ Polyglossia for proper Greek hyphenation

## Requirements
- XeLaTeX or LuaLaTeX
- Greek font (e.g., GFS Didot, GFS Neohellenic)
- polyglossia package

## Compilation

### Using XeLaTeX:
```bash
xelatex Elements.tex
xelatex Elements.tex  # Run twice for references
```

### Using LuaLaTeX:
```bash
lualatex Elements.tex
lualatex Elements.tex
```

### Using Makefile:
```bash
make -f Makefile.xelatex
```

## Greek Text Corrections
The following issues have been fixed:
- Spacing issues (μ ῆκος → μῆκος)
- Character confusion (ἐχ → ἐξ, σθ → σχ)
- Final sigma positioning
- Elision marks (ἐφ' ἑαυτῆς)

## Font Configuration
Edit the \newfontfamily\greekfont line to use your preferred Greek font:
- GFS Didot (classical style)
- GFS Neohellenic (modern style)
- Linux Libertine
- Gentium Plus

## Original Version
For pdfLaTeX compatibility, use the master branch.
