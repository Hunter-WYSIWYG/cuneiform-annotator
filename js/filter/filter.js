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
 * eliminates duplicates from arrays
 */
function eliminateDuplicates(arr) {
    return arr.filter(function(item, pos) {
        return arr.indexOf(item) == pos;
    })
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
 * returns an array of tablet names that match the given filter of this category for language objects
 */
function filterLanguageObjects(category, categoryfilterName, languagesObject) {
    var languageArray = Object.entries(languagesObject);
    let languageTuples = languageArray.filter(function(languageTuple) {
        let languageObject = languageTuple[1]
        return languageObject[category] == categoryfilterName;
    })
    return concatFirst(languageTuples);
}

/**
 * returns an array of tablet names that match every filter of this category for language objects
 */
function filterLanguageTabletNames(category, categoryNames, languagsObject) {
    let result = [];
    for (var currentIndex in categoryNames) {
        result = result.concat(filterLanguageObjects(category, categoryNames[currentIndex], languagsObject));
    }
    return eliminateDuplicates(result);
}

/**
 * return an array of tablet names that fit at least one period filter
 */
function filterKeyValueObjectTablets(filterNames, keyValueObject) {
    let result = [];
    for (var currentIndex in filterNames) {
        result = result.concat(filterKeyValueObjectTuples(filterNames[currentIndex], keyValueObject));
    }
    return eliminateDuplicates(result);
}

/**
 * returns an array of tablet names that match the given period filter
 */
function filterKeyValueObjectTuples(filterName, keyValueObject) {
    let keyValueArray = Object.entries(keyValueObject);
    let keyValueTuples = keyValueArray.filter(function(keyValueTuple) {
        return keyValueTuple[1] == filterName;
    })
    return concatFirst(keyValueTuples);
}

/**
 * apply the current filter to the urls
 * returns a tuple of 2d url objects and 3d url objects
 */
function filterSuggestions(activeFilterArray, filterCategoriesArray, urls2d, urls3d, periodsObject, languagsObject, cdliObject) {
    var filtered2DTabletNames = getfilteredTabletNames(activeFilterArray, filterCategoriesArray, urls2d, periodsObject, languagsObject, cdliObject);
    var filtered3DTabletNames = getfilteredTabletNames(activeFilterArray, filterCategoriesArray, urls3d, periodsObject, languagsObject, cdliObject);

    var filtered2DUrlsArray = Object.entries(urls2d).filter(function(urlArray) {
        return (filtered2DTabletNames.includes(urlArray[0]));
    });
    let filtered2DUrlsObject = Object.fromEntries(filtered2DUrlsArray);

    var filtered3DUrlsArray = Object.entries(urls3d).filter(function(urlArray) {
        return (filtered3DTabletNames.includes(urlArray[0]));
    });
    let filtered3DUrlsObject = Object.fromEntries(filtered3DUrlsArray);
    return [filtered2DUrlsObject, filtered3DUrlsObject];
}

/**
 * returns an array of all tablet names that should be visible with the current filters
 */
function getfilteredTabletNames(activeFilterArray, filterCategoriesArray, urlsObject, periodsObject, languagsObject, cdliObject) {
    let filteredTabletNames = concatFirst(Object.entries(urlsObject));
    let noActivefilters = true;
    for (var index in activeFilterArray) {
        noActivefilters = noActivefilters && (activeFilterArray[index].length <= 0)
    }
    if (!noActivefilters) {
        let activeTablets = [];
        for (var categoryIndex in filterCategoriesArray) {
            let category = filterCategoriesArray[categoryIndex]
            switch (category) {
                case "period":
                    activeTablets = union(activeTablets, filterKeyValueObjectTablets(activeFilterArray[categoryIndex], periodsObject));
                    break;
                case "CDLI":
                    activeTablets = union(activeTablets, filterKeyValueObjectTablets(activeFilterArray[categoryIndex], cdliObject));
                    break;
                default:
                    activeTablets = union(activeTablets, filterLanguageTabletNames(category, activeFilterArray[categoryIndex], languagsObject));
                    break;
            }
        }
        filteredTabletNames = intersect(filteredTabletNames, activeTablets);
    }
    return filteredTabletNames;
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
 * returns the intersection of 2 arrays
 */
function intersect(arr1, arr2) {
    let withDuplicates = arr1.filter(function(item) {
        return arr2.indexOf(item) !== -1;
    });
    return eliminateDuplicates(withDuplicates);
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
 * reduces the object to a sorted array of distinct values
 */
function reduceToDistinctValues(periodsObject) {
    return sortByPeriod(
        eliminateDuplicates(
        Object.values(periodsObject)
        )
    );
}

/**
 * sorts period name array by time period, starting with the latest;
 * precondition: time periods are set BC
 */
 function sortByPeriod(arr) {
    return arr.sort(function(periodName1, periodName2) {
        let periodBegin1 = getPeriodBegin(periodName1)
        let periodBegin2 = getPeriodBegin(periodName2)
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
 * returns the sorted union of 2 arrays
 */
 function union(arr1, arr2) {
    return eliminateDuplicates(arr1.concat(arr2)).sort();
}

module.exports = {
    eliminateDuplicates: eliminateDuplicates,
    extractNumbers: extractNumbers,
    getPeriodBegin: getPeriodBegin,
    sortByPeriod: sortByPeriod,
    mapToField: mapToField,
    reduceToDistinctField: reduceToDistinctField,
    reduceToDistinctValues: reduceToDistinctValues,
    concatFirst: concatFirst,
    filterKeyValueObjectTuples: filterKeyValueObjectTuples,
    filterKeyValueObjectTablets: filterKeyValueObjectTablets,
    filterLanguageObjects: filterLanguageObjects,
    filterLanguageTabletNames: filterLanguageTabletNames,
    intersect: intersect,
    union: union,
    getfilteredTabletNames: getfilteredTabletNames,
    filterSuggestions: filterSuggestions,
    concatFirst: concatFirst,
    markUnassigned: markUnassigned,
}