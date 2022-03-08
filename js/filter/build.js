/**
 * init arrays of distinct filter values
 */
var distinctCDLI = reduceToDistinctValues(hs2CDLI)
var distinctPeriods = reduceToDistinctValues(periods)
var distinctGenre = reduceToDistinctField(languages, filterCategories[0]);
var distinctSubgenre = reduceToDistinctField(languages, filterCategories[1]);
var distinctLanguages = reduceToDistinctField(languages, filterCategories[2]);
var distinctMaterial = reduceToDistinctField(languages, filterCategories[3]);
var distinctProvenience = reduceToDistinctField(languages, filterCategories[4]);

/**
 * returns the list of distinct filter values for a filter category
 */
 function getFilterNames(filterCategory) {
    switch (filterCategory) {
        case "CDLI":
            return distinctCDLI;
        case "period":
            return distinctPeriods;
        case "genre":
            return distinctGenre;
        case "subgenre":
            return distinctSubgenre;
        case "language":
            return distinctLanguages;
        case "material":
            return distinctMaterial;
        case "provenience":
            return distinctProvenience;
    }
    return []
}

/**
 * init active filter array
 */
var activeFilter = [];
for (var cat in filterCategories) {
    activeFilter.push([]);
}

/**
 * init the active filter tab
 */
var activeFilterTab = filterCategories[0];

/**
 * keep track of the active filter tab
 */
function updateActiveFilterTab(newTab) {
    activeFilterTab = newTab;
}

/**
 * adds or removes filters from activeFilters variable
 */
function updateActiveFilters(filterCategory, filterName) {
    let filterCatIndex = filterCategories.indexOf(filterCategory);
    if (activeFilter[filterCatIndex].includes(filterName)) {
        index = activeFilter[filterCatIndex].indexOf(filterName);
        activeFilter[filterCatIndex].splice(index, 1);
    } else {
        activeFilter[filterCatIndex].push(filterName);
        activeFilter[filterCatIndex].sort();
    }
}
 
/**
 * activates every filter-check of the active tab
 */
function activateAllChecks() {
     let filterNames = getFilterNames(activeFilterTab);
     for (var index in filterNames) {
         let currentCheck = document.getElementById("check-" + activeFilterTab + "-" + index);
         currentCheck.checked = true;
     }
     let catIndex = filterCategories.indexOf(activeFilterTab);
     activeFilter[catIndex] = filterNames;
}
 
/**
 * deactivates every filter-check of the active tab
 */
function deactivateAllChecks() {
     let filterNames = getFilterNames(activeFilterTab);
     for (var index in filterNames) {
         let currentCheck = document.getElementById("check-" + activeFilterTab + "-" + index);
         currentCheck.checked = false;
     }
     let catIndex = filterCategories.indexOf(activeFilterTab);
     activeFilter[catIndex] = [];
}

/**
 * build filter tabs and tab content
 */
var filterTab = document.getElementById("filter-tab");
var filterTabContent = document.getElementById("filter-tab-content");

for (var filterCategoryIndex in filterCategories) {
     let filterCategory = filterCategories[filterCategoryIndex];
     let filterCategoryCapital = filterCategory.charAt(0).toUpperCase() + filterCategory.slice(1);
     let activeString = "";
     let showActiveString = "";
     if (filterCategoryIndex == 0) {
         activeString = "active";
         showActiveString = "show active";
     }
 
     var newTab = document.createElement("li");
     newTab.setAttribute("class","nav-item");
     newTab.setAttribute("role","presentation");
     var newButton = document.createElement("button");
     newButton.setAttribute("class","nav-link " + activeString);
     newButton.setAttribute("id",filterCategory + "-tab");
     newButton.setAttribute("data-bs-toggle","tab");
     newButton.setAttribute("data-bs-target","#" + filterCategory + "-content");
     newButton.setAttribute("type","button");
     newButton.setAttribute("role","tab");
     newButton.setAttribute("aria-controls",filterCategory);
     newButton.setAttribute("aria-selected","true");
     newButton.setAttribute("onclick","updateActiveFilterTab('" + filterCategory + "')");
     newButton.textContent = filterCategoryCapital;
     newTab.appendChild(newButton);
     filterTab.appendChild(newTab);
 
     var newContent = document.createElement("div");
     newContent.setAttribute("class","tab-pane fade " + showActiveString);
     newContent.setAttribute("id",filterCategory + "-content");
     newContent.setAttribute("role","tabpanel");
     newContent.setAttribute("aria-labelledby",filterCategory + "-tab");
     filterTabContent.appendChild(newContent);
 
     let filterNames = getFilterNames(filterCategory);
     for (var index in filterNames) {
         let filterName = filterNames[index]
         var newCheck = document.createElement("div");
         newCheck.setAttribute("class","form-check");
         newContent.appendChild(newCheck);
 
         var newInput = document.createElement("input");
         newInput.setAttribute("class","form-check-input");
         newInput.setAttribute("type","checkbox");
         newInput.setAttribute("value","");
         newInput.setAttribute("id","check-" + filterCategory + "-" + index);
         newInput.setAttribute("onclick", "updateActiveFilters('" + filterCategory + "', '" + filterName + "')");
         newCheck.appendChild(newInput);
 
         var newLabel = document.createElement("label");
         newLabel.setAttribute("class","form-check-label");
         newLabel.setAttribute("for","flexCheckDefault");
         if (filterName == "") {
            newLabel.innerHTML = "unassigned";
         } else {
            newLabel.innerHTML = filterName;
         }
         newCheck.appendChild(newLabel);
     }
}