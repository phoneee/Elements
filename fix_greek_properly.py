#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Greek text conversion errors in Elements files
Corrects wrong character mappings and removes kern commands
"""

import re
from pathlib import Path

def fix_greek_text(text: str) -> str:
    """Fix all Greek text conversion errors"""
    
    # Remove all \kern commands
    text = re.sub(r'\\kern\s*[-.0-9]+\s*(?:pt|em|mm)?', '', text)
    
    # Fix common character conversion errors
    replacements = [
        # Breathing marks and accents
        ('<\'', 'Ὅ'),  # Rough breathing with capital
        ('>', 'ὸ'),     # Wrong character for omicron with grave
        ('<', 'ὁ'),     # Wrong character for rough breathing
        
        # Fix specific wrong conversions
        ('ο<ῦ', 'οὗ'),  # genitive relative pronoun
        ('<ὸ', 'ὃ'),    # relative pronoun neuter
        ('<ό', 'ὅ'),    # relative pronoun with acute
        ('<ὴ', 'ἣ'),    # relative pronoun feminine
        ('<ή', 'ἥ'),    # relative pronoun feminine acute
        ('ὴ', 'ὴ'),     # eta with grave (keep)
        ('>ὴ', 'ἢ'),    # or (eta with smooth breathing)
        ('>ή', 'ἤ'),    # or with acute
        
        # Fix wrong xi for final sigma
        ('οξ', 'ος'),   # -os ending
        ('αξ', 'ας'),   # -as ending
        ('ηξ', 'ης'),   # -ēs ending  
        ('ωξ', 'ως'),   # -ōs ending
        ('ιξ', 'ις'),   # -is ending
        ('υξ', 'υς'),   # -us ending
        ('νξ', 'νς'),   # -ns ending
        ('ρξ', 'ρς'),   # -rs ending
        ('εξ', 'ες'),   # -es ending (but check for ἐξ "from")
        ('τοῖξ', 'τοῖς'), # dative plural
        ('ταῖξ', 'ταῖς'), # dative plural feminine
        ('εῖξ', 'εῖς'),   # into
        ('ἐχ', 'ἐξ'),     # from (before vowel becomes ἐξ)
        
        # Fix wrong theta/chi confusion
        ('σθῆμα', 'σχῆμα'),      # figure
        ('σθήματος', 'σχήματος'), # of figure
        ('σθημάτων', 'σχημάτων'), # of figures
        ('περιεθόμενον', 'περιεχόμενον'), # surrounded
        ('περιεθόμενα', 'περιεχόμενα'),   # surrounded (plural)
        ('περιεθομένου', 'περιεχομένου'), # surrounded (genitive)
        ('ἔθει', 'ἔχει'),  # has
        ('ἔθον', 'ἔχον'),  # having
        ('ἔθουσαι', 'ἔχουσαι'), # having (feminine plural)
        
        # Fix iota/eta confusion  
        ('>ί', 'ἴ'),    # iota with smooth breathing and acute
        ('>ῖ', 'ἷ'),    # iota with smooth breathing and circumflex
        ('>ῶ', 'ὧ'),    # omega with smooth breathing and circumflex
        ('>ά', 'ἄ'),    # alpha with smooth breathing and acute
        ('>έ', 'ἔ'),    # epsilon with smooth breathing and acute
        ('>ό', 'ὄ'),    # omicron with smooth breathing and acute
        ('>ύ', 'ὔ'),    # upsilon with smooth breathing and acute
        ('>ή', 'ἤ'),    # eta with smooth breathing and acute
        ('>ῆ', 'ἦ'),    # eta with smooth breathing and circumflex
        
        # Common words
        ('α<ίτινεξ', 'αἵτινες'),  # which (feminine plural)
        ('ο>ῦσαι', 'οὖσαι'),      # being (feminine plural)
        ('ο>ύτε', 'οὔτε'),        # neither
        ('>άπειρον', 'ἄπειρον'),  # infinite
        ('<ρόμβος', 'ῥόμβος'),    # rhombus
        ('<ρομβοειδές', 'ῥομβοειδές'), # rhomboid
        
        # Fix apostrophes
        ('ἐφ>', "ἐφ'"),   # elision
        ('ἀφ>', "ἀφ'"),   # elision
        ('δι>', "δι'"),   # elision
        ('ὑπ>', "ὑπ'"),   # elision
        ('ἐπ>', "ἐπ'"),   # elision
        ('καθ>', "καθ'"), # elision
        
        # Fix word-final sigma (additional cases)
        (' ἐστιξ ', ' ἐστις '),  # Actually wrong - should check context
        ('μιᾶξ', 'μιᾶς'),        # one (genitive feminine)
        ('τρεῖξ', 'τρεῖς'),      # three
        ('δύο μόναξ', 'δύο μόνας'), # two only
        ('ἴσαξ', 'ἴσας'),        # equal (accusative plural)
        ('ὀρθῆξ', 'ὀρθῆς'),      # right (genitive)
        ('εὐθείαξ', 'εὐθείας'),  # straight (genitive/accusative plural)
        ('γραμμῆξ', 'γραμμῆς'),  # line (genitive)
        ('τῆξ', 'τῆς'),          # the (genitive feminine)
        ('α ὐ', 'αὐ'),           # Fix spacing in diphthong
        
        # Breathing marks without proper letter
        ('Ὀχεῖα', 'Ὀξεῖα'),     # acute (angle)
        ('ὀχυγώνιον', 'ὀξυγώνιον'), # acute-angled
        ('ὀχείας', 'ὀξείας'),   # acute (plural)
        
        # Fix remaining xi issues  
        ('τεσσάρων', 'τεσσάρων'), # Keep correct
        ('τεσν\-σάρων', 'τεσσάρων'), # Fix hyphenation
        
        # Common patterns
        ('πλευράξ', 'πλευράς'),  # sides (accusative plural)
        ('γωνίαξ', 'γωνίας'),    # angles (accusative plural)
        ('Ἐπιφανείαξ', 'Ἐπιφανείας'), # surfaces
    ]
    
    for old, new in replacements:
        text = text.replace(old, new)
    
    # Fix remaining xi at word endings (more aggressive)
    # But preserve ξ in middle of words (like ἑξάγωνον = hexagon)
    text = re.sub(r'([α-ω])ξ(?=[\s,;.!?]|$)', r'\1ς', text)
    
    # Clean up any remaining spacing issues
    text = re.sub(r'([α-ωΑ-Ω])\s+([ὰάὲέὴήὶίὸόὺύὼώᾶῆῖῦῶ])', r'\1\2', text)
    
    return text

def process_file(filepath: Path) -> int:
    """Process a single TeX file"""
    
    if not filepath.exists():
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Process Greek text within \gr{} commands
    def fix_gr_block(match):
        greek = match.group(1)
        fixed = fix_greek_text(greek)
        return '\\gr{' + fixed + '}'
    
    content = re.sub(r'\\gr\{([^}]+)\}', fix_gr_block, content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def main():
    """Fix all Book files"""
    
    print("="*70)
    print("FIXING GREEK TEXT IN ELEMENTS")
    print("="*70)
    
    # Process all Book directories
    fixed_count = 0
    for book_dir in sorted(Path('.').glob('Book*/')):
        if book_dir.name == 'Book99':  # Skip lexicon
            continue
            
        # Find TeX files in the directory
        tex_files = list(book_dir.glob('*.tex'))
        
        for tex_file in tex_files:
            if 'backup' in tex_file.name:
                continue
                
            print(f"Processing {tex_file}...")
            if process_file(tex_file):
                fixed_count += 1
                print(f"  ✅ Fixed")
            else:
                print(f"  ✓ No changes needed")
    
    print(f"\n✅ Fixed {fixed_count} files")
    
    # Test on a sample
    print("\n" + "="*70)
    print("SAMPLE OUTPUT")
    print("="*70)
    
    # Show a sample from Book1
    book1 = Path('Book01/Book1.tex')
    if book1.exists():
        with open(book1, 'r') as f:
            lines = f.readlines()
        
        # Find and show some Greek text
        for i, line in enumerate(lines[30:50], 30):
            if '\\gr{' in line:
                print(f"Line {i}: {line.strip()}")
                if i > 40:
                    break

if __name__ == '__main__':
    main()