import os
import re
import re


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", name).lower()


for root, dirs, files in os.walk("pretext"):
    folder = root.split("/")[-1]
    folder = camel_to_snake(folder)
    for file in files:
        if "toctree" in file:
            continue
        if ".ptx" in file:
            with open(os.path.join(root, file)) as f:
                text = f.read()
            all_xrefs = re.findall(r'<xref ref="(.*?)".*?>', text)
            if all_xrefs:
                print(f"FIlE: {file}")
            for x in all_xrefs:
                save_x = x
                if "#" in x:
                    x = x.split("#")[0]
                if "/" in x:
                    x = x.replace("../", "")
                    newps = []
                    parts = x.split("/")
                    for part in parts:
                        newps.append(camel_to_snake(part))
                    newps[0] = newps[0]
                    new_xref = "_".join(newps)
                    print(new_xref)
                elif "fig-" in x or "lst-" in x:
                    continue
                else:
                    new_xref = f"{folder}_{camel_to_snake(x)}"
                    print(new_xref)
                text = text.replace(save_x, new_xref)
            text = text.replace('xml:id=""', "")
            text = text.replace("&#8220;", "<q>")
            text = text.replace("&#8221;", "</q>")
            text = text.replace("&#8217;", "'")
            text = text.replace('width="150%"', 'width="75%"')
            text = text.replace('width="560"', 'width="auto"')

            with open(os.path.join(root, file), "w") as f:
                f.write(text)
