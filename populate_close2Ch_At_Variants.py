#!/usr/bin/python

''' This will insert the variants for the Arabidopsis accessions selected to be sampled from close to 
    Cardamine accessions into the MySQL At_variant table.
    It assumes that the variants are stored in gzip archives of sdi variant tables '''

import MySQLdb
import gzip
from os import listdir
from os.path import isfile, join
import ext
import re

## for quick and dirty paralellization safe multiple copies of this script with different 'do' lines uncommented
## and submit as several jobs to the LSF. Take care that the range does not exceed the actual number of accessions  
do = range(0,4) 
#do = range(4,8) 
#do = range(8,12) 
#do = range(12,16) 
#do = range(16,20) 
#do = range(20,24) 
#do = range(24,28) 
#do = range(28,32) 
#do = range(32,36) 
#do = range(36,40) 
#do = range(40,44) 
#do = range(44,48) 
#do = range(48,52) 

db = MySQLdb.connect(host="mysql2.mpipz.mpg.de", user="pieper", passwd=ext.sentry, db="pieper_chpoly")
cur = db.cursor()

gz_path = "/biodata/dep_tsiantis/common/ath_accessions/" # location of the gzip files
curpath = "/biodata/dep_tsiantis/common/Bjorn/At_1001_database/" # current path (not used a.t.m.)

with open(gz_path + 'list.txt', 'r') as acc: # list.txt contains the accession names, codes, and some more info
  accessions = [[x.strip('\n') for x in y.split('\t')] for y in acc ]

gz_files = [ x for x in listdir(gz_path) if re.search('\.gz$', x) and isfile(join(gz_path, x)) and x.strip('.sdi.gz') in [accessions[y][0] for y in do] ]

col = ['allele', 'chromosome', 'position', 'length', 'reference', 'consensus', 'quality', 'percentage', 'phred', 'ignore_this']

if len(gz_files) > 0:
  for strain in gz_files:
    straincode = [x for x in accessions if x[0] == strain.strip('.sdi.gz')][0][1]
    with gzip.open(gz_path + strain, 'r') as SDI:
      count = 0
      for sdi in SDI:
        temp = [ x.strip('\n') for x in sdi.split('\t') ]
        stmt = "INSERT INTO At_variants (`" + '`, `'.join(col[0:len(temp)+1]) + "`) VALUES (%s)" % ("'" + "', '".join([straincode] + temp) + "'")
        cur.execute(stmt)
        count = count+1
        if count == 25: # commit every 25 records so that the progress can be followed from the MySQL client.
          db.commit()
          count = 0

