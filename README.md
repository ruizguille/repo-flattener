# Repository Flattener

A utility script that flattens a repository's structure into a single directory while preserving path information in filenames. Perfect for providing context to LLM tools (like Claude Projects or ChatGPT) when analyzing your codebase.

Instead of uploading files one by one and explaining your project structure, this script creates a flattened version of your repository where all files are in a single directory, with their original paths encoded in the filenames.

For example, this structure:
```
my-app/
  ├── src/
  │   ├── components/
  │   │   └── Button.jsx
  │   └── utils/
  │       └── validation.js
  └── package.json
```

Becomes:
```
my-app_flat/
  ├── src__components__Button.jsx
  ├── src__utils__validation.js
  └── package.json
```

Now you can easily drag and drop these files into your favorite LLM tool while preserving the original structure information!

For a detailed walkthrough of the code and the technologies used, check out this blog post: []()

## Configuration

The script includes several configuration variables you can customize:

- `EXCLUDED_DIRS`: Directories to skip (e.g., 'node_modules', '.git', 'venv').
- `EXCLUDED_FILES`: Specific files to skip (e.g., '.gitignore', 'package-lock.json').
- `EXCLUDED_EXTENSIONS`: File extensions to skip (e.g., images, binary files).
- `DEFAULT_INCLUDED_EXTENSIONS`: File extensions to include by default.

The default configuration is tuned for Python and JavaScript projects but can be easily adjusted for other technologies.

## Usage

Navigate to the directory containing `flatten_repo.py` and run:

```bash
python flatten_repo.py /path/to/your/project
```

Arguments:
- Path to the directory you want to flatten (optional, defaults to current directory)
- `--include-all` flag to include all file extensions except those explicitly excluded

## Global Command Setup

For more convenient usage, you can make the script available as a global command. For example in macOS/Linux:

1. Make the script executable:
    ```bash
    chmod +x flatten_repo.py
    ```

2. Create a symlink in your system's bin directory:
    ```bash
    ln -s /path/to/flatten_repo.py /usr/local/bin/flatten-repo
    ```

Now you can run `flatten-repo` from any directory!

*On Windows, you need to either add the script’s folder to your PATH or create a batch file that calls the script.*