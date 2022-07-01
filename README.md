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

::

    python ~/Runestone/Runestone2PreTeXt/xml2ptx.py /path/to/bookfolder

### Fix up stuff that has not been fixed.

From the main folder of the book -- pretext should be a subdirectory. Run the following scripts in this order to fix things up. They should each walk the pretext folder and fix various things that the main conversion was not able to deal with.

::

    python ~/Runestone/Runestone2PreTeXt/fixIds.py
    python ~/Runestone/Runestone2PreTeXt/fix_xrefs.py
    python ~/Runestone/Runestone2PreTeXt/reformatPtx.py

### Create a PreTeXt project file

Run the command `pretext init` and answer any questions it asks.

.. code-block:: xml

    <project>
    <targets>
        <target name="web">
        <format>html</format>
        <source>pretext/<yourmainhere>.ptx</source>
        <publication>pretext/publication-rs-for-all.xml</publication>
        <output-dir>output/html</output-dir>
        </target>
    ...

Create a `publication-rs-for-all.xml` file

.. code-block:: xml

    <!-- Testing for Runestone -->
    <publication>

        <source>
            <directories external="Figures" generated="GenFigs" />
        </source>

        <html>
            <platform host="web" />
            <!-- knowled checkpoints interfere with ActiveCode problems -->
            <knowl exercise-inline="no" example="no" listing="yes" />
        </html>

        <stringparam key="debug.rs.services.file" value="/Users/bmiller/Runestone/RunestoneComponents/runestone/dist/webpack_static_imports.xml" />
    </publication>

### Build the PreTeXt book

`pretext build web`

### External and Generated

The source tag in the publication file tells PreTeXt where your images are. The paths to the images must be **relative to your main PreTeXt source file**. This may take some work to move some images around and it will need to match the path you have specified in your source. The generated folder is for generated assets, for a typical book being converted from restructuredText this will only mean the traces needed for a CodeLens. Your can run `pretext generate` and it will build any traces that are needed. You don't need to run this step every time, only when you change a CodeLens.

TODO:

-   Need a better way to get images into the build directory for PreTeXt
