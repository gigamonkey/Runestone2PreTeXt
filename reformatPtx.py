import os
import subprocess
from pathlib import Path

os.environ["XMLLLINT_INDENT"] = "    "
# Recursively walk the tree
for root, dirs, files in os.walk("pretext"):
    for file in files:
        if file.endswith(".ptx"):
            procfile = Path(os.path.join(root, file))
            try:
                res = subprocess.run(
                    f"xmllint --format --output {procfile} {procfile}",
                    shell=True,
                    check=True,  # ensure that WE capture the exception
                    capture_output=True,
                )
            except:
                print(f"Failed to reformat {procfile}")
