import os
from cp2pdf.config import SUPPORTED_EXTENSIONS, HIDDEN_DIRS

class TreeNode:
    """Represents a file or directory in the selection tree."""
    def __init__(self, name, path, is_dir, parent=None):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.parent = parent
        self.children = []
        self.expanded = False # Folders are collapsed by default visually
        self.selected = True  # Requirement: All folders and files marked by default

def scan_directory(base_path):
    """
    Recursively scans the directory and builds a tree structure.
    It ignores HIDDEN_DIRS but includes everything else (like 'notes').
    Filters files by SUPPORTED_EXTENSIONS.
    """
    root_name = os.path.basename(os.path.normpath(base_path))
    if not root_name:
        root_name = base_path
        
    root_node = TreeNode(root_name, base_path, True)
    
    def _build_tree(current_dir, parent_node):
        try:
            entries = sorted(os.listdir(current_dir))
        except PermissionError:
            return
            
        # Separate into directories and files for nice ordering (dirs first)
        dirs = []
        files = []
        
        for entry in entries:
            if entry in HIDDEN_DIRS:
                continue
                
            full_path = os.path.join(current_dir, entry)
            if os.path.isdir(full_path):
                dirs.append((entry, full_path))
            else:
                if entry.endswith(SUPPORTED_EXTENSIONS):
                    files.append((entry, full_path))
                    
        # Process directories
        for d_name, d_path in dirs:
            dir_node = TreeNode(d_name, d_path, True, parent=parent_node)
            _build_tree(d_path, dir_node)
            # Only add directory if it contains valid files recursively
            if dir_node.children:
                parent_node.children.append(dir_node)
                
        # Process files
        for f_name, f_path in files:
            file_node = TreeNode(f_name, f_path, False, parent=parent_node)
            parent_node.children.append(file_node)

    _build_tree(base_path, root_node)
    
    # Auto-expand the root node by default
    root_node.expanded = True
    return root_node
