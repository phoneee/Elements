#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrate corrected Unicode Greek text into original Elements structure
For XeLaTeX/LuaLaTeX compatibility
"""

import re
from pathlib import Path
import shutil

def update_for_xelatex(content: str) -> str:
    """Update TeX content for XeLaTeX/LuaLaTeX compatibility"""
    
    # Replace babel with polyglossia for XeLaTeX
    content = content.replace(r'\usepackage[polutonikogreek,english]{babel}', 
                            r'%\usepackage[polutonikogreek,english]{babel} % Disabled for XeLaTeX')
    
    # Add polyglossia if XeLaTeX
    if '\\usepackage{fontspec}' not in content:
        # Add XeLaTeX packages after documentclass
        xelatex_packages = """
% XeLaTeX/LuaLaTeX Unicode support
\\usepackage{ifxetex}
\\usepackage{ifluatex}
\\ifxetex
  \\usepackage{fontspec}
  \\usepackage{polyglossia}
  \\setdefaultlanguage{english}
  \\setotherlanguage[variant=ancient]{greek}
  \\newfontfamily\\greekfont{GFS Didot}[Script=Greek] % or another Greek font
\\else\\ifluatex
  \\usepackage{fontspec}
  \\usepackage{polyglossia}
  \\setdefaultlanguage{english}
  \\setotherlanguage[variant=ancient]{greek}
  \\newfontfamily\\greekfont{GFS Didot}[Script=Greek]
\\else
  % pdfLaTeX fallback
  \\usepackage[LGR,T1]{fontenc}
  \\usepackage[utf8]{inputenc}
  \\usepackage[polutonikogreek,english]{babel}
\\fi\\fi
"""
        # Insert after documentclass
        def replace_func(match):
            return match.group(0) + '\n' + xelatex_packages
        content = re.sub(r'(\\documentclass[^}]+})', replace_func, content, count=1)
    
    return content

def copy_corrected_greek(source_dir: Path, target_dir: Path) -> int:
    """Copy corrected Greek from Elements_Perfect to Book directories"""
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return 0
    
    copied = 0
    
    # Map source files to target directories
    for source_file in sorted(source_dir.glob('Book*.tex')):
        # Extract book number
        match = re.search(r'Book(\d+)', source_file.name)
        if not match:
            continue
        
        book_num = match.group(1)
        
        # Find target directory
        target_book_dir = target_dir / f'Book{book_num}'
        if not target_book_dir.exists():
            print(f"⚠️ Target directory not found: {target_book_dir}")
            continue
        
        # Find the main TeX file in target directory
        target_files = list(target_book_dir.glob('Book*.tex'))
        if not target_files:
            target_files = list(target_book_dir.glob('*.tex'))
        
        if not target_files:
            print(f"⚠️ No TeX files found in {target_book_dir}")
            continue
        
        target_file = target_files[0]  # Use first TeX file found
        
        # Read source (corrected Greek)
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()
        
        # Read target (original structure)
        with open(target_file, 'r', encoding='utf-8') as f:
            target_content = f.read()
        
        # Extract Greek blocks from source
        greek_blocks = re.findall(r'\{\\greekfont\s+([^}]+)\}', source_content)
        
        if not greek_blocks:
            print(f"⚠️ No Greek blocks found in {source_file}")
            continue
        
        # Replace Greek blocks in target
        greek_iter = iter(greek_blocks)
        
        def replace_greek(match):
            try:
                new_greek = next(greek_iter)
                return '{\\greekfont ' + new_greek + '}'
            except StopIteration:
                return match.group(0)  # Keep original if we run out
        
        updated_content = re.sub(r'\{\\greekfont\s+([^}]+)\}', replace_greek, target_content)
        
        # Update for XeLaTeX
        updated_content = update_for_xelatex(updated_content)
        
        # Backup original
        backup_file = target_file.with_suffix('.tex.backup')
        if not backup_file.exists():
            shutil.copy2(target_file, backup_file)
            print(f"  📋 Backed up: {backup_file.name}")
        
        # Write updated content
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"  ✅ Updated: {target_file.relative_to(target_dir)}")
        copied += 1
    
    return copied

def update_main_elements_file(main_file: Path) -> None:
    """Update main Elements.tex for XeLaTeX"""
    
    if not main_file.exists():
        print(f"⚠️ Main file not found: {main_file}")
        return
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    backup = main_file.with_suffix('.tex.backup')
    if not backup.exists():
        shutil.copy2(main_file, backup)
        print(f"📋 Backed up: {backup.name}")
    
    # Update for XeLaTeX
    content = update_for_xelatex(content)
    
    # Write updated
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {main_file.name}")

def create_xelatex_makefile() -> None:
    """Create Makefile for XeLaTeX compilation"""
    
    makefile_content = """# Makefile for Euclid's Elements with XeLaTeX
# Unicode Greek support

# Compiler selection
LATEX = xelatex
# Alternative: LATEX = lualatex

# Main document
MAIN = Elements

# Build targets
all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex Book*/*.tex
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex  # Run twice for references

clean:
	rm -f *.aux *.log *.out *.toc *.pdf Book*/*.aux

# Compile individual books
book%:
	cd Book$* && $(LATEX) Book$*.tex

.PHONY: all clean
"""
    
    makefile = Path('Makefile.xelatex')
    with open(makefile, 'w') as f:
        f.write(makefile_content)
    
    print(f"✅ Created: {makefile}")

def create_readme() -> None:
    """Create README for Unicode branch"""
    
    readme_content = """# Euclid's Elements - Unicode XeLaTeX/LuaLaTeX Version

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
Edit the \\newfontfamily\\greekfont line to use your preferred Greek font:
- GFS Didot (classical style)
- GFS Neohellenic (modern style)
- Linux Libertine
- Gentium Plus

## Original Version
For pdfLaTeX compatibility, use the master branch.
"""
    
    readme = Path('README_UNICODE.md')
    with open(readme, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created: {readme}")

def main():
    """Main integration process"""
    
    print("="*70)
    print("INTEGRATING UNICODE GREEK INTO ELEMENTS")
    print("For XeLaTeX/LuaLaTeX compatibility")
    print("="*70)
    
    # Paths
    source_dir = Path('Elements_Perfect')
    target_dir = Path('.')  # Current directory with Book folders
    
    # Copy corrected Greek
    print("\n📁 Copying corrected Greek text...")
    copied = copy_corrected_greek(source_dir, target_dir)
    print(f"✅ Updated {copied} book files")
    
    # Update main Elements.tex
    print("\n📄 Updating main Elements.tex...")
    update_main_elements_file(Path('Elements.tex'))
    
    # Create Makefile
    print("\n📝 Creating build files...")
    create_xelatex_makefile()
    
    # Create README
    create_readme()
    
    print("\n" + "="*70)
    print("✅ INTEGRATION COMPLETE!")
    print("="*70)
    print("""
Next steps:
1. Test compilation:
   xelatex Elements.tex
   
2. Commit changes:
   git add -A
   git commit -m "Add Unicode Greek support for XeLaTeX/LuaLaTeX"
   
3. Push branch:
   git push origin unicode-xelatex
""")

if __name__ == '__main__':
    main()