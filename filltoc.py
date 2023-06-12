# %% [markdown]
#
# We need to fill in the places where the .rst contained a toctree with XML
# includes. The initial XSLT conversion translates the toctree nodes into a
# marker tag that we can find and replace with the appropriate XML.
#
# %%

from pathlib import Path
import os
import re
import sys


blank = re.compile(r'^\s*$')
comment = re.compile('^\s*\.\. ')
marker = re.compile(r'^\s*<tocToBeReplaced/>\s*$')
toctree = re.compile(r'^\s*.. toctree::\s*')
element = re.compile(r'(<\w+)')
addXi = r'\1 xmlns:xi="http://www.w3.org/2001/XInclude" xml:lang="en-US"';


def is_blank(line):
    return blank.fullmatch(line)

def is_comment(line):
    return comment.match(line)

def getTOC(rstfile):
    state = 'start'
    toc_names = []
    with open(rstfile) as f:
        for line in f:
            if state == 'start' and toctree.fullmatch(line):
                state = 'saw_toctree'
            elif state == 'saw_toctree' and is_blank(line):
                state = 'in_toc'
            elif state == 'in_toc':
                if is_blank(line):
                    break
                elif is_comment(line):
                    pass
                else:
                    toc_names.append(re.sub(r'\.rst$', '', line.strip()))
    return toc_names


def toc2xml(names):
    return [f"<xi:include href='./{name}.ptx'/>\n" for name in names]
    

def processPTX(ptx, ptxdir, sourcedir):
    lines = []
    saw_marker = False
    found_root = False
    with open(ptx) as f:
        for line in f:
            if not found_root:
                fixed, n = element.subn(addXi, line, count=1)
                if n == 1:
                    found_root = True
                    lines.append(fixed)
                else:
                    lines.append(line)
            elif marker.fullmatch(line):
                saw_marker = True
                rst = sourcedir / ptx.relative_to(ptxdir).parent / (ptx.stem + '.rst')
                for toc in toc2xml(getTOC(rst)):
                    lines.append(toc)
            else:
                lines.append(line)

    if saw_marker:
        savePTX(ptx, lines)


def savePTX(ptx, lines):
    print(f"Filled TOC in {ptx}", file=sys.stderr)
    with open(ptx, "w") as f:
        for line in lines:
            f.write(line)


def walk(ptxdir, sourcedir):
    for root, dirs, files in os.walk(ptxdir):
        for f in files:
            ptx = Path(f)
            if ptx.suffix == '.ptx':
                processPTX(Path(root) / ptx, ptxdir, sourcedir)

            
if __name__ == '__main__':
    
    ptxdir, sourcedir, *files = [Path(p) for p in sys.argv[1:]]

    if not files:
        walk(ptxdir, sourcedir)
    else:
        for f in files:
            processPTX(f, ptxdir, sourcedir)

