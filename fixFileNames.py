import os
import re
import shutil

fdict = {}
for root, dirs, files in os.walk("pretext"):
    for file in files:
        if "toctree" in file:
            continue
        parent = root.split("/")[-1]
        if file in fdict:
            fdict[file].append(root)
        else:
            fdict[file] = [root]

for k in fdict:
    if ".ptx" not in k:
        continue
    if len(fdict[k]) > 1:
        print(fdict[k])
        for root in fdict[k]:
            parent = root.split("/")[-1]
            ft = open(os.path.join(root, k)).read()
            if g := re.search(r'section xml:id="(.*?)"', ft):
                oldid = g.group(1)
                newid = f"{parent}_{oldid}".lower()
            ft = ft.replace(f'section xml:id="{oldid}"', f'section xml:id="{newid}"')
            with open(os.path.join(root, k), "w") as nf:
                nf.write(ft)
