<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template name="wrap-string">
        <xsl:param name="str" />
        <xsl:param name="wrap-col" />
        <xsl:param name="break-mark" />
        <xsl:param name="pos" select="0" />
        <xsl:choose>

            <xsl:when test="contains( $str, ' ' )">
                <xsl:variable name="first-word" select="substring-before( $str, ' ' )" />
                <xsl:variable name="pos-now" select="$pos + 1 + string-length( $first-word )" />
                <xsl:choose>

                    <xsl:when test="$pos > 0 and $pos-now >= $wrap-col">
                        <xsl:copy-of select="$break-mark" />
                        <xsl:call-template name="wrap-string">
                            <xsl:with-param name="str" select="$str" />
                            <xsl:with-param name="wrap-col" select="$wrap-col" />
                            <xsl:with-param name="break-mark" select="$break-mark" />
                            <xsl:with-param name="pos" select="0" />
                        </xsl:call-template>
                    </xsl:when>

                    <xsl:otherwise>
                        <xsl:value-of select="$first-word" />
                        <xsl:text> </xsl:text>
                        <xsl:call-template name="wrap-string">
                            <xsl:with-param name="str" select="substring-after( $str, ' ' )" />
                            <xsl:with-param name="wrap-col" select="$wrap-col" />
                            <xsl:with-param name="break-mark" select="$break-mark" />
                            <xsl:with-param name="pos" select="$pos-now" />
                        </xsl:call-template>
                    </xsl:otherwise>

                </xsl:choose>
            </xsl:when>

            <xsl:otherwise>
                <xsl:if test="$pos + string-length( $str ) >= $wrap-col">
                    <xsl:copy-of select="$break-mark" />
                </xsl:if>
                <xsl:value-of select="$str" />
            </xsl:otherwise>

        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
