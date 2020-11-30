import json

CJN_FLAG_PREFIX = "#%"
CJN_FLAG_IGNORE = CJN_FLAG_PREFIX + " " + "IGNORE"
CJN_FLAG_COMPILE = CJN_FLAG_PREFIX + " " + "COMPILE"

CJN_OPT_COMPILE_MARKED = "compile_marked"
CJN_OPT_ENFORCE_EXEC_COUNT = "enforce_exec_count"

def _read_json(fpath):
    with open(fpath, 'r') as f:
        s = f.read()
    return json.loads(s)

def _clean_cell_head(cell):
    return cell['source'][0].upper().strip()

def _cell_can_compile(cell, opts):
    if not cell['cell_type']=='code':
        return False
    if len(cell['source'])==0:
        return False
    if _clean_cell_head(cell)==CJN_FLAG_IGNORE:
        return False
    if CJN_OPT_COMPILE_MARKED in opts:
        if opts[CJN_OPT_COMPILE_MARKED]:
            return _clean_cell_head(cell)==CJN_FLAG_COMPILE
    return True

def compile_notebook(notebook, output, opts={}):
    nb = _read_json(notebook)
    code = ''
    
    def build_exec_count_fn(opts):
        if CJN_OPT_ENFORCE_EXEC_COUNT in opts:
            if opts[CJN_OPT_ENFORCE_EXEC_COUNT]:
                return lambda c_p: (c_p[0]['execution_count'] > c_p[1], c_p[0]['execution_count'])
        return lambda c_p: True, None
    
    exec_count_check = build_exec_count_fn(opts)
    
    p = 0
    for cell in nb['cells']:
        if _cell_can_compile(cell, opts):
            contig, p = exec_count_check((cell, p))
            if not contig:
                raise Exception("Cell execution count was not contiguous.")
            
            for i in range(len(cell['source'])):
                line = cell['source'][i]
                if i > 0 or line[0:2] != CJN_FLAG_PREFIX:
                    code += line
            code += '\n\n'
    
    with open(output, 'w') as f:
        f.write(code)

def load_compscript(compscript):
    return _read_json(compscript)

def save_compscript(script_def, compscript):
    j = json.dumps(script_def)
    with open(output, 'w') as f:
        f.write(j)

def append_compscript(file_defs, compscript):
    j = load_compscript(compscript)
    for fd in file_defs.keys():
        j[fd] = file_defs[fd]
    save_compscript(j, compscript)

def run_compile_script(compscript):
    cs = load_compscript(compscript)
    
    for f in cs.keys():
        compile_notebook(f, cs[f]['output'], cs[f]['opts'])

