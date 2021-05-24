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

outputcsv=""

arffdata="@data\n"

exportdir="public/thumbnails/"
singlefolder=False
purpose="Transliteration"
if len(sys.argv)>1:
    exportdir=sys.argv[1]
if len(sys.argv)>2:
    if sys.argv[2]=="true":
        singlefolder=True
if len(sys.argv)>3:
    purpose=sys.argv[3]
for filename in os.listdir("result"):
    #print(sys.argv[1]+"/"+filename)
    if filename==".gitkeep" or filename.startswith("."):
        continue
    with open("result/"+filename) as json_file:
        jsondata=json.load(json_file)
    for annotation in jsondata:
        print(annotation)
        print(jsondata[annotation]["target"]["selector"]["value"])
        if "svg" in jsondata[annotation]["target"]["selector"]["value"]:
            f = open("temp.svg", 'w')
            f.write(jsondata[annotation]["target"]["selector"]["value"])
            f.close()
            path=svg2paths2("temp.svg")
            bb=path[0][0].bbox()
            coords=[]
            coords.append(int(bb[0]))
            coords.append(int(bb[1]))
            coords.append(int(bb[2]))
            coords.append(int(bb[3]))
        else:
            coords=jsondata[annotation]["target"]["selector"]["value"].replace("xywh","").replace("pixel:","").replace("=","").split(",")
        print(coords)
        translit=""
        for annoobj in jsondata[annotation]["body"]:
            if annoobj["purpose"]==purpose:
                translit=annoobj["value"]
        if translit=="":
            continue
        if translit in translits:
            translits[translit]=translits[translit]+1
        else:
            translits[translit]=1
        outputcsv+=filename[0:filename.rfind("_")]+";"+filename[filename.rfind("_")].replace(".png.json","")+";"
        outputcsv+=str(coords)+";"+translit+"\n"      
        f=urlopen(imgurls[filename])
        arffdata+=str(translit)+"_"+str(translits[translit])+".jpg,"+str(translit)+"\n"
        print(coords)
        try:
            with Image(file=f) as img:
                width=img.width
                height=img.height
                print("w"+str(width)+" h"+str(height))
                print(str(coords[2])+"x"+str(coords[3])+"+"+str(coords[0])+"+"+str(coords[1]))
                with img[int(coords[0]):int(coords[1]),int(coords[2]):int(coords[3])] as cropped:
                    if singlefolder:
                        with cropped.convert('jpg') as converted:
                            converted.save(filename=exportdir+str(translit)+"_"+str(translits[translit])+".jpg")
                    else:
                        if(not os.path.exists(exportdir+str(translit))):
                            os.makedirs(exportdir+str(translit))
                        with cropped.convert('jpg') as converted:
                            converted.save(filename=exportdir+str(translit)+"/"+str(translit)+"_"+str(translits[translit])+".jpg")
                    if not translit in homepagejson:
                        homepagejson[translit]=[]
                    if singlefolder:
                        homepagejson[translit].append("thumbnails/"+str(translit)+"_"+str(translits[translit])+".jpg")
                    else:
                        homepagejson[translit].append("thumbnails/"+str(translit)+"/"+str(translit)+"_"+str(translits[translit])+".jpg")
        except:
            e = sys.exc_info()[0]
            print(e)
if not singlefolder:
    f = open("public/js/thumbnails.js", 'w')
    f.write("var thumbnails="+json.dumps(homepagejson))
    f.close()

arffexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
for trans in sorted(translits):
    arffexport+=str(trans)+","
arffexport=arffexport[:-1]+"}\n\n"
if singlefolder:
    f = open(exportdir+"mlset.arff", 'w')
    f.write(arffexport+arffdata)
    f.close()
    f = open(exportdir+"translitmetadata.csv", 'w')
    f.write(outputcsv)
    f.close()
else:
    f = open("public/mlset.arff", 'w')
    f.write(arffexport+arffdata)
    f.close()
    f = open("public/translitmetadata.csv", 'w')
    f.write(outputcsv)
    f.close()


