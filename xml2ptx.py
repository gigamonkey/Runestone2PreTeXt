# apply the xslt stylesheet to all available xml files

import subprocess
import lxml.etree as ET
import os
import re
from pathlib import Path
import pdb
import sys

xsl_filename = "/Users/bmiller/Runestone/Runestone2Pretext/docutils2ptx.xsl"
basedir = sys.argv[1]


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
    # maybe need to make folder
    if ptx_filename.startswith("/"):
        ptx_filename = ptx_filename[1:]
    fpath = Path(basedir) / "pretext" / Path(ptx_filename)
    if "/" in ptx_filename:
        fpath.parent.mkdir(parents=True, exist_ok=True)

    with open(fpath, "w") as ptfile:
        ptfile.write(ET.tostring(newdom, pretty_print=True).decode("utf8"))


os.chdir(f"{basedir}")

# Recursively walk the tree
for root, dirs, files in os.walk("build/xml"):
    for file in files:
        if file.endswith(".xml"):
            transform_one_page(root, Path(os.path.join(root, file)), file)
