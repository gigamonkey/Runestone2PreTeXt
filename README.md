# Runestone 2 PreTeXt

Two commands:

To convert rst files to xml run

`make xml`

To convert xml output by a sphinx build:

`xsltproc docutils2ptx.xsl book/_build/xml/foo.xml  > foo.ptx`

to build the pretext

`pretext build -i foo.ptx -o output [html|latex]`

Its good to check latex as it is pickier than html
