# Runestone 2 PreTeXt

## Converting RST to PreTeXt

Lets just acknowledge that this is a somewhat cumbersom multi-step process, but do keep in mind that it is not meant to be done everyday. Ideally this is done once for each book, so it should not be so bad.

### RST + Runestone to Generic XML

First hack the pavement.py file. Make a copy of the `template_args` dictionary and past it outside the Options bunch.

Simply run `runestone rst2xml` this will put xml files in `build/xml`. It will also create a file called `rs-substitutes.xml` this contains the html for **some** of the components that have not been converted. The remaining pieces of the `rs-substitutes.xml` file
can be populated from the database by running the `updateSubs.py` script in the book folder.

### Generic XML to PreTeXt

Edit your index.rst file and change the toctree directives to use xml includes. Then convert the toctree.rst files with the script `toctree2xml.py`

To convert xml output by a sphinx build you have two options

1. run `xsltproc /path/to/docutils2ptx.xsl /path/to/build/xml/foo.xml > foo.ptx` for every sub chapter.

2. run `python xml2ptx.py` which will walk the directories in in the build/xml folder. This will read the xml source from the build/xml folder and write pretext source to the pretext folder.

### Build the PreTeXt book

`pretext build html -i index.ptx -p publication.xml --param runestone.dev:yes`

Or using Robs dev script
python ~/src/pretext/pretext/pretext -c all -f html -p publication-rs-for-all.xml -d ../beta thinkcspy.ptx

To build for academy use the publication-rs-for-academy.xml file See https://pretextbook.org/doc/guide/html/publication-file-online.html

Its good to check latex as it is pickier than html

TODO:

-   Need a better way to get images into the build directory for PreTeXt
