// ==UserScript==
// @name         Lemmy Enhancements
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  A suite of enhancements for Lemmy, the federated reddit alternative.
// @author       Artillect
// @match        https://kbin.social/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=kbin.social
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // For each post, unroll the more dropdown into a list of buttons.
    document.querySelectorAll('article .dropdown__menu').forEach((dropdown) => {
        // Move child li elements to the parent ul.
        dropdown.querySelectorAll('li').forEach((li) => {
            dropdown.parentElement.parentElement.appendChild(li);
        });
    });
    // Delete the now empty dropdowns.
    document.querySelectorAll('article .dropdown').forEach((dropdown) => {
        dropdown.remove();
    });
})();