from urllib.request import urlopen
from wand.image import Image
import sys
import os
import json

translits={}

with open('js/newurls2.js') as f:
  imgurls = json.load(f)

for filename in os.listdir("result"):
    #print(sys.argv[1]+"/"+filename)
    if filename==".gitkeep" or filename.startswith("."):
        continue
    with open("result/"+filename) as json_file:
        jsondata=json.load(json_file)
    for annotation in jsondata:
        coords=annotation["target"]["selector"]["value"].replace("xywh","").split(",")
        translit=""
        for annobj in annotation["body"]:
            if annoobj["purpose"]=="Transliteration":
                translit=annoobj["value"]
        if translit in translits:
            translits[translit]=translits[translit]+1
        else:
            translits[translit]=1      
        f=urlopen(imgurls[filename])
        with Image(file=f) as img:
            width=img.width
            height=img.height
            with img[coords[0]:coords[1], coords[2]:coords[3]] as cropped:
                if(not os.path.exists("public/thumbnails/"+translit)):
                    os.makedirs("public/thumbnails/"+translit)
                cropped.save(filename="public/thumbnails/"+translit+"/"+translit+"_"+translits[translit]+".png")
