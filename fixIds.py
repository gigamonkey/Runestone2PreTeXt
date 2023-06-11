import re
import os

counter = 0
idval = 1
for root, dirs, files in os.walk("pretext"):
    for file in files:
        counter += 1
        if "toctree" in file:
            continue
        if ".ptx" in file:
            with open(os.path.join(root, file)) as f:
                text = f.read()
            text = text.replace('"id1 ', f'"_{counter}_id1')
            text = text.replace('"id2 ', f'"_{counter}_id2')
            text = text.replace(" index-0", f"{counter}_index-0")
            text = text.replace(" index-1", f"{counter}_index-1")
            text = re.sub(r'xml:id="([\w+-]+) ([\w+-]+)"', r'xml:id="\1"', text)

            with open(os.path.join(root, file), "w") as f:
                f.write(text)
