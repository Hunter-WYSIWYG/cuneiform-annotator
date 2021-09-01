import requests
from conllu import parse
from conllu import parse_incr
import json
import csv
import os
import sys

positionmap={"o.":"@obverse","r.":"@reverse"}

positionmappings={"@obverse":"front_","@revers":"back_","@reverse":"back_","@left":"left_","@right":"right_","@top":"top_","@bottom":"bottom_"}

with open('js/hs2CDLI.js', 'r') as myfile:
    data=myfile.read()
# parse file
hs2CDLI = json.loads(data.replace("var hs2CDLI=",""))
def downloadCONLL():
    for hsnumber in hs2CDLI:
        response = requests.get("https://raw.githubusercontent.com/cdli-gh/mtaac_cdli_ur3_corpus/master/ur3_corpus_data/annotated/pos/"+str(hs2CDLI[hsnumber][0:4])+"/"+str(hs2CDLI[hsnumber])+".conll", stream=True)
        if response.status_code == 200:
            print("https://raw.githubusercontent.com/cdli-gh/mtaac_cdli_ur3_corpus/master/ur3_corpus_data/annotated/pos/"+str(hs2CDLI[hsnumber][0:4])+"/"+str(hs2CDLI[hsnumber])+".conll")
            with open('conll/'+hs2CDLI[hsnumber]+".conll", 'w') as out_file:
                out_file.write(response.text)
            
def processCONLL():
    posresult={}
    posresultchars={}
    CDLI2hs = {v: k for k, v in hs2CDLI.items()}
    for filename in os.listdir("conll"):
        print(filename)
        possid=filename.replace(".conll","")
        if possid.replace(".conll","") in CDLI2hs:
           posid=CDLI2hs[possid.replace(".conll","")]
        else:
            posid=possid
        posresult[posid]={}
        posresultchars[posid]={}
        try:
            data_file = list(csv.reader(open("conll/"+filename,"r",encoding="utf-8"), delimiter='\t'))
            #linecounter=1
            skipfirst2=0
            lastline=""
            for line in data_file:
                skipfirst2+=1
                if skipfirst2>2:
                    #linecounter+=1
                    word=line[1]
                    translation=line[2]
                    postag=line[3]
                    position=line[0]
                    posprefix=position[0:2]
                    linecounter=position.split(".")[1]
                    if linecounter!=lastline:
                        charcounter=1
                        lastline=linecounter
                    print(position+" "+word+" "+translation)
                    if not positionmap[posprefix] in posresult[posid]:
                        posresult[posid][positionmap[posprefix]]={}
                        posresultchars[posid][positionmap[posprefix]]={}
                        #linecounter=1
                    #posresultchars[posid][positionmap[posprefix]]=[]
                    posresult[posid][positionmap[posprefix]][position]={"word":word,"pos":translation,"charlist":{}}
                    if "-" in word:
                        for char in word.split("-"):
                            posresult[posid][positionmap[posprefix]][position]["charlist"][str(linecounter)+"_"+str(charcounter)]=char
                            posresultchars[posid][positionmap[posprefix]][positionmappings[positionmap[posprefix]]+str(linecounter)+"_"+str(charcounter)]={"word":word,"pos":postag,"translation":translation.replace(word,"").replace("[","").replace("]",""),"char":char}
                            charcounter+=1
                            print("Char: "+str(char)+" "+str(linecounter)+"_"+str(charcounter)) 
                    else:
                        posresult[posid][positionmap[posprefix]][position]["charlist"][str(linecounter)+"_"+str(charcounter)]=word
                        posresultchars[posid][positionmap[posprefix]][positionmappings[positionmap[posprefix]]+str(linecounter)+"_"+str(charcounter)]={"word":word,"pos":postag,"translation":translation.replace(word,"").replace("[","").replace("]",""),"char":word}
                        charcounter+=1
            print(data_file)     
        except:
            print("Error: "+str(posid))
            e = sys.exc_info()[0]
            print(e)
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])
    f = open("js/character_postags.js", "w")
    f.write("var character_postags="+json.dumps(posresult,indent=2))
    f.close() 
    f = open("js/character_postags2.js", "w")
    f.write("var character_postags="+json.dumps(posresultchars,indent=2))
    f.close()       
processCONLL()