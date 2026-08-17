import curses
import os

def run_dir_picker(stdscr, start_dir="."):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
        
    stdscr.nodelay(0)
    
    # Colors
    has_color = False
    try:
        if curses.has_colors():
            has_color = True
    except curses.error:
        pass
        
    current_dir = os.path.abspath(start_dir)
    
    cursor_y = 0
    offset = 0
    
    def get_items(path):
        try:
            items = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            items.sort(key=lambda x: x.lower())
            return [".."] + items
        except PermissionError:
            return [".."]
            
    items = get_items(current_dir)
    
    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        
        max_visible = max(1, height - 4)
        if cursor_y < offset:
            offset = cursor_y
        elif cursor_y >= offset + max_visible:
            offset = cursor_y - max_visible + 1
            
        # Header
        header_text = f" Directory Picker | Current: {current_dir} "
        attr_header = curses.color_pair(1) | curses.A_BOLD if has_color else curses.A_BOLD
        stdscr.addstr(0, 0, header_text.ljust(width)[:width], attr_header)
        
        # Content
        for i in range(max_visible):
            idx = offset + i
            if idx >= len(items):
                break
                
            item = items[idx]
            icon = "📁 "
            if item == "..":
                icon = "🔙 "
                
            line_text = f"  {icon}{item}"
            padded_line = line_text.ljust(width)[:width-1]
            
            screen_y = i + 2
            
            if idx == cursor_y:
                attr_highlight = curses.color_pair(2) | curses.A_BOLD if has_color else curses.A_REVERSE | curses.A_BOLD
                stdscr.addstr(screen_y, 0, padded_line, attr_highlight)
            else:
                stdscr.addstr(screen_y, 0, padded_line)
                
        # Footer
        footer_text1 = " [↑/↓] Move   [ENTER] Open Folder   [X] Select Current Folder   [ESC] Cancel "
        attr_footer = curses.color_pair(1) if has_color else curses.A_REVERSE
        try:
            stdscr.addstr(height - 1, 0, footer_text1.center(width)[:width], attr_footer)
        except curses.error:
            pass
            
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_UP:
            cursor_y = max(0, cursor_y - 1)
        elif key == curses.KEY_DOWN:
            cursor_y = min(len(items) - 1, cursor_y + 1)
        elif key == curses.KEY_NPAGE:
            cursor_y = min(len(items) - 1, cursor_y + max_visible)
        elif key == curses.KEY_PPAGE:
            cursor_y = max(0, cursor_y - max_visible)
        elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
            # Open directory
            selected_item = items[cursor_y]
            new_dir = os.path.abspath(os.path.join(current_dir, selected_item))
            if os.path.isdir(new_dir):
                current_dir = new_dir
                items = get_items(current_dir)
                cursor_y = 0
                offset = 0
        elif key in [ord('x'), ord('X')]:
            # Select current directory
            return current_dir
        elif key == 27: # ESC
            return None

if __name__ == "__main__":
    print(run_dir_picker("."))
