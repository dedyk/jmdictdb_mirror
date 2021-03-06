#!/usr/bin/env python3
# Copyright (c) 2008,2014,2018 Stuart McGraw
# SPDX-License-Identifier: GPL-2.0-or-later

# This program creates rows in table "xref" based on the
# textual (kanji and kana) xref information saved in table
# "xresolv".  xresolv contains "unresolved" xrefs -- that
# is, xrefs defined only by a kanji/kana text(s) which for
# which there may be zero or multiple target entries.
#
# Each xresolv row contains the entr id and sens number
# of the entry that contained the xref, the type of xref,
# and the xref target entry kanji and or reading, and
# optionally, sense number.
#
# This program searchs for an entry matching the kanji
# and reading and creates one or more xref records using
# the target entry's id number.  The matching process is
# more involved than doing a simple search because a kanji
# xref may match several entries, and our job is to find
# the right one.  This is currently done by a fast but
# inaccurate method that does not take into account restr,
# stagr, and stag restrictions which limit certain reading-
# kanji combinations and thus would make unabiguous some
# xrefs that this program considers ambiguous.  See the
# comments in sub choose_entry() for a description of
# the algorithm.
#
# When an xref text is not found, or multiple candidate
# entries still exist after applying the selection
# algorithm, the fact is reported and that xref skipped.
#
# NOTE: references in the comments to 'xresolv' rows are not
# strictly accurate: the rows returned by get_xresolv_block()
# and subsequently by get_xresolv_set() are rows from the
# xresolv table augmented with additional info from the
# associated entry: .src, .seq, .stat, .unap.

import sys, re, itertools, io, pdb
_=sys.path; _[0]=_[0]+('/' if _[0] else '')+'..'
from jmdictdb import logger; from jmdictdb.logger import L
from jmdictdb import db, jdb

#-----------------------------------------------------------------------

def main (cmdln_args):
        args = parse_cmdline (cmdln_args)
        dburi = args.database
        try: dbconn = db.connect (dburi)
        except jdb.dbapi.OperationalError as e:
            sys.exit ("Error, unable to connect to database: %s" % str(e))
        KW = jdb.Kwds (dbconn.cursor())
          # Monkey patch jdb module until migration to db module is complete
          # because many lib functions still expect KW as a jdb global.
        jdb.KW = KW
        level = loglevel (args.level)
        logger.log_config (level=1 if args.messages else level,
                           filename=args.logfile)
        if args.messages:
            try: filter = parse_mlist (args.messages, level)
            except ValueError as e: sys.exit("Bad -m option: '%s'" % str (e))
            L().handlers[0].addFilter (filter)

        try: xref_src = get_src_ids (args.source_corpus)
        except KeyError:
            L('unknown corpus').warning(args.source_corpus)
            sys.exit (0)
        try: targ_src = get_src_ids (args.target_corpus)
        except KeyError:
            L('unknown corpus').warning(args.target_corpus)
            sys.exit (0)

          # Read the unresolved xrefs and their candidate targets
          # from the database, choose the optimal candidates and write
          # the xrefs generated from them to file 'tmpf'.
        tmpf = io.StringIO()
        entrcnt, unrefcnt, xrefcnt \
            = resolve (dbconn, tmpf, xref_src, targ_src,
                       start=args.start, stop=args.stop,
                       active=not args.ignore_nonactive)

          # Write the generated xrefs in file 'tmpf' back to the
          # database using Postgresql's COPY command (via psycopg2's
          # 'copy_from()' function).
        cursor = dbconn.cursor()
        tmpf.seek(0)
          #FIXME: wrap following in try/except
        cursor.copy_from (tmpf, 'xref')

          # Now delete any unresolved xrefs that have corresponding
          # resolved xrefs.  The delete is restricted to the same
          # xref and target .src values and start and stop entry id's
          # that were used in selecting the unresolved xrefs.  However
          # we still delete *any* matching unresolved xref whether
          # the matched xref was created by us or not.
        delcnt = 0
        if not args.keep:
            delcnt = del_xresolv (dbconn, xref_src, targ_src,
                                  start=args.start, stop=args.stop,
                                  active=not args.ignore_nonactive)
        L().info("processed %d unresolved, %d xrefs generated, "
                 "%d xresolvs deleted" % (unrefcnt, xrefcnt, delcnt))
        if args.noaction:
            L().info("rollback due to --noaction")
            dbconn.rollback()
        else: dbconn.commit()

def resolve (dbconn, tmpf, xref_src, targ_src, start=None, stop=None,
                           active=False):
          # Call process_entr_cands() to get candidate entries for the
          # unresolved xrefs limited by our function arguments, choose the
          # optimal one for each unresolved xref, create a corresponding
          # xref row and write to the temp file 'tmpf'.
        entrcnt = unrefcnt = xrefcnt = 0
        for rows in get_entr_cands (dbconn, xref_src, targ_src,
                                            start, stop, active):
              # 'rows' is a set of target candidate rows for all the
              # unresolved xrefs for a single entry.
            xrefs = process_entr_cands (rows)
            L('resolve').debug("process_entr_cands returned %s xrefs"
                               % len(xrefs))
            for x in xrefs:
                csv  = '\t'.join ([str(x.entr), str(x.sens), str(x.xref),
                                   str(x.typ), str(x.xentr), str(x.xsens),
                                   str(x.rdng) if x.rdng else '\\N',
                                   str(x.kanj) if x.kanj else '\\N',
                                   x.notes or '\\N',
                                   "t" if x.nosens else "f",
                                   "t" if x.lowpri else "f"]) + '\n'
                tmpf.write (csv)
            entrcnt += 1
            unrefcnt += unrefcount (rows)
            xrefcnt += len (xrefs)
        return entrcnt, unrefcnt, xrefcnt

def process_entr_cands (rows):
        xrefs = []
        key = lambda x: (x.entr, x.sens, x.typ, x.ord)
        for _,cands in itertools.groupby (rows, key=key):
              # 'cands' is the set of target candidate rows for
              # each single unresolved xref in 'rows'.
            row = choose_candidate (list(cands))
            if not row: continue
            xref = mkxref (row)
            if not xref: continue
            xrefs.append (xref)
        return xrefs

def get_entr_cands (dbconn, xref_src, targ_src, start=None, stop=None,
                            active=False):
        # Yield sets of candidates rows for all unresolved xrefs
        # for a single entry.
        #
        # dbconn -- An open dbapi connection to a jmdictdb database.
        # xref_src -- A 2-tuple consiting of:
        #   0: a sequence of numbers identifying the entr.src numbers
        #     to be included or excluded when searching for xrefs to
        #     resolve.
        #   1: (bool) if false the values in item 0 specify src numbers
        #     to include; if false they are numbers to exclude.
        # targ_src -- Same format as 'xref_src' but for target entry
        #   .src numbers.
        # start -- Lowest entry id number to process.  If None of not
        #   given default is 1.
        # stop -- Process entries up to but not including this id number.
        # active -- (bool) If true do not process any unresolved xrefs
        #   that are attached to deleted, rejected, or unapproved entries
        #   (i.e. restrict processing to active, approved entries).
        #   If false, such unresolved xrefs will be processed along with
        #   the active, approved ones.
        ## Following parameter is currently ignored, see comments below.
        ## appr_targ -- (bool) if true restrict target candidate entries
        ##   to those that are approved.  If false, unapproved entries
        ##   will also be target candidates.

        L().info("reading candidates from database, may take a while...")
          #FIXME: this replicates same WHERE logic used in del_xresolv();
          # should factor out to a single location, either in python
          # code or in a database view.
        c1, args1 = src_clause (xref_src, targ_src)
        c2, args2 = idrange_clause (start, stop)
          #FIXME: should not hardwire 'stat' value.
        c3 = "v.stat=2 AND NOT v.unap" if active else ""
          # Disallow resolution to deleted or rejected entries.
          #FIXME: should not hardwire 'stat' value.
        c4 = "(tstat=2 OR tstat IS NULL)"
          # Disallow resolution from rejected or deleted entries.
          #FIXME: should not hardwire 'stat' value.
        c6 = "stat=2"
          #FIXME: following condition controls whether or not unapproved
          # xrefs are considered as target candidates.  It is disabled
          # because it is probably the wrong thing to do right now.  If an
          # xref is resolved to an unapproved entry, the target unapproved
          # entry will not get the reverse xref and if it is approved the
          # resulting new active entry will not have the reverse xref.
          # We probably need to generate xrefs to all the unapproved entries
          # as well as the approved active one but that means restoring a
          # flavor of the "one unresolved -> multiple xrefs" capability
          # that was removed in hg-180615-3e9e9c.
          # Without this condition unapproved edits will result in
          # resolution failing due to multiple targets forcing manual
          # intervention which seems the best option at the moment.
        c5 = "" #"NOT tunap" if appr_targ else "")

        whr = " AND ".join([c for c in [c1,c2,c3,c4,c5,c6] if c])
        if whr: whr = "WHERE " + whr
        args = tuple (args1 + args2)
        sql = "SELECT * FROM vrslv v %s"\
              " ORDER BY entr,sens,typ,ord,targ" % whr
        L().debug("sql: %s" % sql)
        L().debug("args: %r" % (args,))
        rs = db.query (dbconn, sql, args)
        L().info("read %d candidates from database" % len(rs))
        key = lambda x: (x.entr, x.sens, x.typ, x.ord)
        key = lambda x: x.entr
        for _, rows in itertools.groupby (rs, key=key):
            yield list(rows)

def src_clause (xref_src, targ_src):
        xs_lst, xs_inv = xref_src or ([], None)
        ts_lst, ts_inv = targ_src or ([], None)
        args = []
        c1 = ("src %sIN %%s" % ('NOT ' if xs_inv else '')) if xs_lst else ''
        if c1: args.append(xs_lst)
        if ts_lst:
            c2 = "(tsrc %sIN %%s OR tsrc IS NULL)" % ('NOT ' if ts_inv else '')
            args.append (ts_lst)
        else: c2 = ""
        clause = c1 + (" AND " if c1 and c2 else "") + c2
        return clause, args

def idrange_clause (start=None, stop=None):
        args = []
        r1 = "v.entr>=%s" if start else ""
        r2 = "v.entr<%s" if stop else ""
        if r1: args.append (start)
        if r2: args.append (stop)
        clause = r1 + (" AND " if r1 and r2 else "") + r2
        return clause, args

def choose_candidate (rows):
        L('choose_candidate').debug("received %d rows" % len(rows))
        if len(rows) == 1:
              # There is only one candidates row based on which we can decide
              # unambiguously among three possibilities: 1) there was no match,
              # 2) there were multiple matches, or 3) we found exactly one
              # match.
            v = rows[0]
            if v.tsrc is None:
                L('xref target not found').error(fs(v))
                return None
            if v.nentr==1:
                L('xref resolved (1)').info(fs(v))
                return v
            if rows[0].nentr>1:
                L('multiple candidates').error(fs(v))
                return None
          # If there were multiple candidates rows we need to look through
          # them all to find the best choice.  We will never choose a
          # candidates row that has .nentr>1 since that is definitionally
          # a match to multiple targets.  Also note the candidates must
          # already match the unresolved xref's reading or kanji or both
          # (if the xref specifies both).
        for v in rows:
               # If looking for a reading match, first choice is a match
               # to the first reading of an entry that has no kanji.
            if v.nentr == 1 and not v.ktxt and v.rdng==1 and v.nokanji:
                L('xref resolved (2)').info(fs(v))
                return v
        for v in rows:
               # Otherwise look for a candidate that matches on either the
               # first reading or first kanji.
            first = (v.rtxt and v.rdng==1) or (v.ktxt and v.kanj==1)
            if v.nentr == 1 and first:
                L('xref resolved (3)').info(fs(v))
                return v
        for v in rows:
               # And as last choice accept a candidate with a matching
               # reading and/or kanji regardless of the position of the
               # matches.
            if v.nentr == 1:
                L('xref resolved (4)').info(fs(v))
                return v
        L('multiple candidates').error(fs(v))
        return None

def del_xresolv (dbconn, xref_src=[], targ_src=None, start=None, stop=None,
                         active=False):
          # CAUTION: we assume here that xref.xref has the same value
          #  as xresolv.ord and thus we can use xref.xref to delete
          #  the corresponding xresolv row.  That is currently true but
          #  has not been true in past and could change in the future.
          #FIXME: this replicates same WHERE logic used in resolve();
          # should factor out to a single location, either in python
          # code or in a database view.
        c0 = "v.entr=x.entr AND v.sens=x.sens"\
             " AND v.typ=x.typ AND v.ord=x.xref"
        c1, args1 = src_clause (xref_src, targ_src)
        c2, args2 = idrange_clause (start, stop)
          # 'c3' is not quite the same as in get_entr_cands() because 
          # that is based on view "rslv" but this query is based on 
          # table "xresolv".
        c3 = "x.stat=2 AND NOT x.unap" if active else ""
        c4 = "(tstat=2 OR tstat IS NULL)"
        c6 = "stat=2"
        c5 = "" #"NOT tunap" if appr_targ else "")
        whr = " AND ".join([c for c in [c0,c1,c2,c3,c4,c5,c6] if c])
        if whr: whr = "WHERE " + whr
        args = args1 + args2
        sql = "DELETE FROM xresolv v"\
              " USING (SELECT x.entr, x.sens, x.xref, x.typ,"\
                            " ex.src, ex.stat, ex.unap,"\
                            " et.src as tsrc,et.stat AS tstat,et.unap AS tunap"\
                     " FROM xref x"\
                     " JOIN entr ex ON x.entr=ex.id"\
                     " JOIN entr et ON x.xentr=et.id) AS x"\
              " %s" % whr
        L('del_xresolv.sql').debug("sql: %s" % sql)
        L('del_xresolv.sql').debug("args: %r" % (args,))
        cursor = db.ex (dbconn, sql, args)
        return cursor.rowcount

def mkxref (v):
          # If there is no tsens, generate an xref to only the first
          # sense.  Rationale: Revs prior to ~2018-06-07 we generated
          # xrefs to all senses in this scenario.  When there were a
          # lot of reverse xrefs to a word from the Example sentences,
          # every sense of the target word would have them all repeated.
          # However unless there is only one target sense, we can be
          # sure we are wrong: if the senses were so similar to be
          # interchangable they wouldn't be separate senses.  Since
          # we'll be wrong either way and someone will need to manually
          # correct it later, choose the way that produces the least
          # amount of clutter in the entry.  Also, in many cases the
          # first *will* be the right sense.
        nosens = False
        if not v.tsens:
            if v.nsens != 1:
                L('multiple senses').warning("using 'nosens' xref: %s"\
                                             % (fs(v)))
                nosens = True
            v.tsens = 1
        if v.tsens > v.nsens:
            L('sense number too big').error(fs(v))
            return None
        xref = jdb.Obj (entr=v.entr, sens=v.sens, xref=v.ord, typ=v.typ,
                        xentr=v.targ, xsens=v.tsens, rdng=v.rdng, kanj=v.kanj,
                        notes=v.notes, nosens=nosens,
                          # v.prio will be None for jmdict, et.al. words and
                          # should result in lowprio=False.  For Tatoeba
                          # sentences v.prio will be True (for exemplar
                          # sentences) or False (other sentences) and lowpri
                          # should have opposite truth value.
                        lowpri=not (v.prio is None or v.prio))
        return xref

def unrefcount (rows):
          # Count and return the number of unique unresolved xrefs in
          # a set of candidate rows.  Since a single unresolved xref
          # may have multiple candidates the number may be smaller than
          # the length of 'rows'.  The view "vrslv" which is the source
          # of 'rows' guarantees there will be at least on row for each
          # unresolved xref.
        count = set()
        for r in rows: count.add ((r.entr,r.sens,r.typ,r.ord))
        return len (count)

def fs (v):
          # Format unresolved xref 'v' in a standard way for messages.
        s = "%s.%d (%d,%d,%d) %s:" \
           % (jdb.KW.SRC[v.src].kw,v.seq, v.entr,v.sens,v.ord,
              fmt_jitem(v.ktxt, v.rtxt, [v.tsens] if v.tsens else []))
        return s

def fmt_jitem (ktxt, rtxt, slist):
          # FIXME: move this function into one of the formatting
          # modules (e.g. fmt.py or fmtjel.py).
        jitem = (ktxt or "") + ('・' if ktxt and rtxt else '') + (rtxt or "")
        if slist: jitem += '[' + ','.join ([str(s) for s in slist]) + ']'
        return jitem

def get_src_ids (srclist):
        if not srclist: return None
        neg = False
        if srclist.startswith ('-'):
            neg = True; srclist = srclist[1:]
        srcs = srclist.split(',')
        ids = tuple([get_src_id (x) for x in srcs if x])
        return ids, neg

def get_src_id (id_or_name):
          # Return the kwsrc.id value corresponding to 'id_or_name'.
        if not id_or_name: return None
        src = id_or_name
        try: src = int (src)
        except (ValueError): pass
        src = jdb.KW.SRC[src].id
        return src

def parse_mlist (mlist, thresh):
        regexes = []
        for regex in mlist:
            neg = False
            if regex.startswith ('!'): regex, neg = regex[1:], True
            regexes.append ((neg, regex))
        filter = lambda x: logmsg_filter (x, regexes, thresh)
        return filter

def logmsg_filter (logrec, regexes, thresh=30):
        for neg, regex in regexes:
            if not re.search(regex,logrec.name): continue
              # The last regex matched.  For a regular match (ie, no "!"
              # was given and 'inverted' is False) return True to print
              # the log message.  If "!" was given, 'inverted' is True
              # and we return False to suppress the message.
            return not neg
        return logrec.levelno >= thresh

def loglevel (thresh):
        try:
            try: lvl = int(thresh)
            except (ValueError, TypeError):
                lvl = {'e':40, 'w':30, 'i':20, 'd':10}.get (thresh[0].lower())
        except (ValueError, TypeError, IndexError):
            raise ValueError ("Bad 'level' option: %s" % thresh)
        return lvl

#-----------------------------------------------------------------------

import argparse
from jmdictdb.pylib.argparse_formatters import ParagraphFormatterML
def parse_cmdline (cmdln_args):
        p = argparse.ArgumentParser (prog=cmdln_args[0],
            formatter_class=ParagraphFormatterML,
            description="Resolve a set of unresolved xrefs by identifying "
                "one specific target entry for each one and creating "
                "xrefs to them.")

        p.add_argument ("-n", "--noaction", default=False,
            action="store_true",
            help="Resolve xrefs and generate log file but don't make "
                "any changes to database. (This implies --keep.)")

        p.add_argument ("-i", "--ignore-nonactive", default=False,
            action="store_true",
            help="Ignore unresolved xrefs belonging to entries with a"
                "status of deleted or rejected or which are unapproved ")

        p.add_argument ("-s", "--source-corpus", default=None,
            metavar='CORPORA',
            help="Limit to xrefs occuring in entries of CORPORA (a comma-"
                "separated list of corpus names or id numbers).  If preceeded "
                "by a \"-\", all corpora will be included except those listed.")

        p.add_argument ("-t", "--target-corpus", default=None,
            metavar='CORPORA',
            help="Limit to xrefs that resolve to targets in CORPORA (a comma-"
                "separated list of corpus names or id numbers).  If preceeded "
                "by a \"-\", all corpora will be included except those listed.")

        p.add_argument ("--start", default=None,
            help="Limit processing to unresolved xrefs with entry id numbers "
                "equal to or greater than this value.")

        p.add_argument ("--stop", default=None,
            help="Limit processing to unresolved xrefs with entry id numbers "
                "less than this value.")

        p.add_argument ("-k", "--keep", default=False, action="store_true",
            help="Do not delete unresolved xrefs after they are resolved.  "
                "This is primarily to aid in debugging.  If not given "
                "unresolved xrefs that match an existing xref (match based "
                "on the values of entr, sens, typ, and ord) subject to the "
                "conditions given by --source-corpus, --target-corpus, "
                "--start and --stop will be deleted.  "
                "Note that all matching unresolved xrefs will be deleted, "
                "whether the matching xref was created by this execution "
                "of the program or earlier.")

        p.add_argument ("-l", "--logfile", default=None,
            help="Name of file log messages will be written to."
                "If not given messages will be written to stderr.")

        p.add_argument ("-v", "--level", default='warn',
            help="Logging level, one of: "
                "'error', 'warning', 'info', 'debug'.  "
                "May be abbreviated to a single letter.  Log messages at "
                "or above this level will be printed sans the exceptions"
                "specified by any --messages options given.")

        p.add_argument ("-m", "--messages", default=[], action="append",
            help="Allows finer-grained control of logging messages than "
                "provided by --level.  The value of this option is a "
                "a regular expression, optionally prefixed with a \"!\" "
                "character.  Multiple --message options may be given.  "
                "When a logging message is generated the message's source "
                "string (aka logger name) is matched against each --message "
                "regex in turn; if it matches and no \"!\" was given, the "
                "log message is printed.  If no \"!\" was given the message "
                "is not printed.  In either case no further --message regexes "
                "are checked for that log message.  If there was no match, "
                "the next regex is checked.  If no regexes match, the result "
                "is determined by the --level option.")

        p.add_argument ("-d", "--database", default="jmdict",
            help="URI for the database to use.")
          # p.epilog text is indented by one space in order to include a
          # space character between each line of text.  Putting the space
          # character at the end of each line is undesirable because it
          # prevents running a cleanup tool on the file that removes
          # trailing whitespace.
        p.epilog = """\
 When a program such as jmparse.py or exparse.py parses
 a corpus file, any xrefs in that file are in textual
 form (often a kanji and/or kana text string that identifies
 the target of the xref).  The database stores xrefs using
 the actual entry id number of the target entry but the
 textual form canot be resolved into the id form at parse
 time since the target entry may not even be in the database
 yet. Instead, the parser programs save the textual form of
 the xref in a table, 'xresolv', and it is the job of this
 program, when run later, to convert the textual 'xresolv'
 table xrefs into the id form of xrefs and load them into
 table 'xref'.

 Each xresolv row contains the entr id and sens number
 of the entry that contained the xref, the type of xref,
 and the xref target entry kanji and/or reading, and
 optionally, sense number.

 This program searches for an entry matching the kanji
 and reading and creates an xref record using the target
 entry's id number.  The matching process is more involved
 than doing a simple search because a kanji xref may match
 several entries, and our job is to find the right one.
 This is currently done by a fast but inaccurate method
 that does not take into account restr, stagr, and stag
 restrictions which limit certain reading-kanji combinations
 and thus would make unabiguous some xrefs that this program
 considers ambiguous.  See the comments in sub choose_entry()
 for a description of the algorithm.

 When an xref text is not found, or multiple candidate
 entries still exist after applying the selection
 algorithm, the fact is reported and that xref skipped.

 Error and other messages refer to unresolved xrefs using
 the format: "corpus.seq# (entr-id, sens#, ord#) where
 all except ord# refer to the entry the xref is from.
 Error (E) messages indicate no resolved xref was generated.
 Warning (W) messages indicate an xref was produced but
 might not be what was wanted.  Info (I) messages report
 sucessful completion of an action.  There are also
 a number of debug (D) messages that can be optionally
 enabled.
."""

        args = p.parse_args (cmdln_args[1:])
        return args

if __name__ == '__main__': main (sys.argv)
