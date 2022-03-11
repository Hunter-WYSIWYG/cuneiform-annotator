/**
 * track if filter modal is open
 */
var isFilterModalOpen = false;

/**
 * assigns the new filter modal state
 */
function updateFilterModalState() {
    isFilterModalOpen = calculateFilterModalState(isFilterModalOpen);
    console.log(isFilterModalOpen);
}

/**
 * update filter modal state
 */
function calculateFilterModalState(oldState) {
    return !oldState;
}

module.exports = calculateFilterModalState