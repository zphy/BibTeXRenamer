#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 20:15:09 2018

@author: hyzhou

Go through .bib reference file and only keep citations that were used
"""
fdn = './'
fnin = 'main.aux'
fnbib = 'main.bib' # already cleaned by me
fnout = 'clean_main.bib'
dataout = ''
goodkeys = []
with open(fnin,'r',encoding='utf-8') as f1:
    data=f1.read().replace('\n', '')
    pos = 0
    pos2 = 0
    datalen = len(data)
    while pos < datalen:
        while pos < datalen and data[pos] != '\\':
            pos = pos + 1
        if data[pos+1:pos+9] != 'citation':
            pos = pos + 9
            continue
        pos2 = pos + 9
        openBr = 1
        while openBr >= 1:
            pos2 = pos2 + 1
            if data[pos2] == '{':
                openBr = openBr + 1
            elif data[pos2] == '}':
                openBr = openBr - 1
        curr_data = data[pos+10:pos2]
        if curr_data[0:4]  == 'lier':
            1
        split_data = curr_data.split(',')
        for item in split_data:
            if item not in goodkeys:
                goodkeys.append(item)
        pos = pos2
with open(fnbib,'r',encoding='utf-8') as f2:
    data=f2.read().replace('\n', '')
    pos = 0
    pos2 = 0
    datalen = len(data)
    dataout = ''
    while pos < datalen:
        while pos < datalen and data[pos] != '@':
            pos = pos + 1
        pos2 = pos + 1
        while pos2 < datalen and data[pos2] != '{':
            pos2 = pos2 + 1
        pos3 = pos2
        while pos2 < datalen and data[pos2] != ',':
            pos2 = pos2 + 1
        curr_key = data[pos3+1:pos2].lower()
        if curr_key in goodkeys:
            openBr = 1
            while openBr >= 1:
                pos2 = pos2 + 1
                if data[pos2] == '{':
                    openBr = openBr + 1
                elif data[pos2] == '}':
                    openBr = openBr - 1
            curr_data = data[pos:pos2]
            dataout = dataout + curr_data + '}' + '\n'
        pos = pos2
with open(fdn+fnout+'.bib','w',encoding='utf-8') as fout:
    fout.write(dataout)
print('Number of keys processed: ' + str(len(goodkeys)))
        
    #p = re.search(r'\citation\{.+\}',curr_data)
    