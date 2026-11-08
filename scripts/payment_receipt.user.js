// ==UserScript==
// @name         BLS Payment Receipt Helper
// @namespace    https://github.com/nagatoara4/bls-algeria-appointment-engine
// @version      1.0
// @description  Auto-print and copy payment link token on CMI payment page
// @author       ylivo4real
// @match        https://payment.cmi.co.ma/*
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  // Auto print if receipt is present (page is short-lived)
  if (document.querySelector("#print")) {
    window.print();
  }

  const tokenInput = document.querySelector("input[name=paymentLinkToken]");
  if (tokenInput && tokenInput.value) {
    const url = "https://payment.cmi.co.ma/fim/paymentLinkService?token=" + tokenInput.value;
    console.log("Payment link:", url);
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => {
        console.log("Payment link copied to clipboard");
      }).catch(() => {});
    }
  }
})();
