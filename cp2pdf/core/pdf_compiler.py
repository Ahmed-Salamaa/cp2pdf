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
        res1 = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(tex_file),
            text=True,
            errors='replace'
        )
        
        # Second Pass (Builds TOC with correct page numbers)
        print("Running pdflatex (Pass 2/3)...")
        res2 = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(tex_file),
            text=True,
            errors='replace'
        )
        
        # Third Pass (Resolves all references and multicol TOC issues)
        print("Running pdflatex (Pass 3/3)...")
        res3 = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(tex_file),
            text=True,
            errors='replace'
        )
        
        if os.path.exists(tex_file.replace('.tex', '.pdf')):
            print(f"Successfully compiled {tex_file.replace('.tex', '.pdf')}")
        else:
            print("Warning: pdflatex encountered fatal errors and could not generate a PDF.")
            print("Please check for invalid UTF-8 characters or syntax errors in your files.")
            print("\n--- pdflatex Error Output (Pass 3) ---")
            print(res3.stdout)
            if res3.stderr:
                print(res3.stderr)
            print("--------------------------------------\n")
        
    except FileNotFoundError:
        print("Error: 'pdflatex' is not installed or not in PATH.")
        print("Please install a LaTeX distribution (like TeX Live).")
