import os
import json
import re

mappings={"@obverse":"03_front","@revers":"06_back","@reverse":"06_back","@left":"02_left","@right":"04_right","@top":"01_top","@bottom":"05_bottom"}

with open('hs_transliterations.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data.replace("var transliterations=",""))
result={}
for tabletid in obj:
    for line in obj[tabletid].split("\n"):
        #print(line)
        if line.startswith("@Tablet") or line.startswith("$") or line.startswith("#"):
            continue
        if line.startswith("@"):
            curside=line[0:line.find(" ")]
            if curside in mappings: 
                curid=str(tabletid)+"_"+str(mappings[curside]+".png.json")
                print("Curside: "+str(curside))
                result[curid]=0
            continue
        for word in line.split(" "):
            word=word.replace("{","-").replace("}","-")
            if word=="" or re.search('^\s*[0-9]+\'\.',word) or re.search('^\s*[0-9]+\.',word) or word=="[x]" or word=="x" or word=="[...]":
                continue
            #print("Word: "+str(word))
            for char in word.split("-"):
                if curid in result and char!="" and char!="column" and char!="..." and char!="?" and char!="...]" and char!="[..." and char!="[...]" and char!="x":
                    print("Char: "+str(char))
                    result[curid]+=1
jsonString = json.dumps(result, indent=2)
jsonFile = open("js/translitcount.js", "w")
jsonFile.write("var translitcount="+jsonString)
jsonFile.close()

