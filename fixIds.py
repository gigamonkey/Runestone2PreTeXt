import re
import os

idval = 1
for root, dirs, files in os.walk("pretext"):
    for file in files:
        if "toctree" in file:
            continue
        if ".ptx" in file:
            with open(os.path.join(root, file)) as f:
                text = f.read()
            text = text.replace('"id1 ', '"')
            text = text.replace('"id2 ', '"')
            text = text.replace(" index-0", "")
            text = text.replace(" index-1", "")
            text = re.sub(r'xml:id="([\w+-]+) ([\w+-]+)"', r'xml:id="\1"', text)

            with open(os.path.join(root, file), "w") as f:
                f.write(text)
