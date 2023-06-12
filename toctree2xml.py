# %% [markdown]
# We need to convert each toctree.rst file to an xml file similar to this one.
#
# ```
# <?xml version="1.0" encoding="UTF-8"?>
#
# <pretext xmlns:xi="http://www.w3.org/2001/XInclude" xml:lang="en-US">
#   <xi:include href="./bookinfo.ptx"/>
#
#   <book xml:id="dmoi" permid="xel">
#     <title>Discrete Mathematics</title>
#     <subtitle>An Open Introduction, 3rd edition</subtitle>
#     <xi:include href="./frontmatter.ptx"/>
#
#     <xi:include href="./ch_intro.ptx"/>
#
#     <xi:include href="./ch_counting.ptx"/>
#
#     <xi:include href="./ch_sequences.ptx"/>
#
#     <xi:include href="./ch_logic.ptx"/>
#
#     <xi:include href="./ch_graphtheory.ptx"/>
#
#     <xi:include href="./ch_additionalTopics.ptx"/>
#
#     <xi:include href="./backmatter.ptx"/>
#   </book>
# </pretext>
# ```
#

# %% [markdown]
# Proceed as follows:
#
# 1. Read in the file as a list of strings
# 1. Open afile for writing and put in the boilerplate using the first line of toctree as the chapter tag.
# 1. Find the line that contains .. toctree::
# 1. Then find the first blank line after that.  Throw out everything before and including the blank
# 1. For each of the lines until we get to the end of the file or another blank
#    1. convert the filename.rst (.rst may be missing) to an `<xi:include>` tag
# 1. close the chapter and pretext file.
#

# %%
import re


def convert_one_toctree(root, path):
    tt = open(path).readlines()
    newroot = root.replace("_sources", "pretext")
    with open(os.path.join(newroot, "toctree.ptx"), "w") as ttx:
        ttx.write(
            """\
<?xml version="1.0" encoding="UTF-8"?>\n"""
        )
        ttx.write(
            '    <chapter xmlns:xi="http://www.w3.org/2001/XInclude" xml:lang="en-US">\n'
        )
        ttx.write(f"        <title>{tt[0].strip()}</title>\n")

        for istart, line in enumerate(tt):
            if ".. toctree::" in line:
                break
        for ix, line in enumerate(tt[istart + 1 :]):
            if re.match(r"^\s*$", line):
                break
        print(istart, ix)
        for line in tt[istart + ix + 2 :]:
            fname = line.replace(".rst", "").strip()
            if fname:
                ttx.write(f"        <xi:include href='./{fname}.ptx' />\n")
            if re.match(r"^\s*$", line):
                break

        ttx.write("    </chapter>\n")


# %%
import os
from pathlib import Path
import sys

# sys.argv[1] should be path to the top level of the book
os.chdir(sys.argv[1])

# Recursively walk the tree
for root, dirs, files in os.walk("."):
    for file in files:
        if file == "toctree.rst":
            convert_one_toctree(root, Path(os.path.join(root, file)))

# %%
