#!/usr/bin/env python3
"""
Fix oversized illustrations in Euclid's Elements by adding proper scaling.
The figures should respect their bounding boxes and fit within the text width.
"""

import re
import os
from pathlib import Path
from typing import Tuple, Optional

def get_eps_bounding_box(eps_file: str) -> Optional[Tuple[float, float, float, float]]:
    """Extract bounding box from EPS file."""
    try:
        with open(eps_file, 'r', encoding='latin-1') as f:
            # Read first 50 lines (bounding box is usually at the beginning)
            for i, line in enumerate(f):
                if i > 50:
                    break
                if '%%BoundingBox:' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        return tuple(float(x) for x in parts[1:5])
    except:
        pass
    return None

def calculate_scale_factor(bbox: Tuple[float, float, float, float], 
                          max_width_pt: float = 345.0) -> float:
    """
    Calculate appropriate scale factor based on bounding box.
    Default max_width is 345pt (approximately 4.8 inches for standard text width).
    """
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    
    # Calculate scale to fit width
    scale = max_width_pt / width if width > max_width_pt else 1.0
    
    # Also check height constraint (max ~6 inches = 432pt)
    max_height_pt = 432.0
    if height * scale > max_height_pt:
        scale = max_height_pt / height
    
    # Round to 2 decimal places
    return round(scale, 2)

def fix_includegraphics(content: str, book_dir: str) -> str:
    r"""
    Fix \includegraphics commands to add proper scaling.
    """
    lines = content.split('\n')
    modified = False
    
    for i, line in enumerate(lines):
        # Match \includegraphics{...} or \includegraphics[...]{...}
        match = re.search(r'\\includegraphics(\[.*?\])?\{([^}]+)\}', line)
        if match:
            options = match.group(1)
            filename = match.group(2)
            
            # Skip if already has scaling options
            if options and ('scale=' in options or 'width=' in options or 'height=' in options):
                continue
            
            # Try to find the actual file
            possible_files = [
                os.path.join(book_dir, filename),
                os.path.join(book_dir, filename.replace('.pdf', '.eps')),
                os.path.join(book_dir, filename.replace('.eps', '.pdf')),
                filename if '/' in filename else None
            ]
            
            bbox = None
            for pf in possible_files:
                if pf and os.path.exists(pf):
                    if pf.endswith('.eps'):
                        bbox = get_eps_bounding_box(pf)
                        if bbox:
                            break
            
            if bbox:
                scale = calculate_scale_factor(bbox)
                if scale < 1.0:  # Only add scaling if needed
                    # Add scale option
                    if options:
                        # Merge with existing options
                        new_options = options[:-1] + f',scale={scale}]'
                    else:
                        new_options = f'[scale={scale}]'
                    
                    new_command = f'\\includegraphics{new_options}{{{filename}}}'
                    lines[i] = line.replace(match.group(0), new_command)
                    modified = True
                    print(f"  Scaled {filename} to {scale}")
    
    return '\n'.join(lines) if modified else content

def process_tex_file(tex_file: str) -> bool:
    """Process a single TeX file to fix illustrations."""
    print(f"Processing {tex_file}...")
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    book_dir = os.path.dirname(tex_file)
    new_content = fix_includegraphics(content, book_dir)
    
    if new_content != content:
        # Backup original
        backup_file = tex_file + '.bak_illustrations'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write modified content
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  Modified and backed up to {backup_file}")
        return True
    else:
        print(f"  No changes needed")
        return False

def main():
    """Process all book files."""
    modified_files = []
    
    # Process each book
    for book_num in range(1, 14):
        book_dir = f'Book{book_num:02d}'
        tex_file = os.path.join(book_dir, f'Book{book_num}.tex')
        
        if os.path.exists(tex_file):
            if process_tex_file(tex_file):
                modified_files.append(tex_file)
    
    # Also process introduction and lexicon
    for special_file in ['Book00/Introduction.tex', 'Book99/Lexicon.tex']:
        if os.path.exists(special_file):
            if process_tex_file(special_file):
                modified_files.append(special_file)
    
    print(f"\nSummary: Modified {len(modified_files)} files")
    if modified_files:
        print("Modified files:")
        for f in modified_files:
            print(f"  - {f}")

if __name__ == '__main__':
    main()