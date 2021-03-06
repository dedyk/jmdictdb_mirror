#!/usr/bin/env python3
# yply.py
#
#
# Converts a UNIX-yacc specification file into a PLY-compatible
# Python parser file.   To use, simply do this:
#
#   % python yply.py [--nocode] [--tokens] inputfile.y >myparser.py
#
# Based on the yply code written by David Beazley (dave@dabeaz.com)
# October 2, 2006 and distributed with the examples in Ply-2.3.

import sys, os, inspect, pdb
_=sys.path; _[0]=_[0]+('/' if _[0] else '')+'..'
from jmdictdb import ylex, yparse
from ply import *

def main (args, opts):
        yparse.emit_code = not opts.nocode
        yparse.emit_tokens = opts.tokens
        instr = open(args[0], encoding='utf-8').read()
        instr = instr.expandtabs()
        yacc.parse(instr,debug=opts.debug)

import optparse
def parse_cmdline ():
        from optparse import OptionParser
        u = \
"""\n\tpython %prog [options] input_filename

  %prog will generate a PLY-compatible parser module from a YACC
  specification file."""

        p = OptionParser (usage=u)
        p.add_option ("-c", "--nocode",
            action="store_true", dest="nocode", default=False,
            help="Don't produce any of the semantic action code.  "\
                "Default is to write all the action code to the "\
                "output file.  ")
        p.add_option ("-t", "--tokens",
            action="store_true", dest="tokens", default=False,
            help="Generate a \"tokens\" statement in the output file.  "\
                "Default is not to generate the statement on the assumtion "\
                "that the tokens will be imported from the lexer.  ")
        p.add_option ("-d", "--debug",
            type="int", dest="debug", default=0,
            help="Set parser debug flag when parsing the input file.  ")
        p.epilog = "Arguments: input_filename  (traditionaly this will be "\
                "named with a \".y\" suffix.)"

        opts, args = p.parse_args ()
        #...arg defaults can be setup here...
        if len (args) > 1: p.error ("Expected only one argument (input file name)")
        if len (args) < 1: p.error ("Expected one argument (input file name)")
        return args, opts

if __name__ == '__main__':
        args, opts = parse_cmdline ()
        sys.argv[0] = sys.argv[0].split('\\')[-1].split('/')[-1]
        main (args, opts)

