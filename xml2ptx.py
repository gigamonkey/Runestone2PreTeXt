# apply the xslt stylesheet to all available xml files

import subprocess
import lxml.etree as ET
import os
import re
from pathlib import Path
import pdb

xsl_filename = "/Users/bmiller/Runestone/Runestone2Pretext/docutils2ptx.xsl"


def to_snake(name):
    name = re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()
    return name


# handles acronyms better
def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", name).lower()


def transform_one_page(root, xml_filename, fileonly):
    if "toctree" in str(xml_filename):
        return
    try:
        dom = ET.parse(xml_filename)
    except Exception as e:
        print(f"Failed to parse {xml_filename}")
        print(e)
        return
    stringparams = {"filename": ET.XSLT.strparam(fileonly)}
    folder = root.split("/")[-1].strip()
    folder = camel_to_snake(folder)
    stringparams["folder"] = ET.XSLT.strparam(folder)

    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    try:
        newdom = transform(
            dom, **stringparams
        )  # can add an unparsed dictionary of stringparams
    except Exception as e:
        print(f"Failed to transform {xml_filename}")
        print(e)
        return
    newroot = root.replace("build/xml", "")
    ptx_filename = str(xml_filename).replace(".xml", ".ptx").replace("build/xml", "")
    with open(
        f"/Users/bmiller/Runestone/books/thinkcspy/pretext/{ptx_filename}", "w"
    ) as ptfile:
        ptfile.write(ET.tostring(newdom, pretty_print=True).decode("utf8"))


os.chdir("/Users/bmiller/Runestone/books/thinkcspy")

# Recursively walk the tree
for root, dirs, files in os.walk("build/xml"):
    for file in files:
        if file.endswith(".xml"):
            transform_one_page(root, Path(os.path.join(root, file)), file)
