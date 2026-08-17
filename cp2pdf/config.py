# Configuration and Constants for cp2pdf

import os

# Default file extensions to look for
SUPPORTED_EXTENSIONS = ('.cpp', '.h', '.md', '.pdf')

# Folders and files to strictly exclude from the UI
# We do NOT exclude "notes" or other normal folders by default as requested.
# We MUST exclude CP_Template.pdf so the script doesn't recursively embed previous outputs!
HIDDEN_DIRS = {'.git', '.vscode', '__pycache__', 'build', 'cp2pdf', 'CP_Template.pdf', 'CP_Template.tex'}

# Output names
STRUCTURE_FILE = 'structure.json'
MASTER_TEX = 'master.tex'
FINAL_PDF = 'CP_Template.pdf'
BUILD_DIR = 'build'
