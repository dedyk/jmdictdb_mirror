#!/usr/bin/env python3
# Copyright (c) 2008 Stuart McGraw
# SPDX-License-Identifier: GPL-2.0-or-later

# This program will read a JMdict XML file and extract selected entries.

import sys, os, re, pdb
_=sys.path; _[0]=_[0]+('/' if _[0] else '')+'..'
from jmdictdb import jdb, jmxml

def main (args, opts):
        if sys.stdout.encoding != opts.encoding:
            sys.stdout = open (sys.stdout.fileno(), 'w', encoding=opts.encoding)
        jdb.KW = KW = jdb.Kwds (jdb.std_csv_dir())
        seqlist = []; first = True
        infn = args.pop (0)
        if opts.seqfile:
            seqlist = parse_seqfile (opts.seqfile)
        else:
            for arg in args:
                seq, x, cnt = arg.partition (',')
                seqlist.append ((int (seq), int (cnt or 1)))
        fin = open (infn, encoding="utf_8_sig")
        if seqlist:
            for seq,entr in jmxml.extract (fin, seqlist, opts.dtd, opts.all):
                print (seq, file=sys.stderr)
                if opts.dtd and first:
                    toplev, dtd = seq, entr
                    print ('\n'.join (dtd))
                    print ("<%s>" % toplev)
                    first = False;  continue
                print ('\n'.join (entr))
            if opts.dtd: print (("</%s>" % toplev))
        else: print ("No seq numbers!", file=sys.stderr)

def parse_seqfile (fname):
        seqlist = []
        f = open (fname)
        for lnnum, ln in enumerate (f):
            if ln.isspace() or re.search (r'^\s*#', ln): continue
            lnx = re.sub (r'\s*#.*', '', ln)
            lnx = re.sub (r'\s+', ' ', lnx).strip()
            seq, dummy, count = lnx.partition (' ')
            try: seqlist.append ((int (seq), int (count or 1)))
            except ValueError:
                print ("Line %d, bad format: %s" % (lnnum+1, ln.rstrip()), file=sys.stderr)
        return seqlist

#######################################################################

from optparse import OptionParser
from jmdictdb.pylib.optparse_formatters import IndentedHelpFormatterWithNL

def parse_cmdline ():
        u = \
"""\
Usage:
  %prog [options] filename seqnum[,count] [...]
  %prog [options] -s seqfile filename

  Extracts entries from a JMdict or JMnedict XML file 'filename'.
  The extracted entry(s), prepended with the files's DTD (unless
  -d was given), is written to stdout.  The arguments give the
  sequence numbers of the entries to be written.  Each can optionally
  be followed by a comma and a second number that is a count of
  the number successive entries to be extracted (including the
  first.  I.e., 1000320,3 will extract entry 1000320 and the next
  two entries.)

  The Monash JMnedict file does not contain sequence numbers.  In
  this case the 'seq' arguments are interpreted as ordinal entry
  numbers (starting from one).

  %prof assumes the entries in the input file are ordered by seq
  number and it will stop scanning for entries after a seq number
  greater than the largest seq number in the argument list is seen.
  The can be disabled, resulting is a full scan of the input file,
  with the -f option.

Arguments:
        filename -- Name of input JMdict or JMnedict xml file.
        seqnum,count -- Seq number (or ordinal number in the
            case of JMnedict) of an entry to extract optionally
            followed by a comma and count of sucessive entries
            (including 'seq') to extract."""

        p = OptionParser (usage=u, add_help_option=False,
                formatter=IndentedHelpFormatterWithNL())

        p.add_option ("--help",
            action="help", help="Print this help message.")

        p.add_option ("-s", "--seqfile", default=None,
            help="""Name of a file containing seq number and
           count pairs, one pair per line with the count being
           optional, but if present, separated by whitespace.
           Comments start with "#" and are ignored as are blank
           lines.""")

        p.add_option ("-d", "--dtd", default=True,
            action="store_false",
            help="Don't prepend the DTD extracted from the input "
                "file to the output.")

        p.add_option ("-a", "--all", default=False,
            action="store_true",
            help="""Scan the whole file looking for entries.  Normally
            %prog stops scanning after a sequence number greater than
            the largest seq number in arguments is seen, since it assumes
            sequence numbers are in increasing order.""")

        p.add_option ("-e", "--encoding", default='utf-8',
            type="str", dest="encoding",
            help="Encoding for output and error messages.  Note that "
                "this does not change the encoding declaration in the "
                "output DTD (if any).  It is intended to facilitate "
                "viewing output when directed to an interactive screen.")

        opts, args = p.parse_args ()
        if opts.seqfile:
            if len (args) < 1: p.error ("Not enough arguments, expected input filename.")
            if len (args) > 1: p.error ("Too many arguments, only input filename allowed when -w given.")
        else:
            if len (args) < 2: p.error ("Not enough arguments, expected at least two.")
        return args, opts

if __name__ == '__main__':
        args, opts = parse_cmdline()
        main (args, opts)
