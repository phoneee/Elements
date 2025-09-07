# Unicode Greek Support for Euclid's Elements

This branch (`unicode-xelatex`) contains Unicode Greek text that requires XeLaTeX or LuaLaTeX for compilation.

## Changes from Master Branch

1. **Greek Text**: All Beta code Greek text has been converted to Unicode
   - Beta code like `Shme~i'on >estin` → Unicode `Σημεῖόν ἐστιν`
   - Preserves all diacritical marks (breathing, accents, iota subscript)

2. **LaTeX Engine**: Must use XeLaTeX or LuaLaTeX (not pdfLaTeX)
   - pdfLaTeX uses LGR encoding and cannot handle Unicode Greek directly
   - XeLaTeX/LuaLaTeX have native Unicode support

3. **Font Configuration**: Uses modern fontspec package with Greek fonts
   - Main font: Times New Roman
   - Greek font: GFS Porson (or alternatives like Linux Libertine, Gentium Plus)

4. **Graphics**: Updated from old `epsf` package to modern `graphicx`
   - `\epsffile{...}` → `\includegraphics{...}`

## Compilation

### Using XeLaTeX:
```bash
cd Elements
xelatex Elements-xelatex.tex
```

### Using LuaLaTeX:
```bash
cd Elements
lualatex Elements-xelatex.tex
```

## Known Issues

1. **EPS Files**: XeLaTeX cannot directly include EPS files. Solutions:
   - Convert EPS to PDF: `epstopdf *.eps`
   - Or use `--shell-escape` flag: `xelatex --shell-escape Elements-xelatex.tex`

2. **Font Availability**: Ensure Greek fonts are installed:
   - GFS Porson (recommended)
   - Or use alternatives specified in Elements-xelatex.tex

## File Structure

- `Elements-xelatex.tex` - Main document configured for XeLaTeX/LuaLaTeX
- `Book*/Book*.tex` - Individual books with Unicode Greek text
- `*.beta_backup` - Original Beta code backups (if preserved)

## Conversion Scripts

The following Python scripts were used for conversion:
- `convert_elements_beta.py` - Beta code to Unicode converter
- `fix_unicode_issues.py` - Fixed conversion errors
- `fix_latex_markers.py` - Restored embedded LaTeX commands
- `fix_epsf_commands.py` - Updated graphics commands

## Original Beta Code

To return to Beta code for pdfLaTeX compatibility:
```bash
# Restore from backups
for backup in $(find . -name "*.beta_backup"); do
    original="${backup%.beta_backup}"
    cp "$backup" "$original"
done
```

## Resources

- [Beta Code Reference](https://www.tlg.uci.edu/encoding/)
- [Unicode Greek Block](https://en.wikipedia.org/wiki/Greek_and_Coptic)
- [XeLaTeX Documentation](https://www.overleaf.com/learn/latex/XeLaTeX)