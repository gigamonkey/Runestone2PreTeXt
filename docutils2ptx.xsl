<?xml version='1.0'?>

<!--
    Transform docutuls xml to pretext
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


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
        <book>
            <xsl:apply-templates select="node()|@*" />
        </book>
    </pretext>
</xsl:template>

<xsl:template match="section">
    <xsl:variable name="division">
        <xsl:variable name="depth" select="count(ancestor::section)"/>
        <xsl:choose>        
            <xsl:when test="$depth = 0">
                <xsl:text>chapter</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 1">
                <xsl:text>section</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 2">
                <xsl:text>subsection</xsl:text>
            </xsl:when>
            <xsl:when test="$depth = 3">
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



<xsl:template match="paragraph">
    <p>
        <xsl:apply-templates select="node()|@*" />
    </p>
</xsl:template>

<xsl:template match="bullet_list">
    <ul>
        <xsl:apply-templates select="node()" />
    </ul>
</xsl:template>

<xsl:template match="list_item">
    <li>
        <xsl:apply-templates select="node()|@*" />
    </li>
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


</xsl:stylesheet>