from urllib.request import urlopen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from libxmp import *
import sys
import os
import uuid
import json
import math
import requests
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import FOAF, NamespaceManager
import urllib.parse
from svgpathtools import svg2paths, wsvg
from svgpathtools import svg2paths2

graph = Graph()

graph.namespace_manager.bind('prefix', URIRef('https://mainzed.org/maicubeda/cuneiform/annotation/'))

def defineBBOX(coordarray,maxcoordarray):
    try:
      if coordarray[0]<maxcoordarray[0]:
          maxcoordarray[0]=coordarray[0]
      if coordarray[1]>maxcoordarray[1]:
          maxcoordarray[1]=coordarray[1]
      if coordarray[2]<maxcoordarray[2]:
          maxcoordarray[2]=coordarray[2]
      if coordarray[3]>maxcoordarray[3]:
          maxcoordarray[3]=coordarray[3]
    except:
        e = sys.exc_info()[0]
        print(e)
        print(sys.exc_info()[1])
        print(sys.exc_info()[2])
    return maxcoordarray

xmpmetadata_anno={
    "dc":{
        "publisher": "Zenodo",
        "subject": "Cuneiform, Sign, Image",
        "format": "image/jpg",        
        "creator": "Timo Homburg",
    },
    "xmp":{
        "CreatorTool": "MaiCuBeDa Generator Script"       
    },
    "xmpRights":{
        "UsageTerms": "CC BY SA 4.0"       
    }

}

def writeXMP(filepath, title, identifier):
    #print(filepath)
    try:
        xmpfile = XMPFiles( file_path=filepath, open_forupdate=True )
        #print(xmpfile)
        xmp=xmpfile.get_xmp()
        #print(xmp)
        for prop in xmpmetadata_anno["dc"]:
            xmp.set_property(dc,prop,xmpmetadata_anno["dc"][prop])
        for prop in xmpmetadata_anno["xmp"]:
            xmp.set_property("http://ns.adobe.com/xap/1.0/",prop,xmpmetadata_anno["xmp"][prop])
        for prop in xmpmetadata_anno["xmpRights"]:
            xmp.set_property("http://ns.adobe.com/xap/1.0/rights/",prop,xmpmetadata_anno["xmpRights"][prop])
        xmp.set_property(dc,"title",title)
        xmp.set_property(dc,"identifier",identifier)
        #print(xmpfile.can_put_xmp(xmp))
        if xmpfile.can_put_xmp(xmp):
            xmpfile.put_xmp(xmp)
        #print("Write XMP")
        xmpfile.close_file()
    except:
        print("XMP error "+str(filepath))
        e = sys.exc_info()[0]
        print(e)
        print(sys.exc_info()[1])
        print(sys.exc_info()[2])

translits={}

translitperiods={}

charOccurances={}

periodss={"Unknown":0}

charperperiod={}

linepadding=0.5

languagess={"Unknown":0}

genress={"Unknown":0}

arffthresholdlines={}

mlThreshold=9

with open('js/data/newurls2.js') as f:
  imgurls = json.load(f)
  
with open('js/data/periods.js') as f:
  strs=f.read()
  periods = json.loads(strs.replace("var periods=",""))

homepagejson={}

outputcsv="ID;Filename;CDLI_Number;IRI;;Time_period;Language;Genre;side;bbox;column;line;charindex;charname;transliteration\n"

linecsv=""

wordcsv=""

errorlog=""

zooniverse_char_verify="image;charclass;transliteration;#broken\n"

zooniverse_char_verify_ref="image;ref;charclass;transliteration;#broken\n"

zooniverse_char_verify_line="image;line;charclass;transliteration;#broken\n"

translitstats="filename,annotations,expected,percentage,indexedannotations,expected,percentage\n"

translitstatsJSON={}

arffdata="@data\n"

arffdataperiods="@data\n"

arffdatasignperiods="@data\n"

arffdatalanguages="@data\n"

arffdatagenres="@data\n"

arffdatathreshold="@data\n"

unknownchars=""

completejsonld=[]

dc = "http://purl.org/dc/elements/1.1/"

totalexpectedchars=0
totalcountedchars=0
totalindexedchars=0
seenchars={}
chardistributionstats={}

datanamespace="http://www.mainzed.org/maicubeda/"

cdlinamespace="http://cdli.ucla.edu/"

imagewidth=250
imageheight=250

exportdir="public/thumbnails/"
singlefolder=False
purpose="Transliteration"
charindexpurpose="Charindex"
wordindexpurpose="Wordindex"
columnindexpurpose="Column"
curcharindex=-1
curlineindex=-1
linepurpose="Line"
taggingpurpose="tagging"
tagging=""
exportoption=""
emptycounter=0
ttlstring=set()
ttlheader=""
ttlheader+="@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
ttlheader+="@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
ttlheader+="@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
ttlheader+="@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
ttlheader+="@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n"
ttlheader+="@prefix my: <http://www.example.com/> .\n"
ttlheader+="@prefix cunei: <http://www.cuneiform.com/cunei/> .\n"
ttlheader+="@prefix lemon: <http://lemon-model.net/lemon#> .\n"
ttlheader+="@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .\n"
ttlheader+="foaf:depiction rdf:type owl:DatatypeProperty .\n"
ttlheader+="my:line rdf:type owl:DatatypeProperty .\n"
ttlheader+="my:charindex rdf:type owl:DatatypeProperty .\n"
ttlheader+="my:text rdf:type owl:ObjectProperty .\n"
ttlheader+="my:unicode rdf:type owl:ObjectProperty .\n"
ttlheader+="cidoc:TX1_WrittenText rdf:type owl:Class .\n"
ttlheader+="lemon:Character rdf:type owl:Class .\n"
ttlheader+="cidoc:Glyph rdf:type owl:Class .\n"
ttlheader+="cidoc:Tablet rdf:type owl:Class .\n"
ttlheader+="cidoc:refersTo rdf:type owl:ObjectProperty .\n"
ttlheader+="cidoc:isDepictedBy rdf:type owl:ObjectProperty .\n"
ttlheader+="cidoc:P56_isFoundOn rdf:type owl:ObjectProperty .\n"
ttlheader+="cidoc:P138_represents rdf:type owl:ObjectProperty .\n"
ttlheader+="cidoc:includes rdf:type owl:ObjectProperty .\n"
if len(sys.argv)>1:
    exportdir=sys.argv[1]
if len(sys.argv)>2:
    if sys.argv[2]=="true":
        singlefolder=True
if len(sys.argv)>3:
    purpose=sys.argv[3]
if len(sys.argv)>4:
    exportoption=sys.argv[4]
dircontent=os.listdir("result")
sorted(dircontent)

with open('js/data/transliterations.js', 'r') as myfile:
    data=myfile.read()
    
transliterations = json.loads(data.replace("var transliterations=",""))
notworkedtransliterations=""

for translit in transliterations:
    if transliterations[translit].strip()!="@tablet":
        if str(translit)+"_03_front.png.json" not in dircontent:
            notworkedtransliterations+=str(translit)+"\n"


with open('js/data/newurls2.js', 'r') as myfile:
    data=myfile.read()

# parse file
hs2IIIF = json.loads(data.replace("var hs2IIIF=",""))
with open('js/data/languages.js', 'r') as myfile:
    data=myfile.read()

# parse file
languages = json.loads(data.replace("var languages=",""))
with open('js/data/charlistmap.js', 'r') as myfile:
    data=myfile.read()

# parse file
charlistmap = json.loads(data.replace("var charlistmap=",""))
with open('js/data/hs2CDLI.js', 'r') as myfile:
    data=myfile.read()

# parse file
hs2CDLI = json.loads(data.replace("var hs2CDLI=",""))
with open('js/data/cuneifymap.js', 'r') as myfile:
    data=myfile.read()

# parse file
cuneifymap = json.loads(data.replace("var cuneifymap=",""))
with open('js/data/translitcount.js', 'r') as myfile:
    data=myfile.read()
translitcount = json.loads(data.replace("var translitcount=",""))
filecounter=0
for filename in dircontent:
    filecounter+=1
    print("Processing file "+str(filecounter)+"/"+str(len(dircontent))+": "+str(filename))
    if filename==".gitkeep" or filename.startswith("."):
        continue
    with open("result/"+filename) as json_file:
        jsondata=json.load(json_file)
    maxcoords={}
    maxwordcoords={}
    charcoordsperline={}
    wordcoordsperline={}
    wordindextoword={}
    maxcoordtemplate=[-99999.0,99999.0,-99999.0,99999.0]
    try:
        r = requests.get(imgurls[filename])
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)
        print("Successfully downloaded "+str(filename)+" "+str(os.path.isfile("temp.jpg"))+": "+str(os.path.getsize("temp.jpg")))
    except:
        e = sys.exc_info()[0]
        print(e)
        print(sys.exc_info()[1])
        print(sys.exc_info()[2])
        continue
    indexedcount=0
    lineannoexport={}
    wordannoexport={}
    for annotation in jsondata:
        #print(annotation)
        #print(jsondata[annotation]["target"]["selector"]["value"])
        completejsonld.append(jsondata[annotation])
        #print("Graph now has "+str(len(graph))+" statements")
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
        #print(coords)
        translit=""
        curcharindex=-1
        curwordindex=-1
        line=-1
        column=-1
        tagging=""
        broken=False
        for annoobj in jsondata[annotation]["body"]:
            if annoobj["purpose"]==purpose and purpose=="Transliteration" and "value" in annoobj: 
                translit=annoobj["value"]
            elif annoobj["purpose"]==charindexpurpose and "value" in annoobj:
                curcharindex=annoobj["value"]
            elif annoobj["purpose"]==wordindexpurpose and "value" in annoobj:
                curwordindex=annoobj["value"]
            elif annoobj["purpose"]==linepurpose:
                line=annoobj["value"]   
            elif annoobj["purpose"]==taggingpurpose and "value" in annoobj and annoobj["value"]=="Character":
                annoobj["purpose"]="classifying"
                tagging=annoobj["value"]
            elif annoobj["purpose"]==taggingpurpose and "value" in annoobj and annoobj["value"]=="Broken":
                broken=True
            elif annoobj["purpose"]==taggingpurpose and "value" in annoobj:
                tagging=annoobj["value"]
            elif annoobj["purpose"]==columnindexpurpose and "value" in annoobj:
                column=annoobj["value"]
        if line!=-1 and curcharindex!=-1:
            indexedcount+=1
        if purpose=="Line" and "Line" in str(tagging):
            translit="Line"+line
        if purpose=="Line" and translit=="":
            continue
        shortfilename=filename[0:filename.rfind("_")]
        if purpose!="Line":
            if shortfilename[0:shortfilename.rfind("_")] in hs2CDLI:
                jsondata[annotation]["body"].append({"type":"TextualBody","purpose":"linking","value":cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)})
        f = open(exportdir+"/charannotations/"+filename, 'w')
        f.write(json.dumps(jsondata,indent=2))
        f.close()
        if line!=-1:
            if not "line"+str(line) in maxcoords:
                maxcoords["line"+str(line)]=[99999.0,-99999.0,99999.0,-99999.0]
            maxcoords["line"+str(line)]=defineBBOX(coords,maxcoords["line"+str(line)])
        if not "line"+str(line) in charcoordsperline:
            charcoordsperline["line"+str(line)]={}
        if curwordindex!=-1:
            if not "word"+str(line)+"_"+str(curwordindex) in maxwordcoords:
                maxwordcoords["word"+str(line)+"_"+str(curwordindex)]=[99999.0,-99999.0,99999.0,-99999.0]
            maxwordcoords["word"+str(line)+"_"+str(curwordindex)]=defineBBOX(coords,maxwordcoords["word"+str(line)+"_"+str(curwordindex)])
        charclass="other" #str(translit)
        charunicode=""
        if(str(translit) in cuneifymap):
            #print(cuneifymap[str(translit)])
            charclass=""
            if len(cuneifymap[str(translit)])>1:
                for chara in cuneifymap[str(translit)]:
                    cc="U+"+str(hex(ord(chara))).replace("0x","")
                    if not cc in seenchars:
                        image = Image.new('RGB', (300, 250), (255, 255, 255))
                        I1 = ImageDraw.Draw(image)
                        myCuneiFont = ImageFont.truetype('CuneiformComposite.ttf', 100)
                        I1.text((50, 50), chara, font=myCuneiFont, fill =(0, 0, 0))
                        image.save(exportdir+"/normalized_signs_comp/"+str(cc)+".jpg")
                        image = Image.new('RGB', (300, 250), (255, 255, 255))
                        I1 = ImageDraw.Draw(image)
                        myCuneiFont = ImageFont.truetype('CuneiformNA.ttf', 100)
                        I1.text((50, 50), chara, font=myCuneiFont, fill =(0, 0, 0))
                        image.save(exportdir+"/normalized_signs_na/"+str(cc)+".jpg")
                        image = Image.new('RGB', (300, 250), (255, 255, 255))
                        I1 = ImageDraw.Draw(image)
                        myCuneiFont = ImageFont.truetype('CuneiformOB.ttf', 100)
                        I1.text((50, 50), chara, font=myCuneiFont, fill =(0, 0, 0))
                        image.save(exportdir+"/normalized_signs_ob/"+str(cc)+".jpg")
                        seenchars[cc]=True 
                    charunicode=cc
                    if cc.upper() in charlistmap and "signName" in charlistmap[cc.upper()] and charlistmap[cc.upper()]["signName"]!="":
                        charclass+=str(charlistmap[cc.upper()]["signName"]).replace(" ","_").replace(",","_").encode("ascii", "ignore").decode()+"+"
                    else:
                        charclass=cc+"+"
            else:
                charclass="U+"+str(hex(ord(cuneifymap[str(translit)]))).replace("0x","")
                charunicode="U+"+str(hex(ord(cuneifymap[str(translit)]))).replace("0x","")
                if not charunicode in seenchars:
                    image = Image.new('RGB', (300, 250), (255, 255, 255))
                    I1 = ImageDraw.Draw(image)
                    myCuneiFont = ImageFont.truetype('CuneiformComposite.ttf', 100)
                    I1.text((50, 50), cuneifymap[str(translit)], font=myCuneiFont, fill =(0, 0, 0))
                    image.save(exportdir+"/normalized_signs_comp/"+str(charunicode)+".jpg")
                    image = Image.new('RGB', (300, 250), (255, 255, 255))
                    I1 = ImageDraw.Draw(image)
                    myCuneiFont = ImageFont.truetype('CuneiformNA.ttf', 100)
                    I1.text((50, 50), cuneifymap[str(translit)], font=myCuneiFont, fill =(0, 0, 0))
                    image.save(exportdir+"/normalized_signs_na/"+str(charunicode)+".jpg")
                    image = Image.new('RGB', (300, 250), (255, 255, 255))
                    I1 = ImageDraw.Draw(image)
                    myCuneiFont = ImageFont.truetype('CuneiformOB.ttf', 100)
                    I1.text((50, 50), cuneifymap[str(translit)], font=myCuneiFont, fill =(0, 0, 0))
                    image.save(exportdir+"/normalized_signs_ob/"+str(charunicode)+".jpg")
                    seenchars[charunicode]=True
        if charclass.upper() in charlistmap and "signName" in charlistmap[charclass.upper()] and charlistmap[charclass.upper()]["signName"]!="":
            charclass=str(charlistmap[charclass.upper()]["signName"]).replace(" ","_").replace(",","_").encode("ascii", "ignore").decode()
        if charclass in translits:
            translits[charclass]=translits[charclass]+1
        else:
            translits[charclass]=1
        if charclass=="other":
            if str(translit)!="" and str(column)!="-1":
                unknownchars+=str(translit)+" - "+str(filename)+" "+str(column)+" "+str(line)+" "+str(curcharindex)+"\n"
            elif str(translit)!="":
                unknownchars+=str(translit)+" - "+str(filename)+" "+str(line)+" "+str(curcharindex)+"\n"
            #print(str(translit))
        if str(translit)=="":
            continue
        translit=translit.replace(",","_")
        per=filename[0:filename.rfind("_")]
        per=per[0:per.rfind("_")]
        savedfilename=""
        try:
            #f=open("temp.jpg", "rb")
            with Image.open("temp.jpg") as img:
                width=img.width
                height=img.height
                #print("w"+str(width)+" h"+str(height))
                #print(str(coords[2])+"x"+str(coords[3])+"+"+str(coords[1]-coords[0])+"+"+str(coords[3]-coords[2]))
                cropped = img.crop((int(coords[0]),int(coords[2]),int(coords[1]),int(coords[3])))
                charcoordsperline["line"+str(line)][str(translit).replace("/","_").replace("'","_")]=coords
                #print("CROPPED!")
                #with img[int(coords[0]):int(coords[1]),int(coords[2]):int(coords[3])] as cropped:
                savedfilename=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+str(column).replace("-","")+"_"+str(line)+"_"+str(curcharindex)+"_"+filename.replace(".png","").replace(".json","")+".jpg"
                if singlefolder:  
                        resized = cropped.resize((imagewidth, imageheight))
                        #print("RESIZED!")
                        resized.save(exportdir+"/char/"+savedfilename)
                        writeXMP(exportdir+"/char/"+savedfilename,"Cuneiform Sign "+str(translit)+" in text "+filename.replace(".png","").replace(".json","")+" in line "+str(line)+" at character position "+str(curcharindex),str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass]).replace("/","_")+"_"+filename.replace(".png","").replace(".json",""))
                        #print("SAVED!")
                else:
                        if(not os.path.exists(exportdir+str(translit))):
                            os.makedirs(exportdir+str(translit))
                        resized = cropped.resize((imagewidth, imageheight))
                        resized.save(exportdir+"/char/"+savedfilename)
                        writeXMP(exportdir+"/char/"+savedfilename,"Cuneiform Sign "+str(translit)+" in text "+filename.replace(".png","").replace(".json","")+" in line "+str(line)+" at character position "+str(curcharindex),str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass]).replace("/","_")+"_"+filename.replace(".png","").replace(".json",""))
                #if not os.path.exists(exportdir+"/char_annotated/"):
                #  os.makedirs(exportdir+"/char_annotated/")
                #imaag = Image.open(exportdir+"/char/"+str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass]).replace("/","_")+"_"+filename.replace(".png","").replace(".json","")+".jpg")
                I1 = ImageDraw.Draw(resized)
                myFont = ImageFont.truetype('FreeMono.ttf', 25)
                I1.text((10, 10), str(translit), font=myFont, fill =(255, 0, 0))
                I1.text((10, 230), str(charclass), font=myFont, fill =(255, 0, 0))
                #print("ANNOTATED!")
                resized.save(exportdir+"/char_annotated/"+savedfilename.replace(".jpg","_annotated.jpg"))
                writeXMP(exportdir+"/char_annotated/"+savedfilename.replace(".jpg","_annotated.jpg"),"Annotated Cuneiform Sign "+str(translit)+" in text "+filename.replace(".png","").replace(".json","")+" in line "+str(line)+" at character position "+str(curcharindex),str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass]).replace("/","_")+"_"+filename.replace(".png","").replace(".json",""))

                #print("SAVED ANNOTATION")
                if not translit in homepagejson:
                    homepagejson[translit]=[]
                if singlefolder:
                    homepagejson[translit].append("thumbnails/"+str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+".jpg")
                else:
                    homepagejson[translit].append("thumbnails/"+str(translit).replace("/","_").replace("'","_")+"/"+str(translit)+"_"+str(translits[charclass])+".jpg")
                zooniverse_char_verify+=savedfilename.replace(".jpg","_annotated.jpg")+";"+str(charclass)+";"+str(translit)+";"+str(broken)+"\n"
                zooniverse_char_verify_ref+=savedfilename.replace(".jpg","_annotated.jpg")+";"+str(charunicode).upper()+".jpg;"+str(charclass)+";"+str(translit)+";"+str(broken)+"\n"
                zooniverse_char_verify_line+=savedfilename.replace(".jpg","_annotated.jpg")+";charline_"+str(linee).replace("line","")+"_"+str(translit).replace("char","")+"_"+filename.replace(".png","").replace(".json","")+".jpg;"+str(charclass)+";"+str(translit)+";"+str(broken)+"\n"
                #";charline_"+str(line)+"_"+filename.replace(".png","").replace(".json","")+".jpg;"
            if per in periods:
                shortfilename=filename[0:filename.rfind("_")]
                outputcsv+=shortfilename+";"
                outputcsv+=savedfilename+";"
                if shortfilename[0:shortfilename.rfind("_")] in hs2CDLI:
                    outputcsv+=hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+";"
                    outputcsv+=cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_"+filename[filename.rfind("_")+1:].replace(".png.json","")+"_char_"+str(line)+"_"+str(curcharindex)+";"
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> rdf:type lemon:Character .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"> rdf:type cunei:Tablet .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_text> cidoc:P56_isFoundOn <"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"> .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_text> rdf:type cidoc:TX1_WrittenText .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> rdfs:label \""+str(translit)+"\"@en .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:text  <"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_text> .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:line  \""+str(line)+"\"^^xsd:integer .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:charindex  \""+str(curcharindex)+"\"^^xsd:integer .\n")  
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"> rdf:type lemon:Character .\n")      
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:unicode <"+cdlinamespace+urllib.parse.quote(str(charclass))+"> .\n") 
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"> cidoc:isDepictedBy <"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> rdf:type cidoc:Glyph .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> cidoc:P138_represents  <"+cdlinamespace+urllib.parse.quote(str(charclass))+"> .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> cidoc:P56_isFoundOn  <"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"> .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> foaf:depiction  \""+str(filename)+"\"^^xsd:string .\n")
                else:
                    outputcsv+=";;"
                if filename in hs2IIIF:
                    outputcsv+=hs2IIIF[filename].replace("full/full",str(coords[0])+","+str(coords[2])+","+str(abs(coords[1]-coords[0]))+","+str(abs(coords[3]-coords[2]))+"/full")+";"
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> foaf:depiction  \""+filename+"\"^^xsd:string .\n")
                else:
                    outputcsv+=";"
                outputcsv+=periods[per]+";"
                if per in languages:
                    outputcsv+=languages[per]["language"].replace(" ","_")+";"+languages[per]["genre"].replace(" ","_")+";"
                else:
                    outputcsv+=";;" 
                outputcsv+=filename[filename.rfind("_")+1:].replace(".png.json","")+";"
                outputcsv+=str(coords)+";"+str(column)+";"+str(line)+";"+str(curcharindex)+";"+str(charclass)+";"+str(translit)+"\n" 
                if not periods[per] in periodss and periods[per]!="":
                    periodss[periods[per]]=0
                if periods[per]=="":
                    periodss["Unknown"]+=1
                else:
                    periodss[periods[per]]+=1
                if not languages[per]["language"] in languagess and languages[per]["language"]!="":
                    languagess[languages[per]["language"]]=0  
                if languages[per]["language"]=="":
                    languagess["Unknown"]+=1
                else:
                    languagess[languages[per]["language"]]+=1
                if not languages[per]["genre"] in genress and languages[per]["genre"]!="":
                    genress[languages[per]["genre"]]=0
                if languages[per]["genre"]=="":
                    genress["Unknown"]+=1               
                else:
                    genress[languages[per]["genre"]]+=1
                if not str(charclass)+"_"+periods[per] in translitperiods:
                    if periods[per]!="":
                        translitperiods[str(charclass)+"_"+periods[per]]=0
                    else:
                        translitperiods[str(charclass)+"_Unknown"]=0
                    if not str(charclass) in charperperiod:
                        charperperiod[str(charclass)]=0
                    charperperiod[str(charclass)]+=1
                if periods[per]!="":
                    translitperiods[str(charclass)+"_"+periods[per]]+=1
                else:
                    translitperiods[str(charclass)+"_Unknown"]+=1
                arffdataperiods+=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+filename.replace(".png","").replace(".json","")+".jpg,"
                if per in periods and periods[per]!="":
                    arffdataperiods+=periods[per].replace(" ","_")+"\n"
                else:
                    arffdataperiods+="Unknown\n"
                if per in languages:
                    arffdatalanguages+=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+filename.replace(".png","").replace(".json","")+".jpg,"
                    if languages[per]["language"].replace(" ","_")=="":
                        arffdatalanguages+="Unknown\n"
                    else:
                        arffdatalanguages+=languages[per]["language"].replace(" ","_")+"\n"
                    arffdatagenres+=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+filename.replace(".png","").replace(".json","")+".jpg,"
                    if languages[per]["genre"].replace(" ","_")=="":
                        arffdatagenres+="Unknown\n"
                    else:
                        arffdatagenres+=languages[per]["genre"].replace(" ","_")+"\n"
                arffdatasignperiods+=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+filename.replace(".png","").replace(".json","")+".jpg,"+str(charclass)+"_"
                if per in periods and periods[per]!="":
                    arffdatasignperiods+=periods[per].replace(" ","_")+"\n"
                else:
                    arffdatasignperiods+="Unknown\n"
            else:
                shortfilename=filename[0:filename.rfind("_")]
                outputcsv+=shortfilename+";"
                outputcsv+=savedfilename+";"
                if shortfilename[0:shortfilename.rfind("_")] in hs2CDLI:
                    outputcsv+=hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+";"
            
                    if column!=-1:
                        outputcsv+=cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_"+filename[filename.rfind("_")+1:].replace(".png.json","")+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+";"
                    else:
                        outputcsv+=cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_"+filename[filename.rfind("_")+1:].replace(".png.json","")+"_char_"+str(line)+"_"+str(curcharindex)+";"
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> rdf:type lemon:Character .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"> rdf:type cunei:Tablet .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"> cidoc:includes <"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_text> .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_text> rdf:type cidoc:TX1_WrittenText .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> rdfs:label \""+str(translit)+"\"@en .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:text  <"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_text> .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:line  \""+str(line)+"\"^^xsd:integer .\n")
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:charindex  \""+str(curcharindex)+"\"^^xsd:integer .\n")  
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"> rdf:type lemon:Character .\n")      
                    ttlstring.add("<"+cdlinamespace+hs2CDLI[shortfilename[0:shortfilename.rfind("_")]]+"_char_"+str(column)+"_"+str(line)+"_"+str(curcharindex)+"> my:unicode <"+cdlinamespace+urllib.parse.quote(str(charclass))+"> .\n") 
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"> cidoc:isDepictedBy <"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> rdf:type cidoc:Glyph .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> cidoc:refersTo  <"+cdlinamespace+urllib.parse.quote(str(charclass))+"> .\n")
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> foaf:depiction  \""+str(filename)+"\"^^xsd:string .\n")
                else:
                    outputcsv+=";;"
                if filename in hs2IIIF:
                    outputcsv+=hs2IIIF[filename].replace("full/full",str(coords[0])+","+str(coords[2])+","+str(coords[1]-coords[0])+","+str(coords[3]-coords[2])+"/full")+";"
                    ttlstring.add("<"+cdlinamespace+urllib.parse.quote(str(charclass))+"_glyph> foaf:depiction  \""+filename+"\"^^xsd:string .\n")
                else:
                    outputcsv+=";"
                outputcsv+=filename[filename.rfind("_")+1:].replace(".png.json","")+";"
                if per in languages:
                    outputcsv+=languages[per]["language"].replace(" ","_")+";"+languages[per]["genre"].replace(" ","_")+";"
                else:
                    outputcsv+=";;" 
                outputcsv+=str(coords)+";"+str(column)+";"+str(line)+";"+str(curcharindex)+";"+str(charclass)+";"+str(translit)+"\n"      
            arffdata+=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+filename.replace(".png","").replace(".json","")+".jpg,"+str(charclass)+"\n"
            if not charclass in arffthresholdlines:
                arffthresholdlines[charclass]=""
            arffthresholdlines[charclass]+=str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass])+"_"+filename.replace(".png","").replace(".json","")+".jpg,"+str(charclass)+"\n"
            #print(coords)
        except:
            e = sys.exc_info()[0]
            print(e)
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])
            print("char;"+str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass]).replace("/","_")+"_"+filename.replace(".png","").replace(".json","")+".jpg\n")
            errorlog+="char;"+str(translit).replace("/","_").replace("'","_")+"_"+str(translits[charclass]).replace("/","_")+"_"+filename.replace(".png","").replace(".json","")+".jpg"+str(e)+";"+str(sys.exc_info()[1])+";"+str(sys.exc_info()[2])+"\n"
        #f.close()
        width=0
        height=0
        try:
            #print(maxcoords)
            linecsvhead=filename+";"
            wordcsvhead=filename+";"
            shortfilename=filename[0:filename.rfind("_")]
            #fi=open("temp.jpg", "rb")
            with Image.open("temp.jpg") as img2:
                width=img2.width
                height=img2.height
                #print("w"+str(width)+" h"+str(height))
                for linee in maxcoords:
                    #print(str(maxcoords[linee][2])+"x"+str(maxcoords[linee][3])+"+"+str(maxcoords[linee][0])+"+"+str(maxcoords[linee][1]))
                    linecsv+=linecsvhead+str(linee.replace("line",""))+";"+str(maxcoords[linee])+";"
                    iiifurl="line_"+str(linee).replace("line","")+"_"+filename.replace(".png","").replace(".json","")
                    if filename in hs2IIIF:
                        iiifurl=hs2IIIF[filename].replace("full/full",str(maxcoords[linee][0])+","+str(maxcoords[linee][2])+","+str(abs(maxcoords[linee][1]-maxcoords[linee][0]))+","+str(abs(maxcoords[linee][3]-maxcoords[linee][2]))+"/full")
                        linecsv+=iiifurl+";"
                    lineuuid="#"+str(uuid.uuid4())
                    lineannoexport[lineuuid]={"type":"Annotation","body":[{"type":"TextualBody","purpose":"Line","value":linee,"source":"http://purl.org/cuneiform/Line"},{"type":"TextualBody","purpose":"linking","value":"http://cdli.ucla.edu/"+str(filename.replace(".png","").replace(".json",""))+"_line_"+str(linee)}],"target":{"source":iiifurl,"selector":{"type":"SvgSelector","value":"<svg><polygon points=\""+str(str(maxcoords[linee]))+"\"</svg>"},"rights":"https://creativecommons.org/licenses/by-sa/4.0/"}}
                    cropped = img2.crop((int(maxcoords[linee][0]),int(maxcoords[linee][2]),int(maxcoords[linee][1]),int(maxcoords[linee][3])))
                    #with img2[int(maxcoords[linee][0]):int(maxcoords[linee][1]),int(maxcoords[linee][2]):int(maxcoords[linee][3])] as cropped:
                    savedlinename=exportdir+"/line/"+"line_"+str(linee).replace("line","")+"_"+filename.replace(".png","").replace(".json","")+".jpg"
                    cropped.save(savedlinename)
                    if linee in charcoordsperline:
                        for curchar in charcoordsperline[linee]:
                            curcoords=charcoordsperline[linee][curchar]
                            curimg=img2.copy()
                            img1 = ImageDraw.Draw(curimg)  
                            img1.rectangle([int(curcoords[0]),int(curcoords[2]),int(curcoords[1]),int(curcoords[3])], outline ="red",width=3)
                            curcrop = curimg.crop((int(maxcoords[linee][0]),int(maxcoords[linee][2]),int(maxcoords[linee][1]),int(maxcoords[linee][3])))
                            savedannolinename=exportdir+"/charline/"+"charline_"+str(linee).replace("line","")+"_"+str(curchar).replace("char","")+"_"+filename.replace(".png","").replace(".json","")+".jpg"
                            curcrop.save(savedannolinename)
                    writeXMP(savedlinename,"Line "+str(linee).replace("line","")+" in text "+shortfilename[0:filename.rfind("_")]+" on the "+str(filename[filename.rfind("_")+1:filename.rfind(".")]).replace(".png","")+" side",iiifurl)
                    linecsv+="\n"
                for worde in maxwordcoords:
                    #print(str(maxcoords[linee][2])+"x"+str(maxcoords[linee][3])+"+"+str(maxcoords[linee][0])+"+"+str(maxcoords[linee][1]))
                    wordcsv+=wordcsvhead+str(worde.replace("word",""))+";"+str(maxwordcoords[worde])+";"
                    iiifurl="word_"+str(worde).replace("word","")+"_"+filename.replace(".png","").replace(".json","")
                    if filename in hs2IIIF:
                        iiifurl=hs2IIIF[filename].replace("full/full",str(maxwordcoords[worde][0])+","+str(maxwordcoords[worde][2])+","+str(abs(maxwordcoords[worde][1]-maxwordcoords[worde][0]))+","+str(abs(maxwordcoords[worde][3]-maxwordcoords[worde][2]))+"/full")
                        wordcsv+=iiifurl+";"
                    worduuid="#"+str(uuid.uuid4())
                    wordannoexport[worduuid]={"type":"Annotation","body":[{"type":"TextualBody","purpose":"Word","value":linee,"source":"http://purl.org/cuneiform/Word"},{"type":"TextualBody","purpose":"linking","value":"http://cdli.ucla.edu/"+str(filename.replace(".png","").replace(".json",""))+"_word_"+str(worde)}],"target":{"source":iiifurl,"selector":{"type":"SvgSelector","value":"<svg><polygon points=\""+str(str(maxwordcoords[worde]))+"\"</svg>"},"rights":"https://creativecommons.org/licenses/by-sa/4.0/"}}
                    cropped = img2.crop((int(maxwordcoords[worde][0]),int(maxwordcoords[worde][2]),int(maxwordcoords[worde][1]),int(maxwordcoords[worde][3])))
                    #with img2[int(maxcoords[linee][0]):int(maxcoords[linee][1]),int(maxcoords[linee][2]):int(maxcoords[linee][3])] as cropped:
                    savedwordname=exportdir+"/word/"+"word_"+str(worde).replace("word","")+"_"+filename.replace(".png","").replace(".json","")+".jpg"
                    cropped.save(savedwordname)
                    writeXMP(savedwordname,"Word "+str(worde).replace("word","")+" in text "+shortfilename[0:filename.rfind("_")]+" on the "+str(filename[filename.rfind("_")+1:filename.rfind(".")])+" side",iiifurl)
                    wordcsv+="\n"
        except:
            e = sys.exc_info()[0]
            print(e)
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])
            print("line;"+str(maxcoords)+";"+str(width)+";"+str(height)+";line_"+str(line).replace("line","")+"_"+filename.replace(".png","").replace(".json","")+".jpg;\n")
            errorlog+="line;"+str(maxcoords)+";"+str(width)+";"+str(height)+";line_"+str(line).replace("line","")+"_"+filename.replace(".png","").replace(".json","")+".jpg;"+str(e)+";"+str(sys.exc_info()[1])+";"+str(sys.exc_info()[2])+"\n"
    f = open(exportdir+"/wordannotations/words_"+filename, 'w')
    f.write(json.dumps(wordannoexport, indent=2))
    f.close()
    f = open(exportdir+"/lineannotations/lines_"+filename, 'w')
    f.write(json.dumps(lineannoexport, indent=2))
    f.close()
    if filename in translitcount:
        totalexpectedchars+=translitcount[filename]
        totalcountedchars+=len(jsondata)
        totalindexedchars+=indexedcount
        if int(translitcount[filename])!=0:
            translitstats+=filename+","+str(len(jsondata))+","+str(translitcount[filename])+","+str((len(jsondata)/int(translitcount[filename]))*100)+","+str(indexedcount)+","+str(translitcount[filename])+","+str((indexedcount/int(translitcount[filename]))*100)+"\n"
            translitstatsJSON[filename]=str((len(jsondata)/int(translitcount[filename]))*100)#{"annotationcompleteness":,"indexingcompleteness":str((indexedcount/int(translitcount[filename]))*100)}
        else:
            translitstats+=filename+","+str(len(jsondata))+","+str(translitcount[filename])+",100,"+str(indexedcount)+","+str(len(jsondata))+",100\n"
            translitstatsJSON[filename]="100" #{"annotationcompleteness":"100","indexingcompleteness":"100"}
if not singlefolder:
    f = open("public/js/thumbnails.js", 'w')
    f.write("var thumbnails="+json.dumps(homepagejson))
    f.close()
print("JSON-LD TO TTL")
graph.parse(data=json.dumps(completejsonld),format='json-ld')
print("FINAL EXPORTS")
if totalexpectedchars==0:
    totalexpectedchars=1
translitstats+="Total,"+str(totalcountedchars)+","+str(totalexpectedchars)+","+str((totalcountedchars/totalexpectedchars)*100)+","+str(totalindexedchars)+","+str(totalexpectedchars)+","+str((totalindexedchars/totalexpectedchars)*100)+"\n"
arffexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
arffthresholdexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
arffperiodsexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
arfflanguagesexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
arffgenresexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
arfftranslitperiodsexport="@RELATION "+purpose+"\n@ATTRIBUTE\tfilename\tstring\n@ATTRIBUTE\tclass\t{"
for trans in sorted(translits):
    arffexport+=str(trans)+","
    if translits[trans]>mlThreshold:
        arffthresholdexport+=str(trans).replace(",","_")+","
for trans in sorted(periodss):
    arffperiodsexport+=str(trans).replace(" ","_").replace(",","_")+","
for trans in sorted(genress):
    arffgenresexport+=str(trans).replace(" ","_").replace(",","_")+","
for trans in sorted(languagess):
    arfflanguagesexport+=str(trans).replace(" ","_").replace(",","_")+","
for trans in sorted(translitperiods):
    arfftranslitperiodsexport+=str(trans.replace(" ","_").replace(",","_"))+","
arffexport=arffexport[:-1]+"}\n\n"
arffthresholdexport=arffthresholdexport[:-1]+"}\n\n"
arffperiodsexport=arffperiodsexport[:-1]+"}\n\n"
arffgenresexport=arffgenresexport[:-1]+"}\n\n"
arfflanguagesexport=arfflanguagesexport[:-1]+"}\n\n"
arfftranslitperiodsexport=arfftranslitperiodsexport[:-1]+"}\n\n"
if not singlefolder:
    exportdir=exportdir+"/public"
f = open(exportdir+"/mlset.arff", 'w')
f.write(arffexport+arffdata)
f.close()
f = open(exportdir+"/maicubeda.ttl", 'w')
f.write(ttlheader)
for tt in ttlstring:
    f.write(tt)
f.close()
f = open(exportdir+"/mlsetthreshold.arff", 'w')
f.write(arffthresholdexport+arffdatathreshold)
for line in arffthresholdlines:
    if translits[line]>mlThreshold:
        f.write(arffthresholdlines[line])
f.close()
f = open(exportdir+"/mlset_periods.arff", 'w')
f.write(arffperiodsexport+arffdataperiods)
f.close()
f = open(exportdir+"/mlset_languages.arff", 'w')
f.write(arfflanguagesexport+arffdatalanguages)
f.close()
f = open(exportdir+"/mlset_genres.arff", 'w')
f.write(arffgenresexport+arffdatagenres)
f.close()
f = open(exportdir+"/mlset_translitperiods.arff", 'w')
f.write(arfftranslitperiodsexport+arffdatasignperiods)
f.close()
f = open(exportdir+"/translitmetadata.csv", 'w')
f.write(outputcsv)
f.close()
f = open(exportdir+"/linemetadata.csv", 'w')
f.write(linecsv)
f.close()
f = open(exportdir+"/wordmetadata.csv", 'w')
f.write(wordcsv)
f.close()
f = open(exportdir+"/unknownchars.txt", 'w')
f.write(unknownchars)
f.close()
f = open(exportdir+"/errorlog.csv", 'w')
f.write(errorlog)
f.close()
f = open(exportdir+"/notworkedtransliterations.txt", 'w')
f.write(notworkedtransliterations)
f.close()
f = open(exportdir+"/zooniverse_char_verify_manifest.csv", 'w')
f.write(zooniverse_char_verify)
f.close()
f = open(exportdir+"/zooniverse_char_verify_ref_manifest.csv", 'w')
f.write(zooniverse_char_verify_ref)
f.close()
f = open(exportdir+"/zooniverse_char_verify_line_manifest.csv", 'w')
f.write(zooniverse_char_verify_line)
f.close()
f = open(exportdir+"/translitstats.csv", 'w')
f.write(translitstats)
f.close()
try:
    sort_translitstats = sorted(translitstatsJSON.items(), key=lambda x: x[1])
    acc_translitstats={}
    for translit in sort_translitstats:
        if not str(translit[1]) in acc_translitstats:
            acc_translitstats[str(translit[1])]=0
        acc_translitstats[str(translit[1])]+=1
    f = open(exportdir+"/charperperiod.csv", 'w')
    sort_charperiods = sorted(charperperiod.items(), key=lambda x: x[1])
    acc_charperiods={}
    for charr in sort_charperiods:
        f.write(str(charr[0])+","+str(charr[1])+"\n")
        if not str(charr[1]) in acc_charperiods:
            acc_charperiods[str(charr[1])]=0
        acc_charperiods[str(charr[1])]+=1
    f.close()
except:
    print("error")
f = open(exportdir+"/acc_charperperiod.csv", 'w')
f.write("AmountOfChars,NumberPeriods\n")
for charr in acc_charperiods:
    f.write(str(charr)+","+str(acc_charperiods[charr]))
f.close()
f = open(exportdir+"/homepagestats.js", 'w')   
f.write("var charperperiod="+json.dumps(sort_charperiods,indent=2)+";\n"+"var acc_charperperiod="+json.dumps(acc_charperiods,indent=2)+";\nvar numberCharPeriods="+json.dumps(periodss,indent=2)+";\nvar numberLanguages="+json.dumps(languagess,indent=2)+";\nvar genres="+json.dumps(genress,indent=2)+";\nvar acc_translitstats="+json.dumps(acc_translitstats,indent=2)+";\nvar translitstats="+json.dumps(translitstatsJSON,indent=2)+";\nvar charclasses="+json.dumps(translits,indent=2))
f.close()
graph.serialize(destination=exportdir+'/annotations.ttl', format='turtle')
