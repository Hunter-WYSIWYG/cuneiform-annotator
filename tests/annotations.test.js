/**
 * @jest-environment jsdom
 */

const showAnnotationPage = require('../js/annotation/showAnno');
const calculateFilterModalState = require('../js/nav/navigateFilterModal');

/**
 * User story #1
 * As a User, I can hide and show annotations in the 2D view so that there is an unedited or a potentially edited image of a tablet shown.
 */

test('change the bool parameter to show or hide annotations', () => {
    var annotationsVisible = true;

    annotationsVisible = showAnnotationPage(annotationsVisible);
    expect(annotationsVisible).toBe(false);
    annotationsVisible = showAnnotationPage(annotationsVisible);
    expect(annotationsVisible).toBe(true);
});

/**
 * User story #2
 * As a User, I can open the filter modal so that i can start applying filters to the set of selectable tablets.
 */

 test('check if filter modal opens and closes', () => {
    var isFilterModalOpen = false;
    isFilterModalOpen = calculateFilterModalState(isFilterModalOpen);
    expect(isFilterModalOpen).toBe(true);
    isFilterModalOpen = calculateFilterModalState(isFilterModalOpen);
    expect(isFilterModalOpen).toBe(false);
});