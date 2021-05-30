from urllib.request import urlopen
from wand.image import Image
import sys
import os
import csv
import json
import math


exportdir="result"
singlefolder=False
purpose="Transliteration"
emptycounter=0
filename="annotations/bbox_annotations_train_full.csv"

labelmap={}

arffexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
arffthresholdexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"

arffdata="@data\n"

arffdataperiods="@data\n"

arffdatasignperiods="@data\n"

arffdatathreshold="@data\n"

with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lasturl=""
        f=""
        for row in csv_reader:
            filepath=row["tablet_CDLI"]
            bbox=row["bbox"]
            print("https://cdli.ucla.edu/dl/photo/"+row["tablet_CDLI"]+".jpg")
            try:
                if lasturl!="https://cdli.ucla.edu/dl/photo/"+row["tablet_CDLI"]+".jpg":
                    f=urlopen("https://cdli.ucla.edu/dl/photo/"+row["tablet_CDLI"]+".jpg")
                if not row["mzl_label"] in labelmap:
                    labelmap["mzl_label"]=0
                labelmap["mzl_label"]=labelmap["mzl_label"]+1
                with Image(file=f) as img:
                    width=img.width
                    height=img.height
                    coords=bbox.replace("[","").replace("]","").split(",")
                    print(coords)
                    print("w"+str(width)+" h"+str(height))
                    print(str(coords[2])+"x"+str(coords[3])+"+"+str(coords[0])+"+"+str(coords[1]))
                    with img[int(coords[0]):int(coords[2]),int(coords[1]):int(coords[3])] as cropped:
                        with cropped.convert('jpg') as converted:
                            converted.save(filename=exportdir+"/"+row["tablet_CDLI"]+"_"+str(row["mzl_label"])+"_"+str(labelmap["mzl_label"])+".jpg")  
                arffdata+=row["tablet_CDLI"]+"_"+str(row["mzl_label"])+"_"+str(labelmap["mzl_label"])+".jpg,"+str(row["mzl_label"])+"\n"
            except Exception as e:
                print(e)
for trans in sorted(translits):
    arffexport+=str(trans)+","
    if translits[trans]>mlThreshold:
        arffthresholdexport+=str(trans)+","
f = open(exportdir+"mlset.arff", 'w')
f.write(arffexport+arffdata)
f.close()
#f = open(exportdir+"mlsetthreshold.arff", 'w')
#f.write(arffthresholdexport+arffdatathreshold)
#for line in arffthresholdlines:
#  if translits[line]>mlThreshold:
#      f.write(arffthresholdlines[line])
#f.close()
