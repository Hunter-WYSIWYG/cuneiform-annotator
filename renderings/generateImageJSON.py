import os
import json

result={}
files = os.listdir(".")

for f in files:
    result[f]={}
    if os.path.isdir(f):
        result[f]["label"]=f
        result[f]["variants"]=[]
        for dirc in os.listdir(f):
            curobj={"label":dirc,"url":"https://gitlab.rlp.net/api/v4/projects/16599/repository/files/renderings%2F"+str(f)+"%2F"+str(dirc)+"/raw?ref=master&access_token=bPaesdD1s-gcJ5qzaaDv"}
            result[f]["variants"].append(curobj)

f = open("urlsht.js", "w")
f.write("var hturls="+json.dumps(result,indent=2))
f.close()
