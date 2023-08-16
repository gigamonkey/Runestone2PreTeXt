# Runestone 2 PreTeXt

## Converting RST to PreTeXt

Lets just acknowledge that this is a somewhat cumbersom multi-step process, but do keep in mind that it is not meant to be done everyday. Ideally this is done once for each book, so it should not be so bad. It is 100% likely that at the end of this process there will still be a fair amount of manual cleanup to do.

### RST + Runestone to Generic XML

First hack the pavement.py file by making a copy of the `template_args` dictionary and pasting it outside the Options bunch.

Simply run `runestone rs2ptx` inside the shell. This will put xml files in `build/xml`. It will also create a file called `rs-substitutes.xml`. This contains the html for **many** of the components that have not been converted. The remaining pieces of the `rs-substitutes.xml` file can be populated from the database by running the `updateSubs.py` script in the book folder.

### Generic XML to PreTeXt

First, create a `pretext` folder inside the book directory.
Next, to convert xml output by a sphinx build you have two options

1. run `xsltproc /path/to/docutils2ptx.xsl /path/to/build/xml/foo.xml > foo.ptx` for every sub chapter.

2. run `python xml2ptx.py` which will walk the directories in in the build/xml folder. This will read the xml source from the build/xml folder and write pretext source to the pretext folder.

::

    python ~/Runestone/Runestone2PreTeXt/xml2ptx.py /path/to/bookfolder

### Fix up stuff that has not been fixed.

From the main folder of the book (pretext should be a subdirectory) run the following scripts in this order to fix things up. They should each walk the pretext folder and fix various things that the main conversion was not able to deal with.

::

    python ~/Runestone/Runestone2PreTeXt/fixIds.py
    python ~/Runestone/Runestone2PreTeXt/fix_xrefs.py
    python ~/Runestone/Runestone2PreTeXt/reformatPtx.py
    python ~/Runestone/Runestone2PreTeXt/index2main.py

### Create a PreTeXt project file

Now we will create the pretext project.
Run the command `pretext init` (still from the main folder of the book). This will create some new files, including `project.ptx`.
Open `project.ptx` and under `<source>` tag replace `source` with `pretext`

.. code-block:: xml

    <project>
    <targets>
        <target name="web">
        <format>html</format>
        <source>pretext/main.ptx</source>
        <publication>pretext/publication-rs-for-all.xml</publication>
        <output-dir>output/html</output-dir>
        </target>
    ...

Note we also modified the `<publication>` element.  
Create a `publication-rs-for-all.xml` file in the `pretext` folder. Add the following code:

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

### Convert toctree directives

Convert the toctree.rst files with the script `python toctree2xml.py`

::

    python ~/Runestone/Runestone2PreTeXt/toctree2xml.py /path/to/bookfolder

### Copy figures
Run the script `copy_figs.py` to copy any images (png, jpeg, svg, gif, etc) in the rst source to the pretext folder:

    python ~/Runestone/Runestone2PreTeXt/copy_figs.py /path/to/_source /path/to/pretext/Figures

where `/path/to/pretext/Figures` is the directory specified as `external` in `publication-rs-for-all.xml`.

### Build the PreTeXt book

Run `pretext build web`

At this point you may encounter failures! Things that I didn't think of to convert may have resulted in bad xml. Mistakes in the underlying rst may generate unexpected and bad PreTeXt. You may need to fix the rst and run the sequence again. You may discover that there is a pattern to what is bad, but it is not an rst error. In that case maybe a script can fix it in all files. If you find yourself doing global search and replace, that would be a good thing to convert to a python script to save others time. If there are XML tags that are not converted to PTX correctly that would be a good time to add a template to the `docutils2ptx.xsl` file.

### External and Generated

The source tag in the publication file tells PreTeXt where your images are. The paths to the images must be **relative to your main PreTeXt source file**. This may take some work to move some images around and it will need to match the path you have specified in your source. The generated folder is for generated assets, for a typical book being converted from restructuredText this will only mean the traces needed for a CodeLens. Your can run `pretext generate` and it will build any traces that are needed. You don't need to run this step every time, only when you change a CodeLens.

### Make this Collaborative

If you discover something that the above scripts do not handle but you recognize a pattern. Please write a script or update the xsl so that future converters can benefit and make a pull request. Again, Once a book has been satisfactorally converted you should proceed with manual cleanup and never have to do run these scripts for the book again.

TODO:

- ~~Need a better way to get images into the build directory for PreTeXt~~ hopefully addressed with copy_figs.py
