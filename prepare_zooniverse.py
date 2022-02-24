import csv
import sys
import os
import shutil

if len(sys.argv)>1:
    samplesize=sys.argv[1]
else:
    exit()
if not samplesize.isnumeric():
    exit()

if len(sys.argv)>2:
    maxsize=sys.argv[2]
else:
    exit()
if not maxsize.isnumeric():
    exit()


samplesize=int(samplesize)
maxsize=int(maxsize)

list_of_rows=None
with open('zooniverse_char_verify_ref_manifest.csv', 'r') as file:
    csv_reader = csv.reader(file,delimiter=';')
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    print(list_of_rows)

if not os.path.isdir('zooniverse_char_verify_ref_manifest_result'):
    os.makedirs('zooniverse_char_verify_ref_manifest_result')
f = open("zooniverse_char_verify_ref_manifest_result/zooniverse_char_verify_ref_manifest.csv", "w")
alreadyprocessed={}
cursize=0
for row in list_of_rows:
    print(row)
    if cursize>=maxsize:
        break
    if cursize==0:
        f.write(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
        cursize+=1
        continue
    if not row[2] in alreadyprocessed:
        alreadyprocessed[row[2]]=0
    if alreadyprocessed[row[2]]<=samplesize:
        f.write(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
        shutil.copyfile("char_annotated/"+row[0], "zooniverse_char_verify_ref_manifest_result/"+row[0])
        if os.path.isfile("normalized_signs_comp/"+row[1].lower().capitalize()):
            shutil.copyfile("normalized_signs_comp/"+row[1].lower().capitalize(), "zooniverse_char_verify_ref_manifest_result/"+row[1].upper().replace(".JPG",".jpg"))
            print("File found: "+"normalized_signs_comp/"+row[1].lower().capitalize())
        else:
            print("File not found: "+"normalized_signs_comp/"+row[1].lower().capitalize())
        alreadyprocessed[row[2]]+=1
    cursize+=1
f.close()


list_of_rows=None
with open('zooniverse_char_verify_line_manifest.csv', 'r') as file:
    csv_reader = csv.reader(file,delimiter=';')
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    print(list_of_rows)

if not os.path.isdir('zooniverse_char_verify_line_manifest_result'):
    os.makedirs('zooniverse_char_verify_line_manifest_result')
f = open("zooniverse_char_verify_line_manifest_result/zooniverse_char_verify_line_manifest.csv", "w")
alreadyprocessed={}
cursize=0
for row in list_of_rows:
    print(row)
    if cursize>=maxsize:
        break
    if cursize==0:
        f.write(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
        cursize+=1
        continue
    if not row[2] in alreadyprocessed:
        alreadyprocessed[row[2]]=0
    if alreadyprocessed[row[2]]<=samplesize:
        f.write(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
        shutil.copyfile("char_annotated/"+row[0], "zooniverse_char_verify_line_manifest_result/"+row[0])
        if os.path.isfile("charline/"+row[1]):
            shutil.copyfile("charline/"+row[1], "zooniverse_char_verify_line_manifest_result/"+row[1])
            print("File found: "+"charline/"+row[1])
        else:
            print("File not found: "+"charline/"+row[1])
        alreadyprocessed[row[2]]+=1
    cursize+=1
f.close()
