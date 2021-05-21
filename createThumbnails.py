from urllib.request import urlopen
from wand.image import image
import sys
import os
import json

translits={}

for filename in os.listdir("result"):
    #print(sys.argv[1]+"/"+filename)
    if filename==".gitkeep" or filename.startswith("."):
        continue
    with open("result/"+filename) as json_file:
        for annotation in json_file:
            coords=annotation["target"]["selector"]["value"].replace("xywh","")
            translit=""
            for(annobj in annotation["body"]){
                if(annoobj["purpose"]=="Transliteration"){
                    translit=annoobj["value"]
                }
            }
            if(translit in translits){
                translits[translit]=translits[translit]+1
            }else{
                translits[translit]=1
            }
            f=urlopen("")
            with Image(file=f) as img:
                width=img.width
                height=img.height
                with img[10:50, 20:100] as cropped:
                    cropped.save(filename="thumbnails/"+translit+"_"+translits[translit]+".png")
