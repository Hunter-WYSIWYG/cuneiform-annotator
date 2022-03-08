/**
 * @jest-environment jsdom
 */

/**
 * User story #1
 * As a User, I can hide and show annotations in the 2D view so that there is an unedited or a potentially edited image of a tablet shown.
 */

 const negateBool = require('../js/annotation/showAnno');

test('change the bool parameter to show or hide annotations', () => {
    var annotationsVisible = true;

    annotationsVisible = negateBool(annotationsVisible);
    expect(annotationsVisible).toBe(false);
    annotationsVisible = negateBool(annotationsVisible);
    expect(annotationsVisible).toBe(true);
});