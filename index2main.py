import os
import re
from pathlib import Path

id = os.path.basename(os.getcwd())
permid = id[0:3]

def convert_index2main(path):
    tt = open(path).readlines()
    newroot = "./pretext"
    with open(os.path.join(newroot, "main.ptx"), "w") as ttx:
        ttx.write(
            """\
<?xml version="1.0" encoding="UTF-8"?>\n"""
        )
        ttx.write(f'''    <pretext xmlns:xi="http://www.w3.org/2001/XInclude" xml:lang="en-US">
        <xi:include href="./bookinfo.ptx"/>
        <book xml:id= "{id}" permid="{permid}">\n'''
        )
        booktitle = (tt.index(list(filter(lambda a: '===' in a, tt))[0])) + 1
        ttx.write(
                f"            <title>{tt[booktitle].strip()}</title>\n"
        )

        ttx.write(
                '            <subtitle>The PreTeXt Interactive Edition</subtitle> \n'
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
                    ttx.write(f'                <xi:include href="./{fname}.ptx" />\n')
        ttx.write('''            <backmatter>
                <index>
                    <index-list/>
                </index>
            </backmatter>
        </book>
    </pretext>''')


file = "./_sources/index.rst"
convert_index2main(Path(os.path.join(".", file)))
