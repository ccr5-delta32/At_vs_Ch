#!/usr/bin/python

""" April 2015.
    This script will find Arabidopisis accessions that were sampled spatially most closely to the 
    provided Cardamine accessions. To prevent the same Arabidopsis accession to be selected more
    than once it is deleted from the set after being selected. """


import heapq

spath = '/biodata/dep_tsiantis/common/Bjorn/1001genomes/'
lpath = '/home/bpuser/server/biodata/common/Bjorn/1001genomes/'

location = 'local' # 'local' or 'server'

if    location == 'local': path = lpath
elif  location == 'server': path = spath
else: exit('unknown location specified')

with open(path + '1001_80-genomes.txt', 'r') as At80:
    at80coor = [[x.strip('\n') for x in line.split('\t')] for line in At80][1:]
    at80coor = [x for x in at80coor if x != ['']]
with open(path + 'Ch-coordinates.tsv', 'r') as ch:
    chcoor = [[x.strip('\n') for x in line.split('\t')] for line in ch][1:]
    chcoor = [x for x in chcoor if x != ['']]
with open(path + '1001_genomes_final_set', 'r') as at:
    atcoor = [[x.strip('\n') for x in line.split('\t')] for line in at][1:]
    atcoor = [x for x in atcoor if x[4] != '(null)' and x[5] != '(null)']

at_testlist = atcoor

if at_testlist == atcoor:
    lat_indx = 4 
    lon_indx = 5 
elif at_testlist == at80coor:
    lat_indx = 3 
    lon_indx = 4 

result =[]
used = []
check = [0, len(at_testlist), [-1]] 

for line in chcoor:
    diflat = [max(float(x[lat_indx]), float(line[2])) - min(float(x[lat_indx]), float(line[2])) for x in at_testlist]
    diflon = [max(float(x[lon_indx]), float(line[3])) - min(float(x[lon_indx]), float(line[3])) for x in at_testlist]
    difdif = [diflat[x] + diflon[x] for x in range(len(diflat))]
    selected = difdif.index(sorted(heapq.nsmallest(check[1], set(difdif)))[check[0]])
    result.append(at_testlist[selected])
    del at_testlist[selected]


for x in range(len(result)):
    print 'Cardamine  [ ' + str(x) + ' ] : ' + ', '.join(chcoor[x])
    print 'Arabidopsis[ ' + str(x) + ' ] : ' + ', '.join(result[x]) #[y] for y in [3,9,5,6]])

with open(path + 'At_closest_to_Ch_final', 'wb') as out:
    for x in range(len(result)):
 #       out.write('Cardamine  [ ' + str(x) + ' ] : ' + '\t'.join(chcoor[x]) + '\n')
        out.write('Arabidopsis[ ' + str(x) + ' ] : ' + '\t'.join(result[x]) + '\n')

