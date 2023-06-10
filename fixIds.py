import re
import os

seen = set()

def rewrite_id(m):
    text = re.sub(r'\s+', "-", m.group(1))
    text = re.sub(r'^([^A-Za-z_])', r'_\1', text)
    text = uniquify(text or "empty")
    return f'xml:id="{text}"'


def uniquify(text):
    orig = text
    counter = 1
    while text in seen:
        text = f"{orig}-{counter}" 
        counter += 1
    seen.add(text)
    return text


for root, dirs, files in os.walk("pretext"):
    for file in files:
        if "toctree" in file:
            continue
        if ".ptx" in file:
            with open(os.path.join(root, file)) as f:
                text = f.read()
            text = re.sub(r'xml:id="(.*?)"', rewrite_id, text)

            with open(os.path.join(root, file), "w") as f:
                f.write(text)
