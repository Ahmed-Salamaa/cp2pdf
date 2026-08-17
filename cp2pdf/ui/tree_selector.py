import curses
import os

def get_selection_state(node):
    if not node.is_dir:
        return 1 if node.selected else 0
    if not node.children:
        return 0
    states = [get_selection_state(c) for c in node.children]
    if all(s == 1 for s in states): return 1
    if all(s == 0 for s in states): return 0
    return 2 # partial

def toggle_selection(node, state):
    node.selected = state
    for child in node.children:
        toggle_selection(child, state)

def run_interactive_ui(tree_root):
    def ui_loop(stdscr):
        try:
            curses.curs_set(0)
        except curses.error:
            pass
            
        stdscr.nodelay(0)
        
        # Colors
        has_color = False
        try:
            curses.start_color()
            curses.use_default_colors()
            try:
                has_color = True
                bg = -1
                
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Header/Footer
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # Highlight
                curses.init_pair(3, curses.COLOR_GREEN, bg)                   # Selected [x]
                curses.init_pair(4, curses.COLOR_YELLOW, bg)                  # Partial [-]
                curses.init_pair(5, curses.COLOR_CYAN, bg)                    # Dir icon
            except curses.error:
                # Fallback if transparency fails
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
                curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
                curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        except curses.error:
            pass
        
        cursor_y = 0
        offset = 0

        def get_flat_list(node, display_prefix="", next_prefix=""):
            visible = []
            visible.append((node, display_prefix))
            if getattr(node, 'is_dir', False) and getattr(node, 'expanded', False):
                children = getattr(node, 'children', [])
                for i, child in enumerate(children):
                    is_last = (i == len(children) - 1)
                    pointer = "└── " if is_last else "├── "
                    child_display = next_prefix + pointer
                    child_next = next_prefix + ("    " if is_last else "│   ")
                    visible.extend(get_flat_list(child, child_display, child_next))
            return visible

        while True:
            stdscr.erase()
            height, width = stdscr.getmaxyx()
            
            flat_items = get_flat_list(tree_root)
            if not flat_items:
                break
                
            cursor_y = max(0, min(cursor_y, len(flat_items) - 1))
            
            # 2 lines for header, 2 lines for footer
            max_visible = max(1, height - 4)
            if cursor_y < offset:
                offset = cursor_y
            elif cursor_y >= offset + max_visible:
                offset = cursor_y - max_visible + 1

            # Header
            header_text = " ICPC Template Builder - File Selection "
            attr_header = curses.color_pair(1) | curses.A_BOLD if has_color else curses.A_BOLD
            stdscr.addstr(0, 0, header_text.center(width)[:width], attr_header)
            
            # Content
            for i in range(max_visible):
                idx = offset + i
                if idx >= len(flat_items):
                    break
                    
                node, prefix = flat_items[idx]
                state = get_selection_state(node)
                
                if state == 1:
                    cb = "[x]"
                elif state == 2:
                    cb = "[-]"
                else:
                    cb = "[ ]"
                    
                if node.is_dir:
                    icon = "📂 " if node.expanded else "📁 "
                else:
                    icon = "📄 "
                    
                line_text = f" {cb} {prefix}{icon}{node.name}"
                # Pad with spaces for full-width highlight
                padded_line = line_text.ljust(width)[:width-1]
                
                screen_y = i + 2
                
                if idx == cursor_y:
                    attr_highlight = curses.color_pair(2) | curses.A_BOLD if has_color else curses.A_REVERSE | curses.A_BOLD
                    stdscr.addstr(screen_y, 0, padded_line, attr_highlight)
                else:
                    stdscr.addstr(screen_y, 0, padded_line)
                    
            # Footer
            footer_text1 = " [↑/↓] Move   [PgUp/PgDn] Page   [←/→] Expand/Collapse   [SPACE] Toggle "
            footer_text2 = " [A] Select All   [C] Clear All   [ENTER] Confirm & Build "
            attr_footer = curses.color_pair(1) if has_color else curses.A_REVERSE
            try:
                stdscr.addstr(height - 2, 0, footer_text1.center(width)[:width], attr_footer)
                stdscr.addstr(height - 1, 0, footer_text2.center(width)[:width], attr_footer)
            except curses.error:
                pass
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                cursor_y -= 1
            elif key == curses.KEY_DOWN:
                cursor_y += 1
            elif key == curses.KEY_NPAGE:
                cursor_y += max_visible
            elif key == curses.KEY_PPAGE:
                cursor_y -= max_visible
            elif key == curses.KEY_RIGHT:
                if flat_items[cursor_y][0].is_dir:
                    flat_items[cursor_y][0].expanded = True
            elif key == curses.KEY_LEFT:
                if flat_items[cursor_y][0].is_dir:
                    flat_items[cursor_y][0].expanded = False
            elif key == ord(' '):
                node = flat_items[cursor_y][0]
                new_state = False if get_selection_state(node) == 1 else True
                toggle_selection(node, new_state)
            elif key in [ord('c'), ord('C')]:
                toggle_selection(tree_root, False)
            elif key in [ord('a'), ord('A')]:
                toggle_selection(tree_root, True)
            elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                break

    try:
        curses.wrapper(ui_loop)
    except Exception as e:
        print("UI Error: Terminal might be too small, or unsupported environment.")
        print(f"Details: {e}")
        return []
    
    selected_files = []
    def gather_selected(node):
        if not node.is_dir and node.selected:
            selected_files.append(node.path)
        for child in node.children:
            gather_selected(child)
            
    gather_selected(tree_root)
    return selected_files
