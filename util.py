#!/usr/bin/python3
import json
import os

from collections import OrderedDict

def to_json(p, f, l, t, d, main=None, cwe=None, repository=None, report=None):
    return OrderedDict([('project', p), ('file', f), ('line', l), ('type', t),
            ('Main', main), ('CWE', cwe), ('repository', repository),
            ('report', report), ('detector', [d])])

def eq_json(js1, js2):
    return (js1['project'] == js2['project']) and \
        (js1['file'] == js2['file']) and \
        (js1['line'] == js2['line']) and \
        (js1['type'] == js2['type'])
   
def join_json(js1, js2):
    s = set(js1['detector']) | set(js2['detector'])
    js1['detector'] = list(s)
    return js1

def add_json(old_js_list, new_js):
    new_js_list = []
    added = False
    for old_js in old_js_list:
        if eq_json(old_js, new_js):
            joined = join_json(old_js, new_js)
            new_js_list.append(joined)
            added = True
        else:
            new_js_list.append(old_js)
    if not added:
        new_js_list.append(new_js)
    return new_js_list

def dump(args, bug_prj, bug_file, l, t, d, main=None, cwe=None, repository=None, report=None):
    if os.path.exists(args.output):
        with open(args.output, 'r') as f:
            js = json.load(f, object_pairs_hook=OrderedDict)
    else:
        js = []
    labels = add_json(js, to_json(bug_prj, bug_file, l, t, d, main=main, cwe=cwe, repository=repository, report=report))
    with open(args.output, 'w') as f:
        json.dump(labels, f, indent=2)
