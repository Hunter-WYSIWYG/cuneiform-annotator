/**
 * init var to save keyword and clear input
 */
var currentKeyword = "";
document.getElementById('keywordInput').value = "";

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
    filterCharacterPostagTablets: filterCharacterPostagTablets,
    updateKeyword: updateKeyword,
    currentKeyword: currentKeyword
}