#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete fix for Greek text in Elements
Handles all character conversion issues comprehensively
"""

import re
from pathlib import Path
import shutil

def fix_greek_comprehensive(text: str) -> str:
    """Fix all Greek text issues comprehensively"""
    
    # First, remove all kern commands
    text = re.sub(r'\\kern\s*[-.0-9]+\s*pt\s*', '', text)
    
    # Major systematic replacements
    
    # 1. Fix wrong breathing/accent combinations
    # The pattern is: wrong char like < or > should be breathing marks
    text = text.replace('ὁ', 'ὁ')  # Keep correct rough breathing
    text = text.replace('οὁῦ', 'οὗ')  # Genitive relative
    text = text.replace('ὁὸ', 'ὃ')  # Neuter relative
    text = text.replace('ὁό', 'ὅ')  # Relative with acute
    text = text.replace('ὁή', 'ἥ')  # Feminine relative with acute
    text = text.replace('ὁήτις', 'ἥτις')  # Which (feminine)
    text = text.replace('ὁῆ', 'ἣ')  # Feminine relative
    text = text.replace('ὁὴν', 'ἣν')  # Which (accusative)
    text = text.replace('ὁῦ', 'οὗ')  # of which
    
    # 2. Fix all ξ that should be final sigma ς
    # Common word endings
    endings = [
        ('αξ', 'ας'),  # -as ending
        ('ηξ', 'ης'),  # -es ending  
        ('οξ', 'ος'),  # -os ending
        ('ωξ', 'ως'),  # -os ending
        ('ιξ', 'ις'),  # -is ending
        ('υξ', 'υς'),  # -us ending
        ('εξ', 'ες'),  # -es ending (but preserve ἐξ = "from")
    ]
    
    for wrong, right in endings:
        # Only at word boundaries
        text = re.sub(f'{wrong}(?=[\\s,;.!?\\)]|$)', right, text)
    
    # Specific words with ξ → ς
    text = text.replace('πρὸξ', 'πρὸς')  # towards
    text = text.replace('τοῖξ', 'τοῖς')  # the (dative plural)
    text = text.replace('ταῖξ', 'ταῖς')  # the (dative feminine plural)
    text = text.replace('τρεῖξ', 'τρεῖς')  # three
    text = text.replace('πλευράξ', 'πλευράς')  # sides
    text = text.replace('γωνίαξ', 'γωνίας')  # angles
    text = text.replace('εὐθείαξ', 'εὐθείας')  # straight lines
    text = text.replace('ἴσαξ', 'ἴσας')  # equal (plural)
    text = text.replace('μόναξ', 'μόνας')  # only (plural)
    text = text.replace('Γραμμῆξ', 'Γραμμῆς')  # of line
    text = text.replace('τῆξ', 'τῆς')  # the (genitive)
    text = text.replace('ὀρθῆξ', 'ὀρθῆς')  # right (genitive)
    text = text.replace('μιᾶξ', 'μιᾶς')  # one (genitive)
    text = text.replace('Ἐπιφανείαξ', 'Ἐπιφανείας')  # surfaces
    text = text.replace('ἀπλατέξ', 'ἀπλατές')  # without breadth
    
    # 3. Fix wrong smooth breathing marks (ὸ should often be with different marks)
    text = text.replace('ἐξὸίσου', 'ἐξ ἴσου')  # equally (needs space)
    text = text.replace('ἐφὸ', "ἐφ'")  # upon (with elision)
    text = text.replace('ἐπὸ', "ἐπ'")  # on (with elision)
    text = text.replace('ὑπὸ', 'ὑπὸ')  # under (keep as is when not elided)
    text = text.replace('μόνονὸέθει', 'μόνον ἔχει')  # only has
    text = text.replace('ὸέθον', ' ἔχον')  # having
    text = text.replace('ὸέθει', ' ἔχει')  # has
    text = text.replace('ὸή', ' ἢ')  # or
    text = text.replace('ὸίσας', ' ἴσας')  # equal
    text = text.replace('ὸίσαις', ' ἴσαις')  # equal (dative)
    text = text.replace('ὸῶσιν', ' ὦσιν')  # are (subjunctive)
    text = text.replace('ὸό', ' ὅ')  # which
    text = text.replace('ὸὸ', ' ὃ')  # which (neuter)
    text = text.replace('ὸύτε', 'οὔτε')  # neither
    text = text.replace('ὸάπειρον', ' ἄπειρον')  # infinite
    
    # 4. Fix theta/chi confusion
    text = text.replace('σθῆμα', 'σχῆμα')  # figure
    text = text.replace('σθήματος', 'σχήματος')  # of figure  
    text = text.replace('σθημάτων', 'σχημάτων')  # of figures
    text = text.replace('περιεθόμενον', 'περιεχόμενον')  # contained
    text = text.replace('περιεθόμενα', 'περιεχόμενα')  # contained (plural)
    text = text.replace('περιεθομένου', 'περιεχομένου')  # contained (genitive)
    text = text.replace('περιεθομένων', 'περιεχομένων')  # contained (genitive plural)
    text = text.replace('περιεθούσας', 'περιεχούσας')  # containing
    text = text.replace('ἔθει', 'ἔχει')  # has
    text = text.replace('ἔθον', 'ἔχον')  # having
    text = text.replace('ἔθουσαι', 'ἔχουσαι')  # having (feminine)
    
    # 5. Fix wrong acute angle term
    text = text.replace('ὀχεῖα', 'ὀξεῖα')  # acute
    text = text.replace('Ὀχεῖα', 'Ὀξεῖα')  # Acute
    text = text.replace('ὀχυγώνιον', 'ὀξυγώνιον')  # acute-angled
    text = text.replace('ὀχείας', 'ὀξείας')  # acute (plural)
    
    # 6. Fix other specific terms
    text = text.replace('α<ίτινες', 'αἵτινες')  # which (plural)
    text = text.replace('οὁῦσαι', 'οὖσαι')  # being (feminine)
    text = text.replace('οὁύτε', 'οὔτε')  # neither
    text = text.replace('ὁρόμβος', 'ῥόμβος')  # rhombus
    text = text.replace('ὁρομβοειδές', 'ῥομβοειδές')  # rhomboid
    text = text.replace('τεσν-σάρων', 'τεσσάρων')  # four (genitive)
    text = text.replace('τεσν\\-σάρων', 'τεσσάρων')  # four with LaTeX hyphen
    
    # 7. Fix spacing in diphthongs
    text = text.replace('α ὐ', 'αὐ')
    text = text.replace('ε ὐ', 'εὐ')
    text = text.replace('ο ὐ', 'οὐ')
    
    # 8. Clean up apostrophes for elision
    text = text.replace("ἐφ>", "ἐφ'")
    text = text.replace("ἀφ>", "ἀφ'")
    text = text.replace("δι>", "δι'")
    text = text.replace("ὑπ>", "ὑπ'")
    text = text.replace("ἐπ>", "ἐπ'")
    text = text.replace("καθ>", "καθ'")
    
    # 9. Fix remaining wrong symbols
    text = text.replace('<\'Οροι', 'Ὅροι')  # Definitions (title)
    text = text.replace('<\'Οταν', 'Ὅταν')  # When
    text = text.replace('<\'Ετι', 'Ἔτι')  # Moreover
    text = text.replace('<\'Οτι', 'Ὅτι')  # That
    text = text.replace('>', '')  # Remove stray > that shouldn't be there
    text = text.replace('<', '')  # Remove stray < that shouldn't be there
    
    # 10. Final cleanup of common patterns
    text = re.sub(r'([α-ω])\s+([ὰάὲέὴήὶίὸόὺύὼώᾶῆῖῦῶ])', r'\1\2', text)
    
    return text

def process_file(filepath: Path) -> bool:
    """Process a single TeX file"""
    
    if not filepath.exists():
        return False
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Process Greek text in \gr{} blocks
    def fix_gr_block(match):
        greek = match.group(1)
        fixed = fix_greek_comprehensive(greek)
        return '\\gr{' + fixed + '}'
    
    # Apply fixes
    content = re.sub(r'\\gr\{([^}]+)\}', fix_gr_block, content, flags=re.DOTALL)
    
    # Write if changed
    if content != original:
        # Backup first
        backup = filepath.with_suffix('.tex.bak2')
        if not backup.exists():
            shutil.copy2(filepath, backup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Fix all Book files"""
    
    print("="*70)
    print("COMPLETE GREEK TEXT FIX FOR ELEMENTS")
    print("="*70)
    
    fixed_files = []
    
    # Process all Book directories
    for book_dir in sorted(Path('.').glob('Book*/')):
        if book_dir.name == 'Book99':  # Skip lexicon for now
            continue
        
        # Find main TeX file
        tex_files = list(book_dir.glob('Book*.tex'))
        if not tex_files:
            tex_files = list(book_dir.glob('*.tex'))
        
        for tex_file in tex_files:
            if 'backup' in tex_file.name or 'bak' in tex_file.name:
                continue
            
            print(f"Processing {tex_file}...")
            if process_file(tex_file):
                fixed_files.append(tex_file)
                print(f"  ✅ Fixed")
            else:
                print(f"  ✓ Already good")
    
    print(f"\n✅ Fixed {len(fixed_files)} files")
    
    # Show sample output
    if fixed_files:
        print("\n" + "="*70)
        print("SAMPLE FROM BOOK 1")
        print("="*70)
        
        book1 = Path('Book01/Book1.tex')
        if book1.exists():
            with open(book1, 'r') as f:
                lines = f.readlines()
            
            # Show some definitions
            print("\nFirst few definitions:")
            for i, line in enumerate(lines[30:50], 30):
                if '\\ggn{' in line and '\\gr{' in line:
                    print(f"  {line.strip()}")

if __name__ == '__main__':
    main()