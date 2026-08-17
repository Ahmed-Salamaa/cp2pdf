import os
import subprocess
import hashlib

import re

def pre_process_md(file_path, build_dir):
    """
    Extracts raw <svg> tags from a markdown file, converts them to PDFs using rsvg-convert,
    and replaces them with markdown image links. Also strips manual numbering from markdown headings.
    Returns the path to the modified markdown.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    modified = False
    
    # 1. Ensure all headers have a blank line above and below them
    # This prevents Pandoc from treating them as inline text if the user forgot a newline.
    header_wrap_pattern = re.compile(r'([^\n])\n(#{1,6}[ \t]+.*)', re.MULTILINE)
    content, count0 = header_wrap_pattern.subn(r'\1\n\n\2', content)
    
    header_wrap_after = re.compile(r'(^#{1,6}[ \t]+.*)\n([^\n])', re.MULTILINE)
    content, count0_after = header_wrap_after.subn(r'\1\n\n\2', content)
    if count0 > 0 or count0_after > 0:
        modified = True
        
    # 2. Strip manual numbering from headings (e.g. "# 5. Triangles" -> "# Triangles")
    # Use [ \t]+ instead of \s+ so we don't accidentally match across newlines!
    heading_pattern = re.compile(r'^(#+)[ \t]+[\d\.]+[ \t]+(.*)$', re.MULTILINE)
    new_content, count = heading_pattern.subn(r'\1 \2', content)
    if count > 0:
        modified = True
        
    # 3. Remove completely empty headings (e.g. "## ") that cause empty sections in LaTeX
    empty_pattern = re.compile(r'^(#+)[ \t]*$', re.MULTILINE)
    new_content, count2 = empty_pattern.subn('', new_content)
    if count2 > 0:
        modified = True
        
    # 4. Convert SVGs
    svg_pattern = re.compile(r'<svg.*?</svg>', re.IGNORECASE | re.DOTALL)
    matches = svg_pattern.findall(new_content)
    
    if matches:
        modified = True
        for i, svg_content in enumerate(matches):
            base_name = os.path.basename(file_path).replace('.md', '')
            svg_filename = os.path.join(build_dir, f"{base_name}_svg_{i}.svg")
            pdf_filename = os.path.join(build_dir, f"{base_name}_svg_{i}.pdf")
            
            with open(svg_filename, 'w', encoding='utf-8') as sf:
                sf.write(svg_content)
                
            try:
                subprocess.run(
                    ["rsvg-convert", "-f", "pdf", svg_filename, "-o", pdf_filename],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                # Replace SVG block with markdown image pointing to the generated PDF
                new_content = new_content.replace(svg_content, f"\n![]({pdf_filename})\n")
            except Exception as e:
                print(f"Warning: Failed to convert SVG in {file_path}. Ensure 'rsvg-convert' is installed.")
                
    if not modified:
        return file_path
        
    hash_suffix = hashlib.md5(file_path.encode()).hexdigest()[:6]
    new_md_path = os.path.join(build_dir, f"{os.path.basename(file_path)}_{hash_suffix}.md")
    
    with open(new_md_path, 'w', encoding='utf-8') as nf:
        nf.write(new_content)
        
    return new_md_path

def convert_markdown_files(selected_files, build_dir):
    """
    Takes a list of file paths. For any '.md' file, runs pandoc to convert it
    to a LaTeX fragment and saves it in the build directory.
    Returns a new list of file paths, with '.md' files replaced by their new '.tex' counterparts.
    """
    processed_files = []
    
    for file_path in selected_files:
        if file_path.endswith('.md'):
            # Pre-process SVGs to PDFs and strip heading numbers
            target_md_path = pre_process_md(file_path, build_dir)
            
            # Create a unique but readable filename for the tex fragment
            base_name = os.path.basename(file_path).replace('.md', '')
            hash_suffix = hashlib.md5(file_path.encode()).hexdigest()[:6]
            tex_filename = f"{base_name}_{hash_suffix}.tex"
            tex_out_path = os.path.join(build_dir, tex_filename)
            
            try:
                # Call pandoc to convert markdown to latex fragment
                # We don't want a standalone document, just the fragment
                subprocess.run(
                    ["pandoc", target_md_path, "-f", "gfm", "-t", "latex", "--listings", "--shift-heading-level-by=1", "-o", tex_out_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                processed_files.append(tex_out_path)
            except FileNotFoundError:
                print(f"Error: 'pandoc' is not installed or not in PATH. Skipping {file_path}")
            except subprocess.CalledProcessError:
                print(f"Error converting {file_path} using pandoc. Skipping.")
        else:
            # Leave .cpp, .h, and .pdf files unchanged
            processed_files.append(file_path)
            
    return processed_files
