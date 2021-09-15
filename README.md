# Runestone 2 PreTeXt

This is an experiment to convert Runestone's rst to PreTeXt.  My original idea was to use sphinx to generate xml and then simply use xsltproc to convert that xml to PreTeXt. That turns out to be difficult for a few reasons.

1. The XML output processor for sphinx seems to ignore custom directives.  
2. Each rst file is treated as a standalone XML file not as a unit so we end up missing out on all kinds of things like a master toc and section numbering etc.

I think with perseverence this was could work.  But there may be other ways that are better.

1. Write xsltproc rules to convert the html
2. Write a custom output format for sphinx that produces the PreTeXt directly
3. Oscar Levin has written a PreTeXt output format for Pandoc. Perhaps that could be used, although the rst input processing would need to be augmented to understand the runestone directives.
4. A more hacking approach might be to use what I have now, and then output the Runestone components in PreTeXt in a second phase and then merge them.
5. Probably some other thing I'm not thinking of...


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
