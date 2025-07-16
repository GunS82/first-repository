# ABAP Parser Example

This repository contains a small script for parsing ABAP source files using
[Tree-sitter](https://tree-sitter.github.io/) and validating the names of
objects against reference lists. The project is intended to be run locally on a
single machine (Windows or other OS).

## Prerequisites

1. **Python 3.9+**
2. **Node.js** (to install `tree-sitter-cli` for generating the parser)
3. **CMake** (required by Tree-sitter when building languages)

Install Python packages:

```bash
pip install tree_sitter
```

Install Tree-sitter CLI using npm:

```bash
npm install -g tree-sitter-cli
```

## Building the ABAP Parser

Clone the grammar for ABAP and generate the parser:

```bash
git clone https://github.com/abaplint/tree-sitter-abap.git
cd tree-sitter-abap
# Generate source files
tree-sitter generate
cd ..
```

Build the shared library containing the ABAP grammar:

```bash
python - <<'PY'
from tree_sitter import Language
Language.build_library(
    'build/my-languages.so',
    ['tree-sitter-abap']
)
PY
```

After this step the file `build/my-languages.so` will contain the compiled
Tree-sitter grammar used by the parser script.

## Preparing Reference Lists

Create a directory named `base` and add the following text files with one name
per line:

- `tables.txt` – valid table names
- `classes.txt` – valid class names
- `functions.txt` – valid function module names

## Running the Script

```bash
python abap_parser.py path/to/source.abap base output.json
```

The resulting `output.json` will contain all extracted names and statistics
about which names were not found in the reference lists.

## Example JSON Result

```json
{
  "extracted": {
    "classes": ["ZCL_MY_CLASS"],
    "functions": ["MY_FUNCTION"],
    "forms": ["my_form"],
    "tables": ["MARA", "VBAP"]
  },
  "statistics": {
    "tables": {
      "total": 2,
      "valid": 2,
      "invalid": 0,
      "error_percentage": 0.0,
      "invalid_names": []
    },
    "classes": { ... },
    "functions": { ... }
  }
}
```

This example shows the structure of the output where `invalid_names` lists
objects not present in the corresponding base file.
