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

var distinctPeriods =
  sortByPeriod(
    removeEmpty(
      eliminateDuplicates(
        Object.values(periods)
      )
    )
  );
var distinctLanguages = reduceToDistinctField(languages, 'language');
var distinctProvenience = reduceToDistinctField(languages, 'provenience');
var distinctGenre = reduceToDistinctField(languages, 'genre');
var distinctMaterial = reduceToDistinctField(languages, 'material');
var filterCategories = ["period","language","provenience","genre","material"]

/**
 * returns an array of all period tuples that match the period filter
 */
 function filteredPeriodTuples(periodFilter) {
    var periodsArray = Object.entries(periods);
    return periodsArray.filter(function(periodTuple) {
        return periodTuple[1] == periodFilter;
    })
}

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
 * apply the current filter to the current urls
 */
function filterSuggestions(currentPeriodFilter, currentLanguageFilter) {
    var filteredTabletNames = concatFirst(filteredPeriodTuples(currentPeriodFilter));

    var filtered2DUrls = Object.entries(urls).filter(function(urlArray) {
        return (filteredTabletNames.includes(urlArray[0]));
    });
    currentUrls = Object.fromEntries(filtered2DUrls);

    var filtered3DUrls = Object.entries(hs23D).filter(function(urlArray) {
        return (filteredTabletNames.includes(urlArray[0]));
    });
    current3DUrls = Object.fromEntries(filtered3DUrls);
}