#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 14:17:54 2018

@author: hyzhou

Convert Mendeley-exported citation files into desired format
"""
import re, sys, os
fdn = './'
#print(sys.argv[1])
fn_all = ['My Collection.bib']#[str(sys.argv[1])]#
fnout = 'main'
fntex = 'ReferenceExport/ref.tex' # generate tex file
dataout = ''
for fn in fn_all:
    with open(fdn+fn,'r',encoding='utf-8') as fin:
        data=fin.read().replace('\n', '')
        
    # according to https://stackoverflow.com/questions/524548/regular-expression-to-detect-semi-colon-terminated-c-for-while-loops/524624#524624
    # it seems like regular expressions are the wrong tool to do the matching, so
    # I'm just going to implement my own    
    #p = re.search(r"@article\{.*\}", data)
    #p = re.search(r'\{([^\}]+)\}', data)
    #print(p.group(0))
    #matches = re.findall(r'@article\{([^\}]+)\}', data, re.DOTALL)
    #print(matches[0])
    
    # identify text block
    pos = 0
    pos2 = 0
    datalen = len(data)
    key_list = []
    nonart_list = []
    while pos < datalen:
        while pos < datalen and data[pos] != '@':
            pos = pos + 1
        # right now we only specify a consistent notation for articles   
        if data[pos+1:pos+8] == 'article':
            openBr = 1
            pos2 = pos+9
            while openBr >= 1:
                pos2 = pos2 + 1
                if data[pos2] == '{':
                    openBr = openBr + 1
                elif data[pos2] == '}':
                    openBr = openBr - 1
            curr_data = data[pos+9:pos2]
            split_data = curr_data.split(',')
            for j in range(len(split_data)):
                if split_data[j][0:8]=='abstract':
                    k = j
                    while k < len(split_data):
                        if split_data[k].count('}')-split_data[k].count('{')>0 or \
                            (split_data[k].count('{')==1 and split_data[k].count('}')==1 and k==j):
                            break
                        k = k+1
                    split_data = split_data[0:j]+split_data[k+1:]
                    break
            for j in range(len(split_data)):
                if split_data[j][0:4]=='file':
                    k = j
                    while k < len(split_data):
                        if split_data[k].count('}')-split_data[k].count('{')>0 or \
                            (split_data[k].count('}')==split_data[k].count('{') and k == j):
                            break
                        k = k+1
                    split_data = split_data[0:j]+split_data[k+1:]
                    break
            for j in range(len(split_data)):
                if split_data[j][0:6]=='eprint':
                    k = j
                    while k < len(split_data):
                        if split_data[k].count('}')-split_data[k].count('{')>0 or \
                            (split_data[k].count('}')==split_data[k].count('{') and k == j):
                            break
                        k = k+1
                    split_data = split_data[0:j]+split_data[k+1:]
                    break
            for j in range(len(split_data)):
                if split_data[j][0:8]=='keywords':
                    k = j
                    while k < len(split_data):
                        if split_data[k].count('}')-split_data[k].count('{')>0 or \
                            (split_data[k].count('}')==split_data[k].count('{') and k == j):
                            break
                        k = k+1
                    split_data = split_data[0:j]+split_data[k+1:]
                    break
            for j in range(len(split_data)):
                if split_data[j][0:8]=='language':
                    k = j
                    while k < len(split_data):
                        if split_data[k].count('}')-split_data[k].count('{')>0 or \
                            (split_data[k].count('}')==split_data[k].count('{') and k == j):
                            break
                        k = k+1
                    split_data = split_data[0:j]+split_data[k+1:]
                    break
            jflag = 0
            for j in range(len(split_data)):
                if split_data[j][0:7]=='journal':
                    jflag = 1
            if jflag == 0:
                # no journal specified, check if it is an arXiv article
                for j in range(len(split_data)):
                    if split_data[j][0:7]=='arxivId':
                        new_str = 'journal = {arXiv preprint arXiv:' + split_data[j][11:-1] + '}'
                        split_data = split_data + [new_str]
            # now perform processing and find desired information
            # CR-HZ: maybe we need to add additional checks as to whether the fields exist
            temp = re.search(r'year\s*=\s*\{.+\}',curr_data)
            try:
                temp = re.search(r'\{.+\}',temp.group(0))
            except:
                1
            year = temp.group(0)[1:-1]
            temp = re.search(r'author\s*=\s*\{.+\}',curr_data)
            try:
                temp = re.search(r'\{.+\}',temp.group(0))
            except:
                1
            authors = temp.group(0)[1:-1]
            author1 = re.split((', |- |\s'),authors)[0].lower()
            # remove weird characters
            if author1[0] == '{':
                author1 = author1[1:]
            if '{' in author1:
                try:
                    char1 = re.search(r'\{.+\}',author1).group(0)
                    char1 = re.search(r'\{.\}',char1).group(0)
                    ind1 = author1.find('{')
                    ind2 = author1.rfind('}')
                    author1 = author1[0:ind1]+char1[1]+author1[ind2+1:]
                except:
                    1
            #if author1[2:5] == 'alv':
            #    author1 = author1[2:]   # specifically for alvarez
            author1 = author1.replace("{","")
            author1 = author1.replace("}","")
            author1 = author1.replace("\\","")
            author1 = author1.replace("'","")
            
            temp = re.search(r'title\s*=\s*\{\{.+\}\}',curr_data)
            temp = re.search(r'\{\{.+\}\}',temp.group(0))
            title = temp.group(0)[2:-2]
            title1 = re.split('[^a-zA-Z]', title)[0].lower()
            if title1 == 'the' or title1 == 'a' or title1 == 'an' or title1 == 'at':
                title1 = re.split('[^a-zA-Z]', title)[1].lower()
                if title1 == '':
                    title1 = re.split('[^a-zA-Z]', title)[2].lower()
            newkey = author1+year+title1
            if newkey in key_list:
                newkey = newkey + '1'
            while newkey in key_list:
                newkey = newkey[0:-1] + str(int(newkey[-1])+1)
            #print(split_data[0]+' -> '+newkey)
            key_list.append(newkey)
            dataout = dataout + '@article{' + newkey + ',' + ','.join(split_data[1:]) + '}\n'
            pos = pos2
        else:
            while pos2 < datalen and data[pos2] != '{':
                pos2 = pos2 + 1
            post = pos2
            if post < datalen:
                openBr = 1
                while openBr >= 1:
                    pos2 = pos2 + 1
                    try:
                        if data[pos2] == '{':
                            openBr = openBr + 1
                        elif data[pos2] == '}':
                            openBr = openBr - 1
                    except:
                        1
                curr_data = data[post+1:pos2]
                split_data = curr_data.split(',')
                if split_data[0][0:4]=='wade':
                    1
                for j in range(len(split_data)):
                    if split_data[j][0:8]=='abstract':
                        k = j
                        while k < len(split_data):
                            if split_data[k].count('}')-split_data[k].count('{')>0 or \
                                (split_data[k].count('}')==split_data[k].count('{') and k == j):
                                break
                            k = k+1
                        split_data = split_data[0:j]+split_data[k+1:]
                        break
                for j in range(len(split_data)):
                    if split_data[j][0:4]=='file':
                        k = j
                        while k < len(split_data):
                            if split_data[k].count('}')-split_data[k].count('{')>0 or \
                                (split_data[k].count('}')==split_data[k].count('{') and k == j):
                                break
                            k = k+1
                        split_data = split_data[0:j]+split_data[k+1:]
                        break
                for j in range(len(split_data)):
                    if split_data[j][0:8]=='keywords':
                        k = j
                        while k < len(split_data):
                            if split_data[k].count('}')-split_data[k].count('{')>0 or \
                                (split_data[k].count('}')==split_data[k].count('{') and k == j):
                                break
                            k = k+1
                        split_data = split_data[0:j]+split_data[k+1:]
                        break
                dataout = dataout + data[pos:post+1] + ','.join(split_data) + '}\n'
                pos = pos2
                nonart_list.append(split_data[0])
                #pos = pos + 1
with open(fntex,'w') as fn:
    fn.write('\documentclass[onecolumn,superscriptaddress,prl]{revtex4-2}\n \\begin{document}\n'+ \
             '\\cite{' + ','.join(key_list) + ',' + ','.join(nonart_list[0:2]) + '}\n'\
             ' \\bibliography{main}\n \end{document}')  
print(str(len(key_list))+' articles processed!')
print(str(len(nonart_list))+' items are not articles!')
#print(key_list)
#print(nonart_list)
dataout = dataout + '@misc{SM, note={See Supplemental Material}}\n' + '@misc{otherpaper, note={See Accompanying Paper}}'
with open(fdn+fnout+'.bib','w',encoding='utf-8') as fout:
    fout.write(dataout)
os.system('cp main.bib ReferenceExport/main.bib')
os.chdir('ReferenceExport')
os.system('latex ref > /dev/null')   # prevent printing a bunch of stuff on the screen
os.system('latex ref > /dev/null')
print('First compilation done!')
os.system('bibtex ref > /dev/null')
print('Bibtex compilation done!')
os.system('pdflatex ref > /dev/null')
print('Second compilation done!')
os.system('pdflatex ref > /dev/null')
print('Final compilation done!')
