#!/usr/bin/env python3
# Copyright (c) 2008 Stuart McGraw
# SPDX-License-Identifier: GPL-2.0-or-later

# Write an Audacity label track for the sound clips in a
# sound file.  Run with --help option for details.

import sys, os, inspect, pdb
_=sys.path; _[0]=_[0]+('/' if _[0] else '')+'..'
from jmdictdb import jdb

def main (args, opts):
        jdb.reset_encoding (sys.stdout, opts.encoding)
          # Open the database.  jdb.dbopts() extracts the db-related
          # options from the command line options in 'opts'.
        cur = jdb.dbOpen (opts.database, **jdb.dbopts (opts))
        for f in args:
            fname, ldata = getlabels (cur, f)
            if not fname: print ("No data for sound file '%s'" % str(f), file=sys.stderr)
            else:
                print (fname)
                for r in ldata:
                    strt = r.strt/100.0
                    print ("%f\t%f\t%s" % (strt, strt + r.leng/100.0, r.trns))

def getlabels (cur, filenum):
        sql = "SELECT v.loc AS vloc, f.loc AS floc " \
                "FROM sndfile f JOIN sndvol v ON f.vol=v.id " \
                "WHERE f.id=%s"
        rs = jdb.dbread (cur, sql, [filenum])
        if not rs: return None, None
        if len (rs) > 1: raise RuntimeError
        fname = os.path.join (rs[0].vloc, rs[0].floc)

        sql = "SELECT strt,leng,trns,notes FROM snd s WHERE s.file=%s ORDER BY strt,leng"
        rs = jdb.dbread (cur, sql, [filenum])
        return fname, rs


from optparse import OptionParser, OptionGroup
from jmdictdb.pylib.optparse_formatters import IndentedHelpFormatterWithNL

def parse_cmdline ():
        u = \
"""\n\t%prog [options] sndfile-num [sndfile-num [...]]

%prog will generate an Audacity label file for each sndfile
entry in the database whose id number is given as an argument.


Arguments:
        outfile -- Name of the output XML file.  If not given output
                is written to stdout."""

        p = OptionParser (usage=u, add_help_option=False,
                formatter=IndentedHelpFormatterWithNL())

        p.add_option ("--help",
            action="help", help="Print this help message.")

        p.add_option ("-e", "--encoding", default="utf-8",
            help="Encoding for the output.  Default is \"utf-8\".")

        g = OptionGroup (p, "Database access options",
                """The following options are used to connect to a
                database in order to read the entries.  """)
        g.add_option ("-d", "--database", default="jmdict",
            help="Name of the database to load.  Default is \"jmdict\".")
        g.add_option ("-h", "--host", default=None,
            help="Name host machine database resides on.")
        g.add_option ("-u", "--user", default=None,
            help="Connect to database with this username.")
        g.add_option ("-p", "--password", default=None,
            help="Connect to database with this password.")
        p.add_option_group (g)

        opts, args = p.parse_args ()
        if len (args) < 1: p.error ("No arguments given, expected at least one.")
        return args, opts

if __name__ == '__main__':
        args, opts = parse_cmdline()
        main (args, opts)
