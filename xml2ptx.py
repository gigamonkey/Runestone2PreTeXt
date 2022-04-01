# apply the xslt stylesheet to all available xml files

import subprocess
import lxml.etree as ET
import os
from pathlib import Path
import pdb

xsl_filename = "/Users/bmiller/Runestone/Runestone2Pretext/docutils2ptx.xsl"


def transform_one_page(root, xml_filename):
    try:
        dom = ET.parse(xml_filename)
    except Exception as e:
        print(f"Failed to parse {xml_filename}")
        print(e)
        return

    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    try:
        newdom = transform(dom)
    except Exception as e:
        print(f"Failed to transform {xml_filename}")
        print(e)
        return
    newroot = root.replace("build/xml", "")
    ptx_filename = str(xml_filename).replace(".xml", ".ptx").replace("build/xml", "")
    with open(
        f"/Users/bmiller/Runestone/books/thinkcspy/pretext{ptx_filename}", "w"
    ) as ptfile:
        ptfile.write(ET.tostring(newdom, pretty_print=True).decode("utf8"))


os.chdir("/Users/bmiller/Runestone/books/thinkcspy")

# Recursively walk the tree
for root, dirs, files in os.walk("build/xml"):
    for file in files:
        if file.endswith(".xml"):
            transform_one_page(root, Path(os.path.join(root, file)))
