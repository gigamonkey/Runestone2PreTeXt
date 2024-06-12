import re
import os
from collections import defaultdict

seen = defaultdict(int)

def rewrite_id(m):
    text = re.sub(r'\s+', "-", m.group(1))
    text = re.sub(r'^_+', r'', text)
    text = re.sub(r'^(\d)', r'_\1', text)
    text = uniquify(text or "empty")
    return f'xml:id="{text}"'


def uniquify(text):
    c = seen[text]
    seen[text] += 1
    return text if c == 0 else f"{text}-{c}"


for root, dirs, files in os.walk("pretext"):
    for file in files:
        if "toctree" in file:
            continue
        if file.endswith(".ptx"):
            with open(os.path.join(root, file)) as f:
                text = f.read()
            text = re.sub(r'xml:id="(.*?)"', rewrite_id, text)

            with open(os.path.join(root, file), "w") as f:
                f.write(text)
