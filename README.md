# ABAP Parser Example

This repository contains a small script for parsing ABAP source files using the
[ABAP Code Scanner](https://github.com/redrays-io/ABAP-Code-Scanner) library.
The script extracts class names, function module calls and database tables used
in the source and validates them against reference lists. The project is
intended to be run locally on a single machine (Windows or other OS).

## Prerequisites

- **Python 3.9+**

Install the required Python packages:

```bash
pip install -r requirements.txt
```

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
