<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:output method="xml" doctype-system="legacy-compat" encoding="utf-8" indent="yes" />
    <xsl:template match="/">
        <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE HTML&gt;</xsl:text>
        <html>
            <head>
                <title><xsl:value-of select="//meta/title/text()" /></title>
                <style type="text/css">
                    @import url(http://fonts.googleapis.com/css?family=PT+Sans);
                    @import url(http://fonts.googleapis.com/css?family=Alegreya+Sans+SC:500);
                    
                    body {
                    font-family: 'PT Sans', Verdana, sans-serif;
                    }
                    
                    div.container {
                    max-width:600px;
                    width:100%;
                    margin: 0px auto 0px auto;
                    }
                    
                    div.title {
                    font-family: 'Alegreya Sans SC', sans-serif;
                    font-size:2em;
                    display: inline-block;
                    vertical-align:bottom;
                    margin-right:10px;
                    }
                    
                    div.size {
                    font-size:0.8em;
                    display: inline-block;
                    vertical-align:middle;
                    line-height:2em;
                    margin-bottom:0.15em;
                    }
                    
                    div.source {
                    font-size:0.8em;
                    }
                    
                    table {
                    border-collapse:collapse;
                    clear:both;
                    }
                    
                    tr:first-child th, tr:last-child td {
                    border-bottom:2px solid black;
                    }
                    
                    td {
                    border-bottom:1px solid black;
                    }
                    
                    th, td {
                    font-weight:300;
                    text-align:left;
                    padding-right:10px;
                    vertical-align:top;
                    }
                    
                    th:last-child, td:last-child {
                    width:100%;
                    }
                    
                    .comment {
                    background-color:#eee;
                    text-align:center;
                    padding-top:0.3em;
                    padding-bottom:0.3em;
                    }
                    
                    .numberCircle {
                    border-radius: 50%;
                    behavior: url(PIE.htc); /* remove if you don't care about IE8 */
                    
                    width: 1em;
                    height: 1em;
                    padding: 1px;
                    
                    background: #fff;
                    border: 1px solid #000;
                    color: #black;
                    text-align: center;
                    vertical-align:middle;
                    
                    font: 0.7em Arial, sans-serif;
                    line-height:1em;
                    display:inline-block;
                    margin-right:0.3em;
                    margin-bottom:0.15em;
                    }
                </style>
            </head>
            <body>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="recipe">
        <div class="container">
          <div class="title"><xsl:value-of select="meta/title/text()" /></div>
          <div class="size"><xsl:value-of select="meta/size/text()" /></div>
          <table>
              <tr>
                  <th>Zutat</th>
                  <th>Menge</th>
                  <th>Schritte</th>
              </tr>
              <xsl:apply-templates select="instructions" />
          </table>
          <div class="source"><xsl:value-of select="meta/source/text()" /><xsl:text> </xsl:text><xsl:apply-templates select="meta/author" /></div>
        </div>
    </xsl:template>
    
    <xsl:template match="author">
        <xsl:text>recorded by </xsl:text><xsl:value-of select="text()" />
    </xsl:template>
    
    <xsl:template match="instructions">
        <xsl:apply-templates />
    </xsl:template>
    
    <xsl:template match="comment">
        <tr>
            <td colspan="3" class="comment"><xsl:value-of select="text()" /></td>
        </tr>
    </xsl:template>
    
    <xsl:template match="phase">
        <tr>
            <td><xsl:for-each select="ingredient"><xsl:value-of select="name/text()" /><br /></xsl:for-each></td>
            <td><xsl:for-each select="ingredient"><xsl:value-of select="amount/text()" /> <xsl:value-of select="unit/text()" /><br /></xsl:for-each></td>
            <td><xsl:for-each select="step">
                <div class="numberCircle">
                    <xsl:value-of select="count(preceding::step)+1" />
                </div>
                <xsl:value-of select="text()" />
                <br />
            </xsl:for-each></td>
        </tr>
    </xsl:template>
</xsl:stylesheet>
