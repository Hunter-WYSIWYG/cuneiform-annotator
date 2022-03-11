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
function filterLanguageTablets(category, categoryNames, languagsObject) {
    let result = [];
    for (var currentIndex in categoryNames) {
        result = result.concat(filterLanguageObjects(category, categoryNames[currentIndex], languagsObject));
    }
    return eliminateDuplicates(result);
}

/**
 * return an array of tablet names that fit at least one period or CDLI filter
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
    let tabletNamesWithUrl = concatFirst(Object.entries(urlsObject));
    let filteredTabletNamesWithUrl = [];
    let noActivefilters = true;
    for (var index in activeFilterArray) {
        noActivefilters = noActivefilters && (activeFilterArray[index].length <= 0)
    }
    let filteredTablets = [];
    if (!noActivefilters) {
        for (var categoryIndex in filterCategoriesArray) {
            let category = filterCategoriesArray[categoryIndex]
            switch (category) {
                case "period":
                    filteredTablets = union(filteredTablets, filterKeyValueObjectTablets(activeFilterArray[categoryIndex], periodsObject));
                    break;
                case "CDLI":
                    filteredTablets = union(filteredTablets, filterKeyValueObjectTablets(activeFilterArray[categoryIndex], cdliObject));
                    break;
                default:
                    filteredTablets = union(filteredTablets, filterLanguageTablets(category, activeFilterArray[categoryIndex], languagsObject));
                    break;
            }
        }
        filteredTabletNamesWithUrl = intersect(tabletNamesWithUrl, filteredTablets);
    }
    if (currentKeyword!="") {
        filteredTablets = union(filteredTablets, filterCharacterPostagTablets(currentKeyword, character_postags));
        filteredTabletNamesWithUrl = intersect(tabletNamesWithUrl, filteredTablets);
    }
    return filteredTabletNamesWithUrl;
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

/**
 * init var to save keyword
 */
var currentKeyword = "";
 
 /**
  * updates the current keyword to apply as a tablet filter
  */
function updateKeyword(newKeyword) {
     currentKeyword = newKeyword;
}
 
 /**
  * returns every tablet name that contains the given keyword either as a word, pos, translation or char in character_postags
  */
function filterCharacterPostagTablets(keyword, charPostagObject) {
     let activeTabletNames = [];
     /**
      * disassemble Object - extract values
      */
     let tabletObjectArray = Object.entries(charPostagObject);
     for (currentIndex in tabletObjectArray) {
         let tabletPropertyValues = [];
         let nameObjectTuple = tabletObjectArray[currentIndex];
         let tabletName = nameObjectTuple[0];
         let tabletObject = nameObjectTuple[1];
         let obverseReverseTupleArray = Object.entries(tabletObject);
 
         let charPostagArray = [];
         for (obverseReverseTupleIndex in obverseReverseTupleArray) {
             let obverseReverseTuple = obverseReverseTupleArray[obverseReverseTupleIndex];
             let obverseReverseObject = obverseReverseTuple[1];
             let obverseReverseArray = Object.entries(obverseReverseObject);
             charPostagArray = charPostagArray.concat(obverseReverseArray);
         }
 
         /**
          * returns the property values of a charPostag as an array
          */
         function charPostagToProperties(charPostag) {
             let propertyArray = Object.entries(charPostag);
             let postagPropertyValues = [];
             for (propertyIndex in propertyArray) {
                 let propertyTuple = propertyArray[propertyIndex];
                 postagPropertyValues.push(propertyTuple[1]);
             }
             return postagPropertyValues;
         }
 
         for (charPostagTupleIndex in charPostagArray) {
             let charPostagTuple = charPostagArray[charPostagTupleIndex];
             let charPostagValueArray = charPostagToProperties(charPostagTuple[1])
             for (propertyIndex in charPostagValueArray) {
                 tabletPropertyValues.push(charPostagValueArray[propertyIndex]);
             }
         }
         /**
          * disassembling for single tablet complete - values extracted into var tabletPropertyValues
          */
 
         /**
          * check if keyword is included in values
          */
         for (tabletPropertyValueIndex in tabletPropertyValues) {
             propertyValue = tabletPropertyValues[tabletPropertyValueIndex];
             if (propertyValue.includes(keyword)) {
                 activeTabletNames.push(tabletName);
                 break;
             }
         }
     }
     /**
      * disassembling for all tablets complete - tablet names filtered and saved in activeTabletNames
      */
     return activeTabletNames;
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
    filterLanguageTablets: filterLanguageTablets,
    intersect: intersect,
    union: union,
    getfilteredTabletNames: getfilteredTabletNames,
    filterSuggestions: filterSuggestions,
    concatFirst: concatFirst,
    markUnassigned: markUnassigned,
    filterCharacterPostagTablets: filterCharacterPostagTablets,
    updateKeyword: updateKeyword,
    currentKeyword: currentKeyword
}