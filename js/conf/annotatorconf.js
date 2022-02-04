var curnamespace="http://purl.org/cuneiform/"

var mappings={"PaleoCode":{"inputtype":"text","regex":"","handler":null,"paleocodage":true,"uri":curnamespace+"PaleoCode"},
"Transliteration":{"inputtype":"text","regex":"","handler":null,"uri":curnamespace+"Transliteration"},
"UnicodeCharName":{"inputtype":"select","regex":"","handler":null,"uri":curnamespace+"CharacterName"},
"Column":{"inputtype":"number","regex":"","handler":null,"uri":curnamespace+"Column"},
"Line":{"inputtype":"number","regex":"","handler":null,"uri":curnamespace+"Line"},
"Charindex":{"inputtype":"number","regex":"","handler":null,"uri":curnamespace+"Charindex"},
"Wordindex":{"inputtype":"number","regex":"","handler":null,"uri":curnamespace+"Wordindex"}
}

var gitlabhost="https://gitlab.rlp.net"
var repositoryid=16599
var branch="master"
var readOnlyVar=false
const gitlabtoken="bPaesdD1s-gcJ5qzaaDv"
const { Gitlab } = gitbeaker;
const api = new Gitlab({
  token: gitlabtoken, //'9zyFECzKmuhkMo81HKPw',
  host: 'https://gitlab.rlp.net',
  version: 4
});

async function getAnnotation(path){
  var users= await api.RepositoryFiles.show(16599, "result/"+$('#imageside option:selected').text()+".json","master");
  console.log(users)
  console.log(atob(users["content"]))
  return JSON.parse(atob(users["content"]))
}

async function commitData(){
    try{
    var users= await api.RepositoryFiles.create(16599, "result/"+$('#imageside option:selected').text()+".json","master",JSON.stringify(curanno,null,2),"Committed "+$('#imageside option:selected').text()+".json")
    }catch (e) {
    var users= await api.RepositoryFiles.edit(16599, "result/"+$('#imageside option:selected').text()+".json","master",JSON.stringify(curanno,null,2),"Committed "+$('#imageside option:selected').text()+".json")
    }
    console.log(users)
}

async function commit3DBBOX(){
  var users= await api.RepositoryFiles.edit(16599, "js/hs23D.js","master","var hs23D="+JSON.stringify(hs23D,null,2),"Committed js/hs23D.js")
}

async function saveApprovals(){
    tabletnumber=$('#images option:selected').text()
    side=$('#imageside option:selected').text().replace(".png","").replace(tabletnumber+"_","")
    if(!(tabletnumber in approvals)){
      approvals[tabletnumber]={}
    }
    if(!(side in approvals[tabletnumber])){
      approvals[tabletnumber][side]={}
    }
    approvals[tabletnumber][side]["tags"]=$('#tags').val()
    approvals[tabletnumber][side]["positioningcorrect"]=$('#positioningcorrect').val()
    approvals[tabletnumber][side]["transliterationcorrect"]=$('#transliterationcorrect').val()
    approvals[tabletnumber][side]["indexingcorrect"]=$('#indexingcorrect').val()
    approvals[tabletnumber][side]["annotationscorrect"]=$('#annotationscorrect').val()
    approvals[tabletnumber][side]["annotationscomplete"]=$('#annotationscomplete').val()
    var users= await api.RepositoryFiles.edit(16599, "js/approvals.js","master","var approvals="+JSON.stringify(approvals,null,2),"Committed approvals for "+$('#imageside option:selected').text()+".json");
}












