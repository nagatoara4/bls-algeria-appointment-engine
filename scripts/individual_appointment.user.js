// ==UserScript==
// @name         BLS Appointment Helper (Improved)
// @namespace    https://github.com/nagatoara4/bls-algeria-appointment-engine
// @version      1.1
// @description  Auto-fill helper for BLS appointment pages (educational)
// @author       ylivo4real
// @match        *://*.blsspainmorocco.com/*
// @match        *://*.blsspainvisa.com/*
// @match        *://*.blsinternational.com/*
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  // ========== CONFIGURE YOUR DATA HERE ==========
  const PROFILE = {
    firstName: "First Name",
    lastName: "Last Name",
    birth: "1990-01-15",
    passport: "A12345678",
    issueDate: "2020-01-01",
    expiryDate: "2030-01-01",
    issuePlace: "Algiers",
    visaTypeIndex: 1
  };
  // ===============================================

  function tryFill() {
    const dateInput = document.getElementById("app_date");
    if (!dateInput) return;

    // Extract available_dates from page scripts if present
    let code = "";
    for (const s of document.scripts) {
      if (s.text && s.text.includes("available_dates")) {
        code = s.text;
        break;
      }
    }

    if (code && dateInput.value.length === 0) {
      const bgn = code.indexOf("available_dates");
      const end = code.indexOf("fullCapicity_dates");
      if (bgn !== -1 && end !== -1) {
        const table = code.slice(bgn + 20, end - 9);
        if (table) {
          const datee = table.slice(0, 10);
          const dd = datee.slice(0, 2);
          const mm = datee.slice(3, 5);
          const yyyy = datee.slice(6, 10);
          const finDate = `${yyyy}-${mm}-${dd}`;
          if (typeof $ !== "undefined" && $.fn.datepicker) {
            $("#app_date").datepicker("update", finDate);
          } else {
            dateInput.value = finDate;
          }
        }
      }
    }

    // Fill personal fields if date is set
    if (dateInput.value.length > 0) {
      setVal("first_name", PROFILE.firstName);
      setVal("last_name", PROFILE.lastName);
      setDate("dateOfBirth", PROFILE.birth);
      setVal("passport_no", PROFILE.passport);
      setDate("pptIssueDate", PROFILE.issueDate);
      setDate("pptExpiryDate", PROFILE.expiryDate);
      setVal("pptIssuePalace", PROFILE.issuePlace);

      const timeSel = document.getElementById("app_time");
      if (timeSel && timeSel.length > 1) {
        timeSel.selectedIndex = timeSel.length - 1;
      }
      const visaSel = document.getElementById("VisaTypeId");
      if (visaSel) visaSel.selectedIndex = PROFILE.visaTypeIndex;
    }
  }

  function setVal(id, value) {
    const el = document.getElementById(id);
    if (el) el.value = value;
  }

  function setDate(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    if (typeof $ !== "undefined" && $.fn.datepicker) {
      $(`#${id}`).datepicker("update", value);
    } else {
      el.value = value;
    }
  }

  // Run periodically
  setInterval(tryFill, 2000);
  tryFill();
})();
