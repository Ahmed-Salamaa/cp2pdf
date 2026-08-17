import subprocess
import os

def compile_pdf(tex_file):
    """
    Compiles the given LaTeX file into a PDF.
    Runs pdflatex twice to ensure the Table of Contents is generated accurately.
    """
    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} not found.")
        return

    try:
        # First Pass (Collects TOC data)
        print("Running pdflatex (Pass 1/3)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(tex_file),
            check=False
        )
        
        # Second Pass (Builds TOC with correct page numbers)
        print("Running pdflatex (Pass 2/3)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(tex_file),
            check=False
        )
        
        # Third Pass (Resolves all references and multicol TOC issues)
        print("Running pdflatex (Pass 3/3)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(tex_file),
            check=False
        )
        
        if os.path.exists(tex_file.replace('.tex', '.pdf')):
            print(f"Successfully compiled {tex_file.replace('.tex', '.pdf')}")
        else:
            print("Warning: pdflatex encountered fatal errors and could not generate a PDF.")
            print("Please check for invalid UTF-8 characters or syntax errors in your files.")
        
    except FileNotFoundError:
        print("Error: 'pdflatex' is not installed or not in PATH.")
        print("Please install a LaTeX distribution (like TeX Live).")
