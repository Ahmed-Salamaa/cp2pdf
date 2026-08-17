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
            check=True
        )
        
        # Second Pass (Builds TOC with correct page numbers)
        print("Running pdflatex (Pass 2/3)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(tex_file),
            check=True
        )
        
        # Third Pass (Resolves all references and multicol TOC issues)
        print("Running pdflatex (Pass 3/3)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(tex_file),
            check=True
        )
        
        print(f"Successfully compiled {tex_file.replace('.tex', '.pdf')}")
        
    except FileNotFoundError:
        print("Error: 'pdflatex' is not installed or not in PATH.")
        print("Please install a LaTeX distribution (like TeX Live).")
    except subprocess.CalledProcessError:
        print("Warning: pdflatex encountered errors during compilation.")
        print("If you selected a custom font (like Libertinus), ensure you have 'texlive-fontsextra' installed (e.g. pacman -S texlive-fontsextra).")
        print("A PDF might still have been generated, but please check the logs.")
