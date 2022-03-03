/**
 * eliminates duplicates from arrays
 */

function eliminateDuplicates(arr) {
    return arr.filter(function(item, pos) {
        return arr.indexOf(item) == pos;
    })
}

/**
 * removes empty elements from arrays
 */
function removeEmpty(arr) {
    return arr.filter(n => n)
}

/**
 * extracts the numbers from a string
 */
 function extractNumbers(string) {
    return ( string
        .match(/\d+\.\d+|\d+\b|\d+(?=\w)/g) || [] )
        .map(function (v) {return +v;});
}

/**
 * extracts begin of a time period from a period name;
 * returns -1 when there are no numbers in the period name
 */
function getPeriodBegin(periodName) {
    var numbers = extractNumbers(periodName);
    if (typeof numbers !== 'undefined' && numbers.length > 0) {
        return extractNumbers(periodName).shift();
    } else {
        return -1
    }
}

/**
 * sorts period name array by time period, starting with the latest;
 * precondition: time periods are set BC
 */
function sortByPeriod(arr) {
    return arr.sort(function(periodName1, periodName2) {
        periodBegin1 = getPeriodBegin(periodName1)
        periodBegin2 = getPeriodBegin(periodName2)
        if (periodBegin1 == -1 ) {
            return 1;
        }
        if (periodBegin2 == -1 ) {
            return -1;
        }
        if (periodBegin1 <= periodBegin2) {
            return -1;
        } else {
            return 1;
        }
    })
}

/**
 * maps an array of language objects to an array of field strings
 */
function mapToField(arr, field) {
  return arr.map(function(item) {
    return item[field];
  });
}

/**
 * maps every empty string to "unassigned"
 */
function markUnassigned(arr) {
  return arr.map(function(item) {
    if (item == "") {
      return "unassigned";
    }
    return item;
  });
}

/**
 * reduces an object to an sorted array of distinct values of a specified field;
 * designed for the language object
 */
function reduceToDistinctField(obj, field) {
  return markUnassigned(
    eliminateDuplicates(
      mapToField(
        Object.values(obj),
        field
      )
    )
  ).sort();
}

/**
 * an array of every supported filter category name
 */
var filterCategories = ["period","language","provenience","genre","material"]

/**
 * init arrays of distinct filter values
 */
var distinctPeriods =
  sortByPeriod(
    removeEmpty(
      eliminateDuplicates(
        Object.values(periods)
      )
    )
  );
var distinctLanguages = reduceToDistinctField(languages, filterCategories[1]);
var distinctProvenience = reduceToDistinctField(languages, filterCategories[2]);
var distinctGenre = reduceToDistinctField(languages, filterCategories[3]);
var distinctMaterial = reduceToDistinctField(languages, filterCategories[4]);

//activeFilter = [[periods],[languages],...]

/**
 * concat the first element of every array in an array of arrays into a new array
 * example: [[1,2],[4,5],[7,8]] -> [1,4,7]
 */
 function concatFirst(arr) {
    return arr.map(function(item) {
        return item[0];
    });
}

/**
 * returns an array of tablet names that match the given period filter
 */
function filterPeriodTuples(periodName) {
    let periodsArray = Object.entries(periods);
    let periodTuples = periodsArray.filter(function(periodTuple) {
        return periodTuple[1] == periodName;
    })
    return concatFirst(periodTuples);
}

/**
 * return an array of tablet names that fit every period filter
 */
function filterPeriodTabletNames(periodNames) {
    let result = [];
    for (currentIndex in periodNames) {
        result = result.concat(filterPeriodTuples(periodNames[currentIndex]));
    }
    return eliminateDuplicates(result);
}

/**
 * returns an array of tablet names that match the given filter of this category for language objects
 */
function filterLanguageObjects(category, categoryfilterName) {
    var languageArray = Object.entries(languages);
    let languageTuples = languageArray.filter(function(languageTuple) {
        let languageObject = languageTuple[1]
        return languageObject[category] == categoryfilterName;
    })
    return concatFirst(languageTuples);
}

/**
 * returns an array of tablet names that match every filter of this category for language objects
 */
function filterLanguageTabletNames(category, categoryNames) {
    let result = [];
    for (currentIndex in categoryNames) {
        result = result.concat(filterLanguageObjects(category, categoryNames[currentIndex]));
    }
    return eliminateDuplicates(result);
}

/**
 * returns the intersection of 2 arrays
 */
function intersect(arr1, arr2) {
    return arr1.filter(function(item) {
        return arr2.indexOf(item) !== -1;
    });
}

/**
 * returns the union of 2 arrays
 */
 function union(arr1, arr2) {
    return eliminateDuplicates(arr1.concat(arr2));
}

/**
 * returns an array of all tablet names that should be visible with the current filters
 */
function getfilteredTabletNames() {
    let filteredTabletNames = concatFirst(Object.entries(urls));
    let noActivefilters = true;
    for (index in activeFilter) {
        noActivefilters = noActivefilters && (activeFilter[index].length <= 0)
    }
    if (!noActivefilters) {
        let activeTablets = [];
        for (categoryIndex in filterCategories) {
            let category = filterCategories[categoryIndex]
            if (category == "period") {
                activeTablets = union(activeTablets, filterPeriodTabletNames(activeFilter[categoryIndex]));
            } else {
                activeTablets = union(activeTablets, filterLanguageTabletNames(category, activeFilter[categoryIndex]));
            }
        }
        filteredTabletNames = intersect(filteredTabletNames, activeTablets);
    }
    console.log(filteredTabletNames);
    return filteredTabletNames;
}


/**
 * apply the current filter to the urls
 */
function filterSuggestions() {
    var filteredTabletNames = getfilteredTabletNames();

    var filtered2DUrls = Object.entries(urls).filter(function(urlArray) {
        return (filteredTabletNames.includes(urlArray[0]));
    });
    current2DUrls = Object.fromEntries(filtered2DUrls);

    var filtered3DUrls = Object.entries(hs23D).filter(function(urlArray) {
        return (filteredTabletNames.includes(urlArray[0]));
    });
    current3DUrls = Object.fromEntries(filtered3DUrls);
}