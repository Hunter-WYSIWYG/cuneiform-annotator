var 3dannotations=[]

function resetAnnotations(presenter){
    3dannotations=[]
    presenter._selectionPoints=[]
    console.log(3dannotations)
    presenter.repaint()
}

function loadAnnotations(annos,presenter){
    viewer.multiplepolygon=[]
    for(ann in annos){
        presenter._selectionPoints.push(ann["target"]["selector"])
    }
    presenter.repaint()
}

