#!/usr/bin/env python3
"""
make-generic.py — derive a campaign-neutral build from the working mapper.

    python make-generic.py index.html index-generic.html

Removes everything welded to one vault and one setting:

  * POI_NOTES / POI_PERMALINKS / TOWN_NOTE lookup tables
  * OBSIDIAN_VAULT / HEX_NOTE_DIR / POI_DIR path constants
  * exportMapNote() and the three buttons that depend on it
    (Obsidian note, Publish note, Web map)
  * the "Darlene" world-coordinate label

Keeps: Export, Import, Pipeline, Hex notes, Autosave, and — if present —
the legend, calibration watch, and player sharing blocks.

The Player map export replaces Web map. It is driven by state.notes, so it
works for any campaign, which the old one never did.

Idempotent. Refuses to write if the input has already been processed.
"""

import re
import sys


def brace_span(src, start):
    """Byte span of the function whose body opens at the first { after start."""
    i = src.index('{', start)
    depth, j = 0, i
    while True:
        if src[j] == '{':
            depth += 1
        elif src[j] == '}':
            depth -= 1
            if depth == 0:
                return start, j + 1
        j += 1


def cut_const(src, name):
    """Remove `const NAME = ...;` including multi-line object literals."""
    m = re.search(r'\nconst %s\s*=' % re.escape(name), src)
    if not m:
        return src, False
    start = m.start() + 1
    j = m.end()
    depth = 0
    while j < len(src):
        c = src[j]
        if c in '{[':
            depth += 1
        elif c in '}]':
            depth -= 1
        elif c == ';' and depth == 0:
            j += 1
            break
        j += 1
    while j < len(src) and src[j] == '\n':
        j += 1
    return src[:start] + src[j:], True


def main(inp, outp):
    src = open(inp, encoding='utf-8').read()
    original = len(src)

    if 'GENERIC BUILD' in src:
        sys.exit('Already a generic build — nothing to do.')

    report = []

    # 1. buttons that depend on the campaign tables
    for bid in ('obsidianBtn', 'publishBtn', 'webBtn'):
        pat = re.compile(r'\s*<button id="%s".*?</button>' % bid, re.S)
        src, n = pat.subn('', src)
        report.append(('button ' + bid, n))

    # 2. their click handlers (all three sit on one line)
    src, n = re.subn(
        r"\$\('obsidianBtn'\)\.onclick[^;]*;\s*\$\('publishBtn'\)\.onclick[^;]*;\s*\$\('webBtn'\)\.onclick[^;]*;",
        '', src)
    report.append(('export handlers', n))

    # 3. exportMapNote itself
    m = re.search(r'\nfunction exportMapNote', src)
    if m:
        a, b = brace_span(src, m.start() + 1)
        src = src[:a] + src[b:]
        report.append(('exportMapNote()', 1))
    else:
        report.append(('exportMapNote()', 0))

    # 3b. startExport() is now dead — it only ever called exportMapNote
    m = re.search(r'\nfunction startExport', src)
    if m:
        a, b = brace_span(src, m.start() + 1)
        src = src[:a] + src[b:]
        report.append(('startExport()', 1))
    else:
        report.append(('startExport()', 0))

    # 4. the calibration branch that routed into it
    src, n = re.subn(
        r"else exportMapNote\(pendingMode \|\| 'obsidian'\);",
        "else exportHexNotes();", src)
    report.append(('calibration fallthrough', n))

    # 5. campaign constants
    for c in ('POI_NOTES', 'POI_PERMALINKS', 'TOWN_NOTE',
              'OBSIDIAN_VAULT', 'HEX_NOTE_DIR', 'POI_DIR'):
        src, ok = cut_const(src, c)
        report.append(('const ' + c, int(ok)))

    # 6. world-coordinate label: setting-driven, hidden when unset
    src, n = re.subn(r"function darleneLabel\(", "function worldLabel(", src)
    src, n2 = re.subn(r"darleneLabel\(", "worldLabel(", src)
    report.append(('darleneLabel -> worldLabel', n + n2))

    src, n = re.subn(r"parts\.push\('Darlene ' \+ D\)",
                     "parts.push((state.settings.worldLabelName || 'World') + ' ' + D)", src)
    report.append(('badge label', n))

    # offsets default to 0 and the label is suppressed entirely when both are 0
    src, n = re.subn(r"darleneColOff: 100, darleneRowOff: 57",
                     "darleneColOff: 0, darleneRowOff: 0, worldLabelName: '', "
                     "gridCols: 10, gridRows: 8", src)
    report.append(('default offsets', n))

    src, n = re.subn(
        r"(function worldLabel\(col, row\) \{\s*const v = vaultCoord\(col, row\);\s*if \(!v\) return null;)",
        r"\1\n  if (!state.settings.worldLabelName) return null;", src)
    report.append(('suppress when unnamed', n))

    # 7. frontmatter key follows the label name
    # str.replace, not re.subn: the literal \n in the JS source must survive
    _fm_old = '''if (dar) out += 'darlene: "' + dar + '"\\n';'''
    _fm_new = '''if (dar) out += (state.settings.worldLabelName || 'world').toLowerCase() + ': "' + dar + '"\\n';'''
    n = src.count(_fm_old)
    src = src.replace(_fm_old, _fm_new)
    report.append(('hex note frontmatter', n))

    # 8. generic default region
    src, n = re.subn(r"\|\| 'West Marches'", "|| 'Unsorted'", src)
    report.append(('default region', n))

    # 8b. residual campaign prose
    src, n = re.subn(r"terrain colours, regions and Darlene coords",
                     "terrain colours, regions and world coords", src)
    report.append(('pipeline tooltip', n))
    src, n = re.subn(r"// Three grids reconcile through [^\n]*\n", 
                     "// Three grids reconcile through the anchor hex you calibrate against.\n", src)
    report.append(('reconciliation comment', n))

    # 9. marker
    src = src.replace('<head>', '<head>\n<!-- GENERIC BUILD — campaign tables removed by make-generic.py -->', 1)

    open(outp, 'w', encoding='utf-8').write(src)

    print('%-28s %s' % ('CHANGE', 'APPLIED'))
    for label, n in report:
        flag = 'ok' if n else 'NOT FOUND'
        print('%-28s %s' % (label, flag))
    print('\n%d -> %d bytes' % (original, len(src)))

    leftovers = [w for w in ('Ritterstadt', 'Greyhawk', 'Darlene', 'POI_NOTES', 'POI_PERMALINKS')
                 if w in src]
    print('residual campaign references:', leftovers or 'none')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])