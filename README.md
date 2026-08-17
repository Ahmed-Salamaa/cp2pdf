# CP2PDF Converter 📄🚀

A professional, modular Python CLI application that scans a Competitive Programming (CP) repository and converts all C++ templates, Markdown documentation, and existing PDFs into a single, highly compressed, beautifully formatted LaTeX-based PDF Team Reference Document (TRD).

## Features

- **Advanced UI Configuration**: Customize your PDF down to the finest detail. Change Fonts, Page Sizes (A4, Letter, etc.), Margins, Heading Styles, Column layouts, and more directly from a terminal UI!
- **Interactive File Selection**: Selectively include or exclude specific topics, folders, and files using your keyboard.
- **Markdown Support**: Uses `pandoc` to natively parse your `.md` notes and inject them as formatted text.
- **SVG Embedded Graphics**: Automatically detects raw `<svg>` tags in your Markdown, converts them to PDFs, and embeds them as scalable vector graphics in the final LaTeX document!
- **External PDF Support**: Seamlessly stitches existing `.pdf` files (like formula sheets) into the final document using the `pdfpages` package.
- **Customizable Code Styles**: Choose between "Black Border (No Background)" or "Light Gray Background" for your syntax-highlighted `.cpp` code blocks.
- **Document Splitting**: Optionally generate two separate PDFs—one for your documentation and another for your source code!

---

## Prerequisites

Because this tool relies on professional typesetting engines to generate the best possible output, you must have the following installed on your system:

1. **Python 3.7+**
2. **Pandoc**: Used to convert Markdown notes.
   - Ubuntu/Debian: `sudo apt install pandoc`
   - MacOS: `brew install pandoc`
   - Windows: `choco install pandoc` or `scoop install pandoc`
3. **rsvg-convert**: Used to convert SVG graphics inside your Markdown notes.
   - Ubuntu/Debian: `sudo apt install librsvg2-bin`
   - MacOS: `brew install librsvg`
   - Windows: Install MSYS2 and run `pacman -S mingw-w64-x86_64-librsvg`, or use WSL.
4. **A LaTeX Distribution** (with `pdflatex`): Used to compile the document.
   - Ubuntu/Debian: `sudo apt install texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-xetex`
   - MacOS: Install MacTeX (`brew install --cask mactex-no-gui`)
   - Windows: Install MiKTeX (https://miktex.org/download) or TeX Live.

---

## Installation

You can run the script directly, or install it globally using `pip`. Because the app is packaged properly, you can even install it directly from your GitHub repository!

```bash
# Option A: Install directly from GitHub using SSH
pip install git+ssh://git@github.com/Ahmed-Salamaa/cp2pdf.git

# Option B: Clone the repo and install locally
git clone https://github.com/Ahmed-Salamaa/cp2pdf.git
cd cp2pdf
pip install .

# Option C: Clone and run directly without installing
git clone https://github.com/Ahmed-Salamaa/cp2pdf.git
cd cp2pdf
python run.py
```

---

## Usage

If you installed it via `pip`, simply run:

```bash
cp2pdf
```

Or, if running the raw python script locally:

```bash
python run.py
```

### 1. Configuration Menu
Upon launching, you will be greeted by the Configuration Menu. You can customize the source directory, output options, font sizes, margins, orientation, and layout.
- **UP/DOWN Arrow**: Change setting
- **RIGHT/LEFT Arrow**: Change the selected value for the setting
- **ENTER**: Proceed to the File Selection Menu

### 2. File Selection Menu
Once the configuration is accepted, you will see a tree view of your files:
- **UP/DOWN Arrow**: Move your cursor
- **RIGHT/LEFT Arrow**: Expand or collapse a folder
- **SPACE**: Toggle the selection `[x]` of a file or folder. (Unchecking a folder unchecks everything inside it).
- **ENTER**: Confirm your selection and build the PDF

## Output

The application will extract your files, convert your markdown and graphics, generate a `.tex` file in an isolated temporary environment, and compile it into a final `CP_Template.pdf` (or split docs/code PDFs) in your specified output directory!

---

## Contributing

We welcome pull requests! See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
