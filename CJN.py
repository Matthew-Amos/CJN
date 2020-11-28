import json

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
    if _clean_cell_head(cell)=="#% IGNORE":
        return False
    if 'compile_marked' in opts:
        if opts['compile_marked']:
            return _clean_cell_head(cell)=="#% COMPILE"
    return True

def compile_notebook(notebook, output, opts={}):
    nb = _read_json(notebook)
    code = ''
    
    def build_exec_count_fn(opts):
        if 'enforce_exec_count' in opts:
            if opts['enforce_exec_count']:
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
                if i > 0 or line[0:2] != '#%':
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

