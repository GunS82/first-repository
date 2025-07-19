# ABAP Parser Example

This repository contains a simple script for parsing ABAP source files using the
[ABAP-Code-Scanner](https://github.com/redrays-io/ABAP-Code-Scanner) library. It
extracts class, function module, FORM and table names from ABAP code and checks
them against reference lists. The project is intended to be run locally on a
single machine (Windows or other OS).

## Prerequisites

1. **Python 3.9+**

Install Python packages:

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
