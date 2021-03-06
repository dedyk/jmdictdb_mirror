#!/usr/bin/env python3
# Copyright (c) 2008 Stuart McGraw
# SPDX-License-Identifier: GPL-2.0-or-later

import sys

def main (args, opts):
        f = open (args[0], 'r', encoding='utf_8_sig')
        for n,ln in enumerate (f):
            if (opts.format):
                id, part2b, part2t, part1, scope, type, ref_name = ln.split('\t')
                ref_name = ref_name.rstrip()
                lang = part2b or id
            else:
                id, part2b, part2t, ref_name, other = ln.split ('|')
                if id == 'qaa-qtz': continue
                lang = id
            if n == 0: out (opts.style, 1, 'eng', 'English')
            else:
                if lang != 'eng': out (opts.style, n+1, lang, ref_name)

def out (style, n, lang, descr):
        if style == 'csv':
            print ('%d\t%s\t%s' % (n, lang, descr))
        elif style == 'perl':
            print ("\t    '%s' => %d,\t# %s" % (lang, n, descr))
        else:
            raise ValueError ("Invalid 'style' parameter: '%s'" % style)


from optparse import OptionParser

def parse_cmdline ():
        u = \
"""\n\t%prog [-s [csv|perl]] iso-639-file

  This program will read a ISO 639 dataset file containing the complete
  ISO 639 (-2 or -3) standard language codes dataset and generate,
  depending on the command line options given, a tab-delimited csv table
  suitable for use as the pg/data/kwlang.csv file, or a snippent of perl
  code suitable for inclusion in perl/lib/jmdictxml.pm.  Note that the
  -2 and -3 standards are quite different and will produce different output
  from this program.
  Output is written to stdout and is utf-8 encoded.

  The ISO 639-2 dataset file is available from (use the utf-8 version):
    http://www.loc.gov/standards/iso639-2/ascii_8bits.html
  The ISO 639-3 dataset file is available from:
    http://www.sil.org/iso639-3/download.asp

Arguments:
        iso-639-file -- Name of the file containing the iso-639 data."""

        p = OptionParser (usage=u, add_help_option=False)
        p.add_option ("-2", "--iso239-2",
            action="store_false", dest="format",
            help="Input file is a \"|\" delimited ISO-639-2 file. ")
        p.add_option ("-3", "--iso239-3",
            action="store_true", dest="format", default=True,
            help="Input file is a tab delimited ISO-639-3 file. ")
        p.add_option ("-s", "--style", default='csv',
            type="str", dest="style",
            help="Output style.  Must be either \"csv\" or \"perl\".")
        p.add_option ("--help",
            action="help", help="Print this help message.")
        opts, args = p.parse_args ()
        if len(args) != 1: p.error("Expected one command line argument.")
        return args, opts

if __name__ == '__main__':
        args, opts = parse_cmdline()
        main (args, opts)
