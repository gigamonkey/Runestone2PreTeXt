
import os
import sys
import re
from pathlib import Path

id = os.path.basename(os.getcwd())
permid = id[0:3]

def convert_index2main(root, path):
    tt = open(path).readlines()
    newroot = root.replace("_sources", "pretext")
    with open(os.path.join(newroot, "main.ptx"), "w") as ttx:
        ttx.write(
            """\
<?xml version="1.0" encoding="UTF-8"?>\n"""
        )
        ttx.write(
            '    <pretext xmlns:xi="http://www.w3.org/2001/XInclude" xml:lang="en-US">\n'
        )
        ttx.write(
            '   <xi:include href="./bookinfo.ptx"/> \n '
        )
        ttx.write(
            '   <book xml:id= "'f'{id}''" permid="'f'{permid}''"> \n '
        )

        booktitle = (tt.index(list(filter(lambda a: '===' in a, tt))[0])) + 1
        ttx.write(
            f"  <title>{tt[booktitle].strip()}</title>\n"
        )

        ttx.write(
            '   <subtitle>The PreTeXt Interactive Edition</subtitle> \n'
        )

        for istart, line in enumerate(tt):
            if ".. toctree::" in line:
                break
        for ix, line in enumerate(tt[istart + 1 :]):
            if re.match(r"^\s*$", line):
                break
        print(istart, ix)
        for line in tt[istart + ix + 2 :]:
            if ".rst" in line:
                fname = line.replace(".rst", "").strip()
                if fname:
                    ttx.write(f'        <xi:include href="./{fname}.ptx" />\n')


        ttx.write("    <backmatter>\n")
        ttx.write("    <index>\n")
        ttx.write("    <index-list/>\n")
        ttx.write("    </index>\n")
        ttx.write("    </backmatter>\n")
        ttx.write("    </book>\n")
        ttx.write("    </pretext>\n")



# sys.argv[1] should be path to the top level of the book
os.chdir(sys.argv[1])

# Recursively walk the tree
for root, dirs, files in os.walk("."):
    for file in files:
        if file == "index.rst":
            convert_index2main(root, Path(os.path.join(root, file)))