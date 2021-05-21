from urllib.request import urlopen
from wand.image import Image
import sys
import os
import json
import math
from svgpathtools import svg2paths, wsvg
from svgpathtools import svg2paths2

translits={}

with open('js/newurls2.js') as f:
  imgurls = json.load(f)

homepagejson={}

arffdata="@data\n"

for filename in os.listdir("result"):
    #print(sys.argv[1]+"/"+filename)
    if filename==".gitkeep" or filename.startswith("."):
        continue
    with open("result/"+filename) as json_file:
        jsondata=json.load(json_file)
    for annotation in jsondata:
        print(annotation)
        if "svg" in jsondata[annotation]["target"]["selector"]["value"]:
            f = open("temp.svg", 'w')
            f.write(jsondata[annotation]["target"]["selector"]["value"])
            f.close()
            print(jsondata[annotation]["target"]["selector"]["value"])
            path=svg2paths2("temp.svg")
            bb=path[0][0].bbox()
            coords=[]
            coords.append(int(bb[0]))
            coords.append(int(bb[2]))
            coords.append(int(abs(bb[1]-bb[0])))
            coords.append(int(abs(bb[3]-bb[2])))
        else:
            coords=jsondata[annotation]["target"]["selector"]["value"].replace("xywh","").split(",")
        print(coords)
        translit=""
        for annoobj in jsondata[annotation]["body"]:
            if annoobj["purpose"]=="Transliteration":
                translit=annoobj["value"]
        if translit in translits:
            translits[translit]=translits[translit]+1
        else:
            translits[translit]=1      
        f=urlopen(imgurls[filename])
        arffdata+=str(translit)+"_"+str(translits[translit])+".png,"+str(translit)+"\n"
        print(coords)
        with Image(file=f) as img:
            width=img.width
            height=img.height
            print("w"+str(width)+" h"+str(height))
            print(str(coords[2])+"x"+str(coords[3])+"+"+str(coords[0])+"+"+str(coords[1]))
            with img[int(coords[2]):int(coords[3]),int(coords[0]):int(coords[1])] as cropped:
                if(not os.path.exists("public/thumbnails/"+translit)):
                    os.makedirs("public/thumbnails/"+translit)
                cropped.save(filename="public/thumbnails/"+translit+"/"+str(translit)+"_"+translits[translit]+".png")
                if not translit in homepagejson:
                    homepagejson[translit]={}
                homepagejson[translit].push("thumbnails/"+translit+"/"+str(translit)+"_"+translits[translit]+".png")
f = open("public/js/thumbnails.js", 'w')
f.write("var thumbnails="+json.dumps(homepagejson))
f.close()

arffexport="@RELATION\m@ATTRIBUTE filename string\n@ATTRIBUTE class{"
for trans in translits:
    arffexport+=str(trans)+","
arffexport=arffexport[-1]+"}\n\n"
f = open("public/mlset.arff", 'w')
f.write(arffexport+arffdata)
f.close()



