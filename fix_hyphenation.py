#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix LaTeX hyphenation marks in Greek text
Remove \- from Greek words where they shouldn't be
"""

import re
from pathlib import Path
import shutil

def remove_hyphenation(text: str) -> str:
    """Remove LaTeX hyphenation marks from Greek text"""
    
    # Remove \- hyphenation marks
    text = text.replace('\\-', '')
    
    # Also check for any other hyphenation patterns
    # Sometimes there might be soft hyphens or other marks
    text = text.replace('\u00ad', '')  # Soft hyphen
    text = text.replace('\u2010', '-')  # Convert hyphen to regular dash if needed
    
    return text

def fix_other_remaining_issues(text: str) -> str:
    """Fix any other remaining conversion issues"""
    
    # Fix remaining spacing issues
    text = text.replace('α  ὐ', 'αὐ')  # Double space in diphthong
    text = text.replace('ο  ὐ', 'οὐ')
    text = text.replace('ε  ὐ', 'εὐ')
    
    # Fix remaining wrong characters
    text = text.replace('ὸίσον', ' ἴσον')  # equal
    text = text.replace('ὸίσα', ' ἴσα')  # equal (plural)
    text = text.replace('ὸίσην', ' ἴσην')  # equal (accusative)
    text = text.replace('ὸίσης', ' ἴσης')  # equal (genitive)
    text = text.replace('ὸίσαι', ' ἴσαι')  # equal (plural)
    text = text.replace('ὸάρα', ' ἄρα')  # therefore
    text = text.replace('ὸέδει', ' ἔδει')  # it was necessary
    text = text.replace("ὸ'Εστω", 'Ἔστω')  # Let be
    text = text.replace('τῶ|', 'τῷ')  # dative singular (the)
    text = text.replace('τῆ|', 'τῇ')  # dative singular feminine
    text = text.replace('ἐντὸξ', 'ἐντὸς')  # inside (fix final sigma)
    text = text.replace('παντὸξ', 'παντὸς')  # of all
    text = text.replace('ἑνὸξ', 'ἑνὸς')  # of one
    
    # Fix more final sigma issues
    text = re.sub(r'([α-ω])ξ\s', r'\1ς ', text)  # Final sigma before space
    text = re.sub(r'([α-ω])ξ([,;.!?])', r'\1ς\2', text)  # Final sigma before punctuation
    
    return text

def process_file(filepath: Path) -> bool:
    """Process a single TeX file"""
    
    if not filepath.exists():
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Process Greek text in \gr{} blocks
    def fix_gr_block(match):
        greek = match.group(1)
        # Remove hyphenation
        fixed = remove_hyphenation(greek)
        # Fix other issues
        fixed = fix_other_remaining_issues(fixed)
        return '\\gr{' + fixed + '}'
    
    # Apply fixes to all Greek blocks
    content = re.sub(r'\\gr\{([^}]+)\}', fix_gr_block, content, flags=re.DOTALL)
    
    # Also fix Greek in other contexts (like \greekfont if any)
    def fix_greekfont_block(match):
        greek = match.group(1)
        fixed = remove_hyphenation(greek)
        fixed = fix_other_remaining_issues(fixed)
        return '\\greekfont{' + fixed + '}'
    
    content = re.sub(r'\\greekfont\{([^}]+)\}', fix_greekfont_block, content, flags=re.DOTALL)
    
    if content != original:
        # Create backup
        backup = filepath.with_suffix('.tex.bak3')
        if not backup.exists():
            shutil.copy2(filepath, backup)
        
        # Write fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Fix hyphenation in all Book files"""
    
    print("="*70)
    print("FIXING HYPHENATION AND REMAINING ISSUES IN GREEK TEXT")
    print("="*70)
    
    fixed_files = []
    
    # Process all Book directories
    for book_dir in sorted(Path('.').glob('Book*/')):
        # Find Book*.tex files
        for tex_file in book_dir.glob('Book*.tex'):
            if 'backup' in tex_file.name or 'bak' in tex_file.name:
                continue
            
            print(f"Processing {tex_file}...")
            if process_file(tex_file):
                fixed_files.append(tex_file)
                print(f"  ✅ Fixed hyphenation and other issues")
            else:
                print(f"  ✓ No changes needed")
    
    print(f"\n✅ Fixed {len(fixed_files)} files")
    
    # Verify the fix
    print("\n" + "="*70)
    print("VERIFICATION")
    print("="*70)
    
    # Check if hyphenation is gone
    remaining_hyphens = []
    for book_dir in Path('.').glob('Book*/'):
        for tex_file in book_dir.glob('Book*.tex'):
            if 'bak' in tex_file.name:
                continue
            with open(tex_file, 'r') as f:
                content = f.read()
            if '\\-' in content:
                # Count occurrences in Greek text
                gr_blocks = re.findall(r'\\gr\{([^}]+)\}', content, re.DOTALL)
                for block in gr_blocks:
                    if '\\-' in block:
                        remaining_hyphens.append(tex_file.name)
                        break
    
    if remaining_hyphens:
        print(f"⚠️ Files still with hyphenation: {remaining_hyphens}")
    else:
        print("✅ All hyphenation marks removed!")
    
    # Show sample
    print("\n" + "="*70)
    print("SAMPLE FROM BOOK 1")
    print("="*70)
    
    book1 = Path('Book01/Book1.tex')
    if book1.exists():
        with open(book1, 'r') as f:
            content = f.read()
        
        # Find the line that had προσπίπ\-τουσαι
        if 'προσπίπτουσαι' in content:
            print("✅ προσπίπ\\-τουσαι → προσπίπτουσαι")
        
        # Show a few lines with Greek
        lines = content.split('\n')
        shown = 0
        for i, line in enumerate(lines):
            if '\\gr{' in line and shown < 3:
                if 'προσπίπ' in line or 'ἰσόπλευ' in line or 'παράλληλ' in line:
                    print(f"Line {i+1}: {line.strip()[:100]}...")
                    shown += 1

if __name__ == '__main__':
    main()