#!/usr/bin/env python3

import json
import sys
import re

NEWLINE_REGEX = re.compile(r'\r?\n')

INJECTION_REGEX = re.compile(r'(%PANEL%\r?\n(.*?)\r?\n%PANEL%)', flags=re.DOTALL)

PANEL_SRC_REGEX = re.compile(r'^src\(\s*(.*)\s*\)$')
PANEL_TERM_REGEX = re.compile(r'^term\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(".*")\s*\)$')
PANEL_ALT_REGEX = re.compile(r'^alt\((.*)\)$')
PANEL_TITLE_REGEX = re.compile(r'^title\((.*)\)')

INJECTION_GLOSS_TERM = '{{x:{0},y:{1},w:{2},h:{3},content:{4}}}'
INJECTION_SCRIPT = '''
<script>
{{
    const terms = {3};

    const panel_container = document.currentScript.previousElementSibling;
    panel_container.classList.add('comic-panel');

    const img_node = panel_container.childNodes[0];
    img_node.addEventListener('load', e => {{
        const scale = img_node.offsetWidth / img_node.naturalWidth;
        for (const t of terms) {{
            const t_overlay = document.createElement('div');
            t_overlay.classList.add('gloss-term-overlay');
            t_overlay.style = `left:${{t.x*scale}}px;top:${{t.y*scale}}px;width:${{t.w*scale}}px;height:${{t.h*scale}}px;`
            t_overlay.addEventListener('click', e => alert(t.content));
            panel_container.appendChild(t_overlay);
        }}
    }});
}}
</script>
'''
INJECTION_TEMPLATE = '![{0}]({1} {2})\n' + INJECTION_SCRIPT

def create_term_list(terms):
    return '[' + ', '.join((INJECTION_GLOSS_TERM.format(*t) for t in terms)) + ']'

def inject_panels(content):
    matches = INJECTION_REGEX.findall(content)
    replacements = []
    for full_match, match_content in matches:
        cmds = re.split(NEWLINE_REGEX, match_content)
        src_file = None
        alt_text = 'ALT TEXT'
        title = 'TITLE'
        terms = []
        for c in cmds:
            res = PANEL_SRC_REGEX.match(c)
            if res is not None:
                src_file = res.group(1)
                continue
            res = PANEL_TERM_REGEX.match(c)
            if res is not None:
                terms.append(res.groups())
                continue
            res = PANEL_ALT_REGEX.match(c)
            if res is not None:
                alt_text = res.group(1)
                continue
            res = PANEL_TITLE_REGEX.match(c)
            if res is not None:
                title = res.group(1)
                continue
        replacements.append((full_match, alt_text, src_file, title, terms))
    
    res = content
    for (m, a, f, t, terms) in replacements:
        if f is None:
            raise 'You must specify a file for this comic panel!'
        res = res.replace(m, INJECTION_TEMPLATE.format(a, f, f'"{t}"', create_term_list(terms)))
    # print(f'!!INJECT CONTENT!!\n{res}\n!!END!!', file=sys.stderr)
    return res

def do_injection(chapter):
    chapter['content'] = inject_panels(chapter['content'])
    for sub in chapter['sub_items']:
        do_injection(sub['Chapter'])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'supports':
            sys.exit(0)
    
    context, book = json.load(sys.stdin)

    for chapter in book['sections']:
        do_injection(chapter['Chapter'])

    # print(json.dumps(book, indent='  '), file=sys.stderr)

    print(json.dumps(book))

    sys.exit(0)