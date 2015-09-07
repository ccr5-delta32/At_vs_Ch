#!/usr/bin/python

''' This can be used to add variants of a single additional accession to the MySQL database '''

import MySQLdb
import gzip
from os import listdir
from os.path import isfile, join
import ext
import re

db = MySQLdb.connect(host="mysql2.mpipz.mpg.de", user="pieper", passwd=ext.sentry, db="pieper_chpoly")
cur = db.cursor()

gz_path = "/biodata/dep_tsiantis/common/ath_accessions/"
curpath = "/biodata/dep_tsiantis/common/Bjorn/At_1001_database/"

straincode = 'Col-1'
col = ['allele', 'chromosome', 'position', 'length', 'reference', 'consensus', 'quality', 'percentage', 'phred', 'ignore_this']

with gzip.open(gz_path + 'PA7199.sdi.gz', 'r') as SDI:
  count = 0
  for sdi in SDI:
    temp = [ x.strip('\n') for x in sdi.split('\t') ]
    stmt = "INSERT INTO At_variants (`" + '`, `'.join(col[0:len(temp)+1]) + "`) VALUES (%s)" % ("'" + "', '".join([straincode] + temp) + "'")
    cur.execute(stmt)
    count = count + 1
    if count == 25:
      db.commit()
      count = 0
