import json

# read file
with open('urls.js', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)

result={}
result2={}
curobj={}
curlabel=""
for js in obj:
	print(js)
	exportlabel=js["label"]+".json"
	result2[exportlabel]=js["value"]
	curlabel=js["label"][0:js["label"].rfind('_')-2]
	curlabel2=js["label"][0:js["label"].rfind('_')-2]+"_"+js["label"][js["label"].rfind('_')-2:]
	if not curlabel in result:
		result[curlabel]={"label":curlabel,"variants":[{"label":curlabel2,"url":js["value"]}]}
	else:
		result[curlabel]["variants"].append({"label":curlabel2,"url":js["value"]})

f = open("newurls.js", "w")
f.write("var urls="+json.dumps(result, indent=2, sort_keys=True))
f.close()

f = open("newurls2.js", "w")
f.write(json.dumps(result2, indent=2, sort_keys=True))
f.close()