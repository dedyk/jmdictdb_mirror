
# jelparse_tab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BRKTL BRKTR COLON COMMA DOT EQL FF GTEXT HASH KTEXT NUMBER QTEXT RTEXT SEMI SLASH SNUM TEXTentr : preentrpreentr : kanjsect FF rdngsect FF sensespreentr : FF rdngsect FF sensespreentr : kanjsect FF FF senseskanjsect : kanjitemkanjsect : kanjsect SEMI kanjitemkanjitem : krtextkanjitem : krtext taglistsrdngsect : rdngitemrdngsect : rdngsect SEMI rdngitemrdngitem : krtextrdngitem : krtext taglistskrtext : KTEXTkrtext : RTEXTsenses : sensesenses : senses sensesense : SNUM glossesglosses : glossglosses : glosses SEMI glossgloss : GTEXTgloss : GTEXT taglistsgloss : taglists GTEXTgloss : taglists GTEXT tagliststaglists : taglisttaglists : taglists taglisttaglist : BRKTL tags BRKTRtags : tagitemtags : tags COMMA tagitemtagitem : KTEXTtagitem : RTEXTtagitem : TEXTtagitem : QTEXTtagitem : TEXT EQL TEXTtagitem : TEXT EQL TEXT COLONtagitem : TEXT EQL TEXT COLON atexttagitem : TEXT EQL TEXT SLASH TEXT COLONtagitem : TEXT EQL TEXT SLASH TEXT COLON atexttagitem : TEXT EQL jrefsatext : TEXTatext : QTEXTjrefs : jrefjrefs : jrefs SEMI jrefjref : xrefnumjref : xrefnum slistjref : xrefnum DOT jitemjref : jitemjref : jitem TEXTjitem : dotlistjitem : dotlist slistdotlist : jtextdotlist : dotlist DOT jtextjtext : KTEXTjtext : RTEXTjtext : QTEXTxrefnum : NUMBERxrefnum : NUMBER HASHxrefnum : NUMBER TEXTslist : BRKTL snums BRKTRsnums : NUMBERsnums : snums COMMA NUMBER'
    
_lr_action_items = {'FF':([0,3,5,6,7,8,9,11,12,13,14,15,18,19,22,23,35,36,],[4,9,-5,-7,-13,-14,17,20,-9,-11,-8,-24,33,-6,-12,-25,-10,-26,]),'KTEXT':([0,4,9,10,16,21,37,38,62,64,70,],[7,7,7,7,26,7,26,54,54,54,54,]),'RTEXT':([0,4,9,10,16,21,37,38,62,64,70,],[8,8,8,8,27,8,27,55,55,55,55,]),'$end':([1,2,15,23,30,31,34,36,39,40,41,42,44,58,59,71,72,],[0,-1,-24,-25,-4,-15,-3,-26,-16,-17,-18,-20,-2,-21,-22,-19,-23,]),'SEMI':([3,5,6,7,8,11,12,13,14,15,18,19,22,23,35,36,40,41,42,47,48,49,50,51,52,53,54,55,56,58,59,63,66,67,68,69,71,72,77,78,81,83,],[10,-5,-7,-13,-14,21,-9,-11,-8,-24,21,-6,-12,-25,-10,-26,57,-18,-20,62,-41,-43,-46,-55,-48,-50,-52,-53,-54,-21,-22,-44,-47,-56,-57,-49,-19,-23,-42,-45,-51,-58,]),'BRKTL':([6,7,8,13,14,15,22,23,32,36,42,43,49,51,52,53,54,55,56,57,58,59,67,68,72,81,],[16,-13,-14,16,16,-24,16,-25,16,-26,16,16,65,-55,65,-50,-52,-53,-54,16,16,16,-56,-57,16,-51,]),'GTEXT':([15,23,32,36,43,57,],[-24,-25,42,-26,59,42,]),'SNUM':([15,17,20,23,30,31,33,34,36,39,40,41,42,44,58,59,71,72,],[-24,32,32,-25,32,-15,32,32,-26,-16,-17,-18,-20,32,-21,-22,-19,-23,]),'TEXT':([16,37,38,50,51,52,53,54,55,56,60,61,69,81,82,83,],[28,28,46,66,68,-48,-50,-52,-53,-54,73,76,-49,-51,73,-58,]),'QTEXT':([16,37,38,60,62,64,70,82,],[29,29,56,75,56,56,56,75,]),'BRKTR':([24,25,26,27,28,29,45,46,47,48,49,50,51,52,53,54,55,56,60,63,66,67,68,69,73,74,75,77,78,79,80,81,82,83,85,86,],[36,-27,-29,-30,-31,-32,-28,-33,-38,-41,-43,-46,-55,-48,-50,-52,-53,-54,-34,-44,-47,-56,-57,-49,-39,-35,-40,-42,-45,83,-59,-51,-36,-58,-37,-60,]),'COMMA':([24,25,26,27,28,29,45,46,47,48,49,50,51,52,53,54,55,56,60,63,66,67,68,69,73,74,75,77,78,79,80,81,82,83,85,86,],[37,-27,-29,-30,-31,-32,-28,-33,-38,-41,-43,-46,-55,-48,-50,-52,-53,-54,-34,-44,-47,-56,-57,-49,-39,-35,-40,-42,-45,84,-59,-51,-36,-58,-37,-60,]),'EQL':([28,],[38,]),'NUMBER':([38,62,65,84,],[51,51,80,86,]),'COLON':([46,76,],[60,82,]),'SLASH':([46,],[61,]),'DOT':([49,51,52,53,54,55,56,67,68,81,],[64,-55,70,-50,-52,-53,-54,-56,-57,-51,]),'HASH':([51,],[67,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'entr':([0,],[1,]),'preentr':([0,],[2,]),'kanjsect':([0,],[3,]),'kanjitem':([0,10,],[5,19,]),'krtext':([0,4,9,10,21,],[6,13,13,6,13,]),'rdngsect':([4,9,],[11,18,]),'rdngitem':([4,9,21,],[12,12,35,]),'taglists':([6,13,32,42,57,59,],[14,22,43,58,43,72,]),'taglist':([6,13,14,22,32,42,43,57,58,59,72,],[15,15,23,23,15,15,23,15,23,15,23,]),'tags':([16,],[24,]),'tagitem':([16,37,],[25,45,]),'senses':([17,20,33,],[30,34,44,]),'sense':([17,20,30,33,34,44,],[31,31,39,31,39,39,]),'glosses':([32,],[40,]),'gloss':([32,57,],[41,71,]),'jrefs':([38,],[47,]),'jref':([38,62,],[48,77,]),'xrefnum':([38,62,],[49,49,]),'jitem':([38,62,64,],[50,50,78,]),'dotlist':([38,62,64,],[52,52,52,]),'jtext':([38,62,64,70,],[53,53,53,81,]),'slist':([49,52,],[63,69,]),'atext':([60,82,],[74,85,]),'snums':([65,],[79,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> entr","S'",1,None,None,None),
  ('entr -> preentr','entr',1,'p_entr_1','jelparse.py',21),
  ('preentr -> kanjsect FF rdngsect FF senses','preentr',5,'p_preentr_1','jelparse.py',44),
  ('preentr -> FF rdngsect FF senses','preentr',4,'p_preentr_2','jelparse.py',48),
  ('preentr -> kanjsect FF FF senses','preentr',4,'p_preentr_3','jelparse.py',52),
  ('kanjsect -> kanjitem','kanjsect',1,'p_kanjsect_1','jelparse.py',56),
  ('kanjsect -> kanjsect SEMI kanjitem','kanjsect',3,'p_kanjsect_2','jelparse.py',60),
  ('kanjitem -> krtext','kanjitem',1,'p_kanjitem_1','jelparse.py',64),
  ('kanjitem -> krtext taglists','kanjitem',2,'p_kanjitem_2','jelparse.py',68),
  ('rdngsect -> rdngitem','rdngsect',1,'p_rdngsect_1','jelparse.py',75),
  ('rdngsect -> rdngsect SEMI rdngitem','rdngsect',3,'p_rdngsect_2','jelparse.py',79),
  ('rdngitem -> krtext','rdngitem',1,'p_rdngitem_1','jelparse.py',83),
  ('rdngitem -> krtext taglists','rdngitem',2,'p_rdngitem_2','jelparse.py',87),
  ('krtext -> KTEXT','krtext',1,'p_krtext_1','jelparse.py',94),
  ('krtext -> RTEXT','krtext',1,'p_krtext_2','jelparse.py',98),
  ('senses -> sense','senses',1,'p_senses_1','jelparse.py',102),
  ('senses -> senses sense','senses',2,'p_senses_2','jelparse.py',106),
  ('sense -> SNUM glosses','sense',2,'p_sense_1','jelparse.py',110),
  ('glosses -> gloss','glosses',1,'p_glosses_1','jelparse.py',117),
  ('glosses -> glosses SEMI gloss','glosses',3,'p_glosses_2','jelparse.py',121),
  ('gloss -> GTEXT','gloss',1,'p_gloss_1','jelparse.py',125),
  ('gloss -> GTEXT taglists','gloss',2,'p_gloss_2','jelparse.py',129),
  ('gloss -> taglists GTEXT','gloss',2,'p_gloss_3','jelparse.py',133),
  ('gloss -> taglists GTEXT taglists','gloss',3,'p_gloss_4','jelparse.py',137),
  ('taglists -> taglist','taglists',1,'p_taglists_1','jelparse.py',141),
  ('taglists -> taglists taglist','taglists',2,'p_taglists_2','jelparse.py',145),
  ('taglist -> BRKTL tags BRKTR','taglist',3,'p_taglist_1','jelparse.py',150),
  ('tags -> tagitem','tags',1,'p_tags_1','jelparse.py',154),
  ('tags -> tags COMMA tagitem','tags',3,'p_tags_2','jelparse.py',158),
  ('tagitem -> KTEXT','tagitem',1,'p_tagitem_1','jelparse.py',163),
  ('tagitem -> RTEXT','tagitem',1,'p_tagitem_2','jelparse.py',167),
  ('tagitem -> TEXT','tagitem',1,'p_tagitem_3','jelparse.py',171),
  ('tagitem -> QTEXT','tagitem',1,'p_tagitem_4','jelparse.py',180),
  ('tagitem -> TEXT EQL TEXT','tagitem',3,'p_tagitem_5','jelparse.py',189),
  ('tagitem -> TEXT EQL TEXT COLON','tagitem',4,'p_tagitem_6','jelparse.py',193),
  ('tagitem -> TEXT EQL TEXT COLON atext','tagitem',5,'p_tagitem_7','jelparse.py',201),
  ('tagitem -> TEXT EQL TEXT SLASH TEXT COLON','tagitem',6,'p_tagitem_8','jelparse.py',215),
  ('tagitem -> TEXT EQL TEXT SLASH TEXT COLON atext','tagitem',7,'p_tagitem_9','jelparse.py',226),
  ('tagitem -> TEXT EQL jrefs','tagitem',3,'p_tagitem_10','jelparse.py',237),
  ('atext -> TEXT','atext',1,'p_atext_1','jelparse.py',284),
  ('atext -> QTEXT','atext',1,'p_atext_2','jelparse.py',288),
  ('jrefs -> jref','jrefs',1,'p_jrefs_1','jelparse.py',292),
  ('jrefs -> jrefs SEMI jref','jrefs',3,'p_jrefs_2','jelparse.py',296),
  ('jref -> xrefnum','jref',1,'p_jref_1','jelparse.py',300),
  ('jref -> xrefnum slist','jref',2,'p_jref_2','jelparse.py',304),
  ('jref -> xrefnum DOT jitem','jref',3,'p_jref_3','jelparse.py',308),
  ('jref -> jitem','jref',1,'p_jref_4','jelparse.py',312),
  ('jref -> jitem TEXT','jref',2,'p_jref_5','jelparse.py',316),
  ('jitem -> dotlist','jitem',1,'p_jitem_1','jelparse.py',320),
  ('jitem -> dotlist slist','jitem',2,'p_jitem_2','jelparse.py',324),
  ('dotlist -> jtext','dotlist',1,'p_dotlist_1','jelparse.py',328),
  ('dotlist -> dotlist DOT jtext','dotlist',3,'p_dotlist_2','jelparse.py',332),
  ('jtext -> KTEXT','jtext',1,'p_jtext_1','jelparse.py',336),
  ('jtext -> RTEXT','jtext',1,'p_jtext_2','jelparse.py',340),
  ('jtext -> QTEXT','jtext',1,'p_jtext_3','jelparse.py',344),
  ('xrefnum -> NUMBER','xrefnum',1,'p_xrefnum_1','jelparse.py',348),
  ('xrefnum -> NUMBER HASH','xrefnum',2,'p_xrefnum_2','jelparse.py',352),
  ('xrefnum -> NUMBER TEXT','xrefnum',2,'p_xrefnum_3','jelparse.py',356),
  ('slist -> BRKTL snums BRKTR','slist',3,'p_slist_1','jelparse.py',360),
  ('snums -> NUMBER','snums',1,'p_snums_1','jelparse.py',364),
  ('snums -> snums COMMA NUMBER','snums',3,'p_snums_2','jelparse.py',371),
]