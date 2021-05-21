from urllib.request import urlopen
from wand.image import Image
import sys
import os
import json
from svgpathtools import svg2paths, wsvg

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
            svgpaths2(jsondata[annotation]["target"]["selector"]["value"])
            continue
        coords=jsondata[annotation]["target"]["selector"]["value"].replace("xywh","").split(",")
        translit=""
        for annoobj in jsondata[annotation]["body"]:
            print(annoobj)
            if annoobj["purpose"]=="Transliteration":
                translit=annoobj["value"]
        if translit in translits:
            translits[translit]=translits[translit]+1
        else:
            translits[translit]=1      
        f=urlopen(imgurls[filename])
        arffdata+=translit+"_"+translits[translit]+".png,"+translit+"\n"
        print(coords)
        with Image(file=f) as img:
            width=img.width
            height=img.height
            with img[coords[0]:coords[1], coords[2]:coords[3]] as cropped:
                if(not os.path.exists("public/thumbnails/"+translit)):
                    os.makedirs("public/thumbnails/"+translit)
                cropped.save(filename="public/thumbnails/"+translit+"/"+translit+"_"+translits[translit]+".png")
                if not translit in homepagejson:
                    homepagejson[translit]={}
                homepagejson[translit].push("thumbnails/"+translit+"/"+translit+"_"+translits[translit]+".png")
f = open("public/js/thumbnails.js", 'w')
f.write("var thumbnails="+json.dumps(homepagejson))
f.close()

arffexport="@RELATION\m@ATTRIBUTE filename string\n@ATTRIBUTE class{"
for(trans in translits):
    arffexport+=trans+","
arffexport=arffexport[-1]+"}\n\n"
f = open("public/mlset.arff", 'w')
f.write(arffexport+arffdata)
f.close()



