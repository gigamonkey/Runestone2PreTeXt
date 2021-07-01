# Runestone 2 PreTeXt

Two commands:

To convert rst files to xml run

sphinx-build -b xml -d ././build/overview/doctrees -c . -Acourse_id=overview -Alogin_required=false -Aappname=runestone -Aloglevel=10 -Acourse_url=https://runestone.academy -Adynamic_pages=True -Ause_services=true -Abasecourse=overview -Apython3=true -Adownloads_enabled=true -Aallow_pairs=false -Aenable_chatcodes=false -Arunestone_version=5.7.1 -Abuild_info=unknown . ./build/xml

To convert xml output by a sphinx build:

`xsltproc docutils2ptx.xsl book/_build/xml/foo.xml  > foo.ptx`

to build the pretext

`pretext build -i foo.ptx -o output [html|latex]`
`pretext build html -i index.ptx -p publication.xml --param runestone.dev:yes`

Its good to check latex as it is pickier than html


# TODO
1. Find a way to combine -- may need to just reconstruct the toc by hand and use xsltproc to strip off the beginning of each document.

2. `return [nodes.raw(self.block_text, res, format="html")]` When we are building xml try this method instead of the visitor method for the xml nodes.
But how do we know what we are building??
