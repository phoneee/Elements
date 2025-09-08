#!/usr/bin/env python3
"""
Fix oversized illustrations in Euclid's Elements by adding width constraints.
Standard LaTeX article text width is about 345pt (4.8 inches).
"""

import re
import os
from pathlib import Path

def fix_includegraphics_width(content: str) -> tuple[str, int]:
    r"""
    Fix \includegraphics commands to add width constraints.
    Use 0.8\textwidth for most figures to ensure they fit well.
    """
    lines = content.split('\n')
    changes = 0
    
    for i, line in enumerate(lines):
        # Match \includegraphics{...} without any options
        # Using \centerline{\includegraphics{...}} pattern
        if r'\includegraphics{' in line and r'\includegraphics[' not in line:
            # Replace with width-constrained version
            old_pattern = r'\\includegraphics\{([^}]+)\}'
            new_pattern = r'\\includegraphics[width=0.8\\textwidth]{\1}'
            
            new_line = re.sub(old_pattern, new_pattern, line)
            if new_line != line:
                lines[i] = new_line
                changes += 1
    
    return '\n'.join(lines), changes

def process_tex_file(tex_file: str) -> bool:
    """Process a single TeX file to fix illustrations."""
    print(f"Processing {tex_file}...")
    
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"  Error reading file")
        return False
    
    new_content, changes = fix_includegraphics_width(content)
    
    if changes > 0:
        # Backup original
        backup_file = tex_file + '.bak_figures'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write modified content
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  Modified {changes} figure(s), backed up to {backup_file}")
        return True
    else:
        print(f"  No changes needed")
        return False

def main():
    """Process all book files."""
    modified_files = []
    total_changes = 0
    
    # Process each book
    for book_num in range(1, 14):
        book_dir = f'Book{book_num:02d}'
        tex_file = os.path.join(book_dir, f'Book{book_num}.tex')
        
        if os.path.exists(tex_file):
            if process_tex_file(tex_file):
                modified_files.append(tex_file)
    
    # Also process introduction and lexicon if they exist
    for special_file in ['Book00/Introduction.tex', 'Book99/Lexicon.tex']:
        if os.path.exists(special_file):
            if process_tex_file(special_file):
                modified_files.append(special_file)
    
    print(f"\nSummary: Modified {len(modified_files)} files")
    if modified_files:
        print("Modified files:")
        for f in modified_files:
            print(f"  - {f}")
        print("\nAll figures will now use width=0.8\\textwidth for proper sizing")

if __name__ == '__main__':
    main()