import os
import json
import re

mappings={"@obvers":"03_front","@obverse":"03_front","@revers":"06_back","@reverse":"06_back","@left":"02_left","@right":"04_right","@top":"01_top","@bottom":"05_bottom","@seal":"seal","@colophon":"colophon"}

with open('hs_transliterations.json', 'r') as myfile:
    data=myfile.read()

def calculateTranslitCount():
    # parse file
    obj = json.loads(data.replace("var transliterations=",""))
    result={}
    totalchars=0
    for tabletid in obj:
        for line in obj[tabletid].split("\n"):
            #print(line)
            if line.startswith("@Tablet") or line.strip().startswith("$") or line.strip().startswith("#") or line.strip().startswith("&"):
                continue
            if line.startswith("@"):
                curside=line[0:line.find(" ")]
                if curside in mappings: 
                    curid=str(tabletid)+"_"+str(mappings[curside]+".png.json")
                    print("Curside: "+str(curside))
                    result[curid]=0
                continue
            if not re.search('^\s*[0-9]+\'\.',line) and not re.search('^\s*[0-9]+\.',line):
                continue
            for word in line.split(" "):
                word=word.replace("{","-").replace("}","-")
                if word=="" or re.search('^\s*[0-9]+\'\.',word) or re.search('^\s*[0-9]+\.',word) or word=="[x]" or word=="x" or word=="[...]" or "[" in word or "]" in word or "<" in word or ">" in word:
                    continue
                #print("Word: "+str(word))
                for char in word.split("-"):
                    if curid in result and char!="" and char!="column" and char!="..." and char!="!" and char!="?" and char!="...]" and char!="/" and char!="=" and char!="[..." and char!="[...]" and char!="x":
                        print("Char: "+str(char))
                        result[curid]+=1
                        totalchars+=1
    print(totalchars)
    jsonString = json.dumps(result, indent=2)
    jsonFile = open("js/translitcount.js", "w")
    jsonFile.write("var translitcount="+jsonString)
    jsonFile.close()
    
    
def processWebAnnotation(filepath,charmapping):
    print(charmapping)
    print(filepath)
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as myfile:
        data=myfile.read()
        jsondata=json.loads(data)
    charindexpurpose="Charindex"
    wordindexpurpose="Wordindex"
    changed=False
    for annotation in jsondata:
        translit=""
        wordindexobject=None
        curcharindex=-1
        line=-1
        tagging=""
        for annoobj in jsondata[annotation]["body"]:
            if annoobj["purpose"]==charindexpurpose:
                curcharindex=annoobj["value"]
                print("Curcharindex: "+str(curcharindex)+" "+str("c"+str(curcharindex) in charmapping))
            if annoobj["purpose"]==wordindexpurpose:
                curwordindex=annoobj["value"]
                print("Curwordindex: "+str(curwordindex))
                wordindexobject=annoobj
        if curcharindex!=-1 and "c"+str(curcharindex) in charmapping:
            print("Adding wordindex: "+str(charmapping["c"+str(curcharindex)]))
            if wordindexobject!=None:
                jsondata[annotation]["body"].append({"type":"TextualBody","purpose":"Wordindex","value":charmapping["c"+str(curcharindex)]})
                print(json.dumps(jsondata[annotation]["body"],indent=2))
            elif wordindexobject!=None:
                wordindexobject["value"]=charmapping["c"+str(curcharindex)]
            changed=True
    if changed:
        with open(filepath, 'w') as myfile2:
            myfile2.write(json.dumps(jsondata,indent=2))

def enrichWordPositions():
    # parse file
    obj = json.loads(data.replace("var transliterations=",""))
    result={}
    totalchars=0
    for tabletid in obj:
        result[tabletid]={}
        lineindex=1
        charmapping={}
        for line in obj[tabletid].split("\n"):
            wordindex=1
            charindex=0
            if line.startswith("@Tablet") or line.strip().startswith("$") or line.strip().startswith("#") or line.strip().startswith("&"):
                continue
            if line.startswith("@"):
                curside=line[0:line.find(" ")]
                if curside in mappings: 
                    curid=str(mappings[curside])
                    #print("Curside: "+str(curside))
                    processWebAnnotation("result/"+str(tabletid)+"_"+curid+".png.json",charmapping)
                    result[tabletid][curid]={}
                    charmapping={}
                    lineindex=0
                continue
            if not re.search('^\s*[0-9]+\'\.',line) and not re.search('^\s*[0-9]+\.',line):
                continue
            #print(line)
            lineindex+=1
            try:
                result[tabletid][curid][lineindex]={}
                for word in line.split(" "):
                    word=word.replace("{","-").replace("}","-")
                    if word=="" or re.search('^\s*[0-9]+\'\.',word) or re.search('^\s*[0-9]+\.',word) or word=="[x]" or word=="x" or word=="[...]" or "[" in word or "]" in word or "<" in word or ">" in word:
                        continue
                    result[tabletid][curid][lineindex][wordindex]={"word":word,"chars":[]}
                    for char in word.split("-"):
                        if char!="" and char!="column" and char!="..." and char!="!" and char!="?" and char!="...]" and char!="/" and char!="=" and char!="[..." and char!="[...]" and char!="x":
                            #print("Char: "+str(char))
                            charindex+=1
                            #print(result[tabletid][curid][lineindex])
                            result[tabletid][curid][lineindex][wordindex]["chars"].append(charindex)
                            charmapping["c"+str(charindex)]=wordindex
                    wordindex+=1
            except:
                print("except")
    print(totalchars)
    jsonString = json.dumps(result, indent=2)
    jsonFile = open("js/wordindex.js", "w")
    jsonFile.write("var wordindex="+jsonString)
    jsonFile.close()    

calculateTranslitCount()
enrichWordPositions()
