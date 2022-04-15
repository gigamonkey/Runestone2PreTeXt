# %% [markdown]
# # Add labels to sections

# %%
import re
import sys


# %%
def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", name).lower()


def title_to_kebab(title_str):
    # first get rid of spaces and punctuation and latex junk
    title_str = re.sub(r"\{.*\}", "", title_str)
    ret = re.sub(r"[^\w]", "", title_str)
    return camel_to_snake(ret)


# %%
def fixer(mg):
    return mg.group(1) + r"\label{" + title_to_kebab(mg.group(2)) + "}\n"


# %%
if __name__ == "__main__":
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            print(f)
            with open(f) as oldfile:
                text = oldfile.read()
            t = re.sub(r"(\\section\{(.*)\}\n(?!\\label))", fixer, text)
            with open(f, "w") as newfile:
                newfile.write(t)


# %%


# %%
