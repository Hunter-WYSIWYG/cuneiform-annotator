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

var distinctPeriods = sortByPeriod(removeEmpty(eliminateDuplicates(Object.values(periods))));

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
 * filter the urls with the current filter
 * 
 * still needed for 3D!!!
 */
function filterSuggestions(currentPeriodFilter) {
    if (currentPeriodFilter != "None") {
        var filteredTabletNames = concatFirst(filteredPeriodTuples(currentPeriodFilter));
        var filteredUrlArray = Object.entries(urls).filter(function(urlArray) {
            return (filteredTabletNames.includes(urlArray[0]));
        });
        currentUrls = Object.fromEntries(filteredUrlArray);
    }
}

/**
"HS_0044": {
    "label": "HS_0044",
    "variants": [
      {
        "label": "HS_0044_01_top.png",
        "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1107976:570673/full/full/0/default.jpg"
      },
      {
        "label": "HS_0044_02_left.png",
        "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1107977:570674/full/full/0/default.jpg"
      },
      {
        "label": "HS_0044_04_right.png",
        "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1107978:570675/full/full/0/default.jpg"
      },
      {
        "label": "HS_0044_05_bottom.png",
        "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1107979:570676/full/full/0/default.jpg"
      },
      {
        "label": "HS_0044_06_back.png",
        "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1107980:570677/full/full/0/default.jpg"
      },
      {
        "label": "HS_0044_03_front.png",
        "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1108249:570905/full/full/0/default.jpg"
      }
    ]
  },
 */

var filtered3DUrls = hs23D;
/**
"HS_1032B_1": {
    "url": "https://heidicon.ub.uni-heidelberg.de/api/v1/objects/uuid/c84682a4-cf39-4a88-8015-49f664801495/file/id/591868/file_version/name/original/",
    "bbox": {
      "min": [
        -20.921693801879883,
        0,
        -8.682990074157715
      ],
      "max": [
        20.921693801879883,
        45.417762756347656,
        8.682990074157715
      ]
    }
  },
 */