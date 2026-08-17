import sys
import os
import tempfile
import shutil

# Ensure cp2pdf is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cp2pdf.core.scanner import scan_directory
from cp2pdf.core.md_converter import convert_markdown_files
from cp2pdf.core.tex_builder import generate_master_tex
from cp2pdf.core.pdf_compiler import compile_pdf

def test_full_pipeline():
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "samples", "sample_repo"))
    
    # 1. Scan
    tree = scan_directory(sample_dir)
    assert tree is not None
    
    # Extract files
    def get_files(node, path=""):
        res = []
        for child in node.children:
            child_path = os.path.join(path, child.name) if path else child.name
            if child.is_dir:
                res.extend(get_files(child, child_path))
            else:
                res.append(os.path.join(sample_dir, child_path))
        return res
        
    selected_files = get_files(tree)
    assert len(selected_files) == 2, f"Expected 2 files, found {len(selected_files)}"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        build_dir = os.path.join(tmpdir, "build")
        os.makedirs(build_dir)
        
        # 2. Convert markdown
        processed_files = convert_markdown_files(selected_files, build_dir)
        assert len(processed_files) == len(selected_files)
        
        # 3. Build TeX
        master_tex = os.path.join(tmpdir, "master.tex")
        generate_master_tex(selected_files, processed_files, sample_dir, master_tex)
        assert os.path.exists(master_tex)
        
        # 4. Compile PDF
        compile_pdf(master_tex)
        assert os.path.exists(master_tex.replace(".tex", ".pdf"))
        print("Integration test passed successfully!")

if __name__ == "__main__":
    test_full_pipeline()
