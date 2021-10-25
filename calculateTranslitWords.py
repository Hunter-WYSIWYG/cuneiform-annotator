import os
import json
import sys
import re

mappings={"@obvers":"03_front","@obverse":"03_front","@revers":"06_back","@reverse":"06_back","@left":"02_left","@right":"04_right","@top":"01_top","@bottom":"05_bottom","@seal":"seal","@colophon":"colophon"}

curnamespace="http://purl.org/cuneiform/"

mlVocabulary={"Broken":curnamespace+"Broken","Column":curnamespace+"Column","RelCharindex":curnamespace+"RelativeCharacterIndex","Charindex":curnamespace+"CharacterIndex","Wordindex":curnamespace+"WordIndex","Transliteration":curnamespace+"Transliteration","CharacterName":curnamespace+"CharacterName","PaleoCode":curnamespace+"PaleoCode","Line":curnamespace+"LineIndex","Character":curnamespace+"Character","Line":curnamespace+"Line","Image":curnamespace+"Image","Word":curnamespace+"Word","Seal":curnamespace+"Seal","Phrase":curnamespace+"Phrase","Erased":curnamespace+"Erased","StrikeOut":curnamespace+"StrikeOut","Wordstart":curnamespace+"Wordstart","Wordend":curnamespace+"Wordend","InWord":curnamespace+"InWord","UnknownIfWord":curnamespace+"UnknownIfWord"}

licenseOfImages="https://creativecommons.org/licenses/by-sa/4.0/"

creatorstatement={
    "id": "https://orcid.org/0000-0002-9499-5840",
    "type": "Person",
    "name": "Timo Homburg",
    "nickname": "situx",
  }

softwarecreatorstatement= {
    "id": "https://github.com/recogito/annotorious-openseadragon",
    "type": "Software",
    "name": "Annotorious-OpenSeadragon 1.5.6",
    "homepage": "https://github.com/recogito/annotorious-openseadragon"
}

withcredits=True

with open('js/transliterations.js', 'r') as myfile:
    data=myfile.read()

def calculateTranslitCount():
    # parse file
    obj = json.loads(data.replace("var transliterations=",""))
    result={}
    totalchars=0
    seal=False
    for tabletid in obj:
        for line in obj[tabletid].split("\n"):
            #print(line)
            if line.startswith("@Tablet") or line.strip().startswith("$") or line.strip().startswith("#") or line.strip().startswith("&"):
                continue
            if line.startswith("@seal") or line.startswith("seal") or line.startswith("@envelope") or line.startswith("@edge") or line.startswith("edge"):
                seal=True
            if line.startswith("@"):
                seal=False
                curside=line[0:line.find(" ")]
                if curside in mappings: 
                    curid=str(tabletid)+"_"+str(mappings[curside]+".png.json")
                    print("Curside: "+str(tabletid)+"_"+str(curside))
                    result[curid]=0
                continue
            if seal or not re.search('^\s*[0-9]+\'\.',line) and not re.search('^\s*[0-9]+\.',line):
                continue
            for word in line.split(" "):
                word=word.replace("{","-").replace("}","-")
                if word=="" or re.search('^\s*[0-9]+\'\.',word) or re.search('^\s*[0-9]+\.',word) or word=="[x]" or word=="x" or word=="[...]" or "[" in word or "]" in word or "<" in word or ">" in word:
                    continue
                #print("Word: "+str(word))
                for char in word.split("-"):
                    if curid in result and char!="" and char!="column" and char!="..." and char!="!" and char!="?" and char!="...]" and char!="/" and char!="=" and char!="[..." and char!="[...]" and char!="x":
                        #print("Char: "+str(char))
                        result[curid]+=1
                        totalchars+=1
    print(totalchars)
    jsonString = json.dumps(result, indent=2)
    jsonFile = open("js/translitcount.js", "w")
    jsonFile.write("var translitcount="+jsonString)
    jsonFile.close()
    
    
def processWebAnnotation(filepath,charmapping,curline):
    if not os.path.exists(filepath) or len(charmapping)==0:
        return
    print(charmapping)
    print(filepath)
    with open(filepath, 'r') as myfile:
        data=myfile.read()
    jsondata=json.loads(data)
    translitpurpose="Transliteration"
    charindexpurpose="Charindex"
    relcharindexpurpose="RelCharindex"
    linepurpose="Line"
    wordindexpurpose="Wordindex"
    changed=False
    tempdimensions={}
    for annotation in jsondata:
        tempdimensions={}
        translit=""
        wordindexobject=None
        relcharindexobject=None
        curcharindex=-1
        line=-1
        tagging=""
        if withcredits and not "creator" in jsondata[annotation]:
            jsondata[annotation]["creator"]=creatorstatement
            changed=True
        if withcredits and not "generator" in jsondata[annotation]:
            jsondata[annotation]["generator"]=softwarecreatorstatement
            changed=True
        if not "rights" in jsondata[annotation]:
            jsondata[annotation]["rights"]="https://creativecommons.org/publicdomain/zero/1.0/"
            changed=True
        if "target" in jsondata[annotation] and not "rights" in jsondata[annotation]["target"]:
            jsondata[annotation]["target"]["rights"]=licenseOfImages
            changed=True
        for annoobj in jsondata[annotation]["body"]:
            if annoobj["purpose"]==charindexpurpose:
                curcharindex=annoobj["value"]
                #print("Curcharindex: "+str(curcharindex)+" "+str("c"+str(curcharindex) in charmapping))
            if annoobj["purpose"]==wordindexpurpose:
                curwordindex=annoobj["value"]
                #print("Curwordindex: "+str(curwordindex))
                wordindexobject=annoobj
            if annoobj["purpose"]==translitpurpose:
                curchar=annoobj["value"]
            if annoobj["purpose"]==linepurpose:
                line=annoobj["value"]   
            if annoobj["purpose"]==relcharindexpurpose:
                relcharindex=annoobj["value"]
                #print("Relcharindex: "+str(relcharindex))
                relcharindexobject=annoobj
            if annoobj["purpose"] in mlVocabulary and not "source" in annoobj and annoobj["purpose"] in mlVocabulary:
                annoobj["source"]=mlVocabulary[annoobj["purpose"]]
                changed=True
            if annoobj["purpose"]=="tagging" and not "source" in annoobj and annoobj["value"] in mlVocabulary:
                annoobj["source"]=mlVocabulary[annoobj["value"]]
                changed=True
            if "dimensions" in annoobj:
                tempdimensions=annoobj["dimensions"]
                jsondata[annotation]["target"]["dimensions"]=annoobj["dimensions"]
                del annoobj["dimensions"]
                changed=True
            #if annoobj["purpose"]=="tagging" and annoobj["value"]=="Character":
            #annoobj["purpose"]="classifying"
        #if "HS_1113" in filepath:
        #    print("Line: "+str(line)+" - "+str(curline)+" "+str(charmapping["c"+str(curcharindex)]["char"])+" "+curchar)
        if curcharindex!=-1 and line!=-1 and line==curline and "c"+str(curcharindex) in charmapping:
            print("Adding wordindex: "+str(charmapping["c"+str(curcharindex)]))
            if wordindexobject==None:
                jsondata[annotation]["body"].append({"type":"TextualBody","purpose":"Wordindex","value":charmapping["c"+str(curcharindex)]["wordindex"]})
                jsondata[annotation]["body"].append({"type":"TextualBody","purpose":"RelCharindex","value":charmapping["c"+str(curcharindex)]["relcharindex"]})
                #print(json.dumps(jsondata[annotation]["body"],indent=2))
            elif wordindexobject!=None:
                wordindexobject["value"]=charmapping["c"+str(curcharindex)]["wordindex"]
                if relcharindexobject!=None:
                    relcharindexobject["value"]=charmapping["c"+str(curcharindex)]["relcharindex"]
            changed=True
    print("Has changed? "+str(changed))
    #print(jsondata[annotation]["body"])
    if changed:
        with open(filepath, 'w') as myfile2:
            myfile2.write(json.dumps(jsondata,indent=2))

def enrichWordPositions():
    # parse file
    obj = json.loads(data.replace("var transliterations=",""))
    result={}
    totalchars=0
    curid=None
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
                    result[tabletid][curid]={}
                    charmapping={}
                    lineindex=0
                continue
            if not re.search('^\s*[0-9]+\'\.',line) and not re.search('^\s*[0-9]+\.',line):
                continue
            #print(line)
            try:
                result[tabletid][curid][lineindex]={}
                for word in line.split(" "):
                    word=word.replace("{","-").replace("}","-")
                    if word=="" or re.search('^\s*[0-9]+\'\.',word) or re.search('^\s*[0-9]+\.',word) or word=="[x]" or word=="x" or word=="[...]" or "[" in word or "]" in word or "<" in word or ">" in word:
                        continue
                    result[tabletid][curid][lineindex][wordindex]={"word":word,"chars":[]}
                    relcharcounter=0
                    if "-" in word:
                        for char in word.split("-"):
                            if char!="" and char!="column" and char!="..." and char!="!" and char!="?" and char!="...]" and char!="/" and char!="=" and char!="[..." and char!="[...]" and char!="x":
                                #print("Char: "+str(char))
                                charindex+=1
                                #print(result[tabletid][curid][lineindex])
                                result[tabletid][curid][lineindex][wordindex]["chars"].append(charindex)
                                charmapping["c"+str(charindex)]={"wordindex":str(wordindex)+"", "relcharindex":str(relcharcounter)+"","char":char}
                                relcharcounter+=1
                    else:
                        charindex+=1
                        result[tabletid][curid][lineindex][wordindex]["chars"].append(charindex)
                        charmapping["c"+str(charindex)]={"wordindex":str(wordindex)+"", "relcharindex":str(relcharcounter)+"","char":word}
                    wordindex+=1
            except:
                e = sys.exc_info()[0]
                print(e)
                print(sys.exc_info()[1])
                print(sys.exc_info()[2])
            if curid!=None:
                processWebAnnotation("result/"+str(tabletid)+"_"+curid+".png.json",charmapping,str(lineindex))
            lineindex+=1
    print(totalchars)
    jsonString = json.dumps(result, indent=2)
    jsonFile = open("js/wordindex.js", "w")
    jsonFile.write("var wordindex="+jsonString)
    jsonFile.close()    

calculateTranslitCount()
enrichWordPositions()
