/**
 * @jest-environment jsdom
 */

/**
 * import extern variables
 */
const filterCategories = require('../js/filter/categories');
const urls = require('../js/newurls');
const hs23D = require('../js/hs23D');
const periods = require('../js/periods');
const languages = require('../js/languages');

/**
 * import filter functions
 */
const { eliminateDuplicates } = require('../js/filter/filter');
const { extractNumbers } = require('../js/filter/filter');
const { getPeriodBegin } = require('../js/filter/filter');
const { sortByPeriod } = require('../js/filter/filter');
const { mapToField } = require('../js/filter/filter');
const { reduceToDistinctField } = require('../js/filter/filter');
const { reduceToDistinctPeriods } = require('../js/filter/filter');
const { concatFirst } = require('../js/filter/filter');
const { filterPeriodTuples } = require('../js/filter/filter');
const { filterPeriodTabletNames } = require('../js/filter/filter');
const { filterLanguageObjects } = require('../js/filter/filter');
const { filterLanguageTabletNames } = require('../js/filter/filter');
const { intersect } = require('../js/filter/filter');
const { union } = require('../js/filter/filter');
const { getfilteredTabletNames } = require('../js/filter/filter');
const { filterSuggestions } = require('../js/filter/filter');
const { markUnassigned } = require('../js/filter/filter');

let periodsObject = {
    "HS_2440": "Ur III (ca. 2100-2000 BC)",
    "HS_230": "Old Babylonian (ca. 1900-1600 BC)",
    "HS_1326": "Old Babylonian (ca. 1900-1600 BC)",
    "HS_1006": "Ur III (ca. 2100-2000 BC)",
    "HS_1298": "Ur III (ca. 2100-2000 BC)",
    "HS_1338": "Ur III (ca. 2100-2000 BC)",
    "HS_1706": "",
    "HS_2398": "Early Old Babylonian (ca. 2000-1900 BC)",
    "HS_854": "ED IIIb (ca. 2500-2340 BC)"
}

let languageObject = {
    "HS_2440": {
      "genre": "Administrative",
      "subgenre": "",
      "language": "Sumerian",
      "material": "clay",
      "provenience": "Puzri\u0161-Dagan (mod. Drehem)"
    },
    "HS_230": {
      "genre": "Mathematical",
      "subgenre": "",
      "language": "",
      "material": "clay",
      "provenience": "Nippur (mod. Nuffar)"
    },
    "HS_1706": {
        "genre": "Lexical",
        "subgenre": "Obv: P-Izi 1; Rev: P-Izi 1",
        "language": "Sumerian",
        "material": "clay",
        "provenience": "Nippur (mod. Nuffar) ?"
    },
    "HS_1326": {
      "genre": "Administrative",
      "subgenre": "",
      "language": "Sumerian",
      "material": "clay",
      "provenience": "Nippur (mod. Nuffar)"
    }
}

test('eliminate duplicates from an array', () => {
    const distinctArray = eliminateDuplicates(["cheese","lemon","bread","cheese","cheese","apple","tomato","bread","cheese","raspberries","tomato"]);
    expect(distinctArray).toStrictEqual(["cheese","lemon","bread","apple","tomato","raspberries"]);
});

test('extract numbers from a string into an array', () => {
    const extractedNumbers = extractNumbers("Hellenistic (323-63 BC)");
    expect(extractedNumbers).toStrictEqual([323,63]);
});

test('extract the begin of a period from a period string', () => {
    const periodBegin = getPeriodBegin("Hellenistic (323-63 BC)");
    expect(periodBegin).toStrictEqual(323);
});

test('sort period names by period begin, starting with the latest', () => {
    const sortedPeriods = sortByPeriod([
        "Hellenistic (323-63 BC)",
        "Ur III (ca. 2100-2000 BC)",
        "Middle Babylonian (ca. 1400-1100 BC)",
        "ED IIIb (ca. 2500-2340 BC)",
        "Neo-Assyrian (ca. 911-612 BC)",
        "Achaemenid (547-331 BC)",
        "Old Akkadian (ca. 2340-2200 BC)"
    ]
    );
    const testPeriodsArray = [
        "Hellenistic (323-63 BC)",
        "Achaemenid (547-331 BC)",
        "Neo-Assyrian (ca. 911-612 BC)",
        "Middle Babylonian (ca. 1400-1100 BC)",
        "Ur III (ca. 2100-2000 BC)",
        "Old Akkadian (ca. 2340-2200 BC)",
        "ED IIIb (ca. 2500-2340 BC)"
    ]
    expect(sortedPeriods).toStrictEqual(testPeriodsArray);
});

test('map an array of language objects to an array of strings of one specified language object field', () => {
    const genreArray = mapToField(Object.values(languageObject), "genre");
    const testGenreArray = [
        "Administrative",
        "Mathematical",
        "Lexical",
        "Administrative",
    ]
    expect(genreArray).toStrictEqual(testGenreArray);

    const provenienceArray = mapToField(Object.values(languageObject), "provenience");
    const testProvenienceArray = [
        "Puzri\u0161-Dagan (mod. Drehem)",
        "Nippur (mod. Nuffar)",
        "Nippur (mod. Nuffar) ?",
        "Nippur (mod. Nuffar)",
    ]
    expect(provenienceArray).toStrictEqual(testProvenienceArray);
});

test('reduce a language object to a sorted array of distinct values of a specified field', () => {
    let languageObject = {
        "HS_2440": {
          "genre": "Administrative",
          "subgenre": "",
          "language": "Sumerian",
          "material": "clay",
          "provenience": "Puzri\u0161-Dagan (mod. Drehem)"
        },
        "HS_230": {
          "genre": "Mathematical",
          "subgenre": "",
          "language": "",
          "material": "clay",
          "provenience": "Nippur (mod. Nuffar)"
        },
        "HS_1706": {
            "genre": "Lexical",
            "subgenre": "Obv: P-Izi 1; Rev: P-Izi 1",
            "language": "Sumerian",
            "material": "clay",
            "provenience": "Nippur (mod. Nuffar) ?"
        },
        "HS_1326": {
          "genre": "Administrative",
          "subgenre": "",
          "language": "Sumerian",
          "material": "clay",
          "provenience": "Nippur (mod. Nuffar)"
        }
    }
    const distinctGenreArray = reduceToDistinctField(languageObject, "genre");
    const testDistinctGenreArray = [
        "Administrative",
        "Lexical",
        "Mathematical"
    ]
    expect(distinctGenreArray).toStrictEqual(testDistinctGenreArray);

    const distinctLaguageArray = reduceToDistinctField(languageObject, "language");
    const testDistinctLaguageArray = [
        "Sumerian",
        "unassigned"
    ]
    expect(distinctLaguageArray).toStrictEqual(testDistinctLaguageArray);
});

test('reduce the periods object to an array of distinct period names sorted by period begin', () => {
    const distinctPeriodNames = reduceToDistinctPeriods(periodsObject);
    const testDistinctPeriodNames = [
        "Old Babylonian (ca. 1900-1600 BC)",
        "Early Old Babylonian (ca. 2000-1900 BC)",
        "Ur III (ca. 2100-2000 BC)",
        "ED IIIb (ca. 2500-2340 BC)",
        "",
    ]
    expect(distinctPeriodNames).toStrictEqual(testDistinctPeriodNames);
});

test('concat the first element of every array in an array of arrays into a new array', () => {
    let nestedArray = [[1,2],[7,5],[4,8]];
    const concatFirstArray = concatFirst(nestedArray);
    const testConcatFirstArray = [1,7,4];
    expect(concatFirstArray).toStrictEqual(testConcatFirstArray);
});

test('returns an array of tablet names that match the given period filter', () => {
    const tabletNames = filterPeriodTuples("Ur III (ca. 2100-2000 BC)", periodsObject);
    const testTabletNames = [
        "HS_2440",
        "HS_1006",
        "HS_1298",
        "HS_1338"
    ];
    expect(tabletNames).toStrictEqual(testTabletNames);
});

test('return an array of tablet names that fit at least one period filter', () => {
    let periodNames = [
        "Old Babylonian (ca. 1900-1600 BC)",
        "Early Old Babylonian (ca. 2000-1900 BC)",
        "ED IIIb (ca. 2500-2340 BC)"
    ];
    const tabletNames = filterPeriodTabletNames(periodNames, periodsObject);
    const testTabletNames = [
        "HS_230",
        "HS_1326",
        "HS_2398",
        "HS_854"
    ];
    expect(tabletNames).toStrictEqual(testTabletNames);
});

test('return an array of tablet names that match the given filter of this category for language objects', () => {
    const tabletNamesGenre = filterLanguageObjects("genre", "Administrative", languageObject);
    const testTabletNamesGenre = [
        "HS_2440",
        "HS_1326"
    ];
    expect(tabletNamesGenre).toStrictEqual(testTabletNamesGenre);

    const tabletNamesLanguage = filterLanguageObjects("language", "Sumerian", languageObject);
    const testTabletNamesLanguage = [
        "HS_2440",
        "HS_1706",
        "HS_1326"
    ];
    expect(tabletNamesLanguage).toStrictEqual(testTabletNamesLanguage);
});

test('return an array of tablet names that match every filter of this category for language objects', () => {
    const tabletNamesGenre = filterLanguageTabletNames("genre", ["Administrative","Lexical"], languageObject);
    const testTabletNamesGenre = [
        "HS_2440",
        "HS_1326",
        "HS_1706",
    ];
    expect(tabletNamesGenre).toStrictEqual(testTabletNamesGenre);

    const tabletNamesProvenience = filterLanguageTabletNames("provenience", ["Nippur (mod. Nuffar)", "Puzri\u0161-Dagan (mod. Drehem)"], languageObject);
    const testtabletNamesProvenience = [
        "HS_230",
        "HS_1326",
        "HS_2440"
    ];
    expect(tabletNamesProvenience).toStrictEqual(testtabletNamesProvenience);
});

test('return the intersection of 2 arrays', () => {
    const intersectedArray = intersect([1,2,3,4,5,5,6,7],[0,3,8,4,5,7,8]);
    expect(intersectedArray).toStrictEqual([3,4,5,7]);
});

test('return the union of 2 arrays', () => {
    const unionArray = union([1,2,3,4,5,5,6,7],[0,3,8,4,5,7,8]);
    expect(unionArray).toStrictEqual([0,1,2,3,4,5,6,7,8]);
});

test('filters tablet names with given parameters', () => {
    let activeFilterArray = [["Hellenistic (323-63 BC)"],[],[],[],[]];
    const filteredTabletNames = getfilteredTabletNames(activeFilterArray, filterCategories, urls, periods, languages);
    expect(filteredTabletNames).toStrictEqual(["HS_0748"]);
});

test('map every empty string to "unassigned"', () => {
    const unassignedArray = markUnassigned(["abc","","","123","qwertz",""]);
    expect(unassignedArray).toStrictEqual(["abc","unassigned","unassigned","123","qwertz","unassigned"]);
});

test('returns a tuple of filtered 2d and 3d url objects', () => {
    const activeFilterArray = [
        ["Hellenistic (323-63 BC)","Middle Hittite (ca. 1500-1100 BC)"],
        ["Hittite"],
        [],
        ["Prayer/Incantation","Scientific"],
        ["stone: steatite"]
    ]
    const urlTuple = filterSuggestions(activeFilterArray, filterCategories, urls, hs23D, periods, languages);
    const testUrlTuple = [ Url2DObject, Url3DObject ]
    expect(urlTuple[0]).toMatchObject(testUrlTuple[0]);
    expect(urlTuple[1]).toMatchObject(testUrlTuple[1]);
});

var Url2DObject = {
    "HS_0748": {
        "label": "HS_0748",
        "variants": [
            {
                "label": "HS_0748_01_top.png",
                "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1111129:575284/full/full/0/default.jpg"
            },
            {
                "label": "HS_0748_02_left.png",
                "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1111130:575285/full/full/0/default.jpg"
            },
            {
                "label": "HS_0748_03_front.png",
                "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1111131:575286/full/full/0/default.jpg"
            },
            {
                "label": "HS_0748_04_right.png",
                "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1111132:575287/full/full/0/default.jpg"
            },
            {
                "label": "HS_0748_05_bottom.png",
                "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1111133:575288/full/full/0/default.jpg"
            },
            {
                "label": "HS_0748_06_back.png",
                "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1111134:575289/full/full/0/default.jpg"
            }
        ]
    },
    "HS_1512": {
        "label": "HS_1512",
        "variants": [
          {
            "label": "HS_1512_01_top.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116002:580123/full/full/0/default.jpg"
          },
          {
            "label": "HS_1512_02_left.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116003:580126/full/full/0/default.jpg"
          },
          {
            "label": "HS_1512_03_front.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116004:580127/full/full/0/default.jpg"
          },
          {
            "label": "HS_1512_04_right.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116005:580128/full/full/0/default.jpg"
          },
          {
            "label": "HS_1512_05_bottom.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116006:580129/full/full/0/default.jpg"
          },
          {
            "label": "HS_1512_06_back.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116007:580130/full/full/0/default.jpg"
          }
        ]
    },
    "HS_1556": {
        "label": "HS_1556",
        "variants": [
          {
            "label": "HS_1556_01_top.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116186:580332/full/full/0/default.jpg"
          },
          {
            "label": "HS_1556_02_left.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116187:580333/full/full/0/default.jpg"
          },
          {
            "label": "HS_1556_03_front.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116188:580334/full/full/0/default.jpg"
          },
          {
            "label": "HS_1556_04_right.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116189:580335/full/full/0/default.jpg"
          },
          {
            "label": "HS_1556_05_bottom.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116190:580336/full/full/0/default.jpg"
          },
          {
            "label": "HS_1556_06_back.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1116191:580337/full/full/0/default.jpg"
          }
        ]
    },
    "HS_1883": {
        "label": "HS_1883",
        "variants": [
          {
            "label": "HS_1883_01_top.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118218:582594/full/full/0/default.jpg"
          },
          {
            "label": "HS_1883_02_left.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118219:582595/full/full/0/default.jpg"
          },
          {
            "label": "HS_1883_03_front.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118220:582596/full/full/0/default.jpg"
          },
          {
            "label": "HS_1883_04_right.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118221:582597/full/full/0/default.jpg"
          },
          {
            "label": "HS_1883_05_bottom.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118222:582598/full/full/0/default.jpg"
          },
          {
            "label": "HS_1883_06_back.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118223:582599/full/full/0/default.jpg"
          }
        ]
    },
    "HS_1965": {
        "label": "HS_1965",
        "variants": [
          {
            "label": "HS_1965_01_top.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118667:583036/full/full/0/default.jpg"
          },
          {
            "label": "HS_1965_02_left.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118668:583037/full/full/0/default.jpg"
          },
          {
            "label": "HS_1965_03_front.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118669:583038/full/full/0/default.jpg"
          },
          {
            "label": "HS_1965_04_right.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118670:583039/full/full/0/default.jpg"
          },
          {
            "label": "HS_1965_05_bottom.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118671:583040/full/full/0/default.jpg"
          },
          {
            "label": "HS_1965_06_back.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1118672:583041/full/full/0/default.jpg"
          }
        ]
    },
    "HS_325": {
        "label": "HS_325",
        "variants": [
          {
            "label": "HS_325_01_top.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123470:587789/full/full/0/default.jpg"
          },
          {
            "label": "HS_325_02_left.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123471:587790/full/full/0/default.jpg"
          },
          {
            "label": "HS_325_03_front.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123472:587791/full/full/0/default.jpg"
          },
          {
            "label": "HS_325_04_right.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123473:587792/full/full/0/default.jpg"
          },
          {
            "label": "HS_325_05_bottom.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123474:587793/full/full/0/default.jpg"
          },
          {
            "label": "HS_325_06_back.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123475:587794/full/full/0/default.jpg"
          }
        ]
    },
    "HS_326": {
        "label": "HS_326",
        "variants": [
          {
            "label": "HS_326_01_top.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123478:587798/full/full/0/default.jpg"
          },
          {
            "label": "HS_326_02_left.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123479:587799/full/full/0/default.jpg"
          },
          {
            "label": "HS_326_03_front.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123480:587800/full/full/0/default.jpg"
          },
          {
            "label": "HS_326_04_right.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123481:587801/full/full/0/default.jpg"
          },
          {
            "label": "HS_326_05_bottom.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123482:587802/full/full/0/default.jpg"
          },
          {
            "label": "HS_326_06_back.png",
            "url": "https://heidicon.ub.uni-heidelberg.de/iiif/2/1123483:587803/full/full/0/default.jpg"
          }
        ]
    },
}

var Url3DObject = {
    "HS_0748": {
        "url": "https://heidicon.ub.uni-heidelberg.de/eas/partitions/3/0/575000/575283/b5a4f6345b087b803341f39438346f8e42716d82/application/x-ply/HS_0748_HeiCuBeDa_GigaMesh.ply",
        "bbox": {
          "min": [
            -47.84576416015625,
            0,
            -17.06745147705078
          ],
          "max": [
            47.84576416015625,
            84.68763732910156,
            17.06745147705078
          ]
        }
    },
    "HS_1512": {
        "url": "https://heidicon.ub.uni-heidelberg.de/eas/partitions/1/0/580000/580125/efb7d3fe30e9f3701a7388cd7781f5f6b018a848/application/x-ply/HS_1512_HeiCuBeDa_GigaMesh.ply",
        "bbox": {
          "min": [
            -32.19923400878906,
            0,
            -11.353035926818848
          ],
          "max": [
            32.19923400878906,
            56.860572814941406,
            11.353035926818848
          ]
        }
    },
    "HS_1556": {
        "url": "https://heidicon.ub.uni-heidelberg.de/eas/partitions/1/0/580000/580331/14e78f4847d3580d061f43b68f768ffdfed770de/application/x-ply/HS_1556_HeiCuBeDa_GigaMesh.ply",
        "bbox": {
          "min": [
            -21.59473991394043,
            0,
            -9.948512077331543
          ],
          "max": [
            21.59473991394043,
            88.87762451171875,
            9.948512077331543
          ]
        }
    },
    "HS_1883": {
        "url": "https://heidicon.ub.uni-heidelberg.de/eas/partitions/1/0/582000/582602/1e78e86882f89450296be7d7d5ab8634e4e2a9dc/application/x-ply/HS_1883_HeiCuBeDa_GigaMesh.ply"
    },
    "HS_1965": {
        "url": "https://heidicon.ub.uni-heidelberg.de/eas/partitions/3/0/583000/583035/117794c760417cac8944492e9c2f95e26c53807f/application/x-ply/HS_1965_HeiCuBeDa_GigaMesh.ply"
    },
}