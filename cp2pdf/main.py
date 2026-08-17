import os
import shutil
import argparse
import tempfile
from cp2pdf.core.scanner import scan_directory
from cp2pdf.ui.tree_selector import run_interactive_ui
from cp2pdf.core.md_converter import convert_markdown_files
from cp2pdf.core.tex_builder import generate_master_tex
from cp2pdf.core.pdf_compiler import compile_pdf

def run_app():
    parser = argparse.ArgumentParser(description="Convert CP Templates to a PDF Team Reference Document.")
    parser.add_argument("directory", nargs="?", default=None, help="The root directory of the CP template.")
    
    args = parser.parse_args()
    
    from cp2pdf.ui.config_menu import run_config_menu
    
    config = run_config_menu()
    if not config:
        print("Configuration cancelled or failed.")
        return
        
    target_dir = os.path.abspath(config["target_dir"])
    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        return
        
    output_dir = os.path.abspath(config["output_dir"])
    want_pdf = "PDF" in config["format"]
    want_tex = "LaTeX" in config["format"] or "Both" in config["format"]
    split_docs = "Yes" in config["split"]
    
    font_choice = config["font"]
    font_size = config["font_size"]
    heading_style = config["heading_style"]
    page_format = config["page_format"]
    orientation = "landscape" if config["orientation"] == "Landscape" else "portrait"
    
    margin = config["margin"].split(" ")[0]
    code_style = config["code_style"]
    page_number_location = config.get("page_number_location", "Bottom Center")
    cover_title = config.get("cover_title", "ICPC Team Reference")
    
    try:
        columns = int(config["columns"])
    except ValueError:
        columns = 1
    
    print(f"\nScanning directory: {target_dir}")
    tree_root = scan_directory(target_dir)
    if not tree_root.children:
        print("No supported files found in the directory.")
        return

    print("Launching interactive selection menu...")
    selected_files = run_interactive_ui(tree_root)
    
    if not selected_files:
        print("No files selected. Exiting.")
        return
        
    print(f"Selected {len(selected_files)} files. Proceeding with generation...")
    
    # Work inside a temporary directory
    with tempfile.TemporaryDirectory() as temp_env:
        print(f"Creating isolated temporary workspace...")
        
        BUILD_DIR = os.path.join(temp_env, "build")
        os.makedirs(BUILD_DIR)
        
        print("\nConverting Markdown files...")
        
        if split_docs:
            code_files = [f for f in selected_files if not f.endswith(('.md', '.pdf'))]
            doc_files = [f for f in selected_files if f.endswith(('.md', '.pdf'))]
            
            code_processed = convert_markdown_files(code_files, BUILD_DIR)
            doc_processed = convert_markdown_files(doc_files, BUILD_DIR)
            
            MASTER_TEX_CODE = os.path.join(temp_env, "master_code.tex")
            MASTER_TEX_DOCS = os.path.join(temp_env, "master_docs.tex")
            
            print("Generating master LaTeX files...")
            generate_master_tex(code_files, code_processed, target_dir, MASTER_TEX_CODE, title=f"{cover_title} - Source Code", page_format=page_format, orientation=orientation, columns=columns, font_choice=font_choice, font_size=font_size, heading_style=heading_style, margin=margin, code_style=code_style, page_number_location=page_number_location)
            generate_master_tex(doc_files, doc_processed, target_dir, MASTER_TEX_DOCS, title=f"{cover_title} - Documentation", page_format=page_format, orientation=orientation, columns=columns, font_choice=font_choice, font_size=font_size, heading_style=heading_style, margin=margin, code_style=code_style, page_number_location=page_number_location)
            
            if want_pdf:
                print("Compiling PDFs (this may take a moment)...")
                if code_files: compile_pdf(MASTER_TEX_CODE)
                if doc_files: compile_pdf(MASTER_TEX_DOCS)
            
            print("\nMoving results to final location...")
            if want_pdf:
                if code_files:
                    temp_pdf_path = MASTER_TEX_CODE.replace('.tex', '.pdf')
                    final_pdf_path = os.path.join(output_dir, "CP_Template_Code.pdf")
                    if os.path.exists(temp_pdf_path):
                        shutil.copy2(temp_pdf_path, final_pdf_path)
                        print(f"Source Code PDF ready at: {final_pdf_path}")
                    else:
                        print("Error: Source Code PDF compilation failed, no output found.")
                        log_path = MASTER_TEX_CODE.replace('.tex', '.log')
                        if os.path.exists(log_path):
                            fail_log = os.path.join(output_dir, "CP_Template_Code_Failed.log")
                            shutil.copy2(log_path, fail_log)
                            print(f"Compilation log saved to: {fail_log}")
                if doc_files:
                    temp_pdf_path = MASTER_TEX_DOCS.replace('.tex', '.pdf')
                    final_pdf_path = os.path.join(output_dir, "CP_Template_Docs.pdf")
                    if os.path.exists(temp_pdf_path):
                        shutil.copy2(temp_pdf_path, final_pdf_path)
                        print(f"Documentation PDF ready at: {final_pdf_path}")
                    else:
                        print("Error: Documentation PDF compilation failed, no output found.")
                        log_path = MASTER_TEX_DOCS.replace('.tex', '.log')
                        if os.path.exists(log_path):
                            fail_log = os.path.join(output_dir, "CP_Template_Docs_Failed.log")
                            shutil.copy2(log_path, fail_log)
                            print(f"Compilation log saved to: {fail_log}")
            
            if want_tex:
                if code_files:
                    final_tex_path = os.path.join(output_dir, "CP_Template_Code.tex")
                    if os.path.exists(MASTER_TEX_CODE):
                        shutil.copy2(MASTER_TEX_CODE, final_tex_path)
                        print(f"Source Code LaTeX ready at: {final_tex_path}")
                if doc_files:
                    final_tex_path = os.path.join(output_dir, "CP_Template_Docs.tex")
                    if os.path.exists(MASTER_TEX_DOCS):
                        shutil.copy2(MASTER_TEX_DOCS, final_tex_path)
                        print(f"Documentation LaTeX ready at: {final_tex_path}")
                
        else:
            MASTER_TEX = os.path.join(temp_env, "master.tex")
            processed_files = convert_markdown_files(selected_files, BUILD_DIR)
            
            print("Generating master LaTeX file...")
            generate_master_tex(selected_files, processed_files, target_dir, MASTER_TEX, title=cover_title, page_format=page_format, orientation=orientation, columns=columns, font_choice=font_choice, font_size=font_size, heading_style=heading_style, margin=margin, code_style=code_style, page_number_location=page_number_location)
            
            if want_pdf:
                print("Compiling PDF (this may take a moment)...")
                compile_pdf(MASTER_TEX)
            
            print("\nMoving results to final location...")
            if want_pdf:
                temp_pdf_path = MASTER_TEX.replace('.tex', '.pdf')
                final_pdf_path = os.path.join(output_dir, "CP_Template.pdf")
                if os.path.exists(temp_pdf_path):
                    shutil.copy2(temp_pdf_path, final_pdf_path)
                    print(f"Your PDF is ready at:  {final_pdf_path}")
                else:
                    print("Error: PDF compilation failed, no output found.")
                    log_path = MASTER_TEX.replace('.tex', '.log')
                    if os.path.exists(log_path):
                        fail_log = os.path.join(output_dir, "CP_Template_Failed.log")
                        shutil.copy2(log_path, fail_log)
                        print(f"Compilation log saved to: {fail_log}")
                    
            if want_tex:
                final_tex_path = os.path.join(output_dir, "CP_Template.tex")
                if os.path.exists(MASTER_TEX):
                    shutil.copy2(MASTER_TEX, final_tex_path)
                    print(f"Your LaTeX is ready at: {final_tex_path}")
                
    print(f"\nProcess complete! All temporary files were automatically destroyed. 🎉")
    print(f"Your generated files have been saved to:\n➜  {output_dir}")
