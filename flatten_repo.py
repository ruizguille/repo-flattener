#!/usr/bin/env python3
"""
Repository flattener utility script.
Flattens a repository's structure into a single directory while preserving path information
in filenames. Useful for providing context to LLMs.
"""

from pathlib import Path
import shutil
import argparse
import sys

FILENAME_PATH_SEPARATOR = '__'

EXCLUDED_DIRS = {
    'node_modules', '.git', '.venv', 'venv', '__pycache__', 'dist', 'build', 'data'
}

EXCLUDED_FILES = {
    '.gitignore', '.DS_Store', 'package-lock.json', 'yarn.lock', 'uv.lock', '__init__.py',
    '.env', '.env.local', '.env.development', '.env.production', '.env.test', '.env.staging' 
}

EXCLUDED_EXTENSIONS = {
    '.pyc', '.pyo',  # Python bytecode
    '.jpg', '.jpeg', '.png', '.gif', '.ico', '.svg',  # Images
    '.pdf', '.lock', '.log',  # Other binary/lock files
    '.map'  # Source maps
}

# Default include extensions for Python/JavaScript projects
DEFAULT_INCLUDE_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx',  # Source code
    '.json', '.yaml', '.yml', '.toml',    # Config files
    '.md', '.txt', '.rst'                 # Documentation
}

def should_include_file(path: Path, include_all_extensions: bool) -> bool:
    """Determine if a file should be included in the flattened output."""
    # Check if path contains excluded directories
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    
    # Check if filename is in excluded files
    if path.name in EXCLUDED_FILES:
        return False
        
    # Check if extension is excluded
    if path.suffix.lower() in EXCLUDED_EXTENSIONS:
        return False
        
    # If include_all_extensions is True, include all non-excluded files
    # Otherwise, check if extension is in DEFAULT_INCLUDE_EXTENSIONS
    return include_all_extensions or path.suffix.lower() in DEFAULT_INCLUDE_EXTENSIONS

def get_safe_filename(path: str) -> str:
    """Convert a path to a safe filename by replacing slashes with double underscores."""
    return path.replace('/', '__')

def flatten_repository(source_dir: Path, include_all_extensions: bool = False) -> None:
    """Flatten a repository's structure into a single directory with path-preserving filenames.

    Creates a new directory named '{source_dir}_flat' containing copies of files from the source
    directory. The original directory structure is encoded in the filenames, with slashes 
    replaced by double underscores.
    
    Args:
        source_dir: Path to the directory to flatten
        include_all_extensions: If True, includes all files regardless of their extension
            (except those explicitly excluded). If False, only includes files with
            extensions listed in DEFAULT_INCLUDE_EXTENSIONS.
    """
    # Convert to absolute path and resolve any symlinks
    source_dir = source_dir.resolve()
    
    # Create output directory name based on source directory
    output_dir = source_dir.with_name(f"{source_dir.name}_flat")
    output_dir.mkdir(exist_ok=True)
    
    # Track processed files for collision detection
    processed_files = set()
    
    # Walk through source directory
    for file_path in source_dir.rglob('*'):
        if file_path.is_dir():
            continue
            
        # Skip files in the output directory
        if output_dir in file_path.parents:
            continue
            
        if not should_include_file(file_path, include_all_extensions):
            continue
        
        # Create new filename using original path
        rel_path = str(file_path.relative_to(source_dir))
        display_name = rel_path  # Keep the original path for display
        safe_name = get_safe_filename(rel_path)  # Convert to safe filename
        
        # Check for collisions
        if safe_name in processed_files:
            print(f"Warning: Duplicate file name detected: {display_name}", file=sys.stderr)
            continue
            
        processed_files.add(safe_name)
        
        # Copy file to output directory
        try:
            shutil.copy2(file_path, output_dir / safe_name)
            print(f"Copied: {display_name}")
        except Exception as e:
            print(f"Error copying {display_name}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Flatten a repository's structure while preserving path information."
    )
    parser.add_argument(
        "source_dir",
        type=lambda p: Path(p).resolve(),
        nargs='?',
        default='.',
        help="Source directory to flatten (default: current directory)"
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include all file extensions except those explicitly excluded"
    )

    args = parser.parse_args()

    try:
        flatten_repository(args.source_dir, args.include_all)
        print(f"\nRepository flattened successfully in '{args.source_dir.name}_flat'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()