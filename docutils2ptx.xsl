<?xml version='1.0'?>

<!--
    Transform docutuls xml to pretext
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="xml" omit-xml-declaratino="no" indent="yes"/>

<xsl:template match="/">
    <xsl:apply-templates />
</xsl:template>

<xsl:template match="node()|@*">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*" />
    </xsl:copy>
</xsl:template>

<xsl:template match="document">
    <pretext>
        <docinfo/>
        <xsl:apply-templates select="node()" />
    </pretext>
</xsl:template>


<xsl:template match="section">
    <xsl:variable name="division">
        <xsl:variable name="depth" select="count(ancestor::section)"/>
        <xsl:choose>        
            <xsl:when test="$depth = 0">
                <xsl:text>book</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 1">
                <xsl:text>chapter</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 2">
                <xsl:text>section</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 3">
                <xsl:text>subsection</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 4">
                <xsl:text>subsubsection</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:message>Division depth too deep</xsl:message>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:element name="{$division}">
    <!-- todo: add title -->
        <xsl:apply-templates select="node()|@ids"/>
    </xsl:element>
</xsl:template>

<xsl:template match="@ids">
    <xsl:attribute name="xml:id">
        <xsl:value-of select="."/>
    </xsl:attribute>
</xsl:template>

<!-- <xsl:template match="@enumtype">
    <xsl:attribute name="label">
        <xsl:value-of select="."/>
    </xsl:attribute>
</xsl:template> -->


<xsl:template match="image">
    <image>
        <xsl:attribute name="source">
            <xsl:value-of select="concat('images/', @uri)"/>
        </xsl:attribute>
        <xsl:if test="@width">
            <xsl:attribute name="width">
                <xsl:value-of select="concat(@width, '%')"/>
            </xsl:attribute>
        </xsl:if>
        <xsl:copy-of select="@alt|@height"/>
    </image>
</xsl:template>


<xsl:template match="paragraph">
    <p>
        <xsl:apply-templates select="node()|@*" />
    </p>
</xsl:template>

<xsl:template match="bullet_list">
    <p>
        <ul>
            <xsl:apply-templates select="node()" />
        </ul>
    </p>
</xsl:template>

<xsl:template match="enumerated_list">
    <p>
        <ol>
            <xsl:attribute name="label">
                <xsl:variable name="kind" select="@enumtype"/>
                    <xsl:choose>        
                        <xsl:when test="$kind = 'arabic'">
                            <xsl:text>1</xsl:text>
                        </xsl:when>
                        <xsl:when test="$kind = 'loweralpha'">
                            <xsl:text>a</xsl:text>
                        </xsl:when>
                        <xsl:when test="$kind = 'upperalpha'">
                            <xsl:text>A</xsl:text>
                        </xsl:when>
                        <xsl:when test="$kind = 'lowerroman'">
                            <xsl:text>i</xsl:text>
                        </xsl:when>
                        <xsl:when test="$kind = 'upperroman'">
                            <xsl:text>I</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>A</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates select="node()" />
        </ol>
    </p>
</xsl:template>

<xsl:template match="list_item">
    <li>
        <xsl:apply-templates select="node()|@*" />
    </li>
</xsl:template>

<xsl:template match="table">
    <tabular>
        <xsl:apply-templates select="node()|@ids" />
    </tabular>
</xsl:template>

<xsl:template match="tgroup">
    <xsl:apply-templates select="node()|@ids" />
</xsl:template>

<!-- Delete colspecs-->
<xsl:template match="colspec" />

<xsl:template match="thead|tbody">
    <xsl:apply-templates select="node()|@ids" />
</xsl:template>

<xsl:template match="thead/row">
    <row header="yes">
        <xsl:apply-templates select="node()|@ids" />
    </row>
</xsl:template>

<xsl:template match="tbody/row">
    <row>
        <xsl:apply-templates select="node()|@ids" />
    </row>
</xsl:template>

<xsl:template match="entry">
    <cell>
        <xsl:apply-templates select="node()|@ids" />
    </cell>
</xsl:template>

<xsl:template match="entry/paragraph">
        <xsl:apply-templates select="node()" />
</xsl:template>




<xsl:template match="literal_block[@language='default']">
    <pre>
        <xsl:apply-templates select="node()" />
    </pre>
</xsl:template>

<xsl:template match="literal_block">
    <program>
        <xsl:attribute name="language">
            <xsl:value-of select="@language"/>
        </xsl:attribute>
        <input>
            <xsl:text>&#xa;</xsl:text>
            <xsl:apply-templates select="node()"/>
            <xsl:text>&#xa;</xsl:text>
        </input>
    </program>
</xsl:template>

<xsl:template match="comment">
    <xsl:comment>
        <xsl:value-of select="." />
    </xsl:comment>
</xsl:template>

<!-- ignore the inline element that contains the content (link title) -->
<xsl:template match="reference[@internal='True']">
    <xref>
        <xsl:attribute name='ref'>
            <xsl:value-of select="@refuri"/>
        </xsl:attribute>
    </xref>
</xsl:template>

<xsl:template match="reference[not(@internal)]">
    <url>
        <xsl:attribute name='href'>
            <xsl:value-of select="@refuri"/>
        </xsl:attribute>
        <xsl:attribute name='visual'>
            <xsl:value-of select="@refuri"/>
        </xsl:attribute>
        <!-- Don't copy refuri or name attributes-->
        <xsl:apply-templates select="node()"/>
    </url>
</xsl:template>

<!-- target was a sibling of reference that we want to ignore -->
<xsl:template match="target">
    <xsl:message>Ignored Target</xsl:message>
    <xsl:text>[TARGET]</xsl:text>
</xsl:template>

<xsl:template match="compound">
    <xsl:message>Ignoring Compound for now</xsl:message>
    <xsl:text>[COMPOUND]</xsl:text>
</xsl:template>


</xsl:stylesheet>