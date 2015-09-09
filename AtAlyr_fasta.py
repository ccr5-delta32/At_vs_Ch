#!/usr/bin/python

''' This will produce a FASTA alignment for A. lyrata at all polymorphic sites of A. thaliana 
    that were put in the SNP tables by the make_At_SNP_close2Ch_c<n> script '''

import MySQLdb
import ext

dbcon = MySQLdb.connect(host='mysql2.mpipz.mpg.de', user='pieper', passwd=ext.sentry, db='pieper_chpoly')
cur = dbcon.cursor()

for CHR in range(1,6):

  path = '/biodata/dep_tsiantis/common/Bjorn/At_1001_database/At_SNP_tables/'

  with open(path + 'Chr' + str(CHR) + '_At_close2_Ch_SNP_raw', 'r') as SNPs:
    header = [ x.strip('\n') for x in SNPs.readline().split('\t') ]
    data = [[x.strip('\n') for x in y.split('\t')] for y in SNPs ]

  strains = [ x.strip('\n') for x in header if x not in ['chromosome', 'position'] ] + ['A_lyrata']
  current = [[] for x in strains]
  positions = []

  for x in range(1,len(data)):
    
    test = ''.join(data[x][2:len(data[0])])
    if len(test) == len(strains)-1 and test.count('A') + test.count('T') + test.count('G') + test.count('C') == len(strains)-1:
      positions.append(data[x][1])
      for y in range(2,len(data[0])):
        current[strains.index(strains[y-2])].append(data[x][header.index(strains[y-2])])

      stmt = "select * from genmat_AtAlyr where chromosome='Chr" + str(CHR) + "' and position=" + str(data[x][1])
      cur.execute(stmt)
      result = cur.fetchall()

      if len(result) == 0 or result[0][4] not in ['A', 'G', 'C', 'T']:
        current[len(current)-1].append('N')
      else:
        current[len(current)-1].append(result[0][4])

  with open('positions_At_C' + str(CHR) + '_fasta', 'wb') as output:
    for x in positions:
      output.write(x)
      output.write('\n')
    del(positions)

  with open('At_C' + str(CHR) + '_fasta.fa', 'wb') as output:
    for x in strains:
      output.write('>' + x + '\n')
      output.write(''.join(current[strains.index(x)]) + '\n')
    del(current)
