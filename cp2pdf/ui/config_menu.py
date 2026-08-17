import curses
import os

def run_config_menu():
    def ui_loop(stdscr):
        try:
            curses.curs_set(1)
        except:
            pass
        stdscr.nodelay(0)
        curses.start_color()
        curses.use_default_colors()
        
        # Safe color initialization using transparent background (-1)
        bg = -1
            
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_GREEN, bg)
        curses.init_pair(4, curses.COLOR_YELLOW, bg)
        
        # Options definition
        config = {
            "target_dir": ".",
            "output_dir": ".",
            "format": ["Both PDF and LaTeX", "PDF Only", "LaTeX Only"],
            "split": ["Yes (Docs & Code)", "No (Single Document)"],
            "font": ["Computer Modern (Default)", "Libertinus", "Times", "Palatino"],
            "font_size": [f"{i}pt" for i in range(9, 41)],
            "heading_style": ["Bold", "Italic", "Small Caps", "Normal"],
            "page_format": ["a4paper", "letterpaper", "b5paper"],
            "margin": ["1.5cm (Normal)", "1.0cm (Narrow)", "2.0cm (Wide)", "0.5cm (Minimal)"],
            "orientation": ["Portrait", "Landscape"],
            "columns": ["2", "1", "3"],
            "code_style": ["Black Border (No Background)", "Light Gray Background"]
        }
        
        # Current index in the lists for enum options
        selections = {
            "format": 0, "split": 0, "font": 0, "font_size": 0, "heading_style": 0, 
            "page_format": 0, "margin": 0, "orientation": 0, "columns": 0, "code_style": 0
        }
        
        fields = [
            ("target_dir", "Target Directory"),
            ("output_dir", "Output Directory"),
            (None, ""),
            ("format", "Output Format"),
            ("split", "Split Documents"),
            (None, ""),
            ("font", "Font Family"),
            ("font_size", "Base Font Size"),
            ("heading_style", "Heading Style"),
            ("page_format", "Page Format"),
            ("margin", "Page Margins"),
            ("orientation", "Page Orientation"),
            ("columns", "Columns"),
            (None, ""),
            ("code_style", "Code Block Style"),
            (None, ""),
            ("BUILD", "[ Proceed to File Selection ]")
        ]
        
        cursor_y = 0
        
        # Move to the first selectable field
        while fields[cursor_y][0] is None:
            cursor_y += 1

        def edit_string(title, initial):
            curses.echo()
            try:
                curses.curs_set(1)
            except:
                pass
            
            prompt = f"Enter new value for {title}: "
            height, width = stdscr.getmaxyx()
            
            edit_win = curses.newwin(5, width - 4, height//2 - 2, 2)
            edit_win.bkgd(' ', curses.color_pair(1))
            edit_win.box()
            edit_win.addstr(1, 2, prompt)
            edit_win.addstr(2, 2, initial)
            edit_win.refresh()
            
            # Use getstr to get user input
            s = edit_win.getstr(2, 2, 255).decode('utf-8').strip()
            
            curses.noecho()
            try:
                curses.curs_set(0)
            except:
                pass
            
            return s if s else initial

        try:
            curses.curs_set(0)
        except:
            pass

        while True:
            stdscr.erase()
            height, width = stdscr.getmaxyx()
            
            header_text = " ICPC Template Builder - Configuration Menu "
            has_color = curses.has_colors()
            attr_header = curses.color_pair(1) | curses.A_BOLD if has_color else curses.A_BOLD
            stdscr.addstr(0, 0, header_text.center(width)[:width], attr_header)
            
            for i, (key, label) in enumerate(fields):
                if key is None:
                    continue
                    
                screen_y = i + 2
                
                if key == "BUILD":
                    display_text = f"  {label}"
                else:
                    if isinstance(config[key], list):
                        val = config[key][selections[key]]
                        display_text = f"  [{label:<20}] < {val} >"
                    else:
                        val = config[key]
                        display_text = f"  [{label:<20}] {val}"
                
                padded = display_text.ljust(width)[:width-1]
                
                if i == cursor_y:
                    attr_high = curses.color_pair(2) | curses.A_BOLD if has_color else curses.A_REVERSE | curses.A_BOLD
                    stdscr.addstr(screen_y, 0, padded, attr_high)
                else:
                    stdscr.addstr(screen_y, 0, padded)
                    
            footer_text1 = " [↑/↓] Move   [←/→] Change Options   [ENTER] Edit Text / Proceed "
            attr_footer = curses.color_pair(1) if has_color else curses.A_REVERSE
            try:
                stdscr.addstr(height - 1, 0, footer_text1.center(width)[:width], attr_footer)
            except curses.error:
                pass
                
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                cursor_y -= 1
                while cursor_y >= 0 and fields[cursor_y][0] is None:
                    cursor_y -= 1
                if cursor_y < 0:
                    cursor_y = len(fields) - 1
                    while fields[cursor_y][0] is None:
                        cursor_y -= 1
            elif key == curses.KEY_DOWN:
                cursor_y += 1
                while cursor_y < len(fields) and fields[cursor_y][0] is None:
                    cursor_y += 1
                if cursor_y >= len(fields):
                    cursor_y = 0
                    while fields[cursor_y][0] is None:
                        cursor_y += 1
            elif key == curses.KEY_RIGHT:
                k = fields[cursor_y][0]
                if k and isinstance(config[k], list):
                    selections[k] = (selections[k] + 1) % len(config[k])
            elif key == curses.KEY_LEFT:
                k = fields[cursor_y][0]
                if k and isinstance(config[k], list):
                    selections[k] = (selections[k] - 1 + len(config[k])) % len(config[k])
            elif key in [10, 13, curses.KEY_ENTER]:
                k = fields[cursor_y][0]
                if k == "BUILD":
                    break
                elif k in ["target_dir", "output_dir"]:
                    from cp2pdf.ui.dir_picker import run_dir_picker
                    new_dir = run_dir_picker(stdscr, config[k])
                    if new_dir:
                        config[k] = os.path.relpath(new_dir, ".") if new_dir != os.path.abspath(".") else "."
                    # Clear screen to force full redraw of config menu after picker closes
                    stdscr.clear()
                elif k and not isinstance(config[k], list):
                    config[k] = edit_string(fields[cursor_y][1], config[k])

        final_config = {}
        for k in config:
            if isinstance(config[k], list):
                final_config[k] = config[k][selections[k]]
            else:
                final_config[k] = config[k]
                
        return final_config

    try:
        return curses.wrapper(ui_loop)
    except Exception as e:
        print(f"Error launching advanced TUI: {e}")
        return None

if __name__ == "__main__":
    print(run_config_menu())
