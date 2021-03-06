<?xml version="1.0" encoding="ISO-8859-1" ?>
<!--
# Copyright (c) 2008 Jean-Luc Leger <jean-luc.leger@dspnet.fr>
# SPDX-License-Identifier: GPL-2.0-or-later

This xslt stylesheet will convert JMdict_e XML entries to Edict2 format.
(Caution: unlike verion de814571423c (2009-03-07) of this file, this
version works correctly only with JMdict XML that contains only English
language glosses.  
-->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text"/>

<xsl:template match="/">
  <xsl:apply-templates select="/JMdict/entry"/>
</xsl:template>

<xsl:template match="entry">

  <xsl:apply-templates select="k_ele" />

  <xsl:apply-templates select="r_ele" />

  <xsl:text > /</xsl:text>

  <xsl:apply-templates select="sense" />

  <xsl:if test="count(k_ele/ke_pri[.='ichi1' or .='gai1' or .='spec1' or .='news1' or .='spec2']) > 0 or count(r_ele/re_pri[.='ichi1' or .='gai1' or .='spec1' or .='news1' or .='spec2']) > 0">
    <xsl:text>(P)/</xsl:text>
  </xsl:if>

  <xsl:apply-templates select="ent_seq" />

  <xsl:text>
</xsl:text>

</xsl:template>

<xsl:template match="ent_seq">
  <xsl:text >EntL</xsl:text>
  <xsl:value-of select="." />
  <xsl:text >/</xsl:text>
</xsl:template>

<xsl:template match="k_ele">
  <xsl:if test="position() > 1">
    <xsl:text>;</xsl:text>
  </xsl:if>
  <xsl:value-of select="keb" />
  <xsl:apply-templates select="ke_inf" />
  <xsl:if test="last() > 1 and (ke_pri = 'ichi1' or ke_pri = 'gai1' or ke_pri = 'spec1' or ke_pri = 'news1' or ke_pri = 'spec2')">
    <xsl:text>(P)</xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="ke_inf">
  <xsl:text >(</xsl:text>
  <xsl:value-of select="." />
  <xsl:text >)</xsl:text>
</xsl:template>

<xsl:template match="r_ele">
  <xsl:if test="position() = 1 and ../k_ele">
    <xsl:text > [</xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >;</xsl:text>
  </xsl:if>
  <xsl:value-of select="reb" />
  <xsl:apply-templates select="re_restr" />
  <xsl:apply-templates select="re_inf" />
  <xsl:if test="last() > 1 and (re_pri = 'ichi1' or re_pri = 'gai1' or re_pri = 'spec1' or re_pri = 'news1' or re_pri = 'spec2')">
    <xsl:text>(P)</xsl:text>
  </xsl:if>

  <xsl:if test="position() = last() and ../k_ele">
    <xsl:text >]</xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="re_inf">
  <xsl:text >(</xsl:text>
  <xsl:value-of select="." />
  <xsl:text >)</xsl:text>
</xsl:template>

<xsl:template match="re_restr">
  <xsl:if test="position() = 1">
    <xsl:text >(</xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >;</xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
  <xsl:if test="position() = last()">
    <xsl:text >)</xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="sense">
  <xsl:apply-templates select="pos" />

  <xsl:if test="last() > 1">
    <xsl:text >(</xsl:text>
    <xsl:value-of select="position()" />
    <xsl:text >) </xsl:text>
  </xsl:if>

  <xsl:if test="stagk or stagr">
    <xsl:text >(</xsl:text>
    <xsl:apply-templates select="stagk" />
    <xsl:apply-templates select="stagr" />
    <xsl:text > only) </xsl:text>
  </xsl:if>

  <xsl:apply-templates select="s_inf" />
  <xsl:apply-templates select="xref" />
  <xsl:apply-templates select="ant" />

  <xsl:apply-templates select="misc" />
  <xsl:apply-templates select="dial" />
  <xsl:apply-templates select="field" />

  <xsl:apply-templates select="gloss" />
</xsl:template>

<xsl:template match="pos">
  <xsl:if test="position() = 1">
    <xsl:text >(</xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >,</xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
  <xsl:if test="position() = last()">
    <xsl:text >) </xsl:text>
  </xsl:if>
</xsl:template>
 
<xsl:template match="field">
  <xsl:if test="position() = 1">
    <xsl:text >{</xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >;</xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
  <xsl:if test="position() = last()">
    <xsl:text >} </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="misc">
  <xsl:text >(</xsl:text>
  <xsl:value-of select="." />
  <xsl:text >) </xsl:text>
</xsl:template>

<xsl:template match="dial">
  <xsl:if test="position() = 1">
    <xsl:text >(</xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >,</xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
  <xsl:text >:</xsl:text>
  <xsl:if test="position() = last()">
    <xsl:text >) </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="lsource">
  <xsl:if test="position() = 1">
    <xsl:text > (</xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >, </xsl:text>
  </xsl:if>

  <xsl:choose>
    <xsl:when test="@ls_wasei = 'y'">
      <xsl:text >wasei:</xsl:text>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="@xml:lang" />
      <xsl:text >:</xsl:text>
    </xsl:otherwise>
  </xsl:choose>

  <xsl:if test="string-length() > 0">
    <xsl:text > </xsl:text>
    <xsl:value-of select="." />
  </xsl:if> 

  <xsl:if test="position() = last()">
    <xsl:text >)</xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="stagk">
  <xsl:if test="position() > 1">
    <xsl:text >, </xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
</xsl:template>

<xsl:template match="stagr">
  <xsl:if test="position() > 1 or ../stagk">
    <xsl:text >, </xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
</xsl:template>

<xsl:template match="xref">
  <xsl:if test="position() = 1">
    <xsl:text >(See </xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >,</xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
  <xsl:if test="position() = last()">
    <xsl:text >) </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="ant">
  <xsl:if test="position() = 1">
    <xsl:text >(ant: </xsl:text>
  </xsl:if>
  <xsl:if test="position() > 1">
    <xsl:text >,</xsl:text>
  </xsl:if>
  <xsl:value-of select="." />
  <xsl:if test="position() = last()">
    <xsl:text >) </xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="s_inf">
  <xsl:text >(</xsl:text>
  <xsl:value-of select="." />
  <xsl:text >) </xsl:text>
</xsl:template>

<xsl:template match="gloss">
  <xsl:value-of select="." />

  <xsl:if test="position() = 1">
    <xsl:apply-templates select="../lsource" />
  </xsl:if>

  <xsl:text >/</xsl:text>
</xsl:template>

</xsl:stylesheet>
