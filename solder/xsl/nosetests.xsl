<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999.xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output indent="yes" method="html"/>
    <xsl:include href="wrap-string.xsl" />

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template name="summary">
        <xsl:param name="value" />
        <span class="ui-button-text">
            <xsl:value-of select="$value" />/<xsl:value-of select="@tests" />
            (<xsl:value-of select="round($value div @tests * 100)" />%)
        </span>
    </xsl:template>

    <xsl:template match="testsuite">
        <xsl:variable name="success" select="@tests - (@failures + @errors + @skip)" />
        <xsl:text disable-output-escaping="yes"><![CDATA[<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">]]></xsl:text>
        <html>
            <head>
                <title>Nose Test Results - <xsl:value-of select="@name"/></title>
                <link rel="stylesheet" type="text/css" href="/themes/aristo/jquery-ui-1.8.7.custom.css" />
                <link rel="stylesheet" type="text/css" href="/styles/tests.css" />
            </head>
            <body>
                <div id="results" class="ui-widget">
                    <div class="ui-widget-header">
                        <h3>Results for <xsl:value-of select="@name"/></h3>
                        <ul>
                            <li>
                                <button class="ui-button ui-widget ui-state-default ui-corner-all" href="#successes">
                                    <img src="/images/icons/48x48/green.png" />
                                    <xsl:call-template name="summary" select=".">
                                        <xsl:with-param name="value" select="$success" />
                                    </xsl:call-template>
                                </button>
                            </li>

                            <li>
                                <button class="ui-button ui-widget ui-state-default ui-corner-all" href="#failures">
                                    <img src="/images/icons/48x48/red.png" />
                                    <xsl:call-template name="summary" select=".">
                                        <xsl:with-param name="value" select="@failures" />
                                    </xsl:call-template>
                                </button>
                            </li>

                            <li>
                                <button class="ui-button ui-widget ui-state-default ui-corner-all" href="#errors">
                                    <img src="/images/icons/48x48/orange.png" />
                                    <xsl:call-template name="summary" select=".">
                                        <xsl:with-param name="value" select="@errors" />
                                    </xsl:call-template>
                                </button>
                            </li>

                            <li>
                                <button class="ui-button ui-widget ui-state-default ui-corner-all" href="#skipped">
                                    <img src="/images/icons/48x48/blue.png" />
                                    <xsl:call-template name="summary" select=".">
                                        <xsl:with-param name="value" select="@skip" />
                                    </xsl:call-template>
                                </button>
                            </li>
                        </ul>
                    </div>
                    <div class="ui-widget-content">
                        <ul>
                            <xsl:apply-templates><xsl:sort select="@name" /></xsl:apply-templates>
                        </ul>
                    </div>
                </div>

                <script type="text/javascript" src="https://www.google.com/jsapi?key=ABQIAAAAxpQzj0cQbWdgCGNnzurdJxR5vmDMjgQTfK2ZmREKQWlPDUVCsRTZLizJDsRRFLOXNvczT7zBnsTDqA"></script>
                <script type="text/javascript">
                    google.load('jquery', "1");
                    google.load('jqueryui', "1");

                    jQuery(document).ready(function($) {
                        $('button').button();
                    });
                </script>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="testcase">
        <li class="testcase">
            <div class="name"><xsl:value-of select="@name" /></div>
            <div class="classname"><xsl:value-of select="@classname" /></div>
            <div class="time"><xsl:value-of select="@time" /></div>
            <xsl:apply-templates />
        </li>
    </xsl:template>

    <xsl:variable name="start-log" select="'-------------------- &gt;&gt; begin captured logging &lt;&lt; --------------------'" />
    <xsl:variable name="end-log" select="'--------------------- &gt;&gt; end captured logging &lt;&lt; ---------------------'" />

    <xsl:template name="message">
        <xsl:param name="str" />
        <xsl:call-template name="wrap-string">
            <xsl:with-param name="str" select="$str" />
            <xsl:with-param name="wrap-col" select="100" />
            <xsl:with-param name="break-mark">
                <xsl:text>&#10;</xsl:text>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="error|failure">
        <xsl:variable name="message" select="substring-before(@message, $start-log)" />
        <xsl:variable name="log" select="substring-before(substring-after(@message, $start-log), $end-log)" />
        <div>
            <xsl:attribute name="class"><xsl:value-of select="name(.)" /></xsl:attribute>
            <div class="type"><xsl:value-of select="@type"/></div>
            <xsl:if test="$message">
                <div class="message">
                    <xsl:call-template name="message">
                        <xsl:with-param name="str" select="$message" />
                    </xsl:call-template>
                </div>
            </xsl:if>
            <xsl:if test="$log">
                <div class="log">
                    <pre>
                        <xsl:call-template name="message">
                            <xsl:with-param name="str" select="$log" />
                        </xsl:call-template>
                    </pre>
                </div>
            </xsl:if>
        </div>
    </xsl:template>

</xsl:stylesheet>
