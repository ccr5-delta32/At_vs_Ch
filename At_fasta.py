#!/usr/bin/python

''' This will produce a FASTA alignment of all polymorphic sites that were put in the SNP tables
    by the make_At_SNP_close2Ch_c<n> script '''

for CHR in range(1,6):

  path = '/biodata/dep_tsiantis/common/Bjorn/At_1001_database/At_SNP_tables/'

  with open(path + 'Chr' + str(CHR) + '_At_close2_Ch_SNP_raw', 'r') as SNPs:
    header = [ x.strip('\n') for x in SNPs.readline().split('\t') ]
    data = [[x.strip('\n') for x in y.split('\t')] for y in SNPs ]

  strains = [ x.strip('\n') for x in header if x not in ['chromosome', 'position'] ]
  current = [[] for x in strains]
  positions = []

  for x in range(1,len(data)):
    
    test = ''.join(data[x][2:len(data[0])])
    if len(test) == len(strains) and test.count('A') + test.count('T') + test.count('G') + test.count('C') == len(strains):
      positions.append(data[x][1])
      for y in range(2,len(data[0])):
        current[strains.index(strains[y-2])].append(data[x][header.index(strains[y-2])])

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
