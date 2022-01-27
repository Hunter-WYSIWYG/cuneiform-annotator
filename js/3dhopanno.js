var 3dannotations=[]

function reset3DHopAnnotations(presenter){
    3dannotations=[]
    presenter._selectionPoints=[]
    console.log(3dannotations)
    presenter.repaint()
}

function load3DHopAnnotations{
    viewer.multiplepolygon=[]
    for(ann in annos){
        presenter._selectionPoints.push(ann["target"]["selector"])
    }
    presenter.repaint()
}

