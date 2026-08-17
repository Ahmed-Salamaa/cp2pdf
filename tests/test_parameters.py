import unittest
import os
import sys
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cp2pdf.core.tex_builder import generate_master_tex

class TestParameters(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = os.path.join(self.temp_dir.name, "master.tex")
        
        # Create a real dummy file so tex_builder parses it and emits \begin{multicols}
        dummy_file_path = os.path.join(self.temp_dir.name, "dummy.cpp")
        with open(dummy_file_path, "w") as f:
            f.write("int main() {}")
            
        self.dummy_files = [dummy_file_path]
        self.processed = [dummy_file_path]
        self.target_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_fonts(self):
        fonts = ["Computer Modern (Default)", "Libertinus", "Times", "Palatino"]
        expected = {
            "Computer Modern (Default)": "",
            "Libertinus": "\\usepackage{libertinus}",
            "Times": "\\usepackage{mathptmx}",
            "Palatino": "\\usepackage{mathpazo}"
        }
        for font in fonts:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, font_choice=font)
            with open(self.output_path, 'r') as f:
                content = f.read()
                if expected[font]:
                    self.assertIn(expected[font], content)

    def test_font_sizes(self):
        sizes = [f"{i}pt" for i in range(9, 41)]
        for size in sizes:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, font_size=size)
            with open(self.output_path, 'r') as f:
                content = f.read()
                self.assertIn(f"\\changefontsizes{{{size}}}", content)

    def test_heading_styles(self):
        styles = ["Bold", "Italic", "Small Caps", "Normal"]
        expected = {
            "Bold": "\\bfseries",
            "Italic": "\\itshape",
            "Small Caps": "\\scshape",
            "Normal": "\\normalfont"
        }
        for style in styles:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, heading_style=style)
            with open(self.output_path, 'r') as f:
                content = f.read()
                self.assertIn(expected[style], content)

    def test_page_formats(self):
        formats = ["a4paper", "letterpaper", "b5paper"]
        for fmt in formats:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, page_format=fmt)
            with open(self.output_path, 'r') as f:
                content = f.read()
                self.assertIn(fmt, content)

    def test_margins(self):
        margins = ["1.5cm", "1.0cm", "2.0cm", "0.5cm"]
        for margin in margins:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, margin=margin)
            with open(self.output_path, 'r') as f:
                content = f.read()
                self.assertIn(f"margin={margin}", content)

    def test_orientations(self):
        orientations = ["Portrait", "Landscape"]
        for ori in orientations:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, orientation=ori)
            with open(self.output_path, 'r') as f:
                content = f.read()
                self.assertIn(ori.lower(), content)

    def test_columns(self):
        columns = [1, 2, 3]
        for col in columns:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, columns=col)
            with open(self.output_path, 'r') as f:
                content = f.read()
                if int(col) == 1:
                    self.assertNotIn("\\begin{multicols*}", content)
                else:
                    self.assertIn(f"\\begin{{multicols*}}{{{col}}}", content)

    def test_code_styles(self):
        styles = ["Black Border (No Background)", "Light Gray Background"]
        for style in styles:
            generate_master_tex(self.dummy_files, self.processed, self.target_dir, self.output_path, code_style=style)
            with open(self.output_path, 'r') as f:
                content = f.read()
                if style == "Black Border (No Background)":
                    self.assertIn("colback=white", content)
                    self.assertIn("colframe=black", content)
                    self.assertIn("colbacktitle=white", content)
                    self.assertIn("coltitle=black", content)
                    self.assertIn("titlerule=0.5pt", content)
                else:
                    self.assertIn("colback=codebg", content)
                    self.assertIn("colframe=codebg", content)
                    self.assertIn("colbacktitle=codebg", content)
                    self.assertIn("coltitle=black", content)

if __name__ == '__main__':
    unittest.main()
