/**
 * @jest-environment jsdom
 */

/**
 * User story #3
 * As a User, I can navigate from the landing page to the annotation page so that I can start working with the given tools.
 */

 const goToAnntotationPage = require('../js/nav/landingToAnnotation');

 test('initiate the fadeout of the landing page and activate scrollbars', () => {
    const htmlBody = document.createElement("body");
    htmlBody.classList.add("landing-overflow-hidden");
    const htmlLandingContainer = document.createElement("div");

    goToAnntotationPage(htmlLandingContainer, htmlBody);

    expect(htmlBody.classList.contains("landing-overflow-hidden")).toBe(false);
    expect(htmlLandingContainer.classList.contains("fadeout")).toBe(true);
});