# Compile Jupyter Notebooks

Compiles code cells from a Jupyter notebook into a single script.

## Installation

This module is intended to be imported locally, so all you need to do is save
_CJN.py_ to your project directory, then imported via `import CJN`.

## Usage

### Normal Code Cells

The first line in a code cell may be optionally annotated with the following:

`#% ignore` - will ignore the cell.

`#% compile` - explicitly mark a cell for compilation. Compiling with the
option `compile_marked` as `True` will only compile these cells.

### CJN API

__Compile a single notebook__

```python
compile_notebook(
  notebook, # Path to the .ipynb file
  output,   # Path/name of the output file, e.g. myscript.py
  opts={},  # Additional compilation options (see below)
)
```

Compilation options currently include:
- `'compiled_marked`: True|False` - only compiled cells annotated with `#%
  compile`.

__Compile multiple notebooks with a compile script__

Compile commands can be saved in a json encoding. The general form is:

_compile.json_

```json
{
  "CJN.ipynb": {
    "output": "CJN.py",
    "opts": { "compile_marked": true }
  },
  "other.ipynb": {
    "output": "other.jl",
    "opts": { "compiled_marked": false }
  }
}
```

The above can be compiled via `run_compile_script("compile.json")`.

This is useful for creating a standalone script that can process multiple
notebooks at once. Helper commands are available to create the compile script.

- `load_compscript(compscript)` - load the JSON compile script.
- `save_compscript(script_def, compscript)` - save the script definition to the
  _compscript_ file path.
- `append_compscript(file_defs, compscript)`: append file definitions to an
  existing compile script.

