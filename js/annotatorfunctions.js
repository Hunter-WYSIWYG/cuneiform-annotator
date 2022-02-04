visible = true

function showHideAnno() {
    visible = !visible
    anno.setVisible(visible)
}

approvaltags = []

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function addTag(){
  mytag=$('#comment').val()
  approvaltags.push(mytag)
  if(mytag=="")
    return
  $('#mytags').append("<span style=\"background-color:yellow;color:black;border-radius: 25px;border:1px solid black \">"+mytag+"</span>")
  $('#comment').val("")
}

function sync2D3D() {
    console.log($('#images option:selected').text() + " " + $('#3dimages option:selected').text())
    if ($('#images option:selected').text() in threedimageToIndex) {
        console.log($('#images option:selected').text() + " - " + threedimageToIndex[$('#images option:selected').text()])
        document.getElementById('3dimages').selectedIndex = threedimageToIndex[$('#images option:selected').text()]
    }
}

function rescale(X, A, B, C, D) {
    console.log("Input: " + X)
    retval = (((X - A).toFixed(2) / (B - A)) * (D - C)) + C
    console.log("Scale factor: " + ((B - A) * (D - C)))
    console.log("Rescaled: " + retval)
    return retval
}

function getEXIFData(imageid, targetid) {
    var img2 = document.getElementById(imageid);
    console.log("EXIF click")
    EXIF.getData(img2, function() {
        var allMetaData = EXIF.getAllTags(this);
        console.log(allMetaData)
        var allMetaDataSpan = document.getElementById(targetid);
        allMetaDataSpan.innerHTML = JSON.stringify(allMetaData, null, "\t");
        var htmltip = "<ul>"
        for (tag in allMetaData) {
            htmltip += "<li>" + tag + " - " + allMetaData[tag] + "</li>"
        }
        htmltip += "</ul>"
        $("#metadata").tooltip({
            content: htmltip
        });
    });
}

function highlightIndexedChars() {
    console.log(indexedcharids)
    console.log(indexedhiglighted)
    for (indchar of indexedcharids) {
        var element = document.querySelector('.a9s-annotation[data-id="' + indchar + '"]').children
        console.log(element)
        if (!indexedhiglighted) {
            element[1].classList.add("indexhighlight");
        } else {
            element[1].classList.remove("indexhighlight");
        }
    }
    indexedhiglighted = !indexedhiglighted
}

function reinit(param) {
    param = $('#imageside option:selected').val()
    param2 = $('#imageside option:selected').text()

    $('.imagelink').css({
        "backgroundColor": "#f7f7f9",
        "color": "#bd4147",
        "border": "0px"
    })
    viewer.open({
        type: "image",
        url: param
    });
    //}
    manageApprovals()
    curanno = {}
    curcharindex = {}
    $('#annocomplete').html("Unknown")
    $('#indexingcomplete').html("Unknown")
    $.getJSON(gitlabhost + "/api/v4/projects/" + repositoryid + "/repository/files/result%2F" + encodeURIComponent(param2 + ".json") + "/raw?ref=" + branch + "&access_token=" + gitlabtoken, function(result) {
        console.log(result)
        indexedchars = 0
        indexedhiglighted = false
        indexedcharids = []
        annotations = []
        for (ann in result) {
            line = -1
            charindex = -1
            colindex = -1
            for (bod of result[ann]["body"]) {
                if ("purpose" in bod && bod["purpose"] == "Line") {
                    line = bod["value"]
                } else if ("purpose" in bod && bod["purpose"] == "Charindex") {
                    charindex = bod["value"]
                } else if ("purpose" in bod && bod["purpose"] == "Column") {
                    colindex = bod["value"]
                }
            }
            if (charindex != -1 && charindex != "" && line != -1 && line != "") {
                indexedcharids.push(ann)
                indexedchars += 1
                side = param2.replace(".png", "")
                console.log("COLINDEX!!! " + colindex)
                if (colindex != -1) {
                    curimgindex[ann] = side.substring(side.lastIndexOf('_') + 1) + "_column_" + colindex + "_" + line + "_" + charindex
                    curcharindex[side.substring(side.lastIndexOf('_') + 1) + "_column_" + colindex + "_" + line + "_" + charindex] = ann
                } else {
                    curimgindex[ann] = side.substring(side.lastIndexOf('_') + 1) + "_" + line + "_" + charindex
                    curcharindex[side.substring(side.lastIndexOf('_') + 1) + "_" + line + "_" + charindex] = ann
                }
            }
            annotations.push(result[ann])
        }
        console.log(curcharindex)
        curanno = result
        anno.setAnnotations(annotations);
        if ($('#imageside option:selected').text() + ".json" in translitcount) {
            if (annotations.length > 0 && translitcount[$('#imageside option:selected').text() + ".json"] > 0) {
                $('#annocomplete').html((annotations.length / translitcount[$('#imageside option:selected').text() + ".json"] * 100).toFixed(2) + "% (" + annotations.length + "/" + translitcount[$('#imageside option:selected').text() + ".json"] + ")")
            } else {
                $('#annocomplete').html("0% (0/" + translitcount[$('#imageside option:selected').text() + ".json"] + ")")
            }
        } else {
            $('#annocomplete').html("Unknown")
        }
        $('#indexingcomplete').html((indexedchars / translitcount[$('#imageside option:selected').text() + ".json"] * 100).toFixed(2) + "% (" + indexedchars + "/" + translitcount[$('#imageside option:selected').text() + ".json"] + ")")
    }).fail(function(jqXHR, textStatus, errorThrown) {
        anno.setAnnotations([]);
    })

    // Attach handlers to listen to events
    anno.on('createAnnotation', function(a) {
        console.log(a)
        console.log(JSON.stringify(a))
        curanno[a["id"]] = a
    });
    anno.on('deleteAnnotation', function(a) {
        delete curanno[a["id"]]
    });
    anno.on('updateAnnotation', function(a) {
        curanno[a["id"]] = a
    });
}

function loadVariants() {
    console.log($('#images option:selected').text())
    console.log(transliterations)
    toappend = ""
    if ($('#images option:selected').text() in periods) {
        toappend += periods[$('#images option:selected').text()] + " " //$('#period').html(periods[$('#images option:selected').text()])
    }
    if ($('#images option:selected').text() in languages) {
        toappend += languages[$('#images option:selected').text()]["language"] + " " + languages[$('#images option:selected').text()]["genre"]
        if (languages[$('#images option:selected').text()]["subgenre"] != "") {
            toappend += "<br/>" + languages[$('#images option:selected').text()]["subgenre"]
        }
        if (languages[$('#images option:selected').text()]["provenience"] != "") {
            toappend += "<br/>Provenience: " + languages[$('#images option:selected').text()]["provenience"]
        }
    }
    if ($('#images option:selected').text() in transliterations) {
        console.log(transliterations[$('#images option:selected').text()])
        if (transliterations[$('#images option:selected').text()] == "" || transliterations[$('#images option:selected').text()] == "@Tablet") {
            $('#transliterationtextarea').html("No transliteration available for text " + $('#images option:selected').text())
            if ($('#images option:selected').text() in hs2CDLI) {
                $('#textid').html("" + $('#images option:selected').text() + " - <a target=\"_blank\" href=\"https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID=" + hs2CDLI[$('#images option:selected').text()] + "\">" + hs2CDLI[$('#images option:selected').text()] + "</a>")
                $('#cdlilink').html("<a target=\"_blank\" href=\"https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID=" + hs2CDLI[$('#images option:selected').text()] + "\">" + hs2CDLI[$('#images option:selected').text()] + "</a>")
            } else {
                $('#textid').html("" + $('#images option:selected').text() + "")
            }
        } else {
            if ($('#images option:selected').text() in hs2CDLI) {
                $('#textid').html("" + $('#images option:selected').text() + " - <a target=\"_blank\" href=\"https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID=" + hs2CDLI[$('#images option:selected').text()] + "\">" + hs2CDLI[$('#images option:selected').text()] + "</a>")
                $('#cdlilink').html("<a target=\"_blank\" href=\"https://cdli.ucla.edu/search/search_results.php?SearchMode=Text&ObjectID=" + hs2CDLI[$('#images option:selected').text()] + "\">" + hs2CDLI[$('#images option:selected').text()] + "</a>")
            } else {
                $('#textid').html("" + $('#images option:selected').text() + "")
            }
            $('#transliterationtextarea').html(formatTransliteration(transliterations[$('#images option:selected').text()].replaceAll("\n", "<br>")))
            if (!($("#images option:selected").text() in character_postags)) {
                $('#translationtextarea').html("No translation available for text " + $('#images option:selected').text())
            }
            $('#translationtextarea').html(formatTranslation(transliterations[$('#images option:selected').text()].replaceAll("\n", "<br>")))
            $(function() {
                $(document).tooltip({
                    track: true
                });
            });
            $('span.imagelink').mouseover(function() {
                console.log("Selecting annotation")
                myid = $(this).attr("id")
                console.log(myid)
                if (myid in curcharindex) {
                    console.log(curcharindex[myid])
                    anno.disableEditor = true
                    anno.selectAnnotation(curcharindex[myid])
                }
            });
            $('span.imagelink').mouseout(function() {
                if (translitwasclicked) {
                    translitwasclicked = false
                } else {
                    anno.cancelSelected();
                    anno.disableEditor = false
                }
            });
            $('span.imagelink').click(function() {
                if (anno.disableEditor) {
                    anno.disableEditor = false
                } else {
                    anno.disableEditor = true
                }
            });
        }
    } else {
        $('#textid').html("" + $('#images option:selected').text() + "")
        $('#transliterationtextarea').html("No transliteration available for text " + $('#images option:selected').text())
    }
    imgside = ""
    for (obj of urls[$('#images option:selected').text()]["variants"]) {
        if (obj["label"].includes("front")) {
            imgside += "<option value=\"" + obj["url"] + "\" selected=\"selected\">" + obj["label"] + "</option>"
        } else {
            imgside += "<option value=\"" + obj["url"] + "\">" + obj["label"] + "</option>"
        }
    }
    $('#imageside').html(imgside)
    $('#period').html(toappend)
    reinit("abc");
}

function formatTranslation(transliteration) {
    result = ""
    termmap = {
        "@obverse": "front",
        "@reverse": "back",
        "@left": "left",
        "@right": "right",
        "@top": "top",
        "@bottom": "bottom"
    }
    linecounter = 0
    charcounter = 0
    currentside = ""
    currentcolumn = ""
    curterm = ""
    for (line of transliteration.split("<br>")) {
        if (line.trim().startsWith("@")) {
            if (line.trim() in termmap) {
                currentside = termmap[line.trim()]
                curterm = line.trim()
            } else {
                currentside = line.trim()
                cuterm = currentside
            }
            linecounter = 0
            charcounter = 0
            result += line.trim() + "<br/>"
        } else if (line.trim().startsWith("column") || line.trim().startsWith("@column")) {
            currentside = currentside.replace(currentcolumn, "")
            currentcolumn = line.trim().replace(" ", "_")
            currentside = currentside + "_" + currentcolumn
            currentside = currentside.replace("__", "_")
            linecounter = 0
            charcounter = 0
            result += line.trim() + "<br/>"
        } else if (line.trim().match(/^\d/)) {
            linecounter += 1
            charcounter = 0
            newline = line.trim()
            splitted = line.trim().split(" ")
            for (word of splitted) {
                word = word.replace("{", "-{").replace("}", "}-").trim()
                if (word.slice(-1) == "-") {
                    word = word.substring(0, word.length - 1)
                }
                word = word.replace("--", "-")
                lasttranslation = ""
                if (word.includes("-")) {
                    for (char of word.split("-")) {
                        if (char != "") {
                            console.log(curterm)
                            console.log(currentside + "_" + linecounter + "_" + charcounter)
                            if (($("#images option:selected").text() in character_postags) && curterm in character_postags[$("#images option:selected").text()] && currentside + "_" + linecounter + "_" + charcounter in character_postags[$("#images option:selected").text()][curterm]) {
                                titleobj = character_postags[$("#images option:selected").text()][curterm][currentside + "_" + linecounter + "_" + charcounter]
                            }
                            if (typeof titleobj !== 'undefined' && titleobj["translation"] != lasttranslation) {
                                console.log(titleobj)
                                result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\" title=\"" + titleobj["word"] + " "
                                if (titleobj["translation"] != "_") {
                                    result += "[" + titleobj["translation"] + "] (" + titleobj["pos"] + ")\">"
                                    if (titleobj["translation"].includes("[") && !titleobj["translation"].includes("[1]")) {
                                        result += titleobj["translation"].substring(titleobj["translation"].indexOf("[") + 1, titleobj["translation"].indexOf("]")) + "</span>"
                                    } else {
                                        result += titleobj["translation"].replace("[1]", "") + "</span>"
                                    }
                                    lasttranslation = titleobj["translation"]
                                } else {
                                    result += "(" + titleobj["pos"] + ")\">"
                                    if (titleobj["translation"].includes("[") && !titleobj["translation"].includes("[1]")) {
                                        result += titleobj["translation"].substring(titleobj["translation"].indexOf("[") + 1, titleobj["translation"].indexOf("]")) + "</span>"
                                    } else {
                                        result += titleobj["translation"].replace("[1]", "") + "</span>"
                                    }
                                    lasttranslation = titleobj["translation"]
                                }
                            } else {
                                result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\">" + char + "</span>"
                            }
                            if (!char.endsWith("}")) {
                                result += "&nbsp;"
                            }
                            charcounter += 1
                        }
                    }
                } else {
                    if (($("#images option:selected").text() in character_postags) && curterm in character_postags[$("#images option:selected").text()] && currentside + "_" + linecounter + "_" + charcounter in character_postags[$("#images option:selected").text()][curterm]) {
                        titleobj = character_postags[$("#images option:selected").text()][curterm][currentside + "_" + linecounter + "_" + charcounter]
                    }
                    console.log(character_postags)
                    console.log($("#images option:selected").text())
                    console.log(curterm)
                    console.log(currentside + "_" + linecounter + "_" + charcounter)
                    if (typeof titleobj !== 'undefined' && titleobj["translation"] != lasttranslation) {
                        console.log(titleobj)
                        result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\" title=\"" + titleobj["word"] + " "
                        if (titleobj["translation"] != "_") {
                            result += "[" + titleobj["translation"] + "] (" + titleobj["pos"] + ")\">" + titleobj["translation"] + "</span>&nbsp;"
                            lasttranslation = titleobj["translation"]
                        } else {
                            result += "(" + titleobj["pos"] + ")\">" + titleobj["translation"] + "</span>&nbsp;"
                            lasttranslation = titleobj["translation"]
                        }
                    } else {
                        result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\">" + word + "</span>&nbsp;"
                    }
                    charcounter += 1
                }
            }
            result += "<br/>"
        } else {
            result += line + "<br/>"
        }
    }
    return result
}

function formatTransliteration(transliteration) {
    result = ""
    termmap = {
        "@obverse": "front",
        "@reverse": "back",
        "@left": "left",
        "@right": "right",
        "@top": "top",
        "@bottom": "bottom"
    }
    linecounter = 0
    charcounter = 0
    currentside = ""
    currentcolumn = ""
    curterm = ""
    for (line of transliteration.split("<br>")) {
        if (line.trim().startsWith("@")) {
            if (line.trim() in termmap) {
                currentside = termmap[line.trim()]
                curterm = line.trim()
            } else {
                currentside = line.trim()
                cuterm = currentside
            }
            linecounter = 0
            charcounter = 0
            result += line.trim() + "<br/>"
        } else if (line.trim().startsWith("column") || line.trim().startsWith("@column")) {
            currentside = currentside.replace(currentcolumn, "")
            currentcolumn = line.trim().replace(" ", "_")
            currentside = currentside + "_" + currentcolumn
            currentside = currentside.replace("__", "_")
            linecounter = 0
            charcounter = 0
            result += line.trim() + "<br/>"
        } else if (line.trim().match(/^\d/)) {
            linecounter += 1
            charcounter = 0
            newline = line.trim()
            splitted = line.trim().split(" ")
            for (word of splitted) {
                if (result.endsWith("-")) {
                    result = result.substring(0, result.length - 1) + "&nbsp;"
                }
                word = word.replace("{", "-{").replace("}", "}-").trim()
                if (word.slice(-1) == "-") {
                    word = word.substring(0, word.length - 1)
                }
                word = word.replace("--", "__-")
                if (word.includes("-")) {
                    wordsplitted = word.split("-")
                    wordlen = wordsplitted.length
                    wordlencounter = 0
                    for (char of wordsplitted) {
                        if (char != "") {
                            console.log(curterm)
                            console.log(currentside + "_" + linecounter + "_" + charcounter)
                            if (($("#images option:selected").text() in character_postags) && curterm in character_postags[$("#images option:selected").text()] && currentside + "_" + linecounter + "_" + charcounter in character_postags[$("#images option:selected").text()][curterm]) {
                                titleobj = character_postags[$("#images option:selected").text()][curterm][currentside + "_" + linecounter + "_" + charcounter]
                            }
                            if (typeof titleobj !== 'undefined') {
                                console.log(titleobj)
                                result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\" title=\"" + titleobj["word"] + " "
                                if (titleobj["translation"] != "_") {
                                    result += "[" + titleobj["translation"] + "] (" + titleobj["pos"] + ")\">" + char + "</span>"
                                } else {
                                    result += "(" + titleobj["pos"] + ")\">" + char + "</span>"
                                }
                            } else {
                                result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\">" + char + "</span>"
                            }
                            charcounter += 1
                            wordlencounter += 1
                            console.log(word + " - " + wordsplitted[wordlencounter])
                            if (wordlencounter >= wordlen || typeof(wordsplitted[wordlencounter]) == "undefined") {
                                result += "&nbsp;"
                            } else if (wordlencounter < wordlen && char.endsWith("__")) {
                                result += "-"
                            } else if (wordlencounter < wordlen && char.slice(-1) != "}" && wordsplitted[wordlencounter].charAt(0) != "{") {
                                result += "-"
                            }
                        }
                    }
                } else {
                    if (($("#images option:selected").text() in character_postags) && curterm in character_postags[$("#images option:selected").text()] && currentside + "_" + linecounter + "_" + charcounter in character_postags[$("#images option:selected").text()][curterm]) {
                        titleobj = character_postags[$("#images option:selected").text()][curterm][currentside + "_" + linecounter + "_" + charcounter]
                    }
                    console.log(character_postags)
                    console.log($("#images option:selected").text())
                    console.log(curterm)
                    console.log(currentside + "_" + linecounter + "_" + charcounter)
                    if (typeof titleobj !== 'undefined') {
                        console.log(titleobj)
                        result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\" title=\"" + titleobj["word"] + " "
                        if (titleobj["translation"] != "_") {
                            result += "[" + titleobj["translation"] + "] (" + titleobj["pos"] + ")\">" + word + "</span>&nbsp;"
                        } else {
                            result += "(" + titleobj["pos"] + ")\">" + word + "</span>&nbsp;"
                        }
                    } else {
                        result += "<span id=\"" + currentside + "_" + linecounter + "_" + charcounter + "\" class=\"imagelink\">" + word + "</span>&nbsp;"
                    }
                    charcounter += 1
                }
            }
            result += "<br/>"
        } else {
            result += line + "<br/>"
        }
    }
    result = result.replaceAll("-<br/>", "<br/>")
    result = result.replaceAll("__", "").replaceAll("__", "")
    return result
}

function manageApprovals() {
    tabletnumber = $('#images option:selected').text()
    side = $('#imageside option:selected').text().replace(".png", "").replace(tabletnumber + "_", "")
    if (!(tabletnumber in approvals)) {
        approvals[tabletnumber] = {}
    }
    if (!(side in approvals[tabletnumber])) {
        approvals[tabletnumber][side] = {}
    }
    if ("tags" in approvals[tabletnumber][side]) {
        approvaltags = approvals[tabletnumber][side]["tags"]
        taghtml = ""
        for (tag in approvaltags) {
            taghtml += "<span style=\"background-color:yellow;color:black;border-radius: 25px;border:1px solid black \">" + approvaltags[tag] + "</span>"
        }
        $('#mytags').html(taghtml)
    }
    if ("positioningcorrect" in approvals[tabletnumber][side]) {
        $('#positioningcorrect').val(approvals[tabletnumber][side]["positioningcorrect"]).change();
    }
    if ("transliterationcorrect" in approvals[tabletnumber][side]) {
        $('#transliterationcorrect').val(approvals[tabletnumber][side]["transliterationcorrect"]).change();
    }
    if ("indexingcorrect" in approvals[tabletnumber][side]) {
        $('#indexingcorrect').val(approvals[tabletnumber][side]["indexingcorrect"]).change();
    }
    if ("annotationscorrect" in approvals[tabletnumber][side]) {
        $('#annotationscorrect').val(approvals[tabletnumber][side]["annotationscorrect"]).change();
    }
    if ("annotationscomplete" in approvals[tabletnumber][side]) {
        $('#annotationscomplete').val(approvals[tabletnumber][side]["annotationscomplete"]).change();
    }
}
