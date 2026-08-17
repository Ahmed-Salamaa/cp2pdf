# Contributing to CP2PDF

First off, thank you for considering contributing to CP2PDF! We welcome contributions from everyone—whether it's fixing bugs, improving the documentation, or adding entirely new configuration features for LaTeX rendering.

## How to Contribute

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/Ahmed-Salamaa/cp2pdf.git
   cd cp2pdf
   ```
3. **Install dependencies**:
   Make sure you have `pandoc`, `rsvg-convert`, and `pdflatex` installed on your machine.
4. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
5. **Make your changes**. 
   - If you are modifying the LaTeX generation, check `cp2pdf/core/tex_builder.py`.
   - If you are updating the TUI configuration menus, check `cp2pdf/ui/config_menu.py`.
   - If you are modifying the file selection UI, check `cp2pdf/ui/tree_selector.py`.
6. **Test your changes** locally. Run the tool on a dummy CP repository to ensure PDFs generate correctly and LaTeX compilation does not fail.
7. **Commit your changes**:
   ```bash
   git commit -m "Add my awesome feature"
   ```
8. **Push to your fork**:
   ```bash
   git push origin feature/my-awesome-feature
   ```
9. **Submit a Pull Request**! Describe the changes you've made and the issue it resolves.

## Development Guidelines

- **Code Style**: We try to follow PEP-8 conventions. Keep functions small and modular.
- **LaTeX Changes**: Any changes to the `\lstset` or preamble in `tex_builder.py` must be carefully tested since certain package combinations or `\color` commands can easily break LaTeX compilation in `pdflatex`.
- **UI Terminal Issues**: If you modify curses code, test it on a standard terminal emulator to ensure transparency and keybindings (`KEY_UP`, `KEY_DOWN`, etc.) behave correctly without causing infinite loops.

Thanks again for helping make CP2PDF better for the competitive programming community!
