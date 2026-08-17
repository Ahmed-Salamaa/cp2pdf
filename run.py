#!/usr/bin/env python3
import os
import sys

# Add the current directory to sys.path so 'cp2pdf' can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from cp2pdf.main import run_app

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
