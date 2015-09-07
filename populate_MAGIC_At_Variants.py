#!/usr/bin/python

''' This one will add the variants from the MAGIC progenitors to the MySQL database, which are not gzipped. '''

import MySQLdb
from os import listdir
from os.path import isfile, join
import ext
import re

do = range(0,4) 
#do = range(4,8) 
#do = range(8,13) 
#do = range(13,18) 

db = MySQLdb.connect(host="mysql2.mpipz.mpg.de", user="pieper", passwd=ext.sentry, db="pieper_chpoly")
cur = db.cursor()

path80  = "/biodata/dep_tsiantis/common/ath_80/"
curpath = "/biodata/dep_tsiantis/common/Bjorn/At_1001_database/"

with open(curpath + 'MAGIC_prog', 'r') as acc:
  accessions = [[x.strip('\n') for x in y.split('\t')] for y in acc ]

## files in directory
sdifiles = [ x for x in listdir(path80) if re.search('.sdi$', x) and isfile(join(path80, x)) and x.strip('.sdi') in [accessions[y][0] for y in do] ]

col = ['allele', 'chromosome', 'position', 'length', 'reference', 'consensus', 'quality', 'percentage', 'phred', 'ignore_this']

if len(sdifiles) > 0:
  for strain in sdifiles:
    straincode = [x for x in accessions if x[0] == strain.strip('.sdi')][0][1]
    with open(path80 + strain, 'r') as SDI:
      count = 0
      for sdi in SDI:
        temp = [ x.strip('\n') for x in sdi.split('\t') ]
        stmt = "INSERT INTO At_variants (`" + '`, `'.join(col[0:len(temp)+1]) + "`) VALUES (%s)" % ("'" + "', '".join([straincode] + temp) + "'")
        cur.execute(stmt)
        count = count+1
        if count == 25:
          db.commit()
          count = 0
