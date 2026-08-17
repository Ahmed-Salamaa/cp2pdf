import os

def generate_master_tex(selected_files, processed_files, target_dir, output_path, title="ICPC Team Reference", page_format="a4paper", orientation="portrait", columns=1, font_choice="Computer Modern (Default)", font_size="10pt", heading_style="Bold", margin="1.5cm", code_style="Light Gray Background"):
    """
    Generates the master LaTeX file containing all the selected files, preserving the exact directory hierarchy.
    """
    font_package = ""
    if font_choice.startswith("Libertinus"):
        font_package = "\\usepackage{libertinus}\n\\usepackage[scaled=0.85]{DejaVuSansMono}"
    elif font_choice.startswith("Times"):
        font_package = "\\usepackage{mathptmx}"
    elif font_choice.startswith("Palatino"):
        font_package = "\\usepackage{mathpazo}"
        
    heading_fmt = "\\bfseries"
    if heading_style == "Italic":
        heading_fmt = "\\itshape\\bfseries"
    elif heading_style == "Small Caps":
        heading_fmt = "\\scshape\\bfseries"
    elif heading_style == "Normal":
        heading_fmt = "\\normalfont"
        
    lst_style = ""
    if "Black Border" in code_style:
        lst_style = "backgroundcolor=\\color{white},\n    frame=single,\n    rulecolor=\\color{black},"
    else:
        lst_style = "backgroundcolor=\\color{codebg},\n    frame=single,\n    rulecolor=\\color{codebg},"
        
    with open(output_path, 'w', encoding='utf-8') as f:
        # --- LaTeX Preamble ---
        f.write(fr"""\documentclass{{extarticle}}
\usepackage[utf8]{{inputenc}}
\usepackage{{anyfontsize}}
\usepackage{{scrextend}}
\changefontsizes{{{font_size}}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{longtable}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{calc}}
\usepackage{{multicol}}
\usepackage{{listings}}
\usepackage{{xcolor}}
\usepackage[{page_format}, {orientation}, margin={margin}, top={margin}, bottom={margin}]{{geometry}}
\usepackage{{hyperref}}
\usepackage{{pdfpages}}
\usepackage{{fancyhdr}}
\usepackage{{graphicx}}
{font_package}

\providecommand{{\tightlist}}{{%
  \setlength{{\itemsep}}{{0pt}}\setlength{{\parskip}}{{0pt}}}}
  
\providecommand{{\pandocbounded}}[1]{{#1}}
\newcommand{{\passthrough}}[1]{{#1}}

\hypersetup{{
    colorlinks=true,
    linkcolor=black,
    filecolor=black,      
    urlcolor=black,
}}

% Compact Sections without titlesec package
\makeatletter
\renewcommand\section{{\@startsection {{section}}{{1}}{{\z@}}%
                                   {{-3.5ex \@plus -1ex \@minus -.2ex}}%
                                   {{2.3ex \@plus.2ex}}%
                                   {{\normalfont\Large{heading_fmt}}}}}
\renewcommand\subsection{{\@startsection{{subsection}}{{2}}{{\z@}}%
                                     {{-2.5ex\@plus -1ex \@minus -.2ex}}%
                                     {{1.5ex \@plus .2ex}}%
                                     {{\normalfont\large{heading_fmt}}}}}
\renewcommand\subsubsection{{\@startsection{{subsubsection}}{{3}}{{\z@}}%
                                     {{-2.0ex\@plus -1ex \@minus -.2ex}}%
                                     {{1.0ex \@plus .2ex}}%
                                     {{\normalfont\normalsize{heading_fmt}}}}}
\renewcommand\paragraph{{\@startsection{{paragraph}}{{4}}{{\z@}}%
                                     {{-1.5ex\@plus -1ex \@minus -.2ex}}%
                                     {{1.5ex \@plus .2ex}}%
                                     {{\normalfont\normalsize{heading_fmt}}}}}
\renewcommand\subparagraph{{\@startsection{{subparagraph}}{{5}}{{\z@}}%
                                     {{-1.0ex\@plus -1ex \@minus -.2ex}}%
                                     {{1.0ex \@plus .2ex}}%
                                     {{\normalfont\normalsize{heading_fmt}}}}}
\makeatother

% Section Numbering Format (e.g. 1. and 1.1.)
\renewcommand{{\thesection}}{{\arabic{{section}}.}}
\renewcommand{{\thesubsection}}{{\thesection\arabic{{subsection}}.}}
\renewcommand{{\thesubsubsection}}{{\thesubsection\arabic{{subsubsection}}.}}
\renewcommand{{\theparagraph}}{{\thesubsubsection\arabic{{paragraph}}.}}
\renewcommand{{\thesubparagraph}}{{\theparagraph\arabic{{subparagraph}}.}}

\setcounter{{secnumdepth}}{{5}}
\setcounter{{tocdepth}}{{5}}

% Headers and Footers
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyfoot[C]{{\thepage}}
\renewcommand{{\headrulewidth}}{{0pt}}
\renewcommand{{\footrulewidth}}{{0pt}}

% Colors from Reference PDF
\definecolor{{codebg}}{{RGB}}{{235,235,235}}
\definecolor{{codekw}}{{RGB}}{{215,58,73}}
\definecolor{{codetype}}{{RGB}}{{0,92,197}}
\definecolor{{codecomment}}{{RGB}}{{106,115,125}}
\definecolor{{codestring}}{{RGB}}{{3,47,98}}

\lstset{{
    language=C++,
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{{codekw}},
    stringstyle=\color{{codestring}},
    commentstyle=\color{{codecomment}}\itshape,
    morekeywords={{int, float, double, bool, void, char, auto, long, const, struct, class, unsigned, template, typename}},
    {lst_style}
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=4,
    captionpos=b,
    breaklines=true,
    breakatwhitespace=false,
    escapeinside={{\%*}}{{*)}},
    extendedchars=true,
    literate={{≤}}{{{{$\leq$}}}}1 {{≥}}{{{{$\geq$}}}}1 {{—}}{{{{---}}}}1 {{‘}}{{{{`}}}}1 {{’}}{{{{'}}}}1 {{“}}{{{{``}}}}1 {{”}}{{{{''}}}}1 {{×}}{{{{$\times$}}}}1 {{÷}}{{{{$\div$}}}}1 {{≈}}{{{{$\approx$}}}}1 {{≡}}{{{{$\equiv$}}}}1 {{↓}}{{{{$\downarrow$}}}}1 {{→}}{{{{$\rightarrow$}}}}1 {{ω}}{{{{$\omega$}}}}1 {{−}}{{{{$-$}}}}1,
    aboveskip=1em,
    belowskip=1em,
    xleftmargin=0.5em,
    xrightmargin=0.5em,
}}

\begin{{document}}

% --- Title Page ---
\vspace*{{10cm}}
\begin{{center}}
    {{\Huge\bfseries {title}}} \\[1cm]
    {{\large \today}}
\end{{center}}
\thispagestyle{{empty}}
\newpage

% --- TOC ---
\tableofcontents
\newpage
""")
        if columns > 1:
            f.write(f"\\begin{{multicols*}}{{{columns}}}\n")
            
        # --- Content Injection ---
        
        # Build a nested dictionary representing the exact file tree hierarchy
        tree = {}
        for orig_file, proc_file in zip(selected_files, processed_files):
            rel_path = os.path.relpath(orig_file, target_dir)
            parts = rel_path.split(os.sep)
            
            curr = tree
            for part in parts[:-1]:
                if part not in curr:
                    curr[part] = {}
                curr = curr[part]
            curr[parts[-1]] = proc_file

        def write_tree(node, depth=1, parent_name=""):
            # Sort keys to maintain alphabetical order exactly like the file tree
            for name, content in sorted(node.items()):
                clean_name = name.replace('_', r'\_')
                
                if isinstance(content, dict):
                    # It's a directory
                    if depth == 1:
                        f.write(f"\\section{{{clean_name}}}\n")
                    elif depth == 2:
                        f.write(f"\\subsection{{{clean_name}}}\n")
                    else:
                        f.write(f"\\subsubsection{{{clean_name}}}\n")
                    
                    write_tree(content, depth + 1, name)
                else:
                    # It's a file
                    proc_file = content
                    file_base = os.path.splitext(name)[0]
                    clean_file_base = file_base.replace('_', r'\_')
                    
                    # If the file shares the exact name as its parent folder, skip the duplicate heading!
                    skip_heading = (file_base.lower() == parent_name.lower())
                    
                    if proc_file.endswith('.tex'):
                        # Markdown file converted to tex
                        import re
                        with open(proc_file, 'r', encoding='utf-8') as tf:
                            tex_content = tf.read()
                            
                        # Shift heading levels dynamically based on the file's depth in the tree!
                        if depth > 1:
                            shift = depth - 1
                            def shift_heading(match):
                                cmd = match.group(1)
                                levels = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
                                try:
                                    idx = levels.index(cmd)
                                    new_idx = min(idx + shift, len(levels) - 1)
                                    return '\\' + levels[new_idx] + '{'
                                except ValueError:
                                    return match.group(0)
                            
                            tex_content = re.sub(r'\\(section|subsection|subsubsection|paragraph|subparagraph)\{', shift_heading, tex_content)

                        if skip_heading:
                            # The parent directory already wrote a heading for this file!
                            # We must remove the FIRST sectioning command to prevent a duplicate (empty) header.
                            tex_content = re.sub(r'\\(section|subsection|subsubsection|paragraph|subparagraph)\{[^}]*\}', '', tex_content, count=1)
                            
                        with open(proc_file, 'w', encoding='utf-8') as tf:
                            tf.write(tex_content)
                                
                        # We input it directly so its internal headings take over
                        f.write(f"\\input{{{proc_file}}}\n")
                    elif proc_file.endswith('.pdf'):
                        if skip_heading:
                            f.write(f"\\includepdf[pages=-]{{{proc_file}}}\n")
                        else:
                            if depth == 1:
                                f.write("\\includepdf[pages=-, pagecommand={\\section{" + clean_file_base + "}}]{" + proc_file + "}\n")
                            elif depth == 2:
                                f.write("\\includepdf[pages=-, pagecommand={\\subsection{" + clean_file_base + "}}]{" + proc_file + "}\n")
                            else:
                                f.write("\\includepdf[pages=-, pagecommand={\\subsubsection{" + clean_file_base + "}}]{" + proc_file + "}\n")
                    else:
                        # Standard source code file
                        if not skip_heading:
                            if depth == 1:
                                f.write(f"\\section{{{clean_file_base}}}\n")
                            elif depth == 2:
                                f.write(f"\\subsection{{{clean_file_base}}}\n")
                            else:
                                f.write(f"\\subsubsection{{{clean_file_base}}}\n")
                        
                        f.write(f"\\lstinputlisting[title=\\textbf{{{clean_name}}}]{{{proc_file}}}\n")

        write_tree(tree, depth=1)
        if columns > 1:
            f.write(f"\\end{{multicols*}}\n")
        f.write(r"\end{document}" + "\n")
