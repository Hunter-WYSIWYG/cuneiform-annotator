import os
import json

result={}

for filename in os.listdir("result"):
    #print(sys.argv[1]+"/"+filename)
    if filename==".gitkeep" or filename.startswith("."):
        continue
    with open("result/"+filename) as json_file:
        jsondata=json.load(json_file)
    for annotation in jsondata:
        translit=None
        paleocode=None
        for annoobj in jsondata[annotation]["body"]:
            if annoobj["purpose"]=="Transliteration":
                translit=annoobj["value"]
            if annoobj["purpose"]=="PaleoCodage":
                paleocode=annoobj["value"]
        if paleocode!=None and translit!=None:
            if not translit in result:
                result[translit]={}
            if paleocode in result[translit]:
                result[translit][paleocode]=result[translit][paleocode]+1
            else:
                result[translit][paleocode]=1

jsonString = json.dumps(result)
jsonFile = open("public/js/paleocodes.js", "w")
jsonFile.write("var paleocodemap="+jsonString)
jsonFile.close()
