/**
 * Main application coordinator for Jyotishyam Web Platform.
 */

window.currentKundaliData = null;
let currentChartFormat = "south"; // 'south' or 'north'
let currentChartType = "d1";      // 'd1' or 'd9'

document.addEventListener("DOMContentLoaded", () => {
  initGlobalNavigation();
  initGenderToggle();
  initCityAutocomplete();
  initFormSubmit();
  initAnalysisModeToggle();
  initCoupleModule();
  initFamilyModule();
  initTabNavigation();
  initChartControls();
  initPrintButton();
  initPrashnaModule();
  initShishuModule();
  initEclipsesModule();
  initMuhurtamModule();
  initLanguageSelector();
});

function initPrintButton() {
  const btn = document.getElementById("btnPrintReport") || document.getElementById("btnPrintBooklet");
  if (btn) {
    btn.addEventListener("click", () => {
      window.print();
    });
  }
}

/* 1. Gender Selector */
function initGenderToggle() {
  const btns = document.querySelectorAll(".gender-btn");
  const hiddenInput = document.getElementById("genderInput");

  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      btns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      hiddenInput.value = btn.getAttribute("data-val");
    });
  });
}

/* 2. City Autocomplete (Universal Worldwide) */
async function resolveCityOnline(q) {
  try {
    const resp = await fetch(`/api/v1/cities/search?q=${encodeURIComponent(q)}`);
    if (!resp.ok) return [];
    const data = await resp.json();
    return Array.isArray(data) ? data : (data.cities || []);
  } catch (err) {
    console.error("City search error:", err);
    return [];
  }
}

async function ensureCityResolved(inputId, latId, lonId, tzId, feedbackChipId = null) {
  const cityInput = document.getElementById(inputId);
  const latInput = document.getElementById(latId);
  const lonInput = document.getElementById(lonId);
  const tzInput = document.getElementById(tzId);
  const feedbackChip = feedbackChipId ? document.getElementById(feedbackChipId) : null;

  if (!cityInput) return;
  const q = cityInput.value.trim();
  if (q.length < 2) return;

  // Check if current text matches the already recorded selection
  if (cityInput.dataset.selectedText && cityInput.dataset.selectedText.toLowerCase() === q.toLowerCase()) {
    return;
  }

  const cities = await resolveCityOnline(q);
  if (cities && cities.length > 0) {
    const c = cities[0];
    cityInput.value = `${c.name}, ${c.state || c.country}`;
    cityInput.dataset.selectedText = cityInput.value;
    if (latInput) latInput.value = c.lat;
    if (lonInput) lonInput.value = c.lon;
    if (tzInput) tzInput.value = c.tz;

    if (feedbackChip) {
      feedbackChip.innerHTML = `📍 స్థలం: <strong>${c.name}, ${c.state || c.country}</strong> (${c.lat.toFixed(2)}° N, ${c.lon.toFixed(2)}° E, IST +${c.tz}) ✓`;
    }

    // Eclipse-specific auto sync
    if (inputId === "eclipseCity") {
      const countrySel = document.getElementById("eclipseCountry");
      const tzEl = document.getElementById("eclipseTz");
      const tzOffsetEl = document.getElementById("eclipseTzOffset");
      if ((c.country && (c.country.toLowerCase() === "india" || c.country === "IN")) || c.tz === 5.5) {
        if (countrySel) countrySel.value = "IN";
        if (tzEl) tzEl.value = "Asia/Kolkata";
        if (tzOffsetEl) tzOffsetEl.value = "5.5";
      } else if (c.country && (c.country.toLowerCase() === "usa" || c.country === "US")) {
        if (countrySel) countrySel.value = "US";
      }
    }
  }
}

function setupCityAutocomplete(inputId, suggestionsBoxId, latId, lonId, tzId, feedbackChipId = null) {
  const cityInput = document.getElementById(inputId);
  const suggestionsBox = document.getElementById(suggestionsBoxId);
  const latInput = document.getElementById(latId);
  const lonInput = document.getElementById(lonId);
  const tzInput = document.getElementById(tzId);
  const feedbackChip = feedbackChipId ? document.getElementById(feedbackChipId) : null;

  if (!cityInput || !suggestionsBox) return;

  let debounceTimer;
  let currentCities = [];
  let highlightedIndex = -1;

  function selectCity(c) {
    cityInput.value = `${c.name}, ${c.state || c.country}`;
    cityInput.dataset.selectedText = cityInput.value;
    if (latInput) latInput.value = c.lat;
    if (lonInput) lonInput.value = c.lon;
    const tzVal = (typeof c.tz === 'number') ? c.tz : (c.tz_offset !== undefined && c.tz_offset !== null ? c.tz_offset : (c.tz === 'Asia/Kolkata' ? 5.5 : 5.5));
    if (tzInput) tzInput.value = tzVal;

    if (feedbackChip) {
      feedbackChip.innerHTML = `📍 స్థలం: <strong>${c.name}, ${c.state || c.country}</strong> (${c.lat.toFixed(2)}° N, ${c.lon.toFixed(2)}° E, IST +${tzVal}) ✓`;
    }

    // Eclipse auto sync
    if (inputId === "eclipseCity") {
      const countrySel = document.getElementById("eclipseCountry");
      const tzEl = document.getElementById("eclipseTz");
      const tzOffsetEl = document.getElementById("eclipseTzOffset");
      if ((c.country && (c.country.toLowerCase() === "india" || c.country === "IN")) || c.tz === 5.5) {
        if (countrySel) countrySel.value = "IN";
        if (tzEl) tzEl.value = "Asia/Kolkata";
        if (tzOffsetEl) tzOffsetEl.value = "5.5";
      } else if (c.country && (c.country.toLowerCase() === "usa" || c.country === "US")) {
        if (countrySel) countrySel.value = "US";
      }
    }

    suggestionsBox.style.display = "none";
    currentCities = [];
    highlightedIndex = -1;
  }

  cityInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    const q = cityInput.value.trim();
    if (q.length < 2) {
      suggestionsBox.style.display = "none";
      currentCities = [];
      highlightedIndex = -1;
      return;
    }

    debounceTimer = setTimeout(async () => {
      currentCities = await resolveCityOnline(q);
      renderSuggestions(currentCities);
    }, 200);
  });

  function renderSuggestions(cities) {
    suggestionsBox.innerHTML = "";
    highlightedIndex = -1;
    if (!cities || cities.length === 0) {
      suggestionsBox.style.display = "none";
      return;
    }

    cities.forEach((c, idx) => {
      const item = document.createElement("div");
      item.className = "city-item";
      item.setAttribute("data-index", idx);
      item.innerHTML = `<strong>${c.name}</strong>, <small>${c.state ? c.state + ', ' : ''}${c.country}</small>`;

      // Use pointerdown/mousedown for instantaneous response before blur
      item.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        selectCity(c);
      });
      item.addEventListener("click", (e) => {
        e.preventDefault();
        selectCity(c);
      });

      suggestionsBox.appendChild(item);
    });
    suggestionsBox.style.display = "block";
  }

  // Keyboard navigation: ArrowDown, ArrowUp, Enter, Escape
  cityInput.addEventListener("keydown", async (e) => {
    const isVisible = suggestionsBox.style.display === "block" && currentCities.length > 0;

    if (e.key === "ArrowDown") {
      if (!isVisible) return;
      e.preventDefault();
      highlightedIndex++;
      if (highlightedIndex >= currentCities.length) highlightedIndex = 0;
      updateHighlight();
    } else if (e.key === "ArrowUp") {
      if (!isVisible) return;
      e.preventDefault();
      highlightedIndex--;
      if (highlightedIndex < 0) highlightedIndex = currentCities.length - 1;
      updateHighlight();
    } else if (e.key === "Enter") {
      if (isVisible) {
        e.preventDefault(); // Stop premature form submission
        const chosen = highlightedIndex >= 0 ? currentCities[highlightedIndex] : currentCities[0];
        if (chosen) selectCity(chosen);
      } else {
        // Dropdown not open; resolve before submitting
        const q = cityInput.value.trim();
        if (q.length >= 2 && (!cityInput.dataset.selectedText || cityInput.dataset.selectedText.toLowerCase() !== q.toLowerCase())) {
          e.preventDefault();
          await ensureCityResolved(inputId, latId, lonId, tzId, feedbackChipId);
          // Now submit form programmatically
          if (cityInput.form) {
            cityInput.form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
          }
        }
      }
    } else if (e.key === "Escape") {
      suggestionsBox.style.display = "none";
      highlightedIndex = -1;
    }
  });

  function updateHighlight() {
    const items = suggestionsBox.querySelectorAll(".city-item");
    items.forEach((item, idx) => {
      if (idx === highlightedIndex) {
        item.classList.add("active-highlight");
        item.scrollIntoView({ block: "nearest" });
      } else {
        item.classList.remove("active-highlight");
      }
    });
  }

  // Auto-resolve on blur if user typed city without clicking
  cityInput.addEventListener("blur", () => {
    setTimeout(async () => {
      suggestionsBox.style.display = "none";
      const q = cityInput.value.trim();
      if (q.length >= 2 && (!cityInput.dataset.selectedText || cityInput.dataset.selectedText.toLowerCase() !== q.toLowerCase())) {
        await ensureCityResolved(inputId, latId, lonId, tzId, feedbackChipId);
      }
    }, 250);
  });

  // Close dropdown on outside click
  document.addEventListener("click", (e) => {
    if (!cityInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
      suggestionsBox.style.display = "none";
    }
  });
}

function initCityAutocomplete() {
  setupCityAutocomplete("placeInput", "citySuggestions", "latInput", "lonInput", "tzInput", "placeCityFeedback");
}

/* 3. Form Submit & Kundali Generation */
function initFormSubmit() {
  const form = document.getElementById("kundaliForm");
  const btnSubmit = document.getElementById("btnGenerate");
  const resultsContainer = document.getElementById("resultsContainer");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Ensure any freshly typed city is resolved to correct coordinates before submit
    await ensureCityResolved("placeInput", "latInput", "lonInput", "tzInput", "placeCityFeedback");

    const name = document.getElementById("nameInput").value.trim() || "జాతుకుడు";
    const gender = document.getElementById("genderInput").value;
    const dob = document.getElementById("dobInput").value;
    const tob = document.getElementById("tobInput").value;
    const place = document.getElementById("placeInput").value;
    const lat = parseFloat(document.getElementById("latInput").value) || 17.3850;
    const lon = parseFloat(document.getElementById("lonInput").value) || 78.4867;
    const tz = parseFloat(document.getElementById("tzInput").value) || 5.5;
    const ayanamsa = document.getElementById("ayanamsaSelect").value || "lahiri";

    if (!dob || !tob) {
      alert("దయచేసి జన్మ తేదీ మరియు సమయాన్ని నమోదు చేయండి.");
      return;
    }

    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `<span class="spinner"></span> జాతక చక్రం గణితం చేయబడుతోంది...`;

    try {
      const resp = await fetch("/api/v1/kundali/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          gender: gender,
          dob: dob,
          tob: tob,
          place_name: place,
          latitude: lat,
          longitude: lon,
          timezone_offset: tz,
          ayanamsa: ayanamsa
        })
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || "Calculation error");
      }

      const kundali = await resp.json();
      window.displayFullKundali(kundali, null);

    } catch (err) {
      alert(`లోపం ఏర్పడింది: ${err.message}`);
    } finally {
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = `<span>🕉️</span> జాతక చక్రాన్ని రూపొందించండి (Generate Jatakam)`;
    }
  });
}

window.displayFullKundali = function(kundali, contextInfo = null) {
  if (!kundali) return;
  window.currentKundaliData = kundali;

  const returnBanner = document.getElementById("contextualReturnBanner");
  const returnText = document.getElementById("contextualReturnText");
  const returnBtn = document.getElementById("btnContextualReturn");

  if (contextInfo && returnBanner) {
    if (returnText) returnText.innerHTML = contextInfo.text;
    if (returnBtn && contextInfo.btnText) returnBtn.innerHTML = `<span>🔙</span> <span>${contextInfo.btnText}</span>`;
    window.contextReturnAction = contextInfo.returnAction || null;
    returnBanner.style.display = "flex";
  } else if (returnBanner) {
    returnBanner.style.display = "none";
    window.contextReturnAction = null;
  }

  // Populate UI
  renderNativeSummary(kundali);
  updateKundaliChart();
  renderBhavaSphuta(kundali);
  renderAvakahadaChakra(kundali);
  renderPanchangam(kundali);
  renderPlanetaryTable(kundali);
  renderClassicalTables(kundali);
  renderAshtakavarga(kundali);
  renderDashaTimeline(kundali);
  renderDashaAntardashaPredictions(kundali);
  renderGocharam(kundali);
  renderDoshas(kundali);
  renderYogas(kundali);
  renderPredictions(kundali);

  if (typeof window.renderMuhurtamJatakamAssistant === "function") {
    window.renderMuhurtamJatakamAssistant();
  }
  if (typeof window.updateMuhurtamEventContextCard === "function") {
    const evSelect = document.getElementById("muhurtamEventType");
    window.updateMuhurtamEventContextCard(evSelect ? evSelect.value : "naga_pratishtha");
  }

  const resultsContainer = document.getElementById("resultsContainer");
  if (resultsContainer) {
    resultsContainer.style.display = "block";
    resultsContainer.scrollIntoView({ behavior: "smooth" });
    if (window.currentScript && window.currentScript !== "Telugu") {
      applyTransliterationToPage(resultsContainer);
    }
  }
};

window.returnFromFullKundaliView = function() {
  if (typeof window.contextReturnAction === "function") {
    window.contextReturnAction();
    return;
  }
  const indResults = document.getElementById("resultsContainer");
  const coupleResults = document.getElementById("coupleResultsContainer");
  const famResults = document.getElementById("familyResultsContainer");
  if (window.currentAnalysisMode === "couple" && coupleResults) {
    if (indResults) indResults.style.display = "none";
    coupleResults.style.display = "block";
    coupleResults.scrollIntoView({ behavior: "smooth" });
  } else if (window.currentAnalysisMode === "family" && famResults) {
    if (indResults) indResults.style.display = "none";
    famResults.style.display = "block";
    famResults.scrollIntoView({ behavior: "smooth" });
  }
};

/* 4. Render Native Summary */
function renderNativeSummary(data) {
  if (!data) return;
  const inp = data.input || {};
  const isFemale = (inp.gender && inp.gender.toLowerCase() === "female");
  
  const nameEl = document.getElementById("summaryName");
  if (nameEl) nameEl.textContent = inp.name || "జాతుకుడు";

  const genderEl = document.getElementById("summaryGenderBadge");
  if (genderEl) genderEl.textContent = isFemale ? "👩 స్త్రీ జాతకం" : "👨 పురుష జాతకం";

  const placeEl = document.getElementById("summaryPlaceBadge");
  if (placeEl) {
    const pName = inp.place_name || "నమోదిత స్థలం";
    const latStr = (typeof inp.latitude === 'number') ? `${inp.latitude.toFixed(2)}° N` : "";
    const lonStr = (typeof inp.longitude === 'number') ? `${inp.longitude.toFixed(2)}° E` : "";
    placeEl.textContent = `📍 స్థలం: ${pName} ${latStr ? `(${latStr}, ${lonStr})` : ''}`;
  }

  const lagnaEl = document.getElementById("summaryLagnaBadge");
  if (lagnaEl && data.lagna) {
    lagnaEl.textContent = `లగ్నం: ${data.lagna.rashi_name_te} (${data.lagna.formatted_degree})`;
  }

  const rashiEl = document.getElementById("summaryRashiBadge");
  if (rashiEl) {
    let rashiName = "";
    if (data.panchangam) {
      if (typeof data.panchangam.janma_rashi === "string" && isNaN(Number(data.panchangam.janma_rashi))) {
        rashiName = data.panchangam.janma_rashi;
      } else if (data.panchangam.janma_rashi_te) {
        rashiName = data.panchangam.janma_rashi_te;
      } else if (data.panchangam.rashi_name_te) {
        rashiName = data.panchangam.rashi_name_te;
      } else if (typeof data.panchangam.janma_rashi === "number" || (data.panchangam.janma_rashi && !isNaN(Number(data.panchangam.janma_rashi)))) {
        const RASHIS_TE = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"];
        const idx = Number(data.panchangam.janma_rashi);
        rashiName = RASHIS_TE[idx % 12];
      }
    }
    if (!rashiName && data.planets) {
      const moon = data.planets.find(p => p.name_en === "Moon" || p.name_te === "చంద్రుడు");
      if (moon) rashiName = moon.rashi_name_te;
    }
    rashiEl.textContent = `రాశి: ${rashiName || '—'}`;
  }

  const nakEl = document.getElementById("summaryNakshatraBadge");
  if (nakEl && data.panchangam) {
    nakEl.textContent = `నక్షత్రం: ${data.panchangam.nakshatra || ''} (${data.panchangam.pada || ''})`;
  }

  const dashaEl = document.getElementById("summaryDashaBadge");
  if (dashaEl && data.dasha && data.dasha.current_mahadasha && data.dasha.current_bhukti) {
    dashaEl.textContent = `ప్రస్తుత దశ: ${data.dasha.current_mahadasha.lord_te} మహాదశ / ${data.dasha.current_bhukti.lord_te} భుక్తి`;
  }
}

/* 5. Chart Controls (South/North & D1/D9) */
function initChartControls() {
  const fmtBtns = document.querySelectorAll(".chart-fmt-btn");
  const typeBtns = document.querySelectorAll(".chart-type-btn");

  fmtBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      fmtBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentChartFormat = btn.getAttribute("data-fmt");
      updateKundaliChart();
    });
  });

  typeBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      typeBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentChartType = btn.getAttribute("data-type");
      updateKundaliChart();
    });
  });
}

function updateKundaliChart() {
  const container = document.getElementById("chartSvgWrapper");
  if (!container || !window.currentKundaliData) return;

  const data = window.currentKundaliData;
  const chartData = (currentChartType === "d1") ? data.d1_chart :
                    (currentChartType === "d9") ? data.d9_chart :
                    (data.chalit_chart || data.d1_chart);
  const title = (currentChartType === "d1") ? "రాశి చక్రం (D1)" :
                (currentChartType === "d9") ? "నవాంశ చక్రం (D9)" :
                "భావ చలిత చక్రం (Bhava Chalit)";

  if (currentChartFormat === "south") {
    container.innerHTML = renderSouthIndianChart(chartData, title);
  } else {
    container.innerHTML = renderNorthIndianChart(chartData, data.lagna.rashi_index, title);
  }
}


/* 7. Render Birth Panchangam */
function renderPanchangam(data) {
  const p = data.panchangam;
  const grid = document.getElementById("panchangamGrid");
  if (!grid) return;

  const items = [
    { label: "తిథి (Tithi)", val: p.tithi, sub: p.paksha },
    { label: "వారం (Vara)", val: p.vara, sub: `అధిపతి: ${p.vara_lord}` },
    { label: "నక్షత్రం (Nakshatra)", val: p.nakshatra, sub: `${p.pada} (అధిపతి: ${p.nakshatra_lord})` },
    { label: "యోగం (Yoga)", val: p.yoga, sub: "నిత్య యోగం" },
    { label: "కరణం (Karana)", val: p.karana, sub: "సగం తిథి కాలం" },
    { label: "గణం (Gana)", val: p.gana, sub: "వ్యక్తిత్వ లక్షణం" },
    { label: "నాడి (Nadi)", val: p.nadi, sub: "ఆరోగ్య & జీవశక్తి" },
    { label: "యోని (Yoni)", val: p.yoni, sub: "ప్రకృతి మైత్రి" },
    { label: "వర్ణం (Varna)", val: p.varna, sub: "కర్మ సంస్కారం" }
  ];

  grid.innerHTML = items.map(it => `
    <div class="panchangam-card">
      <div class="card-label">${it.label}</div>
      <div class="card-val">${it.val}</div>
      <div class="card-sub">${it.sub}</div>
    </div>
  `).join("");
}

/* 8. Render Planetary Table & Tatkala Graha Positions & Dignity */
window.switchTatkalaKundaliView = function(viewType) {
  const posView = document.getElementById("tatkalaPositionsView");
  const maitriView = document.getElementById("tatkalaMaitriView");
  const btnPos = document.getElementById("btnTatkalaPositions");
  const btnMaitri = document.getElementById("btnTatkalaMaitri");

  if (viewType === 'maitri') {
    if (posView) posView.style.display = "none";
    if (maitriView) maitriView.style.display = "block";
    if (btnPos) btnPos.classList.remove("active");
    if (btnMaitri) btnMaitri.classList.add("active");
  } else {
    if (posView) posView.style.display = "block";
    if (maitriView) maitriView.style.display = "none";
    if (btnPos) btnPos.classList.add("active");
    if (btnMaitri) btnMaitri.classList.remove("active");
  }
};

function renderPlanetaryTable(data) {
  if (!data) return;
  const tbodyTab1 = document.getElementById("tatkalaGrahaKundaliTableBody");
  const tbodyTab3 = document.getElementById("planetsTableBody");
  const chipsContainer = document.getElementById("tatkalaGrahaSummaryChips");

  const bhavaTitles = {
    1: "1వ భావం (తను)",
    2: "2వ భావం (ధన)",
    3: "3వ భావం (భ్రాతృ)",
    4: "4వ భావం (మాతృ/సుఖ)",
    5: "5వ భావం (సంతాన/పుణ్య)",
    6: "6వ భావం (శత్రు/రోగ)",
    7: "7వ భావం (కళత్ర)",
    8: "8వ భావం (ఆయుర్దాయ)",
    9: "9వ భావం (భాగ్య/ధర్మ)",
    10: "10వ భావం (రాజ్య/కర్మ)",
    11: "11వ భావం (లాభ)",
    12: "12వ భావం (వ్యయ/మోక్ష)"
  };

  let html = "";
  // Add Lagna row
  const l = data.lagna;
  if (l) {
    html += `
      <tr style="background: #FFFDF4; font-weight: 700; border-left: 4px solid #D4AF37;">
        <td><strong>${l.rashi_name_te} లగ్నం</strong></td>
        <td>Lagna / Ascendant</td>
        <td>${l.rashi_name_te}</td>
        <td>${l.formatted_degree}</td>
        <td>${l.nakshatra_name_te} (${l.pada}వ పాదం)</td>
        <td>${l.navamsha_rashi_te}</td>
        <td>1వ భావం (తను భావం)</td>
        <td><span class="dignity-tag dignity-exalted">జన్మ లగ్నం</span></td>
      </tr>
    `;
  }

  const exalted = [];
  const ownSign = [];
  const vakra = [];
  const combust = [];
  const debilitated = [];

  if (Array.isArray(data.planets)) {
    data.planets.forEach(p => {
      const digClass = p.dignity_en === "Exalted" ? "dignity-exalted" :
                       (p.dignity_en === "Own Sign" || p.dignity_en === "Moolatrikona") ? "dignity-own" :
                       p.dignity_en === "Debilitated" ? "dignity-debilitated" :
                       p.dignity_en === "Friend" ? "dignity-friend" :
                       p.dignity_en === "Enemy" ? "dignity-enemy" : "dignity-neutral";

      const vakraTag = p.is_retrograde ? `<span class="status-tag tag-vakra">వక్ర</span>` : "";
      const astaTag = p.is_combust ? `<span class="status-tag tag-asta">అస్తంగత</span>` : "";

      if (p.dignity_en === "Exalted") exalted.push(p.name_te);
      if (p.dignity_en === "Own Sign" || p.dignity_en === "Moolatrikona") ownSign.push(p.name_te);
      if (p.is_retrograde) vakra.push(p.name_te);
      if (p.is_combust) combust.push(p.name_te);
      if (p.dignity_en === "Debilitated") debilitated.push(p.name_te);

      const bhavaLabel = bhavaTitles[p.bhava] || `${p.bhava}వ భావం`;

      html += `
        <tr>
          <td><strong>${p.name_te}</strong> ${vakraTag} ${astaTag}</td>
          <td>${p.name_en}</td>
          <td>${p.rashi_name_te}</td>
          <td>${p.formatted_degree}</td>
          <td>${p.nakshatra_name_te} (${p.pada}వ పాదం)</td>
          <td>${p.navamsha_rashi_te}</td>
          <td>${bhavaLabel}</td>
          <td><span class="dignity-tag ${digClass}">${p.dignity_te}</span></td>
        </tr>
      `;
    });
  }

  // Populate Table in Tab 1 (Kundali tab) and Tab 3 (Panchangam tab)
  if (tbodyTab1) tbodyTab1.innerHTML = html;
  if (tbodyTab3) tbodyTab3.innerHTML = html;

  // Render Summary Chips
  if (chipsContainer && l) {
    let chipsHtml = "";
    chipsHtml += `<div class="tatkala-chip tatkala-chip-lagna"><span>🚩</span> లగ్నాధిపతి: <strong>${l.lord_te || ''}</strong></div>`;
    
    if (exalted.length > 0) {
      chipsHtml += `<div class="tatkala-chip tatkala-chip-exalted"><span>🌟</span> ఉచ్ఛ గ్రహాలు: <strong>${exalted.join(", ")}</strong></div>`;
    }
    if (ownSign.length > 0) {
      chipsHtml += `<div class="tatkala-chip tatkala-chip-own"><span>🏠</span> స్వక్షేత్రం: <strong>${ownSign.join(", ")}</strong></div>`;
    }
    if (vakra.length > 0) {
      chipsHtml += `<div class="tatkala-chip tatkala-chip-vakra"><span>⚡</span> వక్ర గ్రహాలు: <strong>${vakra.join(", ")}</strong></div>`;
    }
    if (combust.length > 0) {
      chipsHtml += `<div class="tatkala-chip tatkala-chip-asta"><span>🔥</span> అస్తంగత: <strong>${combust.join(", ")}</strong></div>`;
    }
    if (debilitated.length > 0) {
      chipsHtml += `<div class="tatkala-chip tatkala-chip-debilitated"><span>🔻</span> నీచ గ్రహాలు: <strong>${debilitated.join(", ")}</strong></div>`;
    }
    if (exalted.length === 0 && ownSign.length === 0 && vakra.length === 0 && combust.length === 0 && debilitated.length === 0) {
      chipsHtml += `<div class="tatkala-chip" style="background:#F5F5F5; color:#616161;"><span>ℹ️</span> గ్రహాలన్నీ సాధారణ సమ/మిత్ర క్షేత్ర స్థితిలో ఉన్నాయి</div>`;
    }
    chipsContainer.innerHTML = chipsHtml;
  }

  // Render Tatkalika Maitri Matrix
  const maitriHeader = document.getElementById("tatkalaMaitriTableHeader");
  const maitriBody = document.getElementById("tatkalaMaitriTableBody");
  if (maitriHeader && maitriBody && Array.isArray(data.planets)) {
    const eligiblePlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
    const teNames = {
      "Sun": "సూర్యుడు", "Moon": "చంద్రుడు", "Mars": "కుజుడు",
      "Mercury": "బుధుడు", "Jupiter": "గురువు", "Venus": "శుక్రుడు", "Saturn": "శని"
    };
    const pMap = {};
    data.planets.forEach(p => {
      if (eligiblePlanets.includes(p.name_en)) {
        pMap[p.name_en] = p;
      }
    });

    maitriHeader.innerHTML = `<th>గ్రహం</th>` + eligiblePlanets.map(p => `<th>${teNames[p] || p}</th>`).join("");
    
    maitriBody.innerHTML = eligiblePlanets.map(p1 => {
      const p1Obj = pMap[p1];
      const r1 = p1Obj ? p1Obj.rashi_index : 0;
      const cells = eligiblePlanets.map(p2 => {
        if (p1 === p2) return `<td class="text-center" style="color: #9E9E9E; font-weight: bold;">—</td>`;
        const p2Obj = pMap[p2];
        const r2 = p2Obj ? p2Obj.rashi_index : 0;
        const dist = ((r2 - r1 + 12) % 12) + 1;
        const isFriend = [2, 3, 4, 10, 11, 12].includes(dist);
        return isFriend
          ? `<td class="text-center"><span class="dignity-tag dignity-friend" style="font-weight: 700;">మిత్రుడు (+${dist}వ)</span></td>`
          : `<td class="text-center"><span class="dignity-tag dignity-enemy" style="font-weight: 700;">శత్రువు (${dist}వ)</span></td>`;
      }).join("");
      return `<tr><th>${teNames[p1] || p1}</th>${cells}</tr>`;
    }).join("");
  }

  // Ensure default view is positions
  if (typeof window.switchTatkalaKundaliView === "function") {
    window.switchTatkalaKundaliView('positions');
  }
}

/* 9. Render Dasha Timeline */
function renderDashaTimeline(data) {
  const d = data.dasha;
  const banner = document.getElementById("dashaBalanceBanner");
  const hero = document.getElementById("currentDashaHero");
  const tbody = document.getElementById("dashaTableBody");

  if (banner) banner.textContent = d.birth_balance_text;

  if (hero && d.current_mahadasha && d.current_bhukti) {
    hero.innerHTML = `
      <h3>${d.current_mahadasha.lord_te} మహాదశ — ${d.current_bhukti.lord_te} అంతర్దశ (భుక్తి)</h3>
      <p>మహాదశ ముగింపు తేదీ: <strong>${d.current_mahadasha.end_date}</strong> | భుక్తి ముగింపు: <strong>${d.current_bhukti.end_date}</strong></p>
    `;
  }

  if (tbody && Array.isArray(d.all_mahadashas)) {
    tbody.innerHTML = d.all_mahadashas.map(md => {
      const isCurrent = (md.lord === d.current_mahadasha.lord);
      return `
        <tr ${isCurrent ? 'style="background: #FFF8E7; font-weight: bold;"' : ''}>
          <td>${md.lord_te} (${md.lord})</td>
          <td>${md.total_years} సంవత్సరాలు</td>
          <td>${md.start_date}</td>
          <td>${md.end_date}</td>
          <td>${isCurrent ? '<span class="dignity-tag dignity-exalted">ప్రస్తుతం నడుస్తోంది</span>' : (new Date(md.end_date) < new Date() ? 'గడిచింది' : 'భవిష్యత్తు')}</td>
        </tr>
      `;
    }).join("");
  }
}

/* 10. Render Gocharam */
function renderGocharam(data) {
  const g = data.gocharam;
  const container = document.getElementById("gocharamCardsContainer");
  if (!container) return;

  const shani = g.shani_gochara;
  const guru = g.guru_gochara;
  const rk = g.rahu_ketu_gochara;

  container.innerHTML = `
    <div class="gocharam-card ${shani.is_severe ? 'severe' : (shani.house in [3,6,11] ? 'auspicious' : '')}">
      <h4 style="color: #4A0E17; font-size: 1.15rem; margin-bottom: 8px;">🪐 శని గోచారం (Saturn Transit Status)</h4>
      <p>జన్మ రాశి నుండి స్థానం: <strong>${shani.house}వ స్థానం (${shani.transit_rashi})</strong></p>
      <p style="font-size: 1.05rem; font-weight: bold; color: ${shani.is_severe ? '#B71C1C' : '#2E7D32'}; margin: 8px 0;">
        ${shani.status}
      </p>
      <small style="color: #6C5D53;">శని దేవుని ప్రీత్యర్థం రోజూ హనుమాన్ చాలీసా, దశరథ ప్రోక్త శని స్తోత్ర పారాయణం చేయడం వల్ల కష్టాలు తొలగి శుభాలు చేకూరుతాయి.</small>
    </div>

    <div class="gocharam-card ${guru.has_guru_bala ? 'auspicious' : ''}">
      <h4 style="color: #4A0E17; font-size: 1.15rem; margin-bottom: 8px;">✨ గురు గోచారం (Jupiter Transit & Guru Bala)</h4>
      <p>జన్మ రాశి నుండి స్థానం: <strong>${guru.house}వ స్థానం (${guru.transit_rashi})</strong></p>
      <p style="font-size: 1.05rem; font-weight: bold; color: ${guru.has_guru_bala ? '#2E7D32' : '#E65100'}; margin: 8px 0;">
        ${guru.status}
      </p>
      <small style="color: #6C5D53;">గురు బలం అనుకూలంగా ఉన్నప్పుడు వివాహం, ఉద్యోగ లాభం, నూతన గృహ ప్రవేశాది శుభకార్యాలు దిగ్విజయంగా నెరవేరుతాయి.</small>
    </div>

    <div class="gocharam-card">
      <h4 style="color: #4A0E17; font-size: 1.15rem; margin-bottom: 8px;">🐉 రాహు - కేతు గోచారం (Rahu & Ketu Axis)</h4>
      <p>రాహువు: <strong>${rk.rahu_house}వ స్థానం (${rk.rahu_rashi})</strong> | కేతువు: <strong>${rk.ketu_house}వ స్థానం (${rk.ketu_rashi})</strong></p>
      <small style="color: #6C5D53;">రాహువు 3, 6, 11 స్థానాల్లో శుభప్రదం. కేతువు ఆధ్యాత్మిక దృష్టిని, అంతర్జ్ఞానాన్ని కలిగిస్తాడు.</small>
    </div>
  `;
}

/* 11. Render Yogas */
function renderYogas(data) {
  const list = document.getElementById("yogasContainer");
  if (!list) return;

  if (!Array.isArray(data.yogas) || data.yogas.length === 0) {
    list.innerHTML = `<p>ఈ జాతకంలో విశేష యోగాలు సాధారణ స్థితిలో ఉన్నాయి.</p>`;
    return;
  }

  list.innerHTML = data.yogas.map(y => `
    <div class="yoga-card">
      <div class="yoga-card-header">
        <div class="yoga-title">🌟 ${y.name}</div>
        <span class="dignity-tag dignity-exalted">${y.type}</span>
      </div>
      <p style="color: #2B2118; margin-bottom: 8px;">${y.description}</p>
      <div class="yoga-source">📜 గ్రంథ ప్రమాణం: ${y.source} | ప్రభావం: <strong>${y.strength}</strong></div>
    </div>
  `).join("");
}

/* 11a. Render Avakahada Chakra (OnlineJyotish Style Table) */
function renderAvakahadaChakra(data) {
  const tbody = document.getElementById("avakahadaTableBody");
  if (!tbody || !data.panchangam) return;

  const p = data.panchangam;
  const items = [
    { key: "వర్ణం (Varna)", val: p.varna || "—", desc: "సాత్విక ధర్మం & ఆధ్యాత్మిక సంస్కారం" },
    { key: "వశ్యం (Vashya)", val: p.vashya || "—", desc: "వ్యక్తిత్వ ఆకర్షణ & స్వభావం" },
    { key: "తార (Tara)", val: p.tara || "జన్మ తార", desc: "నవ తార చక్ర నిర్ణయం" },
    { key: "యోని (Yoni)", val: p.yoni || "—", desc: "ప్రకృతి మైత్రి & సహజ శైలి" },
    { key: "గణం (Gana)", val: p.gana || "—", desc: "మానసిక తత్వం & ప్రవర్తన" },
    { key: "నాడి (Nadi)", val: p.nadi || "—", desc: "ఆరోగ్య & వంశ జీవశక్తి" },
    { key: "తత్వం (Tatwa)", val: p.tatwa || "—", desc: "పంచభూతాలలో జన్మ తత్వం" },
    { key: "పాద చక్రం (పాయ)", val: p.paya || "—", desc: p.paya_desc || "శుభప్రదం" },
    { key: "నామ నక్షత్రాక్షరం", val: `<span style="font-size: 1.25rem; color: #4A0E17; font-weight: 800;">${p.nama_aksharam || '—'}</span>`, desc: `నాలుగు పాదాల అక్షరాలు: <strong>${p.all_nama_aksharas || '—'}</strong>` },
    { key: "నక్షత్ర వృక్షం (Tree)", val: p.vruksha || "—", desc: "పూజనీయమైన పవిత్ర వృక్షం" },
    { key: "నక్షత్ర పక్షి (Bird)", val: p.pakshi || "—", desc: "సంప్రదాయ పక్షి శాస్త్రం" }
  ];

  tbody.innerHTML = items.map(it => `
    <tr>
      <td style="font-weight: 700; color: #4A0E17; width: 30%;">🪷 ${it.key}</td>
      <td style="font-weight: 700; color: #111; font-size: 1.05rem; width: 35%;">${it.val}</td>
      <td style="color: #6C5D53; font-size: 0.88rem;">${it.desc}</td>
    </tr>
  `).join("");
}

/* 11b. Render Dvadasa Bhava Sphuta */
function renderBhavaSphuta(data) {
  const tbody = document.getElementById("bhavaSphutaTableBody");
  if (!tbody || !data.bhava_sphuta) return;

  const bhavaTitles = [
    "1వ భావం (లగ్నం - తను స్థానం)",
    "2వ భావం (ధన & కుటుంబ స్థానం)",
    "3వ భావం (భ్రాతృ & పరాక్రమ స్థానం)",
    "4వ భావం (మాతృ & సుఖ స్థానం)",
    "5వ భావం (పుత్ర & పూర్వపుణ్య స్థానం)",
    "6వ భావం (శత్రు & రోగ స్థానం)",
    "7వ భావం (కళత్ర & భాగస్వామ్య స్థానం)",
    "8వ భావం (ఆయుః & రంధ్ర స్థానం)",
    "9వ భావం (భాగ్య & ధర్మ స్థానం)",
    "10వ భావం (రాజ్య & కర్మ స్థానం)",
    "11వ భావం (లాభ స్థానం)",
    "12వ భావం (వ్యయ & మోక్ష స్థానం)"
  ];

  let html = "";
  data.bhava_sphuta.forEach((b, idx) => {
    const rawOccupants = b.occupants || b.planets || [];
    const occStr = (rawOccupants && rawOccupants.length > 0)
      ? rawOccupants.map(o => `<span class="occupant-tag">${o}</span>`).join(" ")
      : `<span style="color: #795548; font-weight: 700;">—</span>`;

    const arambhaStr = b.arambha_formatted || b.arambha_dms || "—";
    const madhyaStr = b.madhya_formatted || b.madhya_dms || "—";
    const anthyaStr = b.anthya_formatted || b.anthya_dms || "—";

    html += `
      <tr>
        <td><strong>${bhavaTitles[idx] || (b.bhava_num + 'వ భావం')}</strong></td>
        <td><strong>${b.rashi_name_te}</strong></td>
        <td>${arambhaStr}</td>
        <td style="color: #4A0E17; font-weight: bold; background: #FFFDF5;">${madhyaStr}</td>
        <td>${anthyaStr}</td>
        <td>${b.lord_te} (${b.lord_en})</td>
        <td>${occStr}</td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

/* 11bb. Render Dasha-Antardasha Predictions (OnlineJyotish Style) */
function renderDashaAntardashaPredictions(data) {
  const da = data.dasha_analysis;
  const mahaCard = document.getElementById("mahadashaDetailCard");
  const bhuktisList = document.getElementById("bhuktisListContainer");

  if (!da || !mahaCard || !bhuktisList) return;

  const mo = da.current_mahadasha_overview || {};

  mahaCard.innerHTML = `
    <div class="prediction-card-header">
      <div class="pred-title">⏳ ${mo.title || 'ప్రస్తుత మహాదశ సమగ్ర ఫలితాలు'}</div>
      <span class="dignity-tag dignity-exalted">ప్రస్తుతం నడుస్తున్న మహాదశ</span>
    </div>
    <div class="pred-body">
      <div class="pred-field">
        <strong>🪐 దశా స్వరూపం & సాధారణ ప్రభావం:</strong>
        <p>${mo.general || '—'}</p>
      </div>
      <div class="pred-field">
        <strong>💼 ఉద్యోగం, వృత్తి & వ్యాపార ఫలితాలు:</strong>
        <p>${mo.career || '—'}</p>
      </div>
      <div class="pred-field">
        <strong>💰 ఆర్థిక స్థితి & ధన లాభాలు:</strong>
        <p>${mo.wealth || '—'}</p>
      </div>
      <div class="pred-field">
        <strong>👨‍👩‍👦 కుటుంబ జీవితం & దాంపత్య సౌఖ్యం:</strong>
        <p>${mo.family || '—'}</p>
      </div>
      <div class="pred-field">
        <strong>🩺 ఆరోగ్య విశేషాలు & తీసుకోవలసిన జాగ్రత్తలు:</strong>
        <p>${mo.health || '—'}</p>
      </div>
      <div class="pred-field alert-guidance">
        <strong>🕉️ శాస్త్రోక్త దశా పరిహారాలు & దైవారాధన:</strong>
        <p>${mo.remedy || '—'}</p>
      </div>
    </div>
  `;

  const bhuktis = da.all_bhuktis || [];
  bhuktisList.innerHTML = bhuktis.map(b => {
    const isAct = b.is_active;
    const isPast = new Date(b.end_date) < new Date();
    const tagClass = isAct ? "dignity-exalted" : (isPast ? "dignity-neutral" : "dignity-friend");
    const tagText = isAct ? "⭐ ప్రస్తుతం నడుస్తోంది (Active)" : (isPast ? "గడిచింది" : "రాబోయే భుక్తి");
    const borderStyle = isAct ? "border: 2px solid #D4AF37; background: #FFFDF4;" : "background: #FFF; border: 1px solid #E5D7B7;";

    return `
      <div class="bhukti-prediction-card" style="${borderStyle}; border-radius: 12px; padding: 18px; margin-bottom: 16px; box-shadow: var(--shadow-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
          <div style="font-size: 1.15rem; font-weight: 700; color: #4A0E17;">
            <span>✨</span> ${b.full_name}
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 0.88rem; color: #6C5D53;">కాలం: <strong>${b.start_date}</strong> నుండి <strong>${b.end_date}</strong></span>
            <span class="dignity-tag ${tagClass}">${tagText}</span>
          </div>
        </div>
        <p style="font-size: 0.98rem; line-height: 1.65; color: #2B2118; margin: 0;">
          ${b.prediction}
        </p>
      </div>
    `;
  }).join("");
}

/* 11c. Render Sarvashtakavarga (SAV) & BAV */
function renderAshtakavarga(data) {
  if (!data.ashtakavarga) return;
  const sav = data.ashtakavarga;

  // 1. Stats and Wealth banner
  const banner = document.getElementById("ashtakavargaInsightBanner");
  if (banner && sav.insights) {
    banner.innerHTML = `
      <p style="font-size: 1.05rem; color: #4A0E17; margin-bottom: 8px;"><strong>💰 ధన & వ్యయ విశ్లేషణ:</strong> ${sav.insights.wealth_status}</p>
      <div class="sav-pill-row">
        <span class="sav-pill">11వ లాభ స్థానం: <strong>${sav.insights.eleventh_points}</strong> బిందువులు</span>
        <span class="sav-pill">12వ వ్యయ స్థానం: <strong>${sav.insights.twelfth_points}</strong> బిందువులు</span>
        <span class="sav-pill">10వ కర్మ స్థానం: <strong>${sav.insights.career_points}</strong> బిందువులు</span>
        <span class="sav-pill">1వ లగ్న బలం: <strong>${sav.insights.lagna_points}</strong> బిందువులు</span>
      </div>
    `;
  }

  // 2. SVG Chart
  const svgWrapper = document.getElementById("ashtakavargaSvgWrapper");
  if (svgWrapper && typeof renderAshtakavargaChart === "function") {
    svgWrapper.innerHTML = renderAshtakavargaChart(sav.sarvashtakavarga_rashi, sav.total_points);
  }

  // 3. Rashi / Bhava Table
  const rashiTbody = document.getElementById("savRashiTableBody");
  if (rashiTbody && Array.isArray(sav.sarvashtakavarga_rashi)) {
    rashiTbody.innerHTML = sav.sarvashtakavarga_rashi.map(r => {
      const isStrong = r.points >= 28;
      const isHigh = r.points >= 32;
      const badgeClass = isHigh ? "badge-high" : (isStrong ? "badge-medium" : "badge-low");

      return `
        <tr>
          <td><strong>${r.rashi_name_te}</strong> (${r.rashi_name_en})</td>
          <td style="font-size: 1.15rem; font-weight: 700; color: ${isStrong ? '#1B5E20' : '#B71C1C'};">${r.points}</td>
          <td><span class="sav-badge ${badgeClass}">${r.status_te}</span></td>
        </tr>
      `;
    }).join("");
  }

  // 4. Bhinna Ashtakavarga Matrix Table
  const bavHeader = document.getElementById("bavTableHeader");
  const bavBody = document.getElementById("bavTableBody");
  if (bavHeader && bavBody && sav.bav_planets) {
    const planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
    const planetNamesTe = {
      "Sun": "రవి", "Moon": "చంద్ర", "Mars": "కుజ", "Mercury": "బుధ",
      "Jupiter": "గురు", "Venus": "శుక్ర", "Saturn": "శని"
    };

    let headerHtml = `<th>రాశి (Sign)</th>`;
    planets.forEach(p => {
      headerHtml += `<th>${planetNamesTe[p]}</th>`;
    });
    headerHtml += `<th>మొత్తం (SAV)</th>`;
    bavHeader.innerHTML = headerHtml;

    const rashiNames = [
      "మేషం", "వృషభం", "మిథునం", "కర్కాటకం",
      "సింహం", "కన్య", "తుల", "వృశ్చికం",
      "ధనుస్సు", "మకరం", "కుంభం", "మీనం"
    ];

    let bodyHtml = "";
    for (let rIdx = 0; rIdx < 12; rIdx++) {
      let rowHtml = `<tr><td><strong>${rashiNames[rIdx]}</strong></td>`;
      planets.forEach(p => {
        const pts = (sav.bav_planets[p] && sav.bav_planets[p][rIdx]) !== undefined ? sav.bav_planets[p][rIdx] : 0;
        rowHtml += `<td style="${pts >= 4 ? 'font-weight: bold; color: #2E7D32;' : 'color: #666;'}">${pts}</td>`;
      });
      const savPts = sav.sarvashtakavarga_rashi ? sav.sarvashtakavarga_rashi[rIdx].points : 0;
      rowHtml += `<td style="font-weight: 800; color: #4A0E17; background: #FFFDF0;">${savPts}</td></tr>`;
      bodyHtml += rowHtml;
    }
    bavBody.innerHTML = bodyHtml;
  }
}

/* 11d. Render Doshas (Kuja Dosha & Kala Sarpa) & Vedic Remedy Recheck Engine */
function renderDoshas(data) {
  // 1. Kuja Dosha Card
  const kujaCard = document.getElementById("kujaDoshaCard");
  if (kujaCard && data.kuja_dosha) {
    const kd = data.kuja_dosha;
    const isCancelled = kd.severity === "cancelled";
    const isPresent = kd.severity === "present";
    const severityClass = isCancelled ? "card-dosha-cancelled" : (isPresent ? "card-dosha-present" : "card-dosha-none");
    const badgeClass = isCancelled ? "dignity-friend" : (isPresent ? "dignity-debilitated" : "dignity-exalted");

    const rv = kd.recheck_verdict || {};
    const rvBannerClass = rv.badge === "success" ? "verdict-success" : (rv.badge === "info" ? "verdict-info" : "verdict-warning");

    let cancelHtml = "";
    if (Array.isArray(kd.cancellations) && kd.cancellations.length > 0) {
      cancelHtml = `
        <div class="dosha-sub-box">
          <h5 style="color: #2E7D32; font-weight: bold; margin-bottom: 6px;">✅ శాస్త్రోక్త మినహాయింపులు & దోష భంగం (Cancellations):</h5>
          <ul style="padding-left: 18px; margin: 0; color: #1B5E20; line-height: 1.6;">
            ${kd.cancellations.map(c => `<li style="margin-bottom: 4px;">${c}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    let remediesHtml = "";
    if (Array.isArray(kd.remedies) && kd.remedies.length > 0) {
      remediesHtml = `
        <div class="dosha-sub-box" style="margin-top: 10px;">
          <h5 style="color: #996515; font-weight: bold; margin-bottom: 6px;">🕉️ శాస్త్రోక్త నివారణ & దైవారాధన:</h5>
          <ul style="padding-left: 18px; margin: 0; color: #5D4037; line-height: 1.6;">
            ${kd.remedies.map(r => `<li style="margin-bottom: 4px;">${r}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    kujaCard.className = `dosha-card ${severityClass}`;
    kujaCard.innerHTML = `
      <div class="dosha-card-header">
        <div class="dosha-title">
          <span>🔥</span> వివాహ కుజ దోష విశ్లేషణ (Kuja / Manglik Analysis)
        </div>
        <span class="dignity-tag ${badgeClass}">${kd.status_te}</span>
      </div>

      <!-- Authentic Shastric Recheck Verdict Banner -->
      <div class="recheck-verdict-banner ${rvBannerClass}" style="margin: 10px 0 14px 0;">
        <span>🛡️</span>
        <div>
          <strong>పూజా పునఃసమీక్ష నిర్ధారణ:</strong> ${rv.verdict_title || kd.status_te}
        </div>
      </div>

      <p class="dosha-summary" style="margin: 8px 0; font-size: 1.02rem; line-height: 1.65;">${kd.summary_te}</p>
      
      <div class="dosha-placements" style="font-size: 0.95rem; color: #6D4C41; margin-bottom: 12px; background: #FFF; padding: 10px; border-radius: 6px; border: 1px solid #EADBCE;">
        <span>లగ్నం నుండి కుజుడు: <strong>${kd.kuja_from_lagna}వ స్థానం</strong></span> • 
        <span>చంద్రుని నుండి: <strong>${kd.kuja_from_moon}వ స్థానం</strong></span> • 
        <span>శుక్రుని నుండి: <strong>${kd.kuja_from_venus}వ స్థానం</strong></span>
      </div>

      <div style="font-size: 0.9rem; color: #4A0E17; margin-bottom: 10px; background: #FAF5EB; padding: 8px 12px; border-radius: 6px;">
        <strong>📜 గ్రంథ ప్రమాణం:</strong> ${kd.shastra_authority || 'ముహూర్త రత్నావళి & బృహత్ పరాశర హోరాశాస్త్రం'}
      </div>

      ${cancelHtml}
      ${remediesHtml}
      ${isPresent ? `
        <div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed #FFCDD2; text-align: right;">
          <button type="button" class="btn-submit" style="padding: 8px 18px; font-size: 0.92rem; border-radius: 6px; background: linear-gradient(135deg, #D84315, #BF360C); display: inline-flex; align-items: center; gap: 8px; cursor: pointer; border: none; color: white; font-weight: 700; box-shadow: 0 2px 6px rgba(191,54,12,0.3);"
            onclick="window.launchMuhurtamForRemedy('kuja_shanti_subrahmanya', 'సుబ్రహ్మణ్య షష్ఠి / కుజ శాంతి హోమం')">
            <span>⏱️</span> ఈ దోష శాంతికి ముహూర్తం లెక్కించండి (Calculate Kuja Shanti Muhurtam)
          </button>
        </div>
      ` : ''}
    `;
  }

  // 2. Kala Sarpa Dosha Card
  const kalaCard = document.getElementById("kalaSarpaCard");
  if (kalaCard && data.kalasarpa_dosha) {
    const ks = data.kalasarpa_dosha;
    const hasKs = ks.has_dosha;
    const isPartial = ks.is_partial;
    const severityClass = !hasKs ? "card-dosha-none" : (isPartial ? "card-dosha-cancelled" : "card-dosha-present");
    const badgeClass = !hasKs ? "dignity-exalted" : (isPartial ? "dignity-friend" : "dignity-debilitated");

    const rv = ks.recheck_verdict || {};
    const rvBannerClass = rv.badge === "success" ? "verdict-success" : (rv.badge === "info" ? "verdict-info" : "verdict-warning");

    let remediesHtml = "";
    if (Array.isArray(ks.remedies) && ks.remedies.length > 0) {
      remediesHtml = `
        <div class="dosha-sub-box" style="margin-top: 10px;">
          <h5 style="color: #996515; font-weight: bold; margin-bottom: 6px;">🕉️ శాస్త్రోక్త నివారణ & దైవారాధన:</h5>
          <ul style="padding-left: 18px; margin: 0; color: #5D4037; line-height: 1.6;">
            ${ks.remedies.map(r => `<li style="margin-bottom: 4px;">${r}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    kalaCard.className = `dosha-card ${severityClass}`;
    kalaCard.innerHTML = `
      <div class="dosha-card-header">
        <div class="dosha-title">
          <span>🐉</span> కాలసర్ప యోగ / దోష విశ్లేషణ (Kala Sarpa Analysis)
        </div>
        <span class="dignity-tag ${badgeClass}">${ks.status_te}</span>
      </div>

      <!-- Authentic Shastric Recheck Verdict Banner -->
      <div class="recheck-verdict-banner ${rvBannerClass}" style="margin: 10px 0 14px 0;">
        <span>🛡️</span>
        <div>
          <strong>పూజా పునఃసమీక్ష నిర్ధారణ:</strong> ${rv.verdict_title || ks.status_te}
        </div>
      </div>

      <h4 style="color: #4A0E17; margin: 8px 0 4px 0;">${ks.type_name || 'కాలసర్ప పరిశీలన'}</h4>
      <p class="dosha-summary" style="margin: 8px 0; font-size: 1.02rem; line-height: 1.65;">${ks.summary_te}</p>
      
      <div style="font-size: 0.9rem; color: #4A0E17; margin-bottom: 10px; background: #FAF5EB; padding: 8px 12px; border-radius: 6px;">
        <strong>📜 గ్రంథ ప్రమాణం:</strong> ${ks.shastra_authority || 'జాతకాభరణం & జాతక పారిజాతం'}
      </div>

      ${remediesHtml}
      ${hasKs ? `
        <div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed #FFCDD2; text-align: right; display: flex; gap: 8px; justify-content: flex-end; flex-wrap: wrap;">
          <button type="button" class="btn-submit" style="padding: 8px 16px; font-size: 0.92rem; border-radius: 6px; background: linear-gradient(135deg, #1565C0, #0D47A1); display: inline-flex; align-items: center; gap: 6px; cursor: pointer; border: none; color: white; font-weight: 700; box-shadow: 0 2px 6px rgba(13,71,161,0.3);"
            onclick="window.launchMuhurtamForRemedy('naga_pratishtha', 'నాగ ప్రతిష్ఠాపన (సర్ప దోష నివారణ)')">
            <span>🐍</span> నాగ ప్రతిష్ఠ ముహూర్తం (Naga Pratishtha)
          </button>
          <button type="button" class="btn-submit" style="padding: 8px 16px; font-size: 0.92rem; border-radius: 6px; background: linear-gradient(135deg, #2E7D32, #1B5E20); display: inline-flex; align-items: center; gap: 6px; cursor: pointer; border: none; color: white; font-weight: 700; box-shadow: 0 2px 6px rgba(27,94,32,0.3);"
            onclick="window.launchMuhurtamForRemedy('ashlesha_bali', 'ఆశ్లేషా బలి పూజ')">
            <span>🌾</span> ఆశ్లేషా బలి ముహూర్తం (Ashlesha Bali)
          </button>
        </div>
      ` : ''}
    `;
  }

  // 2b. Santana & Pregnancy Loss (గర్భస్రావ / సంతాన దోష విశ్లేషణ) Card
  const santanaCard = document.getElementById("santanaDoshaCard");
  if (santanaCard && data.santana_analysis) {
    const sa = data.santana_analysis;
    const sphutas = sa.sphutas || {};
    const beeja = sphutas.beeja_sphuta || {};
    const kshetra = sphutas.kshetra_sphuta || {};
    const doshas = sa.doshas_detected || [];
    const fifth = sa.fifth_house_info || {};

    const overallBadgeClass = sa.overall_badge === "success" ? "dignity-exalted" : (sa.overall_badge === "danger" ? "dignity-debilitated" : "dignity-friend");
    const bannerClass = sa.overall_badge === "success" ? "verdict-success" : (sa.overall_badge === "danger" ? "verdict-danger" : "verdict-warning");

    let doshasListHtml = "";
    if (doshas.length > 0) {
      doshasListHtml = `
        <div style="margin-top: 15px;">
          <h4 style="color: #B71C1C; font-size: 1.05rem; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
            <span>⚠️</span> గుర్తించబడిన సంతాన / గర్భస్రావ ప్రతిబంధక దోషాలు (Detected Doshas):
          </h4>
          ${doshas.map(d => {
            const pRemedy = d.primary_remedy || {};
            const eventType = pRemedy.event_type || 'santana_gopala';
            const remedyName = pRemedy.name || 'శాంతి హోమం';
            return `
              <div style="background: #FFF9F9; border: 1px solid #FFCDD2; border-left: 5px solid #D32F2F; border-radius: 8px; padding: 14px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <h5 style="color: #C62828; font-size: 1.05rem; font-weight: 800; margin: 0;">${d.name_te}</h5>
                  <span class="dignity-tag dignity-debilitated" style="font-size: 0.8rem;">దోషం నిర్ధారితం</span>
                </div>
                <div style="font-size: 0.93rem; color: #5D4037; margin-bottom: 6px;">
                  <strong>🔍 జాతక కారణం:</strong> ${d.astrological_reason}
                </div>
                <div style="font-size: 0.93rem; color: #4A0E17; margin-bottom: 6px;">
                  <strong>⚡ దోష ప్రభావం:</strong> ${d.impact_te}
                </div>
                <div style="font-size: 0.88rem; color: #0D47A1; margin-bottom: 10px; background: #E8EAF6; padding: 4px 8px; border-radius: 4px; display: inline-block;">
                  <strong>📜 ప్రమాణ గ్రంథం:</strong> ${d.shastra_authority}
                </div>
                
                <!-- Primary Shastric Remedy Box -->
                <div style="background: #FFF; border: 1px solid #E0E0E0; border-radius: 6px; padding: 10px 12px; margin-top: 8px;">
                  <div style="font-weight: 700; color: #1B5E20; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                    <span>🕉️</span> ముఖ్య వైదిక పరిహారం: ${pRemedy.name}
                  </div>
                  <p style="margin: 4px 0; font-size: 0.92rem; color: #333;"><strong>విధానం:</strong> ${pRemedy.procedure || '—'}</p>
                  ${pRemedy.mantra ? `<p style="margin: 4px 0; font-size: 0.92rem; color: #6A1B9A;"><strong>మంత్రం:</strong> ${pRemedy.mantra}</p>` : ''}
                  ${pRemedy.japa_count ? `<p style="margin: 4px 0; font-size: 0.9rem; color: #E65100;"><strong>జప సంఖ్య:</strong> ${pRemedy.japa_count}</p>` : ''}
                  
                  <!-- 1-Click Muhurtam Link Button -->
                  <div style="margin-top: 10px; text-align: right;">
                    <button type="button" class="btn-submit" style="padding: 7px 16px; font-size: 0.92rem; border-radius: 6px; background: linear-gradient(135deg, #FF6F00, #E65100); display: inline-flex; align-items: center; gap: 6px; cursor: pointer; border: none; color: white;"
                      onclick="window.launchMuhurtamForRemedy('${eventType}', '${encodeURIComponent(remedyName)}')">
                      <span>⏱️</span> ఈ పరిహారానికి అనుకూల ముహూర్తాలను గణించండి (Calculate Muhurtams)
                    </button>
                  </div>
                </div>
              </div>
            `;
          }).join("")}
        </div>
      `;
    } else {
      doshasListHtml = `
        <div style="background: #F1F8E9; border: 1px solid #C8E6C9; border-radius: 8px; padding: 12px; margin-top: 15px; color: #2E7D32;">
          <strong>✅ శుభప్రదం:</strong> జాతకంలో తీవ్రమైన సర్ప శాప, గర్భస్రావ లేదా మారక దోషాలు లేవు. సామాన్య ఇష్టదైవ ఆరాధన మరియు సంతాన గోపాల స్తోత్ర పఠనం శుభ ఫలితాలనిస్తుంది.
        </div>
      `;
    }

    santanaCard.className = `dosha-card ${sa.overall_badge === 'success' ? 'card-dosha-none' : 'card-dosha-present'}`;
    santanaCard.innerHTML = `
      <div class="dosha-card-header">
        <div class="dosha-title">
          <span>🪷</span> సంతాన, పుత్రభావ & గర్భస్రావ దోష విశ్లేషణ (Progeny & Pregnancy Loss Shastric Analysis)
        </div>
        <span class="dignity-tag ${overallBadgeClass}">${sa.overall_status_te}</span>
      </div>

      <!-- Overall Status Verdict Banner -->
      <div class="recheck-verdict-banner ${bannerClass}" style="margin: 10px 0 14px 0;">
        <span style="font-size: 1.4rem;">👶</span>
        <div>
          <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">సంతాన స్థితి & శాస్త్రోక్త నిర్ధారణ:</div>
          <div style="font-size: 1.08rem; font-weight: 800;">${sa.overall_status_te}</div>
          <p style="margin: 4px 0 0 0; font-size: 0.92rem; font-weight: 500;">${sa.overall_description}</p>
        </div>
      </div>

      <!-- 5th House & Jupiter Dignity Overview -->
      <div style="background: #FFFDF7; border: 1px solid #FFE082; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.93rem;">
        <div><span>🏛️ పంచమ స్థానం (5th House):</span> <strong>${fifth.rashi_name_te || '—'} రాశి</strong></div>
        <div><span>👑 పంచమాధిపతి:</span> <strong>${fifth.lord_te || '—'}</strong></div>
        <div><span>🪐 5వ భావంలో ఉన్న గ్రహాలు:</span> <strong>${Array.isArray(fifth.occupants) ? fifth.occupants.join(", ") : '—'}</strong></div>
        <div><span>🌟 పుత్రకారక గురు స్థితి:</span> <strong>${fifth.jupiter_status || '—'}</strong></div>
      </div>

      <!-- Classical Beeja & Kshetra Sphuta Analysis Grid -->
      <div style="margin-bottom: 16px;">
        <h4 style="color: #4A0E17; font-size: 1.05rem; font-weight: bold; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
          <span>🧬</span> శాస్త్రోక్త బీజ & క్షేత్ర స్పష్ట బలం (Beeja & Kshetra Sphuta - Phaladeepika Ch. 12):
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
          
          <!-- Beeja Sphuta (Male) -->
          <div style="background: #FFF; border: 1px solid #BBDEFB; border-top: 4px solid #1976D2; border-radius: 8px; padding: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <strong style="color: #0D47A1; font-size: 0.98rem;">👨 పురుష బీజ స్పష్టం (Virility & Vitality)</strong>
              <span class="dignity-tag ${beeja.badge === 'success' ? 'dignity-exalted' : (beeja.badge === 'danger' ? 'dignity-debilitated' : 'dignity-friend')}" style="font-size: 0.78rem;">
                ${beeja.badge === 'success' ? 'సంపూర్ణ బలం' : (beeja.badge === 'danger' ? 'దోషం' : 'మధ్యమం')}
              </span>
            </div>
            <div style="font-size: 0.9rem; color: #37474F; margin-bottom: 4px;">
              స్పష్ట డిగ్రీ: <strong>${beeja.degree !== undefined ? beeja.degree + '°' : '—'} (${beeja.rashi_name_te || '—'})</strong>
            </div>
            <div style="font-size: 0.92rem; font-weight: 700; color: #1565C0; margin-bottom: 4px;">
              ${beeja.status || '—'}
            </div>
            <p style="margin: 0; font-size: 0.88rem; color: #555; line-height: 1.5;">${beeja.description || '—'}</p>
          </div>

          <!-- Kshetra Sphuta (Female) -->
          <div style="background: #FFF; border: 1px solid #F8BBD0; border-top: 4px solid #C2185B; border-radius: 8px; padding: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <strong style="color: #880E4F; font-size: 0.98rem;">👩 స్త్రీ క్షేత్ర స్పష్టం (Womb & Fertility Energy)</strong>
              <span class="dignity-tag ${kshetra.badge === 'success' ? 'dignity-exalted' : (kshetra.badge === 'danger' ? 'dignity-debilitated' : 'dignity-friend')}" style="font-size: 0.78rem;">
                ${kshetra.badge === 'success' ? 'సంపూర్ణ బలం' : (kshetra.badge === 'danger' ? 'గర్భస్రావ దోషం' : 'మధ్యమం')}
              </span>
            </div>
            <div style="font-size: 0.9rem; color: #37474F; margin-bottom: 4px;">
              స్పష్ట డిగ్రీ: <strong>${kshetra.degree !== undefined ? kshetra.degree + '°' : '—'} (${kshetra.rashi_name_te || '—'})</strong>
            </div>
            <div style="font-size: 0.92rem; font-weight: 700; color: #AD1457; margin-bottom: 4px;">
              ${kshetra.status || '—'}
            </div>
            <p style="margin: 0; font-size: 0.88rem; color: #555; line-height: 1.5;">${kshetra.description || '—'}</p>
          </div>

        </div>
      </div>

      <!-- Detected Santana Doshas List -->
      ${doshasListHtml}

      <div style="font-size: 0.88rem; color: #5D4037; background: #FAF5EB; padding: 8px 12px; border-radius: 6px; margin-top: 10px;">
        <strong>📖 శాస్త్రోక్త గమనిక:</strong> ${sa.shastric_note || 'ప్రాచీన హోరా శాస్త్రాల ప్రకారం శారీరక వైద్యంతో పాటు శాస్త్రోక్త దైవిక పరిహారాలను శుభ ముహూర్తంలో ఆచరించినప్పుడు సంపూర్ణ సంతాన భాగ్యం కలుగుతుంది.'}
      </div>
    `;
  }

  // 3. Render Vedic Remedy Verification Engine (శాస్త్రోక్త పరిహార పునఃసమీక్ష యంత్రం)
  const recheckContainer = document.getElementById("remedyVerificationContainer");
  if (recheckContainer && data.remedy_verification) {
    const rvData = data.remedy_verification;
    const pujas = rvData.verified_pujas || [];

    let pujasHtml = pujas.map((p, idx) => {
      const bannerClass = p.verdict_badge === "success" ? "verdict-success" :
                          (p.verdict_badge === "info" ? "verdict-info" :
                          (p.verdict_badge === "danger" ? "verdict-danger" : "verdict-warning"));

      return `
        <div class="recheck-audit-card" data-puja-index="${idx}">
          <div class="recheck-card-header">
            <div class="recheck-card-title">
              <span>🕉️</span> ${p.puja_name}
            </div>
            <span class="dignity-tag dignity-exalted" style="font-size: 0.85rem;">శాస్త్రోక్త తనిఖీ పూర్తయినది</span>
          </div>

          <div class="recheck-verdict-banner ${bannerClass}">
            <span style="font-size: 1.3rem;">🛡️</span>
            <div>
              <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">పరిశీలనా ఫలితం (Verdict):</div>
              <div style="font-size: 1.08rem; font-weight: 800;">${p.verdict_title}</div>
            </div>
          </div>

          <p style="font-size: 1rem; color: #2B2118; margin: 10px 0; line-height: 1.65; font-weight: 500;">
            ${p.verdict_summary}
          </p>

          <div class="recheck-detail-grid">
            <div class="recheck-detail-box">
              <div class="recheck-detail-label" style="color: #4A0E17;">
                <span>🔍</span> ఖచ్చితమైన ఖగోళ & జాతక హేతువు:
              </div>
              <p>${p.astrological_reason}</p>
            </div>
            <div class="recheck-detail-box">
              <div class="recheck-detail-label" style="color: #0D47A1;">
                <span>📜</span> ప్రామాణిక గ్రంథ ప్రమాణం:
              </div>
              <p><strong>${p.shastra_authority}</strong></p>
            </div>
          </div>

          <div class="recheck-zero-cost-box">
            <div style="font-size: 0.95rem; font-weight: 800; color: #1B5E20; margin-bottom: 4px;">
              <span>💡</span> ఖర్చులేని నిజమైన శాస్త్రోక్త సాధన & వైదిక పరిహారం:
            </div>
            <p style="color: #2E7D32; margin: 0; line-height: 1.65; font-size: 0.95rem; font-weight: 500;">
              ${p.zero_cost_remedy}
            </p>
          </div>

          <div class="recheck-warning-box">
            <span>⚠️</span> <strong>పరిశీలన & జాగ్రత్త:</strong> ${p.commercial_warning}
          </div>

          <div style="margin-top: 10px; text-align: right;">
            ${(() => {
              let evKey = "navagraha_shanti";
              const pLower = (p.puja_name || "").toLowerCase();
              if (pLower.includes("సర్ప") || pLower.includes("నాగ") || pLower.includes("కాలసర్ప") || pLower.includes("రాహు")) evKey = "naga_pratishtha";
              else if (pLower.includes("కుజ") || pLower.includes("సుబ్రహ్మణ్య") || pLower.includes("మాంగళిక")) evKey = "kuja_shanti_subrahmanya";
              else if (pLower.includes("శని") || pLower.includes("రుద్ర") || pLower.includes("ఈశ్వర")) evKey = "rudra_pashupatam";
              else if (pLower.includes("సంతాన") || pLower.includes("గోపాల")) evKey = "santana_gopala";
              else if (pLower.includes("పితృ") || pLower.includes("నారాయణ")) evKey = "tila_homa_narayana_bali";
              else if (pLower.includes("చండీ") || pLower.includes("దుర్గా")) evKey = "chandi_homam";

              const btnColor = (p.verdict_badge === "danger" || p.verdict_badge === "warning") ? "linear-gradient(135deg, #FF6F00, #E65100)" : "linear-gradient(135deg, #1976D2, #0D47A1)";
              return `
                <button type="button" class="btn-submit" style="padding: 7px 16px; font-size: 0.9rem; border-radius: 6px; background: ${btnColor}; color: white; border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; font-weight: 700; box-shadow: 0 2px 6px rgba(0,0,0,0.15);"
                  onclick="window.launchMuhurtamForRemedy('${evKey}', '${encodeURIComponent(p.puja_name)}')">
                  <span>⏱️</span> ఈ పరిహార పూజకు ముహూర్తం లెక్కించండి (Calculate Muhurtam)
                </button>
              `;
            })()}
          </div>
        </div>
      `;
    }).join("");

    recheckContainer.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
        <div>
          <h3 class="card-title" style="margin: 0; color: #4A0E17; font-size: 1.25rem;">
            <span>🛡️</span> శాస్త్రోక్త పరిహార పునఃసమీక్ష & నిర్ధారణ యంత్రం (Puja Recheck Validator)
          </h3>
          <p class="section-desc" style="margin: 4px 0 0 0;">
            పండితులు లేదా ఇతరులు సూచించిన పూజలు/పరిహారాలు మీ జాతకానికి నిజంగా అవసరమా లేదా దోష భంగం వల్ల నిరర్థకమా అనేది ప్రామాణిక గ్రంథాల ఆధారంగా నిర్ధారించబడింది.
          </p>
        </div>
        <span class="dignity-tag dignity-exalted" style="font-weight: bold;">ప్రామాణిక శాస్త్ర నిర్ధారణ</span>
      </div>

      <div class="verified-pujas-list">
        ${pujasHtml}
      </div>
    `;
  }
}

/* 11e. Render Predictions (సమగ్ర జ్యోతిష్య ఫలాలు) */
function renderPredictions(data) {
  const container = document.getElementById("predictionsContainer");
  if (!container || !data.predictions) return;

  const pred = data.predictions;
  const lp = pred.lagna_predictions || {};
  const np = pred.nakshatra_predictions || {};
  const rp = pred.rashi_predictions || "";
  const dp = pred.dasha_predictions || "";

  container.innerHTML = `
    <!-- 1. Lagna Predictions -->
    <div class="prediction-card">
      <div class="prediction-card-header">
        <div class="pred-title">🪷 ${lp.title || 'లగ్న సమగ్ర ఫలాలు'}</div>
        <span class="dignity-tag dignity-exalted">జన్మ లగ్నం</span>
      </div>
      <div class="pred-body">
        <div class="pred-field">
          <strong>🌿 స్వభావం & మనస్తత్వం:</strong>
          <p>${lp.nature || '—'}</p>
        </div>
        <div class="pred-field">
          <strong>👤 రూపలక్షణాలు & వ్యక్తిత్వం:</strong>
          <p>${lp.physical || '—'}</p>
        </div>
        <div class="pred-field">
          <strong>💼 అనుకూల వృత్తి & వ్యాపార రంగాలు:</strong>
          <p>${lp.career || '—'}</p>
        </div>
        <div class="pred-field alert-guidance">
          <strong>⚠️ జీవన జాగ్రత్తలు & సలహాలు:</strong>
          <p>${lp.caution || '—'}</p>
        </div>
      </div>
    </div>

    <!-- 2. Nakshatra Predictions -->
    <div class="prediction-card">
      <div class="prediction-card-header">
        <div class="pred-title">✨ జన్మ నక్షత్ర ఫలాలు (${np.name || 'నక్షత్రం'})</div>
        <span class="dignity-tag dignity-friend">పాలక గ్రహం: ${np.ruling || '—'}</span>
      </div>
      <div class="pred-body">
        <div class="pred-field">
          <strong>🌟 సహజ గుణగణాలు & నైపుణ్యాలు:</strong>
          <p>${np.traits || '—'}</p>
        </div>
        <div class="pred-field">
          <strong>🩺 ఆరోగ్య సూచనలు & శరీర భాగాలు:</strong>
          <p>${np.health || '—'}</p>
        </div>
      </div>
    </div>

    <!-- 3. Moon Sign (Rashi) Predictions -->
    <div class="prediction-card">
      <div class="prediction-card-header">
        <div class="pred-title">🌙 చంద్ర రాశి ఫలాలు (Moon Sign Outlook)</div>
        <span class="dignity-tag dignity-own">జన్మ రాశి</span>
      </div>
      <div class="pred-body">
        <div class="pred-field">
          <p style="font-size: 1.05rem; line-height: 1.7;">${rp}</p>
        </div>
      </div>
    </div>

    <!-- 4. Active Dasha-Bhukti Predictions -->
    <div class="prediction-card">
      <div class="prediction-card-header">
        <div class="pred-title">⏳ ప్రస్తుత దశా-భుక్తి జ్యోతిష్య ఫలాలు</div>
        <span class="dignity-tag dignity-exalted">ప్రస్తుత కాలమానం</span>
      </div>
      <div class="pred-body">
        <div class="pred-field">
          <p style="font-size: 1.05rem; line-height: 1.7;">${dp}</p>
        </div>
      </div>
    </div>
  `;
}

/* 12. Tabs Navigation */
function initTabNavigation() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(btn => {
    btn.addEventListener("click", () => {
      tabs.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const target = btn.getAttribute("data-tab");
      const targetContent = document.getElementById(target);
      if (targetContent) {
        targetContent.classList.add("active");
        if (window.currentScript && window.currentScript !== "Telugu") {
          applyTransliterationToPage(targetContent);
        }
      }
    });
  });
}

/* 13. Global Module Navigation (Kundali, Prashna, Shishu, Eclipses) */
function initGlobalNavigation() {
  const navBtns = document.querySelectorAll(".global-nav-btn");
  const moduleViews = document.querySelectorAll(".global-module-view");

  navBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetModuleId = btn.getAttribute("data-module");
      if (!targetModuleId) return;

      navBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      moduleViews.forEach(view => {
        if (view.id === targetModuleId) {
          view.style.display = "block";
          if (window.currentScript && window.currentScript !== "Telugu") {
            applyTransliterationToPage(view);
          }
        } else {
          view.style.display = "none";
        }
      });

      if (targetModuleId === "moduleEclipses") {
        const container = document.getElementById("eclipsesResultContainer");
        if (container && (!container.children || container.children.length === 0)) {
          loadEclipses(currentEclipsesYear);
        }
      }

      if (targetModuleId === "moduleMuhurtam") {
        if (typeof window.renderMuhurtamJatakamAssistant === "function") {
          window.renderMuhurtamJatakamAssistant();
        }
        if (typeof window.updateMuhurtamEventContextCard === "function") {
          const evSelect = document.getElementById("muhurtamEventType");
          window.updateMuhurtamEventContextCard(evSelect ? evSelect.value : "naga_pratishtha");
        }
      }
    });
  });
}

/* 14. Classical Tables Renderer (Ghata, Lucky, Jaimini, Maitri, Aspects, Vastu, Gems) */
function renderClassicalTables(data) {
  if (!data || !data.classical_tables) return;
  const tables = data.classical_tables;

  // 1. Ghata Chakra
  const ghata = tables.ghata_chakra;
  const ghataBody = document.getElementById("ghataTableBody");
  if (ghataBody && ghata) {
    ghataBody.innerHTML = `
      <tr><th>జన్మ రాశి</th><td><strong>${ghata.rashi_name_te || ''}</strong></td></tr>
      <tr><th>ఘాత మాసం</th><td>${ghata.masa || ''}</td></tr>
      <tr><th>ఘాత తిథులు</th><td>${ghata.tithi || ''}</td></tr>
      <tr><th>ఘాత వారం</th><td><span class="dignity-tag dignity-enemy">${ghata.vara || ''}</span></td></tr>
      <tr><th>ఘాత నక్షత్రం</th><td>${ghata.nakshatra || ''}</td></tr>
      <tr><th>ఘాత యోగం</th><td>${ghata.yoga || ''}</td></tr>
      <tr><th>ఘాత కరణం</th><td>${ghata.karana || ''}</td></tr>
      <tr><th>ఘాత ప్రహర</th><td>${ghata.prahar || ''}</td></tr>
      <tr><th>ఘాత రాశి (నిషిద్ధం)</th><td><span class="dignity-tag dignity-debilitated">${ghata.ghata_rashi || ghata.rashi || ''}</span></td></tr>
    `;
  }

  // 2. Lucky Factors
  const lucky = tables.lucky_factors;
  const luckyBody = document.getElementById("luckyTableBody");
  if (luckyBody && lucky) {
    const formatVal = (v) => {
      if (v === null || v === undefined) return '—';
      if (Array.isArray(v)) return v.join(", ");
      return String(v);
    };

    luckyBody.innerHTML = `
      <tr><th>అదృష్ట వారాలు</th><td>${formatVal(lucky.days)}</td></tr>
      <tr><th>అనుకూల గ్రహాలు</th><td>${formatVal(lucky.planets)}</td></tr>
      <tr><th>జీవన రత్నం (Lagna Gem)</th><td><strong>${lucky.life_gem || '—'}</strong></td></tr>
      <tr><th>అదృష్ట రత్నం (Lucky Gem)</th><td><strong>${lucky.lucky_gem || '—'}</strong></td></tr>
      <tr><th>భాగ్య రత్నం (Bhagya Gem)</th><td><strong>${lucky.bhagya_gem || '—'}</strong></td></tr>
      <tr><th>అనుకూల లోహం</th><td>${lucky.metal || '—'}</td></tr>
      <tr><th>అనుకూల రంగు</th><td>${lucky.color || '—'}</td></tr>
      <tr><th>అదృష్ట సంఖ్యలు</th><td>${formatVal(lucky.numbers)}</td></tr>
      <tr><th>ఆరాధించవలసిన దైవం</th><td>${lucky.deity || '—'}</td></tr>
    `;
  }

  // 3. Jaimini Chara Karakas
  const jaimini = tables.jaimini_karakas;
  const jaiminiBody = document.getElementById("jaiminiTableBody");
  const karakasList = Array.isArray(jaimini) ? jaimini : ((jaimini && jaimini.chara_karakas) ? jaimini.chara_karakas : []);
  if (jaiminiBody && karakasList.length > 0) {
    jaiminiBody.innerHTML = karakasList.map(k => `
      <tr>
        <td><strong>${k.karaka_code}</strong></td>
        <td><strong>${k.karaka_name_te}</strong><br><small class="text-muted">${k.karaka_name_en}</small></td>
        <td><span class="dignity-tag dignity-exalted">${k.planet_name_te} (${k.planet_name_en})</span></td>
        <td>${k.rashi_name_te} (${k.degree_formatted})</td>
        <td>${k.signifies}</td>
      </tr>
    `).join("");
  }

  // 4. Maitri Chakra (Compound 5-fold Friendship)
  const maitri = tables.maitri_chakra;
  const mHeader = document.getElementById("maitriTableHeader");
  const mBody = document.getElementById("maitriTableBody");
  if (mHeader && mBody && maitri) {
    const planets = Array.isArray(maitri.planets)
      ? maitri.planets
      : (Array.isArray(maitri.order) ? maitri.order.map(p => (maitri.telugu_names && maitri.telugu_names[p]) || p) : []);

    if (planets.length > 0) {
      mHeader.innerHTML = `<th>గ్రహం</th>` + planets.map(p => `<th>${p}</th>`).join("");
      mBody.innerHTML = planets.map(p1 => {
        const cells = planets.map(p2 => {
          if (p1 === p2) return `<td class="text-center">—</td>`;
          let rel = "సమస్థితి";
          if (maitri.panchadha && maitri.panchadha[p1] && maitri.panchadha[p1][p2]) {
            rel = maitri.panchadha[p1][p2];
          } else if (maitri.matrix && maitri.matrix[p1] && maitri.matrix[p1][p2]) {
            rel = maitri.matrix[p1][p2].rel || "సముడు";
          }
          let badgeClass = "dignity-neutral";
          if (rel.includes("అధి మిత్రుడు") || rel.includes("అతిమిత్రుడు")) badgeClass = "dignity-exalted";
          else if (rel.includes("మిత్రుడు")) badgeClass = "dignity-friend";
          else if (rel.includes("అధి శత్రువు") || rel.includes("అతిశత్రువు")) badgeClass = "dignity-debilitated";
          else if (rel.includes("శత్రువు")) badgeClass = "dignity-enemy";
          return `<td class="text-center"><span class="dignity-tag ${badgeClass}">${rel}</span></td>`;
        }).join("");
        return `<tr><th>${p1}</th>${cells}</tr>`;
      }).join("");
    }
  }

  // 5. Aspects
  const aspects = tables.planetary_aspects;
  const pAspectsBody = document.getElementById("planetAspectsTableBody");
  const hAspectsBody = document.getElementById("houseAspectsTableBody");

  if (pAspectsBody && aspects && Array.isArray(aspects.planet_aspects)) {
    pAspectsBody.innerHTML = aspects.planet_aspects.map(pa => {
      const houses = Array.isArray(pa.aspected_houses)
        ? pa.aspected_houses
        : (Array.isArray(pa.aspecting_bhavas) ? pa.aspecting_bhavas : []);
      const aspBadges = houses.map(h => `<span class="dignity-tag dignity-neutral" style="margin: 2px;">${h}వ భావం</span>`).join(" ");
      const pTe = pa.planet_te || pa.planet_name_te || '';
      const pEn = pa.planet_en || pa.planet_name_en || '';
      const curH = pa.current_house || pa.placed_bhava || '';
      const curR = pa.current_rashi_te || '';

      return `
        <tr>
          <td><strong>${pTe}</strong> (${pEn})</td>
          <td><span class="dignity-tag dignity-own">${curH}వ భావం</span> ${curR ? `(${curR})` : ''}</td>
          <td>
            ${aspBadges || '<span class="text-muted">—</span>'}
            ${pa.special_aspects_te ? `<br><small style="color: #c07a16; font-weight: 500;">${pa.special_aspects_te}</small>` : ''}
          </td>
        </tr>
      `;
    }).join("");
  }

  if (hAspectsBody && aspects && Array.isArray(aspects.house_aspects)) {
    hAspectsBody.innerHTML = aspects.house_aspects.map(ha => {
      let planetsList = '<span class="text-muted">ప్రత్యక్ష దృష్టి లేదు</span>';
      if (Array.isArray(ha.aspecting_planets) && ha.aspecting_planets.length > 0) {
        planetsList = ha.aspecting_planets.map(p => `<span class="dignity-tag dignity-friend" style="margin: 2px;">${p}</span>`).join(" ");
      } else if (typeof ha.aspecting_planets === "string" && ha.aspecting_planets && !ha.aspecting_planets.includes("శూన్యం")) {
        planetsList = ha.aspecting_planets.split(", ").map(p => `<span class="dignity-tag dignity-friend" style="margin: 2px;">${p}</span>`).join(" ");
      } else if (typeof ha.aspecting_planets_str === "string" && ha.aspecting_planets_str && !ha.aspecting_planets_str.includes("శూన్యం")) {
        planetsList = ha.aspecting_planets_str.split(", ").map(p => `<span class="dignity-tag dignity-friend" style="margin: 2px;">${p}</span>`).join(" ");
      }

      const hNum = ha.house || ha.bhava || '';
      const sTe = ha.sign_te || '';
      return `
        <tr>
          <td><strong>${hNum}వ భావం</strong> ${sTe ? `(${sTe})` : ''}</td>
          <td>${planetsList}</td>
        </tr>
      `;
    }).join("");
  }

  // 6. Gemstones & Rudraksha
  const gems = tables.gemstones_rudraksha;
  const gemsContainer = document.getElementById("gemstonesContainer");
  if (gemsContainer && gems) {
    gemsContainer.innerHTML = `
      <div class="gem-recommendation-card">
        <div class="gem-badge-row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px;">
          <div class="stat-box" style="text-align: left; padding: 16px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">లగ్నాధిపతి రత్నం (జీవన రత్నం)</span>
            <div style="font-size: 1.25rem; font-weight: 800; color: #B75300; margin: 6px 0;">💍 ${gems.life_gem}</div>
            <p style="font-size: 0.9rem; color: #3E2723; margin: 0; line-height: 1.6; font-weight: 500;">ఆయురారోగ్యాలు, ఆత్మవిశ్వాసం, సర్వతోముఖాభివృద్ధికి నిత్య రక్షణ.</p>
          </div>
          <div class="stat-box" style="text-align: left; padding: 16px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">పంచమాధిపతి రత్నం (అదృష్ట రత్నం)</span>
            <div style="font-size: 1.25rem; font-weight: 800; color: #1B5E20; margin: 6px 0;">✨ ${gems.lucky_gem}</div>
            <p style="font-size: 0.9rem; color: #3E2723; margin: 0; line-height: 1.6; font-weight: 500;">మేధాశక్తి, విద్యా విజయం, సంతాన క్షేమం మరియు ఆలోచనా బలము.</p>
          </div>
          <div class="stat-box" style="text-align: left; padding: 16px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">భాగ్యాధిపతి రత్నం (భాగ్య రత్నం)</span>
            <div style="font-size: 1.25rem; font-weight: 800; color: #0D47A1; margin: 6px 0;">🌟 ${gems.bhagya_gem}</div>
            <p style="font-size: 0.9rem; color: #3E2723; margin: 0; line-height: 1.6; font-weight: 500;">అదృష్టం, దైవానుగ్రహం, ఉన్నత వ్యాపార పదవులు మరియు సంపద.</p>
          </div>
        </div>

        <div style="margin-top: 20px; padding: 18px; background: #FFFDF7; border-radius: 8px; border-left: 4px solid #D84315; border: 1.5px solid #FFE082;">
          <div style="font-size: 1.15rem; font-weight: 800; color: #4A0E17; margin-bottom: 8px;">📿 నక్షత్ర రుద్రాక్ష & ఇష్ట దైవం:</div>
          <p style="margin: 8px 0; font-size: 0.98rem; color: #2B2118;"><strong style="color: #4A0E17;">ధరించవలసిన రుద్రాక్ష:</strong> <span class="dignity-tag dignity-exalted" style="font-weight: 700;">${gems.rudraksha}</span></p>
          <p style="margin: 8px 0; font-size: 0.98rem; color: #2B2118;"><strong style="color: #4A0E17;">ఇష్ట దైవతారాధన:</strong> <strong style="color: #0D47A1;">${gems.ishta_devata}</strong></p>
          <p style="margin: 8px 0; font-size: 0.98rem; color: #2B2118;"><strong style="color: #4A0E17;">పారాయణ స్తోత్రం:</strong> <em style="color: #1B5E20; font-weight: 600;">${gems.stotram}</em></p>
          <p style="margin: 8px 0 0 0; font-size: 0.98rem; color: #3E2723; font-weight: 600; line-height: 1.7;">${gems.deity_mantra_te}</p>
        </div>

        <!-- Strictly Prohibited Gems Warning Matrix (శాస్త్రోక్త రత్న రక్షణ నియమాలు) -->
        <div class="prohibited-gems-wrapper" style="margin-top: 22px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
            <h4 style="color: #B71C1C; margin: 0; font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 6px;">
              <span>🚫</span> ఖచ్చితంగా నిషిద్ధమైన రత్నాలు (Strictly Prohibited Gems)
            </h4>
            <span class="dignity-tag dignity-debilitated">ధరించరాదు • తీవ్ర హానికరం</span>
          </div>

          <div style="font-size: 0.92rem; color: #5D4037; background: #FFF; padding: 10px 14px; border-radius: 6px; border: 1px solid #FFCDD2; margin-bottom: 14px; line-height: 1.6;">
            <strong>📜 శాస్త్రోక్త రత్న ధారణ నియమం:</strong> ${gems.shastra_gem_rule || 'జాతక చంద్రిక: 6, 8, 12 దుఃస్థానాధిపతుల రత్నాలు ధరిస్తే రోగాలు, శత్రుపీడ, ప్రమాదాలు పెరుగుతాయి.'}
          </div>

          ${(gems.strictly_prohibited_gems || []).map(pg => `
            <div class="prohibited-gem-card">
              <div class="prohibited-gem-title">❌ ${pg.gem} (${pg.planet} - ${pg.houses})</div>
              <p class="prohibited-gem-reason"><strong>హేతువు / కారణం:</strong> ${pg.reason}</p>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  // 7. Vastu Facing
  const vastu = tables.vastu_facing;
  const vastuContainer = document.getElementById("vastuContainer");
  if (vastuContainer && vastu) {
    const rules = Array.isArray(vastu.vastu_rules_te) ? vastu.vastu_rules_te : [];
    const rulesList = rules.map(r => `<li style="margin-bottom: 6px;">${r}</li>`).join("");
    vastuContainer.innerHTML = `
      <div class="vastu-recommendation-card">
        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
          <div class="stat-box" style="flex: 1; min-width: 140px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">జన్మ రాశి తత్వం</span>
            <span class="stat-num" style="font-size: 1.15rem; color: #B75300; font-weight: 800;">${vastu.tattva}</span>
          </div>
          <div class="stat-box" style="flex: 1.5; min-width: 180px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">శ్రేష్ఠమైన సింహద్వారం</span>
            <span class="stat-num" style="font-size: 1.15rem; color: #1B5E20; font-weight: 800;">🚪 ${vastu.recommended_facing}</span>
          </div>
          <div class="stat-box" style="flex: 1; min-width: 140px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">ప్రత్యామ్నాయ ద్వారం</span>
            <span class="stat-num" style="font-size: 1.15rem; color: #0D47A1; font-weight: 800;">${vastu.secondary_facing}</span>
          </div>
          <div class="stat-box" style="flex: 1; min-width: 140px; background: #FFFFFF; border: 1.5px solid #EADBCE;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">నిషిద్ధ దిశ</span>
            <span class="stat-num" style="font-size: 1.15rem; color: #C62828; font-weight: 800;">🚫 ${vastu.avoid_direction}</span>
          </div>
        </div>

        <div style="margin-top: 20px; padding: 18px; background: #FAF7F2; border-radius: 8px; border: 1.5px solid #EADBCE;">
          <h4 style="color: #4A0E17; margin-bottom: 10px; font-size: 1.1rem; font-weight: 800;">🏛️ శాస్త్రోక్త వాస్తు నియమాలు:</h4>
          <ul style="padding-left: 22px; line-height: 1.8; color: #2B2118; font-size: 0.95rem; font-weight: 500;">
            ${rulesList}
          </ul>
        </div>
      </div>
    `;
  }
}

/* 15. Prashna Jyotishyam Module */
function initPrashnaModule() {
  const form = document.getElementById("prashnaForm");
  if (!form) return;

  setupCityAutocomplete("prashnaPlace", "prashnaCitySuggestions", "prashnaLat", "prashnaLon", "prashnaTz", "prashnaCityFeedback");

  const btnNow = document.getElementById("btnPrashnaNow");
  if (btnNow) {
    btnNow.addEventListener("click", () => {
      const now = new Date();
      const yyyy = now.getFullYear();
      const mm = String(now.getMonth() + 1).padStart(2, '0');
      const dd = String(now.getDate()).padStart(2, '0');
      const hh = String(now.getHours()).padStart(2, '0');
      const min = String(now.getMinutes()).padStart(2, '0');
      const ss = String(now.getSeconds()).padStart(2, '0');

      document.getElementById("prashnaDate").value = `${yyyy}-${mm}-${dd}`;
      document.getElementById("prashnaTime").value = `${hh}:${min}:${ss}`;
    });
    btnNow.click();
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await ensureCityResolved("prashnaPlace", "prashnaLat", "prashnaLon", "prashnaTz", "prashnaCityFeedback");
    const btnSubmit = document.getElementById("btnSubmitPrashna");
    const container = document.getElementById("prashnaResultContainer");

    const category = document.getElementById("prashnaCategorySelect").value;
    const date = document.getElementById("prashnaDate").value;
    const time = document.getElementById("prashnaTime").value;
    const place = document.getElementById("prashnaPlace").value;
    const lat = parseFloat(document.getElementById("prashnaLat").value) || 17.3850;
    const lon = parseFloat(document.getElementById("prashnaLon").value) || 78.4867;
    const tz = parseFloat(document.getElementById("prashnaTz").value) || 5.5;
    const ayanamsa = document.getElementById("prashnaAyanamsa").value || "lahiri";

    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `<span class="spinner"></span> తాజిక యోగాల విశ్లేషణ జరుగుతోంది...`;

    try {
      const resp = await fetch("/api/v1/prashna/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question_id: category,
          category,
          date,
          time,
          place_name: place,
          latitude: lat,
          longitude: lon,
          timezone_offset: tz,
          ayanamsa
        })
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || "Prashna calculation error");
      }

      const res = await resp.json();
      renderPrashnaResults(res);
      container.style.display = "block";
      container.scrollIntoView({ behavior: "smooth" });
      if (window.currentScript && window.currentScript !== "Telugu") {
        applyTransliterationToPage(container);
      }

    } catch (err) {
      alert(`ప్రశ్న విశ్లేషణలో లోపం: ${err.message}`);
    } finally {
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = `<span>🔮</span> ప్రశ్న విశ్లేషణ చేయండి (Evaluate Prashna)`;
    }
  });
}

function renderPrashnaResults(data) {
  const container = document.getElementById("prashnaResultContainer");
  if (!container) return;

  const score = data.score_percent !== undefined ? data.score_percent : (data.probability_score || 50);
  const verdictText = data.verdict || data.verdict_te || "అనుకూలం (Yes - Favorable)";
  const isFavorable = score >= 70 || verdictText.includes("అనుకూలం") || (data.verdict_badge === "success");
  const isModerate = (score >= 40 && score < 70) || verdictText.includes("మధ్యమం") || (data.verdict_badge === "warning");

  let badgeColor = isFavorable ? "#4caf50" : (isModerate ? "#ff9800" : "#f44336");
  let meterColor = isFavorable ? "linear-gradient(90deg, #ff9800, #4caf50)" : (isModerate ? "linear-gradient(90deg, #2196f3, #ff9800)" : "linear-gradient(90deg, #f44336, #e91e63)");

  const yogas = data.tajika_yogas || [];
  const yogasHtml = (yogas.length > 0)
    ? yogas.map(y => {
      const yName = y.name || y.yoga_name_te || "తాజిక యోగం";
      const yType = y.type || y.yoga_name_en || "Tajika Yoga";
      const yDesc = y.desc || y.details_te || "";
      return `
        <div style="background: #FAF7F2; border: 1.5px solid #EADBCE; border-radius: 8px; padding: 14px 16px; margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <strong style="color: #4A0E17; font-size: 1.1rem; font-weight: 800;">${yName}</strong>
            <span class="dignity-tag dignity-exalted" style="font-weight: 700;">${yType}</span>
          </div>
          <p style="margin: 8px 0 0 0; font-size: 0.95rem; color: #2B2118; line-height: 1.7; font-weight: 500;">${yDesc}</p>
        </div>
      `;
    }).join("")
    : `<p style="color: #5D4037; font-weight: 600; font-style: italic; padding: 12px; background: #FAF7F2; border-radius: 6px;">ప్రత్యేక తాజిక సంయోగం ఏర్పడలేదు (సమగ్ర గ్రహ స్థితి ఆధారంగా ఫలితం లెక్కించబడింది).</p>`;

  const remedies = data.remedies || data.remedies_te || [];
  const remediesHtml = (remedies.length > 0)
    ? remedies.map(r => `<li style="margin-bottom: 6px;">${r}</li>`).join("")
    : `<li style="margin-bottom: 6px;">నిత్యం ఇష్ట దైవ నామస్మరణ చేయండి.</li>`;

  const questionTitle = data.question_title_te || data.question_te || "ప్రశ్న జ్యోతిష్యం";
  const placeText = data.location || data.place_name || "నమోదిత స్థలం";
  const timeText = data.calculation_time || `${data.query_date || ''} ${data.query_time || ''}`.trim();
  const verdictSummary = data.verdict_summary || data.verdict_explanation_te || "";
  const lagnaInfo = data.lagna_dms || (data.prashna_lagna ? `${data.prashna_lagna.rashi_name_te} (${data.prashna_lagna.degree_formatted})` : "—");
  const lagneshaInfo = data.lagnesha || (data.prashna_lagna ? data.prashna_lagna.lord_te : "—");
  const bhavaNum = data.karya_bhava || 10;
  const bhavaTitle = data.karya_bhava_title || `${bhavaNum}వ భావం`;
  const karyeshaInfo = typeof data.karyesha === 'string' ? data.karyesha : (data.karyesha ? `${data.karyesha.lord_te} (${data.karyesha.rashi_te || ''})` : "—");
  const timingInfo = data.timing_estimate || data.event_timing_te || "త్వరలో కార్యసిద్ధి లభించును";

  container.innerHTML = `
    <div class="prediction-card">
      <div class="prediction-card-header">
        <div class="pred-title">🔮 ${questionTitle} — ప్రత్యక్ష ప్రశ్న సమాధానం</div>
        <span class="dignity-tag dignity-own" style="font-weight: 700;">${placeText} | ${timeText}</span>
      </div>
      <div class="pred-body">

        <!-- Verdict Banner -->
        <div style="text-align: center; padding: 24px; background: #FFFFFF; border-radius: 12px; margin-bottom: 24px; border: 2px solid ${badgeColor}; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px; color: #5D4037; font-weight: 700;">శాస్త్రోక్త ప్రశ్న నిర్ణయం (Final Verdict)</div>
          <div style="font-size: 2.2rem; font-weight: 800; color: ${badgeColor}; margin: 8px 0;">${verdictText}</div>
          <p style="font-size: 1.05rem; line-height: 1.7; color: #2B2118; font-weight: 600; max-width: 750px; margin: 0 auto;">${verdictSummary}</p>

          <!-- Probability Meter -->
          <div style="margin-top: 18px; max-width: 500px; margin-left: auto; margin-right: auto;">
            <div style="display: flex; justify-content: space-between; font-size: 0.92rem; color: #37474F; font-weight: 700; margin-bottom: 6px;">
              <span>కార్యసిద్ధి సంభావ్యత (Success Probability)</span>
              <strong style="color: #4A0E17; font-size: 1.05rem;">${score}%</strong>
            </div>
            <div style="background: #ECEFF1; border: 1.5px solid #CFD8DC; border-radius: 10px; height: 14px; overflow: hidden;">
              <div style="width: ${score}%; height: 100%; background: ${meterColor}; border-radius: 10px; transition: width 1s ease;"></div>
            </div>
          </div>
        </div>

        <!-- Astrological Parameters -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px; margin-bottom: 20px;">
          <div class="stat-box" style="background: #FFFFFF; border: 1.5px solid #EADBCE; text-align: left; padding: 14px 18px;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">ప్రశ్న లగ్నం & లగ్నాధిపతి</span>
            <span class="stat-num" style="font-size: 1.12rem; color: #B75300; font-weight: 800;">${lagnaInfo} — అధిపతి: ${lagneshaInfo}</span>
          </div>
          <div class="stat-box" style="background: #FFFFFF; border: 1.5px solid #EADBCE; text-align: left; padding: 14px 18px;">
            <span class="stat-label" style="color: #5D4037; font-weight: 700;">కార్య భావం & కార్యాధిపతి</span>
            <span class="stat-num" style="font-size: 1.12rem; color: #0D47A1; font-weight: 800;">${bhavaTitle} — అధిపతి: ${karyeshaInfo}</span>
          </div>
        </div>

        ${data.aspect_details ? `
        <div style="padding: 14px 18px; background: #FAF7F2; border: 1.5px solid #EADBCE; border-radius: 8px; margin-bottom: 20px;">
          <strong style="color: #4A0E17; font-size: 1rem;">📐 దీప్తాంశ & దృష్టి విశ్లేషణ:</strong> <span style="color: #2B2118; font-weight: 600;">${data.aspect_details}</span>
        </div>` : ''}

        <!-- Tajika Yogas -->
        <h3 class="card-title" style="margin-top: 25px;"><span>🤝</span> ఏర్పడిన తాజిక యోగాలు (Tajika Planetary Yogas)</h3>
        <p class="section-desc">నీలకంఠ తాజిక గ్రంథం ఆధారంగా లగ్నేశ & కార్వేశుల మధ్య కోణీయ దీప్తాంశ సంబంధం:</p>
        <div style="margin-bottom: 20px;">${yogasHtml}</div>

        <!-- Event Timing -->
        <div style="padding: 16px 18px; background: #E3F2FD; border-left: 5px solid #1565C0; border: 1.5px solid #BBDEFB; border-radius: 8px; margin-bottom: 20px;">
          <strong style="color: #0D47A1; font-size: 1.08rem; font-weight: 800;">⏳ ఫలసిద్ధి కాల నిర్ణయం (Timing of Event):</strong>
          <p style="margin: 6px 0 0 0; font-size: 1.02rem; color: #1A237E; font-weight: 700; line-height: 1.7;">${timingInfo}</p>
        </div>

        <!-- Prashna Marga Remedies -->
        <div style="padding: 16px 18px; background: #FFF8E1; border-left: 5px solid #E65100; border: 1.5px solid #FFE082; border-radius: 8px;">
          <strong style="color: #B75300; font-size: 1.08rem; font-weight: 800;">🪔 ప్రశ్న మార్గ శాస్త్రోక్త పరిహారాలు & దైవారాధన:</strong>
          <ul style="margin: 8px 0 0 0; padding-left: 22px; line-height: 1.8; color: #2B2118; font-size: 0.98rem; font-weight: 600;">
            ${remediesHtml}
          </ul>
        </div>

      </div>
    </div>
  `;
}

/* 16. Newborn Shishu Jatakam Module */
function initShishuModule() {
  const form = document.getElementById("shishuForm");
  if (!form) return;

  setupCityAutocomplete("shishuPlace", "shishuCitySuggestions", "shishuLat", "shishuLon", "shishuTz", "shishuCityFeedback");

  const genderBtns = document.querySelectorAll("#moduleShishu .gender-btn");
  const genderInput = document.getElementById("shishuGender");
  genderBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      genderBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      genderInput.value = btn.getAttribute("data-val");
    });
  });

  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const hh = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  const ss = String(now.getSeconds()).padStart(2, '0');

  const dobInput = document.getElementById("shishuDob");
  const tobInput = document.getElementById("shishuTob");
  if (dobInput && !dobInput.value) dobInput.value = `${yyyy}-${mm}-${dd}`;
  if (tobInput && !tobInput.value) tobInput.value = `${hh}:${min}:${ss}`;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await ensureCityResolved("shishuPlace", "shishuLat", "shishuLon", "shishuTz", "shishuCityFeedback");
    const btnSubmit = document.getElementById("btnSubmitShishu");
    const container = document.getElementById("shishuResultContainer");

    const name = document.getElementById("shishuName").value.trim() || "శిశువు";
    const gender = document.getElementById("shishuGender").value;
    const dob = document.getElementById("shishuDob").value;
    const tob = document.getElementById("shishuTob").value;
    const place = document.getElementById("shishuPlace").value;
    const lat = parseFloat(document.getElementById("shishuLat").value) || 17.3850;
    const lon = parseFloat(document.getElementById("shishuLon").value) || 78.4867;
    const tz = parseFloat(document.getElementById("shishuTz").value) || 5.5;
    const ayanamsa = document.getElementById("shishuAyanamsa").value || "lahiri";

    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `<span class="spinner"></span> శిశు జాతకం & బాలారిష్ట విశ్లేషణ జరుగుతోంది...`;

    try {
      const resp = await fetch("/api/v1/shishu/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          gender,
          dob,
          tob,
          place_name: place,
          latitude: lat,
          longitude: lon,
          timezone_offset: tz,
          ayanamsa
        })
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || "Shishu calculation error");
      }

      const res = await resp.json();
      renderShishuResults(res);
      container.style.display = "block";
      container.scrollIntoView({ behavior: "smooth" });
      if (window.currentScript && window.currentScript !== "Telugu") {
        applyTransliterationToPage(container);
      }

    } catch (err) {
      alert(`శిశు జాతక పరిశీలనలో లోపం: ${err.message}`);
    } finally {
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = `<span>👶</span> శిశు జాతకాన్ని పరిశీలించండి (Generate Shishu Jatakam)`;
    }
  });
}

let currentShishuChartFormat = "south";

function renderShishuResults(data) {
  const container = document.getElementById("shishuResultContainer");
  if (!container) return;
  container.style.display = "block";
  window.currentShishuData = data;

  const babyName = data.name || (data.baby_summary ? data.baby_summary.name : "శిశువు");
  const babyGender = data.gender === "female" ? "బాలిక (Girl)" : "బాలుడు (Boy)";
  const babyPlace = data.place_name || (data.baby_summary ? data.baby_summary.place_name : "");
  const babyTime = data.dob_formatted || (data.baby_summary ? `${data.baby_summary.dob} ${data.baby_summary.tob}` : "");

  const lagnaText = data.lagna_dms || (data.baby_summary ? data.baby_summary.lagna_te : "—");
  const rashiText = data.rashi_name_te || (data.baby_summary ? data.baby_summary.rashi_te : "—");
  const nakshatraText = data.nakshatra_name_te || (data.baby_summary ? data.baby_summary.nakshatra_te : "—");
  const padaNum = data.nakshatra_pada || (data.baby_summary ? data.baby_summary.pada : 1);

  const overallStatus = data.overall_status_te || "సర్వ శుభకరం • దోష రహితం";
  const isSafe = (data.overall_badge === "success") || (data.status_code === "SAFE" || data.status_code === "BHANGA_SAFE");
  const statusBadgeColor = isSafe ? "#4caf50" : "#f44336";

  // 1. Naming syllables
  const syllables = data.recommended_naming_syllables || (data.naming_syllables ? data.naming_syllables.pada_syllables : []);
  const syllablesHtml = syllables.map((syl, idx) => {
    const isCurrent = (idx + 1 === padaNum);
    return `
      <div style="padding: 14px 12px; border-radius: 8px; text-align: center; background: ${isCurrent ? '#E8F5E9' : '#FAF7F2'}; border: 1.5px solid ${isCurrent ? '#2E7D32' : '#EADBCE'}; box-shadow: ${isCurrent ? '0 2px 8px rgba(46,125,50,0.15)' : 'none'};">
        <div style="font-size: 0.88rem; font-weight: 700; color: ${isCurrent ? '#1B5E20' : '#5D4037'};">${idx + 1}వ పాదం</div>
        <div style="font-size: 1.9rem; font-weight: 800; color: ${isCurrent ? '#1B5E20' : '#4A0E17'}; margin: 4px 0;">${syl}</div>
        ${isCurrent ? `<span class="dignity-tag dignity-exalted" style="font-size: 0.75rem; font-weight: 700;">జన్మ పాదం ⭐</span>` : ''}
      </div>
    `;
  }).join("");

  // 2. Panchangam Details
  let panchangamHtml = "";
  if (data.panchangam) {
    const p = data.panchangam;
    const pItems = [
      { label: "తిథి (Tithi)", val: p.tithi, sub: p.paksha || "" },
      { label: "వారం (Vara)", val: p.vara, sub: p.vara_lord ? `అధిపతి: ${p.vara_lord}` : "" },
      { label: "నక్షత్రం (Nakshatra)", val: p.nakshatra, sub: `${p.pada || ''} (అధిపతి: ${p.nakshatra_lord || '—'})` },
      { label: "యోగం (Yoga)", val: p.yoga, sub: "నిత్య యోగం" },
      { label: "కరణం (Karana)", val: p.karana, sub: "సగం తిథి కాలం" },
      { label: "పాద చక్రం (పాయ / Foot)", val: p.paya || "రజత పాయ", sub: p.paya_desc || "శుభప్రదం" },
      { label: "గణం (Gana)", val: p.gana || "—", sub: "వ్యక్తిత్వ లక్షణం" },
      { label: "నాడి (Nadi)", val: p.nadi || "—", sub: "ఆరోగ్య & జీవశక్తి" },
      { label: "యోని (Yoni)", val: p.yoni || "—", sub: "ప్రకృతి మైత్రి" },
      { label: "వర్ణం (Varna)", val: p.varna || "—", sub: "ధర్మ సంస్కారం" },
      { label: "వశ్యం (Vashya)", val: p.vashya || "—", sub: "ఆకర్షణ తత్వం" },
      { label: "తత్వం (Tatwa)", val: p.tatwa || "—", sub: "పంచభూత తత్వం" }
    ];

    panchangamHtml = `
      <h3 class="card-title" style="margin-top: 30px;"><span>📜</span> జనన సమయ పంచాంగ & అవకహడ వివరాలు (Birth Panchangam)</h3>
      <p class="section-desc">శిశువు జన్మించిన శుభ ముహూర్త పంచాంగ తత్వాలు మరియు ప్రామాణిక అవకహడ అంశాలు:</p>
      <div class="panchangam-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px;">
        ${pItems.map(it => `
          <div class="panchangam-card" style="background: #FAF7F2; border: 1.5px solid #EADBCE; border-radius: 8px; padding: 14px 16px;">
            <div class="card-label" style="font-size: 0.85rem; color: #5D4037; font-weight: 700; text-transform: uppercase;">${it.label}</div>
            <div class="card-val" style="font-size: 1.15rem; font-weight: 800; color: #4A0E17; margin: 4px 0;">${it.val}</div>
            <div class="card-sub" style="font-size: 0.88rem; color: #2B2118; font-weight: 500;">${it.sub}</div>
          </div>
        `).join("")}
      </div>
    `;
  }

  // 3. Lagna and Navamsha Chakras (D1 & D9)
  let chartsHtml = "";
  if (data.charts) {
    chartsHtml = `
      <h3 class="card-title" style="margin-top: 30px;"><span>☸️</span> లగ్న & నవాంశ చక్రాలు (Lagna & Navamsha Kundali)</h3>
      <p class="section-desc">శిశువు జన్మ లగ్న (D1) రాశి చక్రం మరియు భాగ్య నవాంశ (D9) చక్రం:</p>
      <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
        <div class="chart-toggle-group">
          <button type="button" class="chart-toggle-btn shishu-chart-fmt-btn ${currentShishuChartFormat === 'south' ? 'active' : ''}" data-fmt="south">సాంప్రదాయ దక్షిణ భారత చక్రం</button>
          <button type="button" class="chart-toggle-btn shishu-chart-fmt-btn ${currentShishuChartFormat === 'north' ? 'active' : ''}" data-fmt="north">ఉత్తర భారత వజ్ర చక్రం</button>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 30px;">
        <div style="background: #FFFFFF; border-radius: 10px; padding: 16px; border: 1.5px solid #EADBCE; text-align: center; box-shadow: var(--shadow-sm);">
          <h4 style="color: #4A0E17; margin-bottom: 12px; font-size: 1.15rem; font-weight: 800;">D1 లగ్న రాశి చక్రం (Lagna Chart)</h4>
          <div id="shishuD1Wrapper" class="kundali-svg-container"></div>
        </div>
        <div style="background: #FFFFFF; border-radius: 10px; padding: 16px; border: 1.5px solid #EADBCE; text-align: center; box-shadow: var(--shadow-sm);">
          <h4 style="color: #4A0E17; margin-bottom: 12px; font-size: 1.15rem; font-weight: 800;">D9 నవాంశ చక్రం (Navamsha Chart)</h4>
          <div id="shishuD9Wrapper" class="kundali-svg-container"></div>
        </div>
      </div>
    `;
  }

  // 4. Tatkala Graha Sampatti Table
  let planetsTableHtml = "";
  if (data.tatkala_graha_sampatti && data.tatkala_graha_sampatti.length > 0) {
    let rowsHtml = "";
    if (data.lagna_info) {
      const l = data.lagna_info;
      rowsHtml += `
        <tr style="background: #FFF8E1; font-weight: 700; color: #4A0E17;">
          <td><strong>${l.rashi_name_te} లగ్నం</strong></td>
          <td>Lagna</td>
          <td>${l.rashi_name_te}</td>
          <td>${l.formatted_degree}</td>
          <td>${l.nakshatra_name_te} (${l.pada}వ పాదం)</td>
          <td>${l.navamsha_rashi_te}</td>
          <td><span class="dignity-tag dignity-exalted">జన్మ లగ్నం</span></td>
        </tr>
      `;
    }

    data.tatkala_graha_sampatti.forEach(p => {
      const digClass = p.dignity_en === "Exalted" ? "dignity-exalted" :
                       p.dignity_en === "Own Sign" ? "dignity-own" :
                       p.dignity_en === "Debilitated" ? "dignity-debilitated" :
                       p.dignity_en === "Friend" ? "dignity-friend" : "dignity-neutral";
      const vakraTag = p.is_retrograde ? `<span class="status-tag tag-vakra" style="margin-left: 4px;">వక్ర</span>` : "";
      const astaTag = p.is_combust ? `<span class="status-tag tag-asta" style="margin-left: 4px;">అస్తంగత</span>` : "";

      rowsHtml += `
        <tr>
          <td><strong>${p.name_te}</strong> ${vakraTag} ${astaTag}</td>
          <td>${p.name_en}</td>
          <td>${p.rashi_name_te}</td>
          <td>${p.formatted_degree}</td>
          <td>${p.nakshatra_name_te} (${p.pada}వ పాదం)</td>
          <td>${p.navamsha_rashi_te}</td>
          <td><span class="dignity-tag ${digClass}">${p.dignity_te}</span></td>
        </tr>
      `;
    });

    planetsTableHtml = `
      <h3 class="card-title" style="margin-top: 30px;"><span>🪐</span> తాత్కాలిక గ్రహ సంపత్తి (Tatkala Graha Positions & Dignity)</h3>
      <p class="section-desc">శిశు జనన క్షణంలో నవగ్రహాల రాశి, స్పష్ట డిగ్రీలు, నక్షత్ర పాదం మరియు నవాంశ స్థితులు:</p>
      <div class="table-responsive" style="margin-bottom: 25px;">
        <table class="vedic-table">
          <thead>
            <tr>
              <th>గ్రహం (Planet)</th>
              <th>ఆంగ్ల నామం</th>
              <th>రాశి (Sign)</th>
              <th>స్పష్ట డిగ్రీలు</th>
              <th>నక్షత్రం & పాదం</th>
              <th>నవాంశ రాశి</th>
              <th>గ్రహ స్థితి (Dignity)</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;
  }

  // 5. Doshas
  const doshas = data.doshas || data.doshas_identified || [];
  const doshasHtml = (doshas.length > 0)
    ? doshas.map(d => {
      if (typeof d === 'string') {
        const isBhanga = d.includes("భంగం") || d.includes("నివృత్తి");
        const badgeStyle = isBhanga ? "dignity-friend" : "dignity-debilitated";
        return `<div style="margin-bottom: 8px;"><span class="dignity-tag ${badgeStyle}" style="font-size: 0.95rem; padding: 4px 10px; font-weight: 700;">${d}</span></div>`;
      } else {
        const isBhanga = (d.badge === "success") || (d.status && d.status.includes("భంగం"));
        const borderCol = isBhanga ? "#2E7D32" : "#E65100";
        return `
          <div style="padding: 14px 16px; background: #FAF7F2; border-radius: 8px; margin-bottom: 12px; border-left: 5px solid ${borderCol}; border: 1.5px solid #EADBCE;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
              <strong style="color: #4A0E17; font-size: 1.1rem; font-weight: 800;">${d.name}</strong>
              <span class="dignity-tag ${isBhanga ? 'dignity-exalted' : 'dignity-debilitated'}" style="font-weight: 700;">${d.status || ''}</span>
            </div>
            <p style="margin: 8px 0; font-size: 0.95rem; color: #2B2118; line-height: 1.7; font-weight: 500;">${d.desc || ''}</p>
            ${d.remedy ? `<p style="margin: 6px 0 0 0; font-size: 0.92rem; color: #B71C1C; font-weight: 700;"><strong style="color: #4A0E17;">పరిహారం:</strong> ${d.remedy}</p>` : ''}
          </div>
        `;
      }
    }).join("")
    : `<div style="color: #1B5E20; font-weight: 700; font-size: 1.05rem; padding: 12px; background: #E8F5E9; border-radius: 6px; border: 1.5px solid #A5D6A7;">✓ ఎటువంటి గండాంత, మూల, లేదా సంక్రాంతి దోషాలు లేవు. సర్వ శుభకరం.</div>`;

  const remedies = data.protective_remedies || data.shanti_remedies_te || [];
  const remediesHtml = (remedies.length > 0)
    ? remedies.map(r => `<li style="margin-bottom: 6px;">${r}</li>`).join("")
    : `<li style="margin-bottom: 6px;">నిత్యం ఇష్ట దైవ నామస్మరణ చేయండి.</li>`;

  container.innerHTML = `
    <div class="prediction-card">
      <div class="prediction-card-header">
        <div class="pred-title">👶 నవశిశు జాతక సమగ్ర నివేదిక — ${babyName} (${babyGender})</div>
        <span class="dignity-tag dignity-own" style="font-weight: 700;">${babyPlace} | ${babyTime}</span>
      </div>
      <div class="pred-body">

        <!-- Overall Status Hero -->
        <div style="text-align: center; padding: 24px; background: #FFFFFF; border-radius: 12px; margin-bottom: 24px; border: 2px solid ${statusBadgeColor}; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px; color: #5D4037; font-weight: 700;">శిశు ఆయురారోగ్య & దోష స్థితి (Infant Health Status)</div>
          <div style="font-size: 2.2rem; font-weight: 800; color: ${statusBadgeColor}; margin: 8px 0;">${overallStatus}</div>
          <p style="font-size: 1.05rem; line-height: 1.7; color: #2B2118; font-weight: 600; max-width: 750px; margin: 0 auto;">
            జన్మ లగ్నం: <strong style="color: #4A0E17;">${lagnaText}</strong> | రాశి: <strong style="color: #0D47A1;">${rashiText}</strong> | నక్షత్రం: <strong style="color: #1B5E20;">${nakshatraText} ${padaNum}వ పాదం</strong>
          </p>
          ${data.summary_te ? `<p style="margin: 10px auto 0 auto; color: #37474F; font-size: 0.98rem; font-weight: 500; line-height: 1.7; max-width: 700px;">${data.summary_te}</p>` : ''}
        </div>

        <!-- 1. Naming Syllables -->
        <h3 class="card-title"><span>🔤</span> శాస్త్రోక్త నామాక్షరాలు (Auspicious Naming Syllables)</h3>
        <p class="section-desc">నక్షత్ర పాదం ఆధారంగా శిశువు నామకరణానికి ప్రథమాక్షరాలు:</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 15px; margin-bottom: 25px;">
          ${syllablesHtml}
        </div>

        <!-- 2. Birth Panchangam Details -->
        ${panchangamHtml}

        <!-- 3. Lagna & Navamsha Chakras -->
        ${chartsHtml}

        <!-- 4. Tatkala Graha Sampatti -->
        ${planetsTableHtml}

        <!-- 5. Doshas & Balarishta Evaluation -->
        <h3 class="card-title" style="margin-top: 30px;"><span>🛡️</span> బాలారిష్ట & ప్రత్యేక దోషాల పరిశీలన</h3>
        <div style="margin-bottom: 25px;">
          ${doshasHtml}
        </div>

        <!-- 6. Remedies -->
        <div style="padding: 18px; background: #FFF8E1; border-left: 5px solid #E65100; border: 1.5px solid #FFE082; border-radius: 8px;">
          <strong style="color: #B75300; font-size: 1.1rem; font-weight: 800;">🪔 శాస్త్రోక్త శాంతి పరిహారాలు & రక్షా సూచనలు:</strong>
          <ul style="margin: 8px 0 0 0; padding-left: 22px; line-height: 1.8; color: #2B2118; font-size: 0.98rem; font-weight: 600;">
            ${remediesHtml}
          </ul>
        </div>

      </div>
    </div>
  `;

  // Render SVG charts if charts data exists
  if (data.charts) {
    renderShishuSvgCharts(data, currentShishuChartFormat);

    // Setup chart toggle listeners
    const fmtBtns = container.querySelectorAll(".shishu-chart-fmt-btn");
    fmtBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        fmtBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentShishuChartFormat = btn.getAttribute("data-fmt");
        renderShishuSvgCharts(data, currentShishuChartFormat);
      });
    });
  }
}

function renderShishuSvgCharts(data, format = "south") {
  if (!data || !data.charts) return;
  const d1Wrapper = document.getElementById("shishuD1Wrapper");
  const d9Wrapper = document.getElementById("shishuD9Wrapper");
  if (!d1Wrapper || !d9Wrapper) return;

  const lagnaRashi = data.charts.lagna_rashi_index !== undefined ? data.charts.lagna_rashi_index : (data.lagna_info ? data.lagna_info.rashi_index : 0);
  const navamshaLagnaRashi = (data.lagna_info && data.lagna_info.navamsha_rashi_index !== undefined) ? data.lagna_info.navamsha_rashi_index : 0;

  if (format === "south") {
    d1Wrapper.innerHTML = renderSouthIndianChart(data.charts.d1, "లగ్న రాశి చక్రం (D1)");
    d9Wrapper.innerHTML = renderSouthIndianChart(data.charts.d9, "నవాంశ చక్రం (D9)");
  } else {
    d1Wrapper.innerHTML = renderNorthIndianChart(data.charts.d1, lagnaRashi, "లగ్న రాశి చక్రం (D1)");
    d9Wrapper.innerHTML = renderNorthIndianChart(data.charts.d9, navamshaLagnaRashi, "నవాంశ చక్రం (D9)");
  }
}

/* 17. Worldwide & City-Specific Eclipses Module (స్థానిక నగర గ్రహణ దర్శిని) */
function initEclipsesModule() {
  const form = document.getElementById("cityEclipseForm");
  if (!form) return;

  // Setup city autocomplete
  setupCityAutocomplete("eclipseCity", "eclipseCitySuggestions", "eclipseLat", "eclipseLon", "eclipseTzOffset", "eclipseCityFeedback");

  // Country auto-adjustment
  const countrySelect = document.getElementById("eclipseCountry");
  const tzInput = document.getElementById("eclipseTz");
  const tzOffsetInput = document.getElementById("eclipseTzOffset");

  if (countrySelect && tzInput) {
    countrySelect.addEventListener("change", () => {
      const c = countrySelect.value;
      if (c === "US") {
        if (!tzInput.value || tzInput.value === "Asia/Kolkata") tzInput.value = "America/Chicago";
        if (tzOffsetInput) tzOffsetInput.value = "-5.0";
      } else if (c === "IN") {
        tzInput.value = "Asia/Kolkata";
        if (tzOffsetInput) tzOffsetInput.value = "5.5";
      } else if (c === "GB") {
        tzInput.value = "Europe/London";
        if (tzOffsetInput) tzOffsetInput.value = "0.0";
      } else if (c === "AU") {
        tzInput.value = "Australia/Sydney";
        if (tzOffsetInput) tzOffsetInput.value = "10.0";
      } else if (c === "AE") {
        tzInput.value = "Asia/Dubai";
        if (tzOffsetInput) tzOffsetInput.value = "4.0";
      }
    });
  }

  // Eclipse Type auto-filter listener
  const typeSelect = document.getElementById("eclipseType");
  if (typeSelect) {
    typeSelect.addEventListener("change", () => {
      const val = typeSelect.value;
      if (window.__lastCityEclipseData) {
        filterCityEclipses(val);
      } else {
        fetchAndRenderCityEclipses();
      }
    });
  }

  // Visible Only checkbox listener
  const visOnlyCheck = document.getElementById("eclipseVisibleOnly");
  if (visOnlyCheck) {
    visOnlyCheck.addEventListener("change", () => {
      if (window.__lastCityEclipseData) {
        const curType = document.getElementById("eclipseType") ? document.getElementById("eclipseType").value : "all";
        renderCityEclipsesList(window.__lastCityEclipseData, curType);
      } else {
        fetchAndRenderCityEclipses();
      }
    });
  }

  // Submit Handler
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    fetchAndRenderCityEclipses();
  });

  // Auto-fetch default on initialization (McKinney 2028)
  fetchAndRenderCityEclipses();
}

async function fetchAndRenderCityEclipses() {
  const container = document.getElementById("eclipsesResultContainer");
  const btnSubmit = document.getElementById("btnSubmitCityEclipse");
  if (!container) return;

  await ensureCityResolved("eclipseCity", "eclipseLat", "eclipseLon", "eclipseTzOffset", "eclipseCityFeedback");

  const year = parseInt(document.getElementById("eclipseYear").value) || 2028;
  const country = document.getElementById("eclipseCountry").value || "US";
  const city = document.getElementById("eclipseCity").value.trim() || "McKinney";
  const lon = parseFloat(document.getElementById("eclipseLon").value) || -96.6178;
  const lat = parseFloat(document.getElementById("eclipseLat").value) || 33.1976;
  const tzName = document.getElementById("eclipseTz").value.trim() || "America/Chicago";
  const tzOffset = parseFloat(document.getElementById("eclipseTzOffset").value) || -5.0;
  const eclType = (document.getElementById("eclipseType") ? document.getElementById("eclipseType").value : "all") || "all";
  const lang = document.getElementById("eclipseLang").value || "te";

  if (btnSubmit) {
    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `<span class="spinner"></span> ${city} గ్రహణ సమయాలు లెక్కింపబడుతున్నాయి...`;
  }

  container.innerHTML = `
    <div style="text-align: center; padding: 40px; color: #4A0E17; font-size: 1.05rem; font-weight: 600;">
      <span class="spinner"></span> <strong>${city} (${year})</strong> సూర్య & చంద్ర గ్రహణాల స్పర్శ, మధ్య, మోక్ష సమయాలు లెక్కింపబడుతున్నాయి...
    </div>
  `;

  try {
    const resp = await fetch("/api/v1/eclipses/calculate-city", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        year,
        country,
        city,
        latitude: lat,
        longitude: lon,
        timezone_name: tzName,
        timezone_offset: tzOffset,
        eclipse_type: "all", // Fetch all so user can toggle instantaneously
        visible_only: false,
        language: lang
      })
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || "City Eclipse calculation error");
    }

    const data = await resp.json();
    window.__lastCityEclipseData = data;
    renderCityEclipsesList(data, eclType);
  } catch (err) {
    container.innerHTML = `
      <div class="prediction-card" style="text-align: center; color: #f44336; padding: 30px;">
        గ్రహణ వివరాలను లోడ్ చేయడంలో లోపం ఏర్పడింది: ${err.message}
      </div>
    `;
  } finally {
    if (btnSubmit) {
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = `<span>🔍</span> గ్రహణ సమయాలను శోధించండి (Check Timings)`;
    }
  }
}

function filterCityEclipses(filterKey) {
  if (!window.__lastCityEclipseData) return;
  const typeSelect = document.getElementById("eclipseType");
  if (typeSelect && ["all", "lunar", "solar"].includes(filterKey)) {
    typeSelect.value = filterKey;
  }
  renderCityEclipsesList(window.__lastCityEclipseData, filterKey);
}

window.toggleShowAllEclipses = function() {
  const visCheck = document.getElementById("eclipseVisibleOnly");
  if (visCheck) {
    visCheck.checked = false;
  }
  if (window.__lastCityEclipseData) {
    renderCityEclipsesList(window.__lastCityEclipseData, "all");
  }
};

function renderCityEclipsesList(data, activeFilter = "all") {
  const container = document.getElementById("eclipsesResultContainer");
  if (!container) return;

  const allEclipses = data.eclipses || [];
  if (allEclipses.length === 0) {
    container.innerHTML = `<div class="prediction-card" style="text-align: center; padding: 30px; color: #5D4037; font-size: 1.05rem; font-weight: 700;">ఈ సంవత్సరంలో గ్రహణాలు లేవు.</div>`;
    return;
  }

  // Check if "Show only visible in this location" is active (Default: true)
  const isVisibleOnly = document.getElementById("eclipseVisibleOnly")
    ? document.getElementById("eclipseVisibleOnly").checked
    : true;

  // 1. If visible-only is on, strictly filter to eclipses visible in that city
  const baseEclipses = isVisibleOnly
    ? allEclipses.filter(ec => ec.is_visible_in_city)
    : allEclipses;

  // 2. Next apply activeFilter (all, lunar, solar)
  let filtered = baseEclipses;
  if (activeFilter === "lunar") {
    filtered = baseEclipses.filter(ec => ec.is_lunar);
  } else if (activeFilter === "solar") {
    filtered = baseEclipses.filter(ec => ec.is_solar);
  }

  const lunarCount = baseEclipses.filter(ec => ec.is_lunar).length;
  const solarCount = baseEclipses.filter(ec => ec.is_solar).length;
  const totalShown = baseEclipses.length;
  const visibleCityCount = data.visible_eclipses_count || allEclipses.filter(ec => ec.is_visible_in_city).length;

  // Header & Filter Buttons (Crisp High-Contrast Vedic Styling)
  const headerHtml = `
    <div style="padding: 22px 24px; background: #FFFFFF; border-radius: 14px; margin-bottom: 25px; border: 1.5px solid var(--border-gold); box-shadow: var(--shadow-sm);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div>
          <div style="font-size: 1.35rem; font-weight: 800; color: #4A0E17; display: flex; align-items: center; gap: 8px;">
            <span>📍</span> ${data.city} (${data.country}) — ${data.year} సూర్య & చంద్ర గ్రహణ దర్శిని
          </div>
          <div style="font-size: 0.95rem; color: #5D4037; margin-top: 6px; font-weight: 600;">
            స్థానిక సమయ మండలం: <strong style="color: #0D47A1;">${data.timezone}</strong> | భౌగోళిక స్థానం: <strong style="color: #1B5E20;">${data.coordinates}</strong>
          </div>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <span class="dignity-tag dignity-exalted" style="font-size: 0.95rem; padding: 7px 16px; font-weight: 700;">
            ✓ ${visibleCityCount} గ్రహణాలు ${data.city} లో కనిపిస్తాయి
          </span>
        </div>
      </div>

      <!-- Quick Interactive Filter Pills with High Contrast -->
      <div style="display: flex; gap: 12px; margin-top: 18px; flex-wrap: wrap; padding-top: 16px; border-top: 1.5px solid #F0EAE1;">
        <button type="button" class="btn-filter-pill" onclick="filterCityEclipses('all')"
          style="padding: 8px 20px; border-radius: 20px; font-size: 0.95rem; font-weight: 700; cursor: pointer; border: 1.5px solid ${activeFilter === 'all' ? '#4A0E17' : '#D7CCC8'}; background: ${activeFilter === 'all' ? '#4A0E17' : '#FFFFFF'}; color: ${activeFilter === 'all' ? '#FFFFFF' : '#4A0E17'}; transition: all 0.2s; box-shadow: ${activeFilter === 'all' ? '0 2px 8px rgba(74, 14, 23, 0.25)' : 'none'};">
          ✨ అన్నీ (${isVisibleOnly ? 'కనిపించేవి: ' : 'All: '}${totalShown})
        </button>
        <button type="button" class="btn-filter-pill" onclick="filterCityEclipses('lunar')"
          style="padding: 8px 20px; border-radius: 20px; font-size: 0.95rem; font-weight: 700; cursor: pointer; border: 1.5px solid ${activeFilter === 'lunar' ? '#0D47A1' : '#BBDEFB'}; background: ${activeFilter === 'lunar' ? '#0D47A1' : '#FFFFFF'}; color: ${activeFilter === 'lunar' ? '#FFFFFF' : '#0D47A1'}; transition: all 0.2s; box-shadow: ${activeFilter === 'lunar' ? '0 2px 8px rgba(13, 71, 161, 0.25)' : 'none'};">
          🌕 చంద్ర గ్రహణాలు (${lunarCount})
        </button>
        <button type="button" class="btn-filter-pill" onclick="filterCityEclipses('solar')"
          style="padding: 8px 20px; border-radius: 20px; font-size: 0.95rem; font-weight: 700; cursor: pointer; border: 1.5px solid ${activeFilter === 'solar' ? '#E65100' : '#FFE082'}; background: ${activeFilter === 'solar' ? '#E65100' : '#FFFFFF'}; color: ${activeFilter === 'solar' ? '#FFFFFF' : '#E65100'}; transition: all 0.2s; box-shadow: ${activeFilter === 'solar' ? '0 2px 8px rgba(230, 81, 0, 0.25)' : 'none'};">
          ☀️ సూర్య గ్రహణాలు (${solarCount})
        </button>
      </div>
    </div>
  `;

  if (filtered.length === 0) {
    container.innerHTML = headerHtml + `
      <div class="prediction-card" style="text-align: center; padding: 45px 25px; border-radius: 12px; background: #FFFFFF; border: 1.5px solid #F0E6D2; box-shadow: var(--shadow-sm);">
        <div style="font-size: 2.5rem; margin-bottom: 12px;">🌍✨</div>
        <h3 style="color: #4A0E17; font-size: 1.3rem; font-weight: 800; margin-bottom: 10px;">
          ${data.city} నగరంలో ఈ ఎంపిక ప్రకారం గ్రహణాలు ఏవీ కనిపించవు (Not Visible in this Location)
        </h3>
        <p style="color: #2B2118; font-size: 1rem; max-width: 650px; margin: 0 auto 20px auto; line-height: 1.7; font-weight: 500;">
          ఈ సంవత్సరంలో ${data.city} (${data.country}) భౌగోళిక ప్రాంతం నుండి ఈ గ్రహణాలు దర్శనమివ్వవు (పగటి/రాత్రి వేళ లేదా గ్రహణ రేఖకు ఆవల ఉండుటచే). స్థానికంగా సూతక నియమాలు లేదా శాంతి దానాలు పాటించవలసిన అవసరం లేదు.
        </p>
        ${isVisibleOnly ? `
          <button type="button" class="btn-submit" onclick="toggleShowAllEclipses()" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 24px; font-size: 0.95rem; font-weight: 700; cursor: pointer;">
            <span>🌐</span> ప్రపంచవ్యాప్త గ్రహణాలను కూడా చూడండి (Show Worldwide Eclipses)
          </button>
        ` : `
          <button type="button" class="btn-submit" onclick="filterCityEclipses('all')" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 24px; font-size: 0.95rem; font-weight: 700; cursor: pointer;">
            <span>✨</span> అన్ని గ్రహణాలను చూపించు (Show All)
          </button>
        `}
      </div>
    `;
    return;
  }

  const cardsHtml = filtered.map(ec => {
    const isSolar = ec.is_solar;
    const isLunar = ec.is_lunar;
    const typeIcon = isSolar ? "☀️" : "🌕";
    const typeTitle = isLunar ? "🌕 చంద్ర గ్రహణం (LUNAR ECLIPSE)" : "☀️ సూర్య గ్రహణం (SOLAR ECLIPSE)";
    const themeColor = isLunar ? "#1E88E5" : "#E65100";
    const themeBg = isLunar ? "#F0F8FF" : "#FFF9E6";
    const themeBorder = isLunar ? "#90CAF9" : "#FFE082";
    const titleColor = isLunar ? "#0D47A1" : "#4A0E17";
    const tagColor = isLunar ? "#1565C0" : "#BF360C";

    const categoryBadgeClass = ec.category.includes("సంపూర్ణ") ? "dignity-exalted" :
                               ec.category.includes("కంకణ") ? "dignity-own" :
                               ec.category.includes("పాక్షిక") ? "dignity-friend" : "dignity-neutral";

    const isVisible = ec.is_visible_in_city;
    const visBorderCol = isVisible ? "#2E7D32" : "#546E7A";
    const visBgCol = isVisible ? "#E8F5E9" : "#ECEFF1";
    const visBadgeHtml = isVisible
      ? `<span class="dignity-tag dignity-exalted" style="font-size: 0.95rem; padding: 5px 14px; font-weight: 700;">✓ ${ec.visibility_badge}</span>`
      : `<span class="dignity-tag dignity-neutral" style="font-size: 0.95rem; padding: 5px 14px; font-weight: 700; color: #455A64;">✕ ${ec.visibility_badge}</span>`;

    const impacts = ec.astrology.rashi_impacts || {};
    const rashiGood = (impacts.subha && impacts.subha.length > 0) ? impacts.subha.join(", ") : "—";
    const rashiMixed = (impacts.madhyama && impacts.madhyama.length > 0) ? impacts.madhyama.join(", ") : "—";
    const rashiBad = (impacts.arishta && impacts.arishta.length > 0) ? impacts.arishta.join(", ") : "—";

    const remediesHtml = (ec.shanti_remedies || []).map(r => `<li>${r}</li>`).join("");

    let lagnaKundaliHtml = "";
    if (ec.lagna_kundali) {
      const lk = ec.lagna_kundali;
      let planetRows = `
        <tr style="background: #FFF8E1; font-weight: 700; color: #4A0E17;">
          <td><strong style="color: #4A0E17;">🚩 లగ్నం (Ascendant)</strong></td>
          <td>${lk.lagna_rashi_name_te}</td>
          <td><strong style="color: #B75300;">${lk.lagna_degree_formatted}</strong></td>
          <td>${lk.lagna_nakshatra_te} (${lk.lagna_pada}వ పాదం)</td>
          <td><span class="dignity-tag dignity-exalted">1వ భావం</span></td>
          <td><span class="dignity-tag dignity-exalted">ఉదయ లగ్నం</span></td>
        </tr>
      `;

      (lk.planets || []).forEach(p => {
        const digClass = p.dignity_en === "Exalted" ? "dignity-exalted" :
                         p.dignity_en === "Own Sign" ? "dignity-own" :
                         p.dignity_en === "Debilitated" ? "dignity-debilitated" :
                         p.dignity_en === "Friend" ? "dignity-friend" : "dignity-neutral";
        const vakraTag = p.is_retrograde ? `<span class="status-tag tag-vakra" style="margin-left: 4px;">వక్ర</span>` : "";
        const astaTag = p.is_combust ? `<span class="status-tag tag-asta" style="margin-left: 4px;">అస్తంగత</span>` : "";
        const isEclPlanet = (isSolar && p.name_en === "Sun") || (isLunar && p.name_en === "Moon") || (p.name_en === "Rahu" || p.name_en === "Ketu");
        const rowBg = isEclPlanet ? (isLunar ? "background: #F0F8FF;" : "background: #FFF9E6;") : "";

        planetRows += `
          <tr style="${rowBg}">
            <td><strong style="color: #2B2118;">${p.name_te}</strong> ${vakraTag} ${astaTag}</td>
            <td style="color: #3E2723; font-weight: 600;">${p.rashi_name_te}</td>
            <td style="color: #0D47A1; font-weight: 700;">${p.formatted_degree}</td>
            <td style="color: #37474F;">${p.nakshatra_name_te} (${p.pada}వ పాదం)</td>
            <td><strong style="color: #1B5E20;">${p.bhava}వ భావం</strong></td>
            <td><span class="dignity-tag ${digClass}">${p.dignity_te}</span></td>
          </tr>
        `;
      });

      lagnaKundaliHtml = `
        <!-- Eclipse Peak Lagna Kundali & Planetary Chart -->
        <div style="margin-top: 24px; padding: 22px; background: #FFFFFF; border-radius: 12px; border: 1.5px solid #EADBCE; box-shadow: var(--shadow-sm); margin-bottom: 24px;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 18px; border-bottom: 1.5px solid #F0EAE1; padding-bottom: 14px;">
            <div>
              <div style="font-size: 0.82rem; letter-spacing: 1px; font-weight: 800; color: #B75300; text-transform: uppercase;">
                ASTRONOMICAL & VEDIC ACCURACY
              </div>
              <h4 style="color: #4A0E17; font-size: 1.25rem; font-weight: 800; margin: 4px 0 0 0; display: flex; align-items: center; gap: 8px;">
                <span>☸️</span> గ్రహణ కాల లగ్న కుండలి (Eclipse Lagna Kundali — ${data.city}):
              </h4>
              <div style="font-size: 0.95rem; color: #5D4037; font-weight: 600; margin-top: 4px;">
                ${data.city} లో పరమ గ్రహణ క్షణంలో (<strong style="color: #0D47A1;">${ec.timings.local_madhya}</strong>) ఉదయించిన స్పష్ట లగ్నం & నవగ్రహ చక్రం
              </div>
            </div>
            <div class="chart-toggle-group">
              <button type="button" class="chart-toggle-btn active" id="btnEclSouth_${ec.id}" onclick="toggleEclipseChartFormat('${ec.id}', 'south')">సాంప్రదాయ దక్షిణ భారత చక్రం</button>
              <button type="button" class="chart-toggle-btn" id="btnEclNorth_${ec.id}" onclick="toggleEclipseChartFormat('${ec.id}', 'north')">ఉత్తర భారత వజ్ర చక్రం</button>
            </div>
          </div>

          <!-- Lagna & Eclipse Bhava Hero Info -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 20px;">
            <div style="background: #FAF7F2; padding: 14px 16px; border-radius: 8px; border: 1.5px solid #EADBCE;">
              <div style="font-size: 0.85rem; color: #5D4037; font-weight: 700; text-transform: uppercase;">🚩 గ్రహణ లగ్నం (Rising Lagna at Peak)</div>
              <div style="font-size: 1.2rem; font-weight: 800; color: #4A0E17; margin-top: 4px;">
                ${lk.lagna_rashi_name_te} లగ్నం ${lk.lagna_degree_formatted}
              </div>
              <div style="font-size: 0.88rem; color: #795548; font-weight: 600; margin-top: 2px;">
                ${lk.lagna_nakshatra_te} (${lk.lagna_pada}వ పాదం)
              </div>
            </div>
            <div style="background: #FAF7F2; padding: 14px 16px; border-radius: 8px; border: 1.5px solid #EADBCE;">
              <div style="font-size: 0.85rem; color: #5D4037; font-weight: 700; text-transform: uppercase;">🏛️ లగ్నం నుండి గ్రహణ భావం</div>
              <div style="font-size: 1.2rem; font-weight: 800; color: #0D47A1; margin-top: 4px;">
                ${lk.eclipse_bhava_title_te}
              </div>
              <div style="font-size: 0.88rem; color: #1B5E20; font-weight: 700; margin-top: 2px;">
                ${ec.astrology.rashi_name_te} (${isSolar ? 'సూర్య & రాహు/కేతు సంయోగం' : 'చంద్ర & రాహు/కేతు సంయోగం'})
              </div>
            </div>
          </div>

          <!-- Eclipse Bhava Impact Banner -->
          <div style="padding: 16px 18px; background: #FFF9E6; border-left: 5px solid #D4AF37; border-radius: 8px; margin-bottom: 22px; border: 1.5px solid #FFE082;">
            <strong style="color: #4A0E17; font-size: 1.05rem; font-weight: 800;">
              🧭 ${data.city} స్థానిక గ్రహణ భావ ఫలితం (${lk.eclipse_bhava_title_te}):
            </strong>
            <p style="margin: 8px 0 0 0; color: #2B2118; font-size: 0.98rem; line-height: 1.7; font-weight: 500;">
              ${lk.eclipse_bhava_impact_te}
            </p>
          </div>

          <!-- SVG Visual Chart Container -->
          <div style="display: flex; justify-content: center; margin-bottom: 24px;">
            <div id="eclipseChartWrapper_${ec.id}" style="width: 100%; max-width: 500px; display: flex; justify-content: center;"></div>
          </div>

          <!-- Tatkala Planetary Positions Table at Eclipse Time -->
          <h5 style="color: #4A0E17; font-size: 1.08rem; font-weight: 800; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            <span>🪐</span> గ్రహణ కాల నవగ్రహ స్పష్ట స్థితులు (Tatkala Graha Positions at Peak Moment):
          </h5>
          <div class="table-responsive" style="margin-bottom: 6px;">
            <table class="vedic-table" style="border: 1.5px solid #EADBCE;">
              <thead>
                <tr style="background: #F8F3E6; border-bottom: 2px solid #D4AF37;">
                  <th style="color: #4A0E17; font-weight: 800;">గ్రహం (Planet)</th>
                  <th style="color: #4A0E17; font-weight: 800;">రాశి (Sign)</th>
                  <th style="color: #4A0E17; font-weight: 800;">స్పష్ట డిగ్రీలు (Exact Degree)</th>
                  <th style="color: #4A0E17; font-weight: 800;">నక్షత్రం & పాదం</th>
                  <th style="color: #1B5E20; font-weight: 800;">లగ్నం నుండి స్థానం</th>
                  <th style="color: #4A0E17; font-weight: 800;">గ్రహ బలం / స్థితి</th>
                </tr>
              </thead>
              <tbody style="font-size: 0.95rem;">
                ${planetRows}
              </tbody>
            </table>
          </div>
        </div>
      `;
    }

    return `
      <div class="prediction-card" style="margin-bottom: 30px; border-top: 6px solid ${themeColor}; border: 1.5px solid ${themeBorder}; box-shadow: var(--shadow-md); background: #FFFFFF;">
        <div class="prediction-card-header" style="background: ${themeBg}; padding: 18px 22px; border-radius: 8px 8px 0 0; border-bottom: 1.5px solid ${themeBorder};">
          <div>
            <div style="font-size: 0.85rem; letter-spacing: 1px; font-weight: 800; color: ${tagColor}; text-transform: uppercase; margin-bottom: 4px;">
              ${typeTitle}
            </div>
            <div class="pred-title" style="color: ${titleColor}; font-size: 1.35rem; font-weight: 800;">
              ${typeIcon} ${ec.name}
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <span class="dignity-tag ${categoryBadgeClass}" style="font-size: 0.92rem; padding: 5px 12px; font-weight: 700;">${ec.category}</span>
            ${visBadgeHtml}
          </div>
        </div>
        <div class="pred-body" style="padding: 10px 6px;">

          <!-- City Visibility Hero Banner -->
          <div style="padding: 15px 18px; background: ${visBgCol}; border-left: 5px solid ${visBorderCol}; border-radius: 8px; margin-bottom: 22px;">
            <strong style="color: ${visBorderCol}; font-size: 1.1rem; font-weight: 800;">${ec.visibility_badge}</strong>
            <p style="margin: 6px 0 0 0; color: #2B2118; font-size: 0.98rem; line-height: 1.7; font-weight: 500;">${ec.visibility_note}</p>
          </div>

          <!-- Key Highlights Grid -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 24px;">
            <div style="background: #FAF7F2; padding: 14px 16px; border-radius: 8px; border: 1.5px solid #EADBCE;">
              <div style="font-size: 0.85rem; color: #5D4037; font-weight: 700; text-transform: uppercase;">📅 స్థానిక తేదీ (Local Date)</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #4A0E17; margin-top: 4px;">${ec.date_formatted}</div>
            </div>
            <div style="background: #FAF7F2; padding: 14px 16px; border-radius: 8px; border: 1.5px solid #EADBCE;">
              <div style="font-size: 0.85rem; color: #5D4037; font-weight: 700; text-transform: uppercase;">⏱️ మొత్తం గ్రహణ కాలం (Duration)</div>
              <div style="font-size: 1.15rem; font-weight: 800; color: #1B5E20; margin-top: 4px;">${ec.timings.duration}</div>
            </div>
            <div style="background: #FAF7F2; padding: 14px 16px; border-radius: 8px; border: 1.5px solid #EADBCE;">
              <div style="font-size: 0.85rem; color: #5D4037; font-weight: 700; text-transform: uppercase;">🪐 బాధిత రాశి & నక్షత్రం</div>
              <div style="font-size: 1.12rem; font-weight: 800; color: #0D47A1; margin-top: 4px;">${ec.astrology.rashi_name_te} (${ec.astrology.nakshatra_name_te})</div>
            </div>
          </div>

          <!-- Timings Table: Local Timezone vs UTC vs IST -->
          <h4 style="color: #4A0E17; margin-bottom: 12px; font-size: 1.12rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
            <span>⏱️</span> గ్రహణ కాల ఘట్టాలు — మీ నగర స్థానిక సమయాలు (${data.city} vs UTC vs IST):
          </h4>
          <div class="table-responsive" style="margin-bottom: 24px;">
            <table class="vedic-table" style="border: 1.5px solid #EADBCE;">
              <thead>
                <tr style="background: #F8F3E6; border-bottom: 2px solid #D4AF37;">
                  <th style="color: #4A0E17; font-weight: 800; font-size: 0.92rem;">కాల ఘట్టం (Eclipse Phase)</th>
                  <th style="color: #1B5E20; font-weight: 800; font-size: 0.95rem;">స్థానిక సమయం (${data.city})</th>
                  <th style="color: #4A0E17; font-weight: 700; font-size: 0.92rem;">ప్రపంచ సమయం (UTC)</th>
                  <th style="color: #4A0E17; font-weight: 700; font-size: 0.92rem;">భారత సమయం (IST)</th>
                </tr>
              </thead>
              <tbody style="font-size: 0.95rem; color: #2B2118;">
                <tr>
                  <td><strong style="color: #3E2723;">గ్రహణ ప్రారంభం (స్పర్శ కాలం)</strong></td>
                  <td style="color: #1B5E20; font-weight: 800; font-size: 1.02rem;">${ec.timings.local_sparsha}</td>
                  <td style="color: #37474F; font-weight: 600;">${ec.timings.utc_sparsha}</td>
                  <td style="color: #37474F; font-weight: 600;">${ec.timings.ist_sparsha}</td>
                </tr>
                <tr style="background: #FFF9E6;">
                  <td><strong style="color: #B75300; font-weight: 800;">పరమ గ్రహణం (మధ్య కాలం / Peak)</strong></td>
                  <td style="color: #B75300; font-weight: 800; font-size: 1.08rem;">${ec.timings.local_madhya}</td>
                  <td style="color: #37474F; font-weight: 600;">${ec.timings.utc_madhya}</td>
                  <td style="color: #37474F; font-weight: 600;">${ec.timings.ist_madhya}</td>
                </tr>
                <tr>
                  <td><strong style="color: #3E2723;">గ్రహణ సమాప్తి (మోక్ష కాలం)</strong></td>
                  <td style="color: #1B5E20; font-weight: 800; font-size: 1.02rem;">${ec.timings.local_moksha}</td>
                  <td style="color: #37474F; font-weight: 600;">${ec.timings.utc_moksha}</td>
                  <td style="color: #37474F; font-weight: 600;">${ec.timings.ist_moksha}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Eclipse Peak Lagna Kundali -->
          ${lagnaKundaliHtml}

          <!-- Sutaka Timings Card -->
          <div style="padding: 18px; background: #FFFDF7; border-radius: 10px; margin-bottom: 24px; border: 1.5px solid #FFE082; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
              <strong style="color: #8D4400; font-size: 1.1rem; font-weight: 800;">
                🛑 సూతక కాలం & స్థానిక నియమాలు (${isLunar ? 'చంద్ర గ్రహణం - 3 జాములు' : 'సూర్య గ్రహణం - 4 జాములు'}):
              </strong>
              <span class="dignity-tag dignity-exalted" style="font-size: 0.9rem; font-weight: 700;">${ec.sutaka.rule_hours}</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 12px;">
              <div style="background: #FFFFFF; padding: 12px 14px; border-radius: 6px; border: 1px solid #FFE082;">
                <div style="font-size: 0.85rem; color: #6D4C41; font-weight: 700;">సూతక ప్రారంభ సమయం (Start)</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #B75300; margin-top: 3px;">${ec.sutaka.start}</div>
              </div>
              <div style="background: #FFFFFF; padding: 12px 14px; border-radius: 6px; border: 1px solid #C8E6C9;">
                <div style="font-size: 0.85rem; color: #2E7D32; font-weight: 700;">సూతక సమాప్తి సమయం (End / Moksha)</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #1B5E20; margin-top: 3px;">${ec.sutaka.end}</div>
              </div>
            </div>
            <p style="margin: 0; font-size: 0.96rem; color: #2B2118; line-height: 1.7; font-weight: 500;">${ec.sutaka.rules_te}</p>
          </div>

          <!-- 12 Moon Signs Impacts -->
          <h4 style="color: #4A0E17; margin-bottom: 12px; font-size: 1.12rem; font-weight: 800;">
            <span>♈</span> ద్వాదశ రాశుల ఫలితాలు (Impact on 12 Moon Signs):
          </h4>
          <div class="table-responsive" style="margin-bottom: 24px;">
            <table class="vedic-table" style="border: 1.5px solid #EADBCE;">
              <tbody>
                <tr>
                  <th style="width: 210px; background: #E8F5E9;"><span class="dignity-tag dignity-exalted" style="font-size: 0.88rem; font-weight: 700;">శుభ ఫలితాలు (Good)</span></th>
                  <td style="color: #1B5E20; font-weight: 700; font-size: 1rem;">${rashiGood}</td>
                </tr>
                <tr>
                  <th style="background: #F8F3E6;"><span class="dignity-tag dignity-friend" style="font-size: 0.88rem; font-weight: 700;">మధ్యమ ఫలితాలు (Neutral)</span></th>
                  <td style="color: #37474F; font-weight: 600; font-size: 1rem;">${rashiMixed}</td>
                </tr>
                <tr>
                  <th style="background: #FFEBEE;"><span class="dignity-tag dignity-debilitated" style="font-size: 0.88rem; font-weight: 700;">అనిష్ట ఫలితాలు (Challenging)</span></th>
                  <td><strong style="color: #B71C1C; font-size: 1rem;">${rashiBad}</strong> <span style="color: #C2185B; font-size: 0.88rem; font-weight: 600;">(శాంతి పారాయణ & దానాలు శ్రేయస్కరం)</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Shanti Remedies & Moksha Puja -->
          <div style="padding: 18px; background: #F0F8FF; border-left: 5px solid #1E88E5; border-radius: 8px; border: 1.5px solid #BBDEFB;">
            <strong style="color: #0D47A1; font-size: 1.08rem; font-weight: 800;">
              ${isLunar ? '🪔 చంద్ర గ్రహణ శాస్త్రోక్త పరిహారాలు, దానాలు & రక్షా సూచనలు:' : '🪔 సూర్య గ్రహణ శాస్త్రోక్త పరిహారాలు, దానాలు & రక్షా సూచనలు:'}
            </strong>
            <ul style="margin: 10px 0 0 0; padding-left: 22px; line-height: 1.8; color: #1A237E; font-size: 0.98rem; font-weight: 600;">
              ${remediesHtml}
            </ul>
          </div>

        </div>
      </div>
    `;
  }).join("");

  container.innerHTML = headerHtml + cardsHtml;

  // Render SVG Kundali charts for each eclipse that has lagna_kundali
  filtered.forEach(ec => {
    if (ec.lagna_kundali && ec.lagna_kundali.charts) {
      const fmt = window.__currentEclipseChartFormats[ec.id] || "south";
      renderEclipseSvgChart(ec.id, fmt);
    }
  });

  if (window.currentScript && window.currentScript !== "Telugu") {
    applyTransliterationToPage(container);
  }
}

window.__currentEclipseChartFormats = window.__currentEclipseChartFormats || {};

function renderEclipseSvgChart(eclipseId, format = "south") {
  if (!window.__lastCityEclipseData || !window.__lastCityEclipseData.eclipses) return;
  const ec = window.__lastCityEclipseData.eclipses.find(e => e.id === eclipseId);
  if (!ec || !ec.lagna_kundali || !ec.lagna_kundali.charts) return;

  const wrapper = document.getElementById("eclipseChartWrapper_" + eclipseId);
  if (!wrapper) return;

  const lk = ec.lagna_kundali;
  const title = `${ec.name} — లగ్న చక్రం (D1)`;
  if (format === "south") {
    wrapper.innerHTML = renderSouthIndianChart(lk.charts.d1, title);
  } else {
    wrapper.innerHTML = renderNorthIndianChart(lk.charts.d1, lk.lagna_rashi_index, title);
  }
}

window.toggleEclipseChartFormat = function(eclipseId, format) {
  window.__currentEclipseChartFormats[eclipseId] = format;
  const btnSouth = document.getElementById("btnEclSouth_" + eclipseId);
  const btnNorth = document.getElementById("btnEclNorth_" + eclipseId);
  if (btnSouth && btnNorth) {
    if (format === "south") {
      btnSouth.classList.add("active");
      btnNorth.classList.remove("active");
    } else {
      btnNorth.classList.add("active");
      btnSouth.classList.remove("active");
    }
  }
  renderEclipseSvgChart(eclipseId, format);
};

/* ======================================================= */
/* AKSHARAMUKHA MULTI-LANGUAGE INDIC TRANSLITERATION       */
/* ======================================================= */

window.currentScript = localStorage.getItem("jyotishyam_script") || "Telugu";
window.scriptTranslationCache = {};

function initLanguageSelector() {
  const sel = document.getElementById("scriptSelector");
  if (!sel) return;

  sel.value = window.currentScript;
  applyScriptClass(window.currentScript);

  sel.addEventListener("change", async (e) => {
    const targetScript = e.target.value;
    window.currentScript = targetScript;
    localStorage.setItem("jyotishyam_script", targetScript);
    applyScriptClass(targetScript);

    // Re-render SVG charts in new language if available
    if (window.currentKundaliData && typeof updateKundaliChart === "function") {
      updateKundaliChart();
    }
    if (window.__lastCityEclipseData && typeof window.renderAllEclipseCharts === "function") {
      window.renderAllEclipseCharts();
    }

    await applyTransliterationToPage();
  });

  // If saved language is not Telugu, apply after initial page render
  if (window.currentScript !== "Telugu") {
    setTimeout(() => {
      applyTransliterationToPage();
    }, 200);
  }
}

window.renderAllEclipseCharts = function() {
  if (window.__lastCityEclipseData && window.__lastCityEclipseData.eclipses) {
    window.__lastCityEclipseData.eclipses.forEach(ec => {
      const fmt = window.__currentEclipseChartFormats[ec.id] || "south";
      renderEclipseSvgChart(ec.id, fmt);
    });
  }
};

function applyScriptClass(scriptName) {
  const classes = [
    "script-Devanagari", "script-Tamil", "script-Kannada",
    "script-Malayalam", "script-Bengali", "script-Gujarati",
    "script-Oriya", "script-Gurmukhi"
  ];
  classes.forEach(c => document.body.classList.remove(c));
  if (scriptName && scriptName !== "Telugu" && scriptName !== "IAST") {
    document.body.classList.add(`script-${scriptName}`);
  }
}

function containsTelugu(str) {
  return /[\u0C00-\u0C7F]/.test(str);
}

function getTeluguTextNodes(root = document.body) {
  const textNodes = [];
  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        if (!node || !node.nodeValue) return NodeFilter.FILTER_REJECT;
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        const tag = parent.tagName.toUpperCase();
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT" || tag === "TEXTAREA") {
          return NodeFilter.FILTER_REJECT;
        }
        if (parent.id === "scriptSelector" || parent.closest("#scriptSelector")) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    }
  );

  let currentNode;
  while ((currentNode = walker.nextNode())) {
    textNodes.push(currentNode);
  }
  return textNodes;
}

async function applyTransliterationToPage(root = document.body) {
  const targetScript = window.currentScript || "Telugu";

  // Gather text nodes and store original Telugu text
  const nodes = getTeluguTextNodes(root);
  nodes.forEach(n => {
    if (n._origTelugu === undefined) {
      n._origTelugu = n.nodeValue;
    }
  });

  // If target is Telugu, restore original immediately
  if (targetScript === "Telugu") {
    nodes.forEach(n => {
      if (n._origTelugu !== undefined) {
        n.nodeValue = n._origTelugu;
      }
    });
    return;
  }

  window.scriptTranslationCache[targetScript] = window.scriptTranslationCache[targetScript] || {};
  const cache = window.scriptTranslationCache[targetScript];

  const uniqueToFetch = new Set();
  nodes.forEach(n => {
    const orig = n._origTelugu;
    if (orig && containsTelugu(orig) && cache[orig] === undefined) {
      uniqueToFetch.add(orig);
    }
  });

  if (uniqueToFetch.size > 0) {
    const textsArray = Array.from(uniqueToFetch);
    try {
      const chunkSize = 150;
      for (let i = 0; i < textsArray.length; i += chunkSize) {
        const chunk = textsArray.slice(i, i + chunkSize);
        const resp = await fetch("/api/v1/languages/transliterate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            texts: chunk,
            target_script: targetScript,
            source_script: "Telugu"
          })
        });
        if (resp.ok) {
          const resJson = await resp.json();
          const translatedList = resJson.texts || [];
          chunk.forEach((origText, idx) => {
            cache[origText] = translatedList[idx] || origText;
          });
        }
      }
    } catch (err) {
      console.warn("Transliteration request error:", err);
    }
  }

  // Update text nodes
  nodes.forEach(n => {
    const orig = n._origTelugu;
    if (orig && containsTelugu(orig) && cache[orig] !== undefined) {
      n.nodeValue = cache[orig];
    }
  });
}

/* ========================================================================== */
/* JATHAKAM DOSHA TO MUHURTAM BRIDGE & CONTEXTUAL SHASTRA ENGINE              */
/* ========================================================================== */

const PARIHARA_SHASTRA_INFO = {
  naga_pratishtha: {
    title: "నాగ ప్రతిష్ఠ ముహూర్తం (Naga Pratishtha)",
    authority: "ముహూర్త రత్నావళి (ప్రతిష్ఠా ప్రకరణం) & కాలామృతమ్",
    indication: "లగ్నం, 5వ లేదా 8వ స్థానంలో రాహు/కేతువులు ఉన్నప్పుడు, సర్ప శాపం, నాగ దోషం, లేదా సంతాన ప్రతిబంధక నివారణార్థం అశ్వత్థ వృక్ష సన్నిధిలో నాగ శిలా ప్రతిష్ఠ చేయబడుతుంది.",
    rules: "శుక్ల పంచమి (నాగ పంచమి) లేదా షష్ఠి అత్యుత్తమం. 8వ స్థానంలో పాప గ్రహాలు ఉండరాదు (అష్టమ శుద్ధి).",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.kalasarpa_dosha && k.kalasarpa_dosha.has_dosha) return `కాలసర్ప దోషం నిర్ధారితం: ${k.kalasarpa_dosha.type_name || ''}`;
      if (k.santana_analysis && Array.isArray(k.santana_analysis.doshas_detected)) {
        const found = k.santana_analysis.doshas_detected.find(d => d.shapa_type === "sarpa_shapa" || (d.name_te && d.name_te.includes("సర్ప")));
        if (found) return `సంతాన చక్రంలో సర్ప శాపం: ${found.astrological_reason}`;
      }
      return false;
    }
  },
  ashlesha_bali: {
    title: "ఆశ్లేషా బలి పూజ (Ashlesha Bali Puja)",
    authority: "ధర్మసింధు & స్మృతి ముక్తావళి",
    indication: "కుక్కే సుబ్రహ్మణ్య లేదా సర్ప క్షేత్రాలలో ఆశ్లేషా నక్షత్ర యుక్త దినాన సర్ప దోష ఉపశమనం మరియు చర్మ రోగాలు, వివాహ/సంతాన జాప్య నివారణకై ఆచరిస్తారు.",
    rules: "ఆశ్లేషా నక్షత్రం ఉన్న రోజు ప్రదోష వేళ లేదా సూర్యోదయ లగ్నంలో ఆచరించడం అత్యంత ఫలప్రదం.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.panchangam && k.panchangam.nakshatra_index === 8) return "మీ జన్మ నక్షత్రం ఆశ్లేష — ఆశ్లేషా బలి విశేష రక్షణనిస్తుంది.";
      if (k.kalasarpa_dosha && k.kalasarpa_dosha.has_dosha) return "కాలసర్ప దోష నివారణకు ఆశ్లేషా బలి శ్రేష్ఠమైనది.";
      return false;
    }
  },
  kuja_shanti_subrahmanya: {
    title: "సుబ్రహ్మణ్య షష్ఠి / కుజ శాంతి (Kuja Shanti)",
    authority: "బృహత్ పరాశర హోరాశాస్త్రం & జాతక చంద్రిక",
    indication: "జాతకంలో 1, 2, 4, 7, 8, 12వ స్థానాలలో కుజుడు ఉండి కుజ దోషం (మాంగళిక దోషం) ఏర్పడినప్పుడు దాంపత్య కలహాలు, రక్త సంబంధ సమస్యలు, గర్భస్రావ నివారణకు చేస్తారు.",
    rules: "మంగళవారం, షష్ఠి తిథి, మృగశిర/చిత్త/ధనిష్ఠ నక్షత్రాలు, లేదా మకర/మేష/వృశ్చిక లగ్నాలలో శ్రేష్ఠం.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.kuja_dosha && k.kuja_dosha.severity === "present") return `కుజ దోషం నిర్ధారితం: కుజుడు లగ్నం నుండి ${k.kuja_dosha.kuja_from_lagna}వ స్థానంలో ఉన్నాడు.`;
      if (k.santana_analysis && Array.isArray(k.santana_analysis.doshas_detected)) {
        const found = k.santana_analysis.doshas_detected.find(d => d.shapa_type === "bhauma_kuja" || (d.name_te && d.name_te.includes("కుజ")));
        if (found) return `సంతాన చక్రంలో కుజ దోషం: ${found.astrological_reason}`;
      }
      return false;
    }
  },
  santana_gopala: {
    title: "సంతాన గోపాల హోమం / కృష్ణార్చన (Santana Gopala)",
    authority: "శ్రీమద్భాగవతం & మంత్ర మహోదధి",
    indication: "5వ భావాధిపతి లేదా పుత్రకారక గురుడు బలహీనపడినప్పుడు, సంతానలేమి లేదా ఆలస్య సంతాన నివారణార్థం వంశవృద్ధి కొరకు ఆచరిస్తారు.",
    rules: "గురువారం, రోహిణి/శ్రవణం/పుష్యమి నక్షత్రాలు, శుక్ల పక్ష ఏకాదశి లేదా అష్టమి తిథులలో ప్రశస్తం.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.santana_analysis && k.santana_analysis.overall_badge !== "success") return "మీ సంతాన విశ్లేషణలో దోషం/ప్రతిబంధకం గుర్తించబడింది — సంతాన గోపాల హోమం సర్వశ్రేష్ఠం.";
      return false;
    }
  },
  rudra_pashupatam: {
    title: "రుద్ర పాశుపత హోమం / మహా రుద్రాభిషేకం (Rudra Pashupatam)",
    authority: "కృష్ణ యజుర్వేద తైత్తిరీయ సంహిత & శివపురాణం",
    indication: "జాతకంలో శని తీవ్ర పాప స్థానాలలో ఉన్నప్పుడు (ఏలినాటి శని, అష్టమ శని, అర్థాష్టమ శని), దీర్ఘకాల అనారోగ్యం లేదా అపమృత్యు భయ నివారణకై చేస్తారు.",
    rules: "సోమవారం, శ్రవణా/ఆరుద్ర నక్షత్రాలు, ప్రదోష కాలం లేదా చతుర్దశి తిథులలో అత్యుత్తమం. శివవాస పరిశీలన అవసరం.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.gocharam && (k.gocharam.is_sade_sati || k.gocharam.is_ashtama_shani)) return "ప్రస్తుతం ఏలినాటి శని / అష్టమ శని సంచారం ఉన్నది — రుద్ర పాశుపతం పరమ రక్ష.";
      return false;
    }
  },
  chandi_homam: {
    title: "చండీ హోమం / దుర్గా సప్తశతి (Chandi Homa)",
    authority: "మార్కండేయ పురాణం (దేవీ మాహాత్మ్యం)",
    indication: "జాతకంలో ఒకేసారి పలు పాప గ్రహాల కలయిక, శత్రుపీడ, కంటికి కనిపించని అవరోధాలు, మరియు సమస్త కుటుంబ రక్షణకై ఆచరిస్తారు.",
    rules: "శుక్ల పక్ష అష్టమి, నవమి, లేదా పూర్ణిమ. మంగళ లేదా శుక్రవారాలలో శ్రేష్ఠం. అగ్నివాస శుద్ధి తప్పనిసరి.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.santana_analysis && k.santana_analysis.doshas_detected && k.santana_analysis.doshas_detected.length >= 2) return "జాతకంలో బహుళ గ్రహ ప్రతిబంధకాలు ఉన్నవి — చండీ హోమం సర్వ గ్రహ నివారణి.";
      return false;
    }
  },
  tila_homa_narayana_bali: {
    title: "నారాయణ బలి / తిల హోమం (Pithru Shanti)",
    authority: "గరుడ పురాణం & ధర్మసింధు (పితృ ప్రకరణం)",
    indication: "9వ స్థానంలో రాహు/కేతు కలయిక, సూర్య గ్రహణం లేదా పితృ శాపం వల్ల కుటుంబంలో వంశవృద్ధి లోపించినప్పుడు చేస్తారు.",
    rules: "అమావాస్య లేదా కృష్ణ పక్ష అష్టమి/చతుర్దశి. నారాయణ బలి క్షేత్రాలలో లేదా తీర్థ స్థలాలలో శ్రేష్ఠం.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.santana_analysis && Array.isArray(k.santana_analysis.doshas_detected)) {
        const found = k.santana_analysis.doshas_detected.find(d => d.shapa_type === "pitru_shapa" || (d.name_te && d.name_te.includes("పితృ")));
        if (found) return `పితృ శాప ప్రతిబంధకం గుర్తించబడింది: ${found.astrological_reason}`;
      }
      return false;
    }
  },
  navagraha_shanti: {
    title: "నవగ్రహ శాంతి హోమం (Navagraha Shanti)",
    authority: "శౌనకోక్త నవగ్రహ విధానం & బోధాయన గృహ్యసూత్రాలు",
    indication: "దశా-భుక్తి మార్పుల వేళ, గ్రహాల పరస్పర విరోధం వల్ల కలిగే ఒడుదొడుకులను సరిచేసి సర్వతోముఖ అభివృద్ధిని అందించే సార్వత్రిక వైదిక హోమం.",
    rules: "సూర్య అనుకూల దినాలు, శుక్ల పక్షం, జన్మ తారాబలం ఉన్న శుభ దినాలలో శాస్త్రోక్తంగా ఆచరించవచ్చు.",
    checkDosha: () => "సర్వ జాతకులకు అన్ని సమయాలలోనూ అనుకూలమైన సార్వత్రిక శాంతి హోమం."
  },
  vivaha: {
    title: "వివాహ ముహూర్తం (Marriage Muhurtam)",
    authority: "ముహూర్త చింతామణి & కాలామృతం",
    indication: "నూతన దాంపత్య జీవన ప్రారంభం కొరకు లగ్న శుద్ధి, త్రయోదశ దోష రహితం, గురు-శుక్ర మౌఢ్య రహిత కాల నిర్ణయం.",
    rules: "శుక్ల పక్షం, రోహిణి/మృగశిర/మఖ/ఉత్తర/హస్త/స్వాతి/అనూరాధ/మూల/ఉత్తరాషాఢ/ఉత్తరాభాద్ర/రేవతి నక్షత్రాలు, గురు-శుక్ర బలం.",
    checkDosha: () => null
  },
  grihapravesha: {
    title: "గృహ ప్రవేశ ముహూర్తం (Housewarming)",
    authority: "ముహూర్త రత్నావళి & వాస్తు రాజవల్లభం",
    indication: "నూతన లేదా పురాతన గృహ ప్రవేశం — వాస్తు పురుష పూజ, అష్ట దిక్పాలక అనుగ్రహం కొరకు.",
    rules: "ఉత్తరాయణం, శుక్ల పక్షం, స్థిర లగ్నాలు (వృషభ, సింహ, వృశ్చిక, కుంభం), గురు-శుక్ర మౌఢ్య రహితం.",
    checkDosha: () => null
  },
  namakarana: {
    title: "నామకరణ ముహూర్తం (Baby Naming)",
    authority: "ఆశ్వలాయన గృహ్యసూత్రాలు & బృహత్ పరాశర",
    indication: "శిశువుకు ఆయుష్షు, కీర్తి, రక్షణ కలిగించే శుభ నామకరణ సంస్కారం (10వ, 12వ లేదా 16వ దినమున).",
    rules: "శుక్ల పక్షం, స్థిర లేదా మృదు నక్షత్రాలు, చంద్రబలం.",
    checkDosha: () => null
  },
  annaprashana: {
    title: "అన్నప్రాశన ముహూర్తం (First Solid Feeding)",
    authority: "పారస్కర గృహ్యసూత్రాలు",
    indication: "శిశువుకు 6వ లేదా 8వ మాసమున ప్రథమ ఘనాహార స్వీకరణ — ఆరోగ్య వృద్ధి కొరకు.",
    rules: "శుక్ల పక్షం, ద్వితీయ/తృతీయ/పంచమి/సప్తమి/దశమి తిథులు, గురు/శుక్ర/బుధ వారాలు.",
    checkDosha: () => null
  },
  upanayana: {
    title: "ఉపనయన ముహూర్తం (Sacred Thread Ceremony)",
    authority: "బోధాయన గృహ్యసూత్రాలు & ముహూర్త దర్పణం",
    indication: "బ్రహ్మోపదేశం, గాయత్రీ మంత్ర దీక్ష, విద్యా ప్రారంభ సంస్కారం కొరకు.",
    rules: "ఉత్తరాయణం, వసంత లేదా గ్రీష్మ రుతువు, గురు బలం, శుక్ల పక్షం.",
    checkDosha: () => null
  },
  vyapara_arambha: {
    title: "నూతన వ్యాపార ప్రారంభం (Business Launch)",
    authority: "ముహూర్త గణపతి & కాలామృతం",
    indication: "నూతన వాణిజ్యం, దుకాణం, పరిశ్రమ లేదా కార్యాలయ ప్రారంభం — లక్ష్మీ కటాక్షం కొరకు.",
    rules: "శుక్ల పక్షం, చర లేదా ద్విస్వభావ లగ్నాలు, 11వ లాభ స్థాన శుద్ధి, బుధ/గురు బలం.",
    checkDosha: () => null
  },
  vahana_purchase: {
    title: "నూతన వాహన కొనుగోలు (Vehicle Purchase)",
    authority: "ముహూర్త రత్నావళి (యాన ప్రకరణం)",
    indication: "ద్విచక్ర, చతుశ్చక్ర వాహనాల కొనుగోలు మరియు ప్రథమ ప్రయాణం — క్షేమకర ప్రయాణం కొరకు.",
    rules: "చర లగ్నాలు, శుక్ర బలం, వర్జ్య/రాహుకాల రహిత సమయం.",
    checkDosha: () => null
  },
  aksharabhyasa: {
    title: "అక్షరాభ్యాసం / విద్యారంభం (Aksharabhyasa / Vidyarambham)",
    authority: "ముహూర్త చింతామణి & ముహూర్త దర్పణం",
    indication: "శిశువుకు సరస్వతీ సమారాధన పూర్వకంగా తొలిసారిగా విద్యాభ్యాసం, అక్షర రచన ప్రారంభించే పవిత్ర ముహూర్తం.",
    rules: "బుధ, గురు, శుక్ర వారాలు; రోహిణి, మృగశిర, పునర్వసు, పుష్యమి, హస్త, చిత్త, శ్రవణం; బుధ-గురు లగ్నాలు.",
    checkDosha: () => null
  },
  karnavedha: {
    title: "కర్ణవేధ ముహూర్తం (Karna Vedha - Ear Piercing)",
    authority: "ముహూర్త రత్నావళి (కర్ణవేధ ప్రకరణం)",
    indication: "శిశువు శారీరక ఆరోగ్యం, మేధస్సు, దృష్టి రక్షణ కొరకు చెవులు కుట్టే సంస్కారం.",
    rules: "శుక్ల పక్షం, పగటి వేళ, మృదు/లఘు నక్షత్రాలు, కుజుడు 8వ భావంలో లేని శుభ లగ్నం.",
    checkDosha: () => null
  },
  chowla_karma: {
    title: "చౌల కర్మ / చూడాకరణ (Chowla Karma - First Tonsure)",
    authority: "కాలామృతమ్ & ఆశ్వలాయన గృహ్యసూత్రాలు",
    indication: "శిశువుకు ఆయురారోగ్యాలు, తేజస్సు చేకూరుటకు తొలిసారి పుట్టువెండ్రుకలు సమర్పించే వైదిక సంస్కారం.",
    rules: "ఉత్తరాయణం, శుక్ల పక్షం, మృదు నక్షత్రాలు, చంద్రబలం.",
    checkDosha: () => null
  },
  seemantham: {
    title: "సీమంతం / పుంసవనం (Seemantham / Baby Shower)",
    authority: "స్మృతి ముక్తావళి & ముహూర్త దర్పణం",
    indication: "గర్భిణీ స్త్రీకి మనశ్శాంతి, గర్భ రక్షణ, సుఖ ప్రసవం మరియు తేజోవంతమైన సంతానం కలుగుటకు.",
    rules: "6, 7 లేదా 8వ మాసం, శుక్ల పక్షం, రోహిణి/మృగశిర/పుష్యమి/హస్త/శ్రవణం, అష్టమ శుద్ధి.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.santana_analysis && k.santana_analysis.overall_badge !== "success") return "మీ సంతాన చక్రంలో గ్రహ ప్రతిబంధకం ఉన్నందున సీమంతం శాస్త్రోక్త శుభ ముహూర్తంలో ఆచరించుట పరమ రక్ష.";
      return null;
    }
  },
  nischitartham: {
    title: "నిశ్చితార్థం / వాగ్దానం (Nischitartham / Engagement)",
    authority: "ముహూర్త రత్నావళి (వాగ్దాన ప్రకరణం)",
    indication: "వివాహ నిశ్చయార్థం ఉభయ కుటుంబాల సమ్మతితో తాంబూలాలు మార్చుకుని లగ్న పత్రిక రచించే పవిత్ర కార్యం.",
    rules: "శుక్ల పక్షం, వర-కన్యలిద్దరికీ అష్టమ చంద్రుడు మరియు నైధన తార లేని సమయం.",
    checkDosha: () => null
  },
  samavartanam: {
    title: "సమావర్తనం / విద్యా సమాప్తి (Samavartanam / Graduation)",
    authority: "పారస్కర గృహ్యసూత్రాలు & ధర్మసింధు",
    indication: "విద్యాభ్యాస సమాప్తి, దీక్షా స్నానం, మరియు ఉద్యోగ/గృహస్థాశ్రమ ప్రవేశ అర్హతను సూచించే ఘట్టం.",
    rules: "శుక్ల పక్షం, గురు బలం, శుభ గ్రహ దృష్టి కలిగిన లగ్నం.",
    checkDosha: () => null
  },
  shanku_sthapana: {
    title: "శంకుస్థాపన / గృహారంభం (Foundation Stone Laying)",
    authority: "వాస్తు రాజవల్లభం & ముహూర్త రత్నావళి",
    indication: "నూతన భవన నిర్మాణార్థం వాస్తు పురుష పూజ చేసి ప్రథమ శిలాన్యాసం (పునాది రాయి) వేసే ప్రధాన వాస్తు ముహూర్తం.",
    rules: "స్థిర లగ్నాలు (వృషభం, సింహం, వృశ్చికం, కుంభం), వాస్తు పురుష ప్రబుద్ధ కాలం, ఉత్తరాయణం.",
    checkDosha: () => null
  },
  dwara_bandha: {
    title: "సింహద్వార స్థాపన / ద్వారబంధం (Main Door Fixing)",
    authority: "మయమతం & ముహూర్త చింతామణి",
    indication: "ఇంటికి ప్రధాన లక్ష్మీ ప్రవేశ ద్వారమైన సింహద్వార చట్రాన్ని అమర్చే శుభ ముహూర్తం.",
    rules: "స్థిర లగ్నం, 4వ మరియు 8వ భావ శుద్ధి, శుభ వారాలు.",
    checkDosha: () => null
  },
  bhoomi_puja: {
    title: "భూమి పూజ / స్థల కొనుగోలు & రిజిస్ట్రేషన్ (Land Registry)",
    authority: "కాలామృతమ్ (భూలాభ ప్రకరణం)",
    indication: "స్థలం, ఇల్లు లేదా పొలం కొనుగోలు చేసి రిజిస్ట్రేషన్ చేసుకొనుటకు లేదా భూమిని స్వాధీనం చేసుకొనుటకు.",
    rules: "కుజ దృష్టి కలిగిన శుభ లగ్నం, స్థిర రాశులు, తారాబలం.",
    checkDosha: () => null
  },
  borewell_kupa: {
    title: "బోరువెల్ / బావి తవ్వకం (Borewell / Water Digging)",
    authority: "బృహత్ సంహిత (దకార్గళ అధ్యాయం) & ముహూర్త దర్పణం",
    indication: "భూమిలో అమృత జలాలు పుష్కలంగా పడటానికి నూతన బావి లేదా బోరువెల్ తవ్వకం ప్రారంభించే జల ముహూర్తం.",
    rules: "జల రాశులైన కర్కాటక, వృశ్చిక, మీన లగ్నాలు; జల నక్షత్రాలు; శుక్ర/చంద్ర బలం.",
    checkDosha: () => null
  },
  udyoga_pravesha: {
    title: "నూతన ఉద్యోగ ప్రవేశం (Job Joining / Oath Taking)",
    authority: "ముహూర్త చింతామణి (రాజసేవా ప్రకరణం)",
    indication: "కొత్త ఉద్యోగంలో చేరడానికి, బాధ్యతలు స్వీకరించడానికి, లేదా పదవీ ప్రమాణ స్వీకారానికి.",
    rules: "10వ రాజ్య భావంలో రవి/గురు/బుధ బలం, శుక్ల పక్షం, ఆదిత్య లేదా గురు వారాలు.",
    checkDosha: () => null
  },
  machinery_pratishtha: {
    title: "కర్మాగార యంత్ర ప్రతిష్ఠ (Factory Machinery / Servers)",
    authority: "ముహూర్త రత్నావళి & కాలామృతమ్",
    indication: "పరిశ్రమలు, వర్క్‌షాప్‌లు, లేదా ఐటీ కంప్యూటర్ సర్వర్లు, భారీ యంత్రాలను ప్రారంభించుటకు.",
    rules: "కుజ-శని అనుకూలత, 11వ లాభ స్థాన శుద్ధి, మంగళ లేదా శనివారాలు.",
    checkDosha: () => null
  },
  runa_vimukthi: {
    title: "రుణ విముక్తి / రుణ చెల్లింపు (Debt Repayment - అప్పుల విముక్తి)",
    authority: "ముహూర్త చింతామణి (రుణ ప్రకరణం) — భౌమవారే రవిభే చైవ...",
    indication: "తీవ్రమైన అప్పుల నుండి శాశ్వతంగా బయటపడటానికి మొదటి వాయిదా లేదా పూర్తి అప్పు చెల్లించే విశేష ముహూర్తం.",
    rules: "మంగళవారం నాడు అశ్వినీ లేదా అనూరాధ నక్షత్రం — మళ్లీ అప్పు చేయవలసిన అగత్యం కలగదు.",
    checkDosha: () => null
  },
  swarnabharana_dharana: {
    title: "నూతన వస్త్ర & స్వర్ణాభరణ ధారణ (New Clothes & Gold Jewelry)",
    authority: "కాలామృతమ్ (వస్త్రాభరణ ప్రకరణం)",
    indication: "నూతన సువర్ణాభరణాలు లేదా పట్టు వస్త్రాలను తొలిసారిగా ధరించి లక్ష్మీ స్థిరత్వాన్ని పొందుటకు.",
    rules: "గురు లేదా శుక్రవారాలు; పుష్యమి, ధనిష్ఠ, రోహిణి, రేవతి నక్షత్రాలు; శుభ లగ్నం.",
    checkDosha: () => null
  },
  videsha_prayana: {
    title: "విదేశీ ప్రయాణం / దూర ప్రయాణం (Foreign Travel)",
    authority: "ముహూర్త రత్నావళి (యాత్రా ప్రకరణం)",
    indication: "విదేశీ ప్రయాణం, వీసా ఇంటర్వ్యూ, లేదా సుదూర తీర్థయాత్రలు క్షేమంగా సాగుటకు.",
    rules: "చర లగ్నాలు (మేష, తుల, మకరం), దిక్ శూల రహిత కాలం, శుభ తారాబలం.",
    checkDosha: () => null
  },
  aushadha_sevana: {
    title: "ఔషధ సేవనారంభం (Medicine / Ayurvedic Treatment)",
    authority: "భావప్రకాశ నిఘంటు & ముహూర్త చింతామణి",
    indication: "దీర్ఘకాలిక రోగాల నివారణకు ఆయుర్వేద లేదా అల్లోపతి మందులు, చికిత్సలు ప్రారంభించుటకు.",
    rules: "అశ్వినీ నక్షత్రం (అశ్వినీ దేవతల తార), రవి లేదా చంద్ర వారాలు, అమృత ఘడియలు.",
    checkDosha: () => null
  },
  shastra_chikitsa: {
    title: "శస్త్రచికిత్స ముహూర్తం (Elective Surgery / Procedure)",
    authority: "సుశ్రుత సంహిత & ముహూర్త దర్పణం",
    indication: "ఆపరేషన్ లేదా శస్త్రచికిత్స విజయవంతమై త్వరగా కోలుకోవడానికి శాస్త్రోక్త రక్షా సమయం.",
    rules: "రిక్త తిథులు (4, 9, 14) మరియు అమావాస్య వర్జ్యం, లగ్నంలో చంద్రుడు లేని సమయం.",
    checkDosha: () => null
  },
  satyanarayana_vratam: {
    title: "శ్రీ సత్యనారాయణ స్వామి వ్రతం (Sri Satyanarayana Vratam)",
    authority: "స్కాంద పురాణం (రేవా ఖండం) & ధర్మసింధు",
    indication: "ఇష్టకామ్యార్థ సిద్ధి, కుటుంబ సౌభాగ్యం, సకల విఘ్న నివారణార్థం శ్రీ సత్యనారాయణ పూజ.",
    rules: "పౌర్ణమి లేదా శుక్ల పక్ష ఏకాదశి/త్రయోదశి, సంధ్యా వేళ లేదా ప్రదోష కాలం.",
    checkDosha: () => null
  },
  mrityunjaya_ayushya: {
    title: "మహా మృత్యుంజయ / ఆయుష్య హోమం (Ayushya / Mrityunjaya)",
    authority: "ఋగ్వేదం & బోధాయన గృహ్యసూత్రాలు",
    indication: "జన్మదినం నాడు లేదా అపమృత్యు భయం, మారక దశా కాలంలో ఆయుర్వృద్ధి కొరకు.",
    rules: "శివ వాస పరిశీలన (కైలాస/గౌరీ వాసం), సోమ లేదా గురువారాలు, శుభ తిథులు.",
    checkDosha: (k) => {
      if (!k) return null;
      if (k.gocharam && (k.gocharam.is_sade_sati || k.gocharam.is_ashtama_shani)) return "ప్రస్తుతం ఏలినాటి శని / అష్టమ శని సంచారం ఉన్నది — ఆయుష్య/మృత్యుంజయ హోమం విశేష రక్ష.";
      return null;
    }
  },
  vastu_shanti: {
    title: "వాస్తు శాంతి హోమం (Vastu Shanti - దోష నివారణ)",
    authority: "మత్స్య పురాణం & విశ్వకర్మ ప్రకాశిక",
    indication: "నివాస గృహంలో లేదా వ్యాపార సంస్థలో ఉన్న వాస్తు దోషాలు, దిశా దోషాలు తొలగి శాంతి కలుగుటకు.",
    rules: "స్థిర లగ్నం, అగ్ని వాస పరిశీలన (పృథ్వీ వాసం), శుభ తారాబలం.",
    checkDosha: () => null
  },
  devata_pratishtha: {
    title: "దేవాలయ విగ్రహ ప్రతిష్ఠ (Temple Deity Prana Pratishtha)",
    authority: "పాంచరాత్ర / వైఖానస & శైవాగమం",
    indication: "నూతన దేవాలయంలో విగ్రహ ప్రాణ ప్రతిష్ఠ, కుంభాభిషేకం, మరియు బ్రహ్మోత్సవాల ప్రారంభ కాలం.",
    rules: "ఉత్తరాయణం, శుక్ల పక్షం, స్థిర లగ్నం, సమస్త కేంద్రాలలో శుభ గ్రహాలు.",
    checkDosha: () => null
  }
};

window.renderMuhurtamJatakamAssistant = function() {
  const container = document.getElementById("muhurtamJatakamDoshaAssistant");
  if (!container) return;

  const data = window.currentKundaliData;
  if (!data) {
    container.innerHTML = `
      <div style="background: linear-gradient(135deg, #FFF8E1, #FFF3E0); border: 1px solid #FFE082; border-left: 6px solid #FF8F00; border-radius: 10px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <div style="flex: 1 1 320px;">
            <h4 style="color: #E65100; font-size: 1.08rem; font-weight: 800; margin: 0 0 6px 0; display: flex; align-items: center; gap: 8px;">
              <span>💡</span> మీ జాతకంలో ఏ దోషం ఉన్నదో నిర్ధారించుకున్నారా? (Know Your Exact Doshas First)
            </h4>
            <p style="margin: 0; color: #5D4037; font-size: 0.94rem; line-height: 1.55;">
              ప్రతి ఒక్కరూ అన్ని పరిహార హోమాలు చేయనక్కర్లేదు. ముందుగా మీ జాతక చక్రం వేస్తే, అందులో నిజంగా <strong>సర్ప దోషం, కుజ దోషం, సంతాన ప్రతిబంధకం లేదా పితృ దోషం</strong> ఉన్నదో లేదో శాస్త్రోక్తంగా గుర్తించి, దానికి తగిన నిర్దిష్ట ముహూర్తాన్ని ఇక్కడ సిఫార్సు చేస్తుంది.
            </p>
          </div>
          <button type="button" class="btn-submit" style="padding: 9px 18px; font-size: 0.92rem; border-radius: 8px; background: linear-gradient(135deg, #FF6F00, #E65100); display: inline-flex; align-items: center; gap: 6px; cursor: pointer; border: none; color: white; font-weight: 700; white-space: nowrap;"
            onclick="document.querySelector('.global-nav-btn[data-module=\\'moduleKundali\\']')?.click();">
            <span>🔯</span> ముందుగా జాతక పరిశీలన చేయండి (Examine Kundali)
          </button>
        </div>
      </div>
    `;
    return;
  }

  // Jathakam is available! Collect all detected doshas
  const inp = data.input || {};
  const nativeName = inp.name || "జాతకుడు";
  const p = data.panchangam || {};
  const nakName = p.nakshatra || p.nakshatra_name_te || p.nakshatra_name || "";
  const rashiName = p.janma_rashi || p.rashi_name_te || p.rashi_name || "";

  const detectedList = [];

  // 1. Kala Sarpa / Sarpa Dosha
  if (data.kalasarpa_dosha && data.kalasarpa_dosha.has_dosha) {
    const ks = data.kalasarpa_dosha;
    detectedList.push({
      key: "kala_sarpa",
      name: `సర్ప దోషం / కాలసర్ప దోషం (${ks.type_name || 'కాలసర్ప పరిశీలన'})`,
      reason: ks.summary_te || "రాహు-కేతువుల మధ్య సమస్త గ్రహాలు బంధించబడినవి.",
      authority: ks.shastra_authority || "బృహత్ పరాశర హోరాశాస్త్రం (అధ్యా. 83) & జాతకాభరణం",
      remedyType: "naga_pratishtha",
      remedyLabel: "నాగ ప్రతిష్ఠాపన / ఆశ్లేషా బలి పూజ"
    });
  }

  // 2. Kuja Dosha (Manglik)
  if (data.kuja_dosha && data.kuja_dosha.severity === "present") {
    const kd = data.kuja_dosha;
    detectedList.push({
      key: "kuja_dosha",
      name: `కుజ దోషం / మాంగళిక దోషం (${kd.status_te})`,
      reason: `కుజుడు లగ్నం నుండి ${kd.kuja_from_lagna}వ స్థానంలో, చంద్రుని నుండి ${kd.kuja_from_moon}వ స్థానంలో ఉన్నాడు.`,
      authority: kd.shastra_authority || "ముహూర్త రత్నావళి & జాతక చంద్రిక",
      remedyType: "kuja_shanti_subrahmanya",
      remedyLabel: "సుబ్రహ్మణ్య షష్ఠి / కుజ శాంతి హోమం"
    });
  }

  // 3. Santana & Shapa Doshas
  if (data.santana_analysis && Array.isArray(data.santana_analysis.doshas_detected)) {
    data.santana_analysis.doshas_detected.forEach(d => {
      const pRem = d.primary_remedy || {};
      const evType = pRem.event_type || (d.shapa_type === "sarpa_shapa" ? "naga_pratishtha" : (d.shapa_type === "bhauma_kuja" ? "kuja_shanti_subrahmanya" : (d.shapa_type === "pitru_shapa" ? "tila_homa_narayana_bali" : "santana_gopala")));
      detectedList.push({
        key: d.shapa_type || d.name_te,
        name: d.name_te,
        reason: d.astrological_reason,
        authority: d.shastra_authority || "బృహత్ పరాశర సంతాన ప్రకరణం",
        remedyType: evType,
        remedyLabel: pRem.name || d.name_te
      });
    });
  }

  // 4. Shani / Sade Sati / Ashtama Shani
  if (data.gocharam && (data.gocharam.is_sade_sati || data.gocharam.is_ashtama_shani)) {
    detectedList.push({
      key: "shani_dosha",
      name: `శని గ్రహ పీడ (${data.gocharam.is_sade_sati ? 'ఏలినాటి శని' : 'అష్టమ శని'})`,
      reason: "గోచార రీత్యా శని జన్మ రాశి లేదా అష్టమ స్థానంలో సంచరిస్తున్నాడు.",
      authority: "కృష్ణ యజుర్వేద సంహిత & శివపురాణం",
      remedyType: "rudra_pashupatam",
      remedyLabel: "రుద్ర పాశుపత హోమం / మహా రుద్రాభిషేకం"
    });
  }

  if (detectedList.length > 0) {
    container.innerHTML = `
      <div style="background: linear-gradient(135deg, #FFF9F9, #FFF3F0); border: 1px solid #FFCDD2; border-left: 6px solid #C62828; border-radius: 10px; padding: 18px 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); margin-bottom: 6px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px dashed #FFCDD2;">
          <div style="font-weight: 800; color: #B71C1C; font-size: 1.12rem; display: flex; align-items: center; gap: 8px;">
            <span>🛡️</span> మీ జాతకంలో గుర్తించిన దోషాలు & సూచించబడిన పరిహారాలు (Detected Doshas for ${nativeName})
          </div>
          <span style="font-size: 0.88rem; background: #FFEBEE; color: #C62828; padding: 4px 10px; border-radius: 12px; font-weight: 700; border: 1px solid #EF9A9A;">
            జన్మ నక్షత్రం: ${nakName} · రాశి: ${rashiName}
          </span>
        </div>
        <p style="margin: 0 0 12px 0; font-size: 0.95rem; color: #4E342E; line-height: 1.55;">
          శాస్త్ర గ్రంథాల ప్రకారం మీ జాతక చక్రాన్ని విశ్లేషించగా క్రింది దోషాలు నిర్ధారించబడినవి. తగిన పరిహార కార్యాన్ని ఎంచుకోవడానికి పక్కనున్న బటన్ నొక్కండి:
        </p>
        <div style="display: flex; flex-direction: column; gap: 10px;">
          ${detectedList.map(item => `
            <div style="background: #FFF; border: 1px solid #FFEBEE; border-radius: 8px; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
              <div style="flex: 1 1 300px;">
                <div style="font-weight: 800; color: #C62828; font-size: 1.02rem; display: flex; align-items: center; gap: 6px;">
                  <span>🚩</span> ${item.name}
                </div>
                <div style="font-size: 0.9rem; color: #5D4037; margin: 3px 0;"><strong>జాతక కారణం:</strong> ${item.reason}</div>
                <div style="font-size: 0.85rem; color: #0D47A1;"><strong>శాస్త్ర ప్రమాణం:</strong> ${item.authority}</div>
              </div>
              <div>
                <button type="button" class="btn-submit" style="padding: 7px 14px; font-size: 0.88rem; border-radius: 6px; background: linear-gradient(135deg, #D32F2F, #B71C1C); color: white; border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; font-weight: 700; white-space: nowrap; box-shadow: 0 2px 6px rgba(183,28,28,0.25);"
                  onclick="window.launchMuhurtamForRemedy('${item.remedyType}', '${encodeURIComponent(item.remedyLabel)}')">
                  <span>⏱️</span> ఈ పరిహార ముహూర్తాన్ని ఎంచుకోండి (Select)
                </button>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div style="background: linear-gradient(135deg, #F1F8E9, #E8F5E9); border: 1px solid #C8E6C9; border-left: 6px solid #2E7D32; border-radius: 10px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 6px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
          <div>
            <h4 style="color: #1B5E20; font-size: 1.08rem; font-weight: 800; margin: 0 0 4px 0; display: flex; align-items: center; gap: 8px;">
              <span>🌿</span> మీ జాతకం నిర్మలమైనది — తీవ్ర దోషాలు లేవు (Clear Horoscope)
            </h4>
            <p style="margin: 0; color: #2E7D32; font-size: 0.94rem; line-height: 1.55;">
              జాతకుడు: <strong>${nativeName}</strong> (${nakName} నక్షత్రం, ${rashiName} రాశి) జాతకంలో సర్ప శాపం, కుజ లేదా పితృ దోషాలు ఏవీ లేవు. పరిహార హోమాలు అవసరం లేదు. శుభకార్య ముహూర్తాలను (వివాహం, గృహప్రవేశం, నామకరణం మొదలైనవి) లేదా సమస్త శుభం కొరకు నవగ్రహ శాంతిని ఎంచుకోవచ్చు.
            </p>
          </div>
          <span style="font-size: 0.85rem; background: #E8F5E9; color: #2E7D32; padding: 4px 10px; border-radius: 12px; font-weight: 700; border: 1px solid #A5D6A7;">
            దోష రహిత జాతకం
          </span>
        </div>
      </div>
    `;
  }
};

window.updateMuhurtamEventContextCard = function(eventType) {
  const container = document.getElementById("muhurtamEventContextCard");
  if (!container) return;

  const evKey = eventType || document.getElementById("muhurtamEventType")?.value || "naga_pratishtha";
  const info = PARIHARA_SHASTRA_INFO[evKey];
  if (!info) {
    container.innerHTML = "";
    return;
  }

  const kData = window.currentKundaliData;
  let statusHtml = "";
  if (kData) {
    const doshaVerdict = typeof info.checkDosha === "function" ? info.checkDosha(kData) : null;
    if (doshaVerdict === null) {
      statusHtml = `
        <div style="background: #E8F5E9; border-left: 4px solid #2E7D32; padding: 8px 12px; border-radius: 4px; font-size: 0.92rem; color: #1B5E20; margin-top: 8px;">
          <span>✨</span> <strong>శుభకార్య విశేషం:</strong> ఇది వైదిక సంస్కార ముహూర్తం. జాతకునికి తారాబలం, చంద్రబలం మరియు లగ్న శుద్ధి ఆధారంగా అత్యుత్తమ సమయాలు నిర్ణయించబడతాయి.
        </div>
      `;
    } else if (doshaVerdict) {
      statusHtml = `
        <div style="background: #FFEBEE; border-left: 4px solid #C62828; padding: 8px 12px; border-radius: 4px; font-size: 0.92rem; color: #B71C1C; margin-top: 8px;">
          <span>🚩</span> <strong>మీ జాతకంలో నిర్ధారితం:</strong> ${doshaVerdict} — ఈ పరిహార ముహూర్తం మీకు శాస్త్రోక్తంగా అత్యంత శ్రేయస్కరం!
        </div>
      `;
    } else {
      statusHtml = `
        <div style="background: #F1F8E9; border-left: 4px solid #4CAF50; padding: 8px 12px; border-radius: 4px; font-size: 0.92rem; color: #2E7D32; margin-top: 8px;">
          <span>🌿</span> <strong>మీ జాతకంలో ఈ నిర్దిష్ట దోషం లేదు:</strong> మీ చక్రం ఈ దోషం నుండి నిర్మలంగా ఉంది. కేవలం కుటుంబ సమస్త క్షేమం లేదా ఇష్టపూర్వక సంకల్పం కొరకు ఆచరించవచ్చు.
        </div>
      `;
    }
  } else {
    statusHtml = `
      <div style="background: #FFF8E1; border-left: 4px solid #FFA000; padding: 8px 12px; border-radius: 4px; font-size: 0.9rem; color: #795548; margin-top: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
        <span>ℹ️ మీ జాతక చక్రం ఇంకా విశ్లేషించబడలేదు. మీకు నిజంగా ఈ దోషం ఉన్నదో లేదో నిర్ధారించుకోవడానికి 'జాతక చక్రం' ట్యాబ్‌లో పరిశీలించండి.</span>
        <button type="button" style="padding: 4px 10px; font-size: 0.82rem; border-radius: 4px; background: #FF8F00; color: white; border: none; cursor: pointer;"
          onclick="document.querySelector('.global-nav-btn[data-module=\\'moduleKundali\\']')?.click();">జాతకం వేయండి</button>
      </div>
    `;
  }

  container.innerHTML = `
    <div style="background: #FFFDF9; border: 1px solid #EEDBCE; border-radius: 8px; padding: 12px 16px; font-size: 0.92rem; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px; margin-bottom: 6px;">
        <strong style="color: #4A0E17; font-size: 1rem;">📜 ${info.title} — శాస్త్రోక్త నేపథ్యం</strong>
        <span style="font-size: 0.82rem; color: #0D47A1; background: #E8EAF6; padding: 2px 8px; border-radius: 4px; font-weight: 600;">
          గ్రంథం: ${info.authority}
        </span>
      </div>
      <div style="color: #5D4037; line-height: 1.5; margin-bottom: 4px;">
        <strong>🔍 ఎవరికి అవసరం?</strong> ${info.indication}
      </div>
      <div style="color: #2E7D32; line-height: 1.5;">
        <strong>🌟 ముహూర్త శాస్త్ర నియమం:</strong> ${info.rules}
      </div>
      ${statusHtml}
    </div>
  `;
};

/* ========================================================================== */
/* MODULE 5: VEDIC MUHURTAM CALCULATOR (అత్యంత ఖచ్చితమైన ముహూర్త నిర్ణయం)     */
/* ========================================================================== */

function initMuhurtamModule() {
  // 1. City autocomplete for Muhurtam
  setupCityAutocomplete("muhurtamPlace", "muhurtamCitySuggestions", "muhurtamLat", "muhurtamLon", "muhurtamTz", "muhurtamCityFeedback");

  // 2. Set default start date to today
  const startInput = document.getElementById("muhurtamStartDate");
  if (startInput && !startInput.value) {
    const today = new Date().toISOString().split("T")[0];
    startInput.value = today;
  }

  // 3. Participant Mode Selector (Individual / Couple / Whole Family)
  const modeButtons = document.querySelectorAll(".participant-mode-btn");
  const modeInput = document.getElementById("muhurtamParticipantMode");
  const panelIndividual = document.getElementById("panelParticipantIndividual");
  const panelCouple = document.getElementById("panelParticipantCouple");
  const panelFamily = document.getElementById("panelParticipantFamily");

  modeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      modeButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const mode = btn.dataset.mode || "individual";
      if (modeInput) modeInput.value = mode;

      if (panelIndividual) panelIndividual.style.display = (mode === "individual") ? "grid" : "none";
      if (panelCouple) panelCouple.style.display = (mode === "couple") ? "block" : "none";
      if (panelFamily) panelFamily.style.display = (mode === "family") ? "block" : "none";
    });
  });

  // 4. Dynamic Family Members Table Management
  const NAKSHATRA_NAMES = [
    "1. అశ్విని (Ashwini)", "2. భరణి (Bharani)", "3. కృత్తిక (Krittika)", "4. రోహిణి (Rohini)",
    "5. మృగశిర (Mrigashira)", "6. ఆరుద్ర (Ardra)", "7. పునర్వసు (Punarvasu)", "8. పుష్యమి (Pushya)",
    "9. ఆశ్లేష (Ashlesha)", "10. మఖ (Magha)", "11. పూర్వఫల్గుణి / పుబ్బ (Pubba)", "12. ఉత్తరఫల్గుణి / ఉత్తర (Uttara)",
    "13. హస్త (Hasta)", "14. చిత్త (Chitra)", "15. స్వాతి (Swati)", "16. విశాఖ (Vishakha)",
    "17. అనూరాధ (Anuradha)", "18. జ్యేష్ఠ (Jyeshtha)", "19. మూల (Moola)", "20. పూర్వాషాఢ (Purvashadha)",
    "21. ఉత్తరాషాఢ (Uttarashadha)", "22. శ్రవణం (Shravana)", "23. ధనిష్ఠ (Dhanishta)", "24. శతభిషం (Shatabhisha)",
    "25. పూర్వాభాద్ర (Purvabhadra)", "26. ఉత్తరాభాద్ర (Uttarabhadra)", "27. రేవతి (Revati)"
  ];

  const RASHI_NAMES = [
    "1. మేషం (Aries)", "2. వృషభం (Taurus)", "3. మిథునం (Gemini)", "4. కర్కాటకం (Cancer)",
    "5. సింహం (Leo)", "6. కన్య (Virgo)", "7. తుల (Libra)", "8. వృశ్చికం (Scorpio)",
    "9. ధనుస్సు (Sagittarius)", "10. మకరం (Capricorn)", "11. కుంభం (Aquarius)", "12. మీనం (Pisces)"
  ];

  function buildNakshatraOptions(selectedIdx) {
    let html = `<option value="">-- నక్షత్రం --</option>`;
    NAKSHATRA_NAMES.forEach((name, idx) => {
      const sel = (selectedIdx !== undefined && selectedIdx !== null && String(selectedIdx) === String(idx)) ? "selected" : "";
      html += `<option value="${idx}" ${sel}>${name}</option>`;
    });
    return html;
  }

  function buildRashiOptions(selectedIdx) {
    let html = `<option value="">-- రాశి --</option>`;
    RASHI_NAMES.forEach((name, idx) => {
      const sel = (selectedIdx !== undefined && selectedIdx !== null && String(selectedIdx) === String(idx)) ? "selected" : "";
      html += `<option value="${idx}" ${sel}>${name}</option>`;
    });
    return html;
  }

  window.familyMembersData = [
    { name: "యజమాని / భర్త", role: "head", nakshatra_index: "", rashi_index: "" },
    { name: "భార్య", role: "wife", nakshatra_index: "", rashi_index: "" }
  ];

  window.renderFamilyTable = function() {
    const tbody = document.getElementById("familyMembersTableBody");
    if (!tbody) return;

    tbody.innerHTML = window.familyMembersData.map((m, idx) => `
      <tr data-index="${idx}">
        <td>
          <input type="text" class="form-control fam-name" style="padding: 6px 8px; font-size: 0.88rem;" value="${m.name || ''}" placeholder="సభ్యుని పేరు" onchange="window.updateFamilyMember(${idx}, 'name', this.value)">
        </td>
        <td>
          <select class="form-control fam-role" style="padding: 6px 8px; font-size: 0.88rem;" onchange="window.updateFamilyMember(${idx}, 'role', this.value)">
            <option value="head" ${m.role === 'head' ? 'selected' : ''}>యజమాని (Head)</option>
            <option value="husband" ${m.role === 'husband' ? 'selected' : ''}>భర్త (Husband)</option>
            <option value="wife" ${m.role === 'wife' ? 'selected' : ''}>భార్య (Wife)</option>
            <option value="son" ${m.role === 'son' ? 'selected' : ''}>కుమారుడు (Son)</option>
            <option value="daughter" ${m.role === 'daughter' ? 'selected' : ''}>కుమార్తె (Daughter)</option>
            <option value="father" ${m.role === 'father' ? 'selected' : ''}>తండ్రి (Father)</option>
            <option value="mother" ${m.role === 'mother' ? 'selected' : ''}>తల్లి (Mother)</option>
            <option value="other" ${m.role === 'other' ? 'selected' : ''}>ఇతర బంధువు (Other)</option>
          </select>
        </td>
        <td>
          <select class="form-control fam-nak" style="padding: 6px 8px; font-size: 0.88rem;" onchange="window.updateFamilyMember(${idx}, 'nakshatra_index', this.value)">
            ${buildNakshatraOptions(m.nakshatra_index)}
          </select>
        </td>
        <td>
          <select class="form-control fam-rashi" style="padding: 6px 8px; font-size: 0.88rem;" onchange="window.updateFamilyMember(${idx}, 'rashi_index', this.value)">
            ${buildRashiOptions(m.rashi_index)}
          </select>
        </td>
        <td style="text-align: center;">
          <button type="button" onclick="window.removeFamilyMember(${idx})" style="background: #FFEBEE; color: #C62828; border: 1px solid #FFCDD2; border-radius: 4px; padding: 4px 8px; cursor: pointer; font-size: 0.85rem;" title="తీసివేయండి">
            ✕
          </button>
        </td>
      </tr>
    `).join("");
  };

  window.updateFamilyMember = function(idx, field, value) {
    if (window.familyMembersData[idx]) {
      window.familyMembersData[idx][field] = value;
    }
  };

  window.removeFamilyMember = function(idx) {
    if (window.familyMembersData.length <= 1) {
      alert("కనీసం ఒక సభ్యుని వివరాలు ఉండాలి.");
      return;
    }
    window.familyMembersData.splice(idx, 1);
    window.renderFamilyTable();
  };

  const addBtn = document.getElementById("btnAddFamilyMember");
  if (addBtn) {
    addBtn.addEventListener("click", () => {
      window.familyMembersData.push({
        name: `కుటుంబ సభ్యుడు #${window.familyMembersData.length + 1}`,
        role: "other",
        nakshatra_index: "",
        rashi_index: ""
      });
      window.renderFamilyTable();
    });
  }

  // Initialize family table
  window.renderFamilyTable();

  // 4b. Event selection change listener & assistant initialization
  const eventSelect = document.getElementById("muhurtamEventType");
  if (eventSelect) {
    eventSelect.addEventListener("change", () => {
      window.updateMuhurtamEventContextCard(eventSelect.value);
    });
    window.updateMuhurtamEventContextCard(eventSelect.value);
  }
  // 4c. Classical Avakahada Syllable Auto-Detection for Priests & Users without DOB/TOB
  const AVAKAHADA_PADA_MAP = {
    // 0: Ashwini (Aries / మేషం)
    "చూ": [0, 0, 1], "చే": [0, 0, 2], "చో": [0, 0, 3], "లా": [0, 0, 4], "ల": [0, 0, 4],
    "chu": [0, 0, 1], "che": [0, 0, 2], "cho": [0, 0, 3], "la": [0, 0, 4],

    // 1: Bharani (Aries / మేషం)
    "లీ": [1, 0, 1], "లి": [1, 0, 1], "లూ": [1, 0, 2], "లు": [1, 0, 2], "లే": [1, 0, 3], "లె": [1, 0, 3], "లో": [1, 0, 4], "లొ": [1, 0, 4],
    "lee": [1, 0, 1], "li": [1, 0, 1], "lu": [1, 0, 2], "loo": [1, 0, 2], "le": [1, 0, 3], "lo": [1, 0, 4],

    // 2: Krittika: 1 Aries, 2-4 Taurus
    "ఆ": [2, 0, 1], "అ": [2, 0, 1], "a": [2, 0, 1], "aa": [2, 0, 1],
    "ఈ": [2, 1, 2], "ఇ": [2, 1, 2], "ee": [2, 1, 2], "i": [2, 1, 2],
    "ఊ": [2, 1, 3], "ఉ": [2, 1, 3], "oo": [2, 1, 3], "u": [2, 1, 3],
    "ఏ": [2, 1, 4], "ఎ": [2, 1, 4], "e": [2, 1, 4], "ae": [2, 1, 4],

    // 3: Rohini (Taurus / వృషభం)
    "ఓ": [3, 1, 1], "ఒ": [3, 1, 1], "o": [3, 1, 1],
    "వా": [3, 1, 2], "వ": [3, 1, 2], "va": [3, 1, 2], "wa": [3, 1, 2],
    "వీ": [3, 1, 3], "వి": [3, 1, 3], "vi": [3, 1, 3], "vee": [3, 1, 3], "wi": [3, 1, 3],
    "వూ": [3, 1, 4], "వు": [3, 1, 4], "vu": [3, 1, 4], "voo": [3, 1, 4],

    // 4: Mrigashira: 1-2 Taurus, 3-4 Gemini
    "వే": [4, 1, 1], "వె": [4, 1, 1], "ve": [4, 1, 1], "we": [4, 1, 1],
    "వో": [4, 1, 2], "వొ": [4, 1, 2], "vo": [4, 1, 2], "wo": [4, 1, 2],
    "కా": [4, 2, 3], "క": [4, 2, 3], "ka": [4, 2, 3],
    "కీ": [4, 2, 4], "కి": [4, 2, 4], "ki": [4, 2, 4], "kee": [4, 2, 4],

    // 5: Ardra (Gemini / మిథునం)
    "కూ": [5, 2, 1], "కు": [5, 2, 1], "ku": [5, 2, 1], "koo": [5, 2, 1],
    "ఘా": [5, 2, 2], "ఘ": [5, 2, 2], "gha": [5, 2, 2],
    "ఙ": [5, 2, 3], "ఙా": [5, 2, 3],
    "ఛా": [5, 2, 4], "ఛ": [5, 2, 4], "chha": [5, 2, 4],

    // 6: Punarvasu: 1-3 Gemini, 4 Cancer
    "కే": [6, 2, 1], "కె": [6, 2, 1], "ke": [6, 2, 1], "kay": [6, 2, 1],
    "కో": [6, 2, 2], "కొ": [6, 2, 2], "ko": [6, 2, 2],
    "హా": [6, 2, 3], "హ": [6, 2, 3], "ha": [6, 2, 3],
    "హీ": [6, 3, 4], "హి": [6, 3, 4], "hi": [6, 3, 4], "hee": [6, 3, 4],

    // 7: Pushya (Cancer / కర్కాటకం)
    "హూ": [7, 3, 1], "హు": [7, 3, 1], "hu": [7, 3, 1], "hoo": [7, 3, 1],
    "హే": [7, 3, 2], "హె": [7, 3, 2], "he": [7, 3, 2],
    "హో": [7, 3, 3], "హొ": [7, 3, 3], "ho": [7, 3, 3],
    "డా": [7, 3, 4], "డ": [7, 3, 4], "da": [7, 3, 4],

    // 8: Ashlesha (Cancer / కర్కాటకం)
    "డీ": [8, 3, 1], "డి": [8, 3, 1], "dee": [8, 3, 1], "di": [8, 3, 1],
    "డూ": [8, 3, 2], "డు": [8, 3, 2], "du": [8, 3, 2], "doo": [8, 3, 2],
    "డే": [8, 3, 3], "డె": [8, 3, 3], "de": [8, 3, 3], "day": [8, 3, 3],
    "డో": [8, 3, 4], "డొ": [8, 3, 4], "do": [8, 3, 4],

    // 9: Magha (Leo / సింహం)
    "మా": [9, 4, 1], "మ": [9, 4, 1], "ma": [9, 4, 1],
    "మీ": [9, 4, 2], "మి": [9, 4, 2], "mi": [9, 4, 2], "mee": [9, 4, 2],
    "మూ": [9, 4, 3], "ము": [9, 4, 3], "mu": [9, 4, 3], "moo": [9, 4, 3],
    "మే": [9, 4, 4], "మె": [9, 4, 4], "me": [9, 4, 4], "may": [9, 4, 4],

    // 10: Purva Phalguni (Pubba) (Leo / సింహం)
    "మో": [10, 4, 1], "మొ": [10, 4, 1], "mo": [10, 4, 1],
    "టా": [10, 4, 2], "ట": [10, 4, 2], "ta": [10, 4, 2],
    "టీ": [10, 4, 3], "టి": [10, 4, 3], "ti": [10, 4, 3], "tee": [10, 4, 3],
    "టూ": [10, 4, 4], "టు": [10, 4, 4], "tu": [10, 4, 4], "too": [10, 4, 4],

    // 11: Uttara Phalguni (Uttara): 1 Leo, 2-4 Virgo
    "టే": [11, 4, 1], "టె": [11, 4, 1], "te": [11, 4, 1],
    "టో": [11, 5, 2], "టొ": [11, 5, 2], "to": [11, 5, 2],
    "పా": [11, 5, 3], "ప": [11, 5, 3], "pa": [11, 5, 3],
    "పీ": [11, 5, 4], "పి": [11, 5, 4], "pi": [11, 5, 4], "pee": [11, 5, 4],

    // 12: Hasta (Virgo / కన్య)
    "పూ": [12, 5, 1], "పు": [12, 5, 1], "pu": [12, 5, 1], "poo": [12, 5, 1],
    "షా": [12, 5, 2], "ష": [12, 5, 2], "sha": [12, 5, 2],
    "ణా": [12, 5, 3], "ణ": [12, 5, 3], "na": [12, 5, 3],
    "ఠా": [12, 5, 4], "ఠ": [12, 5, 4], "tha": [12, 5, 4],

    // 13: Chitra: 1-2 Virgo, 3-4 Libra
    "పే": [13, 5, 1], "పె": [13, 5, 1], "pe": [13, 5, 1],
    "పో": [13, 5, 2], "పొ": [13, 5, 2], "po": [13, 5, 2],
    "రా": [13, 6, 3], "ర": [13, 6, 3], "ra": [13, 6, 3],
    "రీ": [13, 6, 4], "రి": [13, 6, 4], "ri": [13, 6, 4], "ree": [13, 6, 4],

    // 14: Swati (Libra / తుల)
    "రూ": [14, 6, 1], "రు": [14, 6, 1], "ru": [14, 6, 1], "roo": [14, 6, 1],
    "రే": [14, 6, 2], "రె": [14, 6, 2], "re": [14, 6, 2], "ray": [14, 6, 2],
    "రో": [14, 6, 3], "రొ": [14, 6, 3], "ro": [14, 6, 3],
    "తా": [14, 6, 4], "త": [14, 6, 4], "tha": [14, 6, 4],

    // 15: Vishakha: 1-3 Libra, 4 Scorpio
    "తీ": [15, 6, 1], "తి": [15, 6, 1], "thi": [15, 6, 1], "thee": [15, 6, 1],
    "తూ": [15, 6, 2], "తు": [15, 6, 2], "thu": [15, 6, 2], "thoo": [15, 6, 2],
    "తే": [15, 6, 3], "తె": [15, 6, 3], "the": [15, 6, 3],
    "తో": [15, 7, 4], "తొ": [15, 7, 4], "tho": [15, 7, 4],

    // 16: Anuradha (Scorpio / వృశ్చికం)
    "నా": [16, 7, 1], "న": [16, 7, 1],
    "నీ": [16, 7, 2], "ని": [16, 7, 2], "ni": [16, 7, 2], "nee": [16, 7, 2],
    "నూ": [16, 7, 3], "ను": [16, 7, 3], "nu": [16, 7, 3], "noo": [16, 7, 3],
    "నే": [16, 7, 4], "నె": [16, 7, 4], "ne": [16, 7, 4], "nay": [16, 7, 4],

    // 17: Jyeshtha (Scorpio / వృశ్చికం)
    "నో": [17, 7, 1], "నొ": [17, 7, 1], "no": [17, 7, 1],
    "యా": [17, 7, 2], "య": [17, 7, 2], "ya": [17, 7, 2],
    "యీ": [17, 7, 3], "యి": [17, 7, 3], "yi": [17, 7, 3],
    "యూ": [17, 7, 4], "యు": [17, 7, 4], "yu": [17, 7, 4], "yoo": [17, 7, 4],

    // 18: Moola (Sagittarius / ధనుస్సు)
    "యే": [18, 8, 1], "యె": [18, 8, 1], "ye": [18, 8, 1],
    "యో": [18, 8, 2], "యొ": [18, 8, 2], "yo": [18, 8, 2],
    "భా": [18, 8, 3], "భ": [18, 8, 3], "bha": [18, 8, 3],
    "భీ": [18, 8, 4], "భి": [18, 8, 4], "bhi": [18, 8, 4], "bhee": [18, 8, 4],

    // 19: Purvashadha (Sagittarius / ధనుస్సు)
    "భూ": [19, 8, 1], "భు": [19, 8, 1], "bhu": [19, 8, 1], "bhoo": [19, 8, 1],
    "ధా": [19, 8, 2], "ధ": [19, 8, 2], "dha": [19, 8, 2],
    "ఫా": [19, 8, 3], "ఫ": [19, 8, 3], "pha": [19, 8, 3], "fa": [19, 8, 3],
    "ఢా": [19, 8, 4], "ఢ": [19, 8, 4],

    // 20: Uttarashadha: 1 Sagittarius, 2-4 Capricorn
    "భే": [20, 8, 1], "భె": [20, 8, 1], "bhe": [20, 8, 1],
    "భో": [20, 9, 2], "భొ": [20, 9, 2], "bho": [20, 9, 2],
    "జా": [20, 9, 3], "జ": [20, 9, 3], "ja": [20, 9, 3],
    "జీ": [20, 9, 4], "జి": [20, 9, 4], "ji": [20, 9, 4], "jee": [20, 9, 4],

    // 21: Shravana (Capricorn / మకరం)
    "ఖీ": [21, 9, 1], "ఖి": [21, 9, 1], "khi": [21, 9, 1], "khee": [21, 9, 1],
    "ఖూ": [21, 9, 2], "ఖు": [21, 9, 2], "khu": [21, 9, 2],
    "ఖే": [21, 9, 3], "ఖె": [21, 9, 3], "khe": [21, 9, 3],
    "ఖో": [21, 9, 4], "ఖొ": [21, 9, 4], "kho": [21, 9, 4],
    "జు": [21, 9, 2], "జే": [21, 9, 3], "జో": [21, 9, 4],

    // 22: Dhanishta: 1-2 Capricorn, 3-4 Aquarius
    "గా": [22, 9, 1], "గ": [22, 9, 1], "ga": [22, 9, 1],
    "గీ": [22, 9, 2], "గి": [22, 9, 2], "gi": [22, 9, 2], "gee": [22, 9, 2],
    "గూ": [22, 10, 3], "గు": [22, 10, 3], "gu": [22, 10, 3], "goo": [22, 10, 3],
    "గే": [22, 10, 4], "గె": [22, 10, 4], "ge": [22, 10, 4], "gay": [22, 10, 4],

    // 23: Shatabhisha (Aquarius / కుంభం)
    "గో": [23, 10, 1], "గొ": [23, 10, 1], "go": [23, 10, 1],
    "సా": [23, 10, 2], "స": [23, 10, 2], "sa": [23, 10, 2],
    "సీ": [23, 10, 3], "సి": [23, 10, 3], "శి": [23, 10, 3], "శీ": [23, 10, 3], "శ్రీ": [23, 10, 3], "శ": [23, 10, 3],
    "si": [23, 10, 3], "see": [23, 10, 3], "shi": [23, 10, 3], "sri": [23, 10, 3], "shree": [23, 10, 3],
    "సూ": [23, 10, 4], "సు": [23, 10, 4], "శు": [23, 10, 4], "శూ": [23, 10, 4],
    "su": [23, 10, 4], "soo": [23, 10, 4], "shu": [23, 10, 4],

    // 24: Purvabhadra: 1-3 Aquarius, 4 Pisces
    "సే": [24, 10, 1], "సె": [24, 10, 1], "se": [24, 10, 1], "say": [24, 10, 1],
    "సో": [24, 10, 2], "సొ": [24, 10, 2], "so": [24, 10, 2],
    "దా": [24, 10, 3], "ద": [24, 10, 3], "da": [24, 10, 3],
    "దీ": [24, 11, 4], "ది": [24, 11, 4], "di": [24, 11, 4], "dee": [24, 11, 4],

    // 25: Uttarabhadra (Pisces / మీనం)
    "దూ": [25, 11, 1], "దు": [25, 11, 1], "du": [25, 11, 1], "doo": [25, 11, 1],
    "శ్యా": [25, 11, 2], "శ్య": [25, 11, 2], "shya": [25, 11, 2],
    "ఝా": [25, 11, 3], "ఝ": [25, 11, 3], "jha": [25, 11, 3],
    "ధా": [25, 11, 4], "ధ": [25, 11, 4],

    // 26: Revati (Pisces / మీనం)
    "దే": [26, 11, 1], "దె": [26, 11, 1], "de": [26, 11, 1], "day": [26, 11, 1],
    "దో": [26, 11, 2], "దొ": [26, 11, 2], "do": [26, 11, 2],
    "చా": [26, 11, 3], "చ": [26, 11, 3], "cha": [26, 11, 3],
    "చీ": [26, 11, 4], "చి": [26, 11, 4], "chi": [26, 11, 4], "chee": [26, 11, 4]
  };

  function detectAvakahadaFromName(name) {
    if (!name || typeof name !== "string") return null;
    const clean = name.trim();
    if (!clean) return null;
    const lower = clean.toLowerCase();

    // Telugu prefixes (length 3, 2, 1)
    for (const len of [3, 2, 1]) {
      if (clean.length >= len) {
        const prefix = clean.substring(0, len);
        if (AVAKAHADA_PADA_MAP[prefix]) {
          const [nIdx, rIdx, pada] = AVAKAHADA_PADA_MAP[prefix];
          return {
            nakIdx: nIdx,
            rashiIdx: rIdx,
            pada: pada,
            nakName: NAKSHATRA_NAMES[nIdx].split(" ")[1] || NAKSHATRA_NAMES[nIdx],
            rashiName: RASHI_NAMES[rIdx].split(" ")[1] || RASHI_NAMES[rIdx],
            syllable: prefix
          };
        }
      }
    }

    // English prefixes (length 5, 4, 3, 2, 1)
    for (const len of [5, 4, 3, 2, 1]) {
      if (lower.length >= len) {
        const prefix = lower.substring(0, len);
        if (AVAKAHADA_PADA_MAP[prefix]) {
          const [nIdx, rIdx, pada] = AVAKAHADA_PADA_MAP[prefix];
          return {
            nakIdx: nIdx,
            rashiIdx: rIdx,
            pada: pada,
            nakName: NAKSHATRA_NAMES[nIdx].split(" ")[1] || NAKSHATRA_NAMES[nIdx],
            rashiName: RASHI_NAMES[rIdx].split(" ")[1] || RASHI_NAMES[rIdx],
            syllable: prefix
          };
        }
      }
    }
    return null;
  }

  window.switchIndividualInputMode = function(mode) {
    const groupName = document.getElementById("groupIndivName");
    const nameInput = document.getElementById("muhurtaNativeName");
    const nakSelect = document.getElementById("muhurtamNativeNak");
    const rashiSelect = document.getElementById("muhurtamNativeRashi");
    const feedback = document.getElementById("indivNameFeedback");
    const btnName = document.getElementById("btnIndivModeName");
    const btnDirect = document.getElementById("btnIndivModeDirect");
    const btnGeneral = document.getElementById("btnIndivModeGeneral");

    [btnName, btnDirect, btnGeneral].forEach(b => { if (b) b.classList.remove("active"); });

    if (mode === "name") {
      if (btnName) btnName.classList.add("active");
      if (groupName) groupName.style.display = "block";
      if (nameInput) {
        nameInput.focus();
        if (nameInput.value) nameInput.dispatchEvent(new Event("input"));
      }
    } else if (mode === "direct") {
      if (btnDirect) btnDirect.classList.add("active");
      if (groupName) groupName.style.display = "block";
      if (feedback) feedback.style.display = "none";
    } else if (mode === "general") {
      if (btnGeneral) btnGeneral.classList.add("active");
      if (nakSelect) nakSelect.value = "";
      if (rashiSelect) rashiSelect.value = "";
      if (feedback) {
        feedback.innerHTML = `✨ <strong>కేవల పంచాంగ & అభిజిత్ శుద్ధి:</strong> సార్వత్రిక దోషరహిత శుభ లగ్నం, అమృత ఘడియలు మరియు సర్వదోషహర 'అభిజిత్ ముహూర్తం' ఆధారంగా గణింపబడుతుంది.`;
        feedback.style.color = "#8D4004";
        feedback.style.display = "block";
      }
    }
  };

  window.clearCoupleDetails = function(role) {
    if (role === "husband") {
      const nak = document.getElementById("muhurtaHusbandNak");
      const rashi = document.getElementById("muhurtaHusbandRashi");
      const fb = document.getElementById("husbandNameFeedback");
      if (nak) nak.value = "";
      if (rashi) rashi.value = "";
      if (fb) {
        fb.innerHTML = `✨ సాధారణ పంచాంగ శుద్ధి పరిశీలింపబడును`;
        fb.style.color = "#8D4004";
        fb.style.display = "block";
      }
    } else if (role === "wife") {
      const nak = document.getElementById("muhurtaWifeNak");
      const rashi = document.getElementById("muhurtaWifeRashi");
      const fb = document.getElementById("wifeNameFeedback");
      if (nak) nak.value = "";
      if (rashi) rashi.value = "";
      if (fb) {
        fb.innerHTML = `✨ సాధారణ పంచాంగ శుద్ధి పరిశీలింపబడును`;
        fb.style.color = "#8D4004";
        fb.style.display = "block";
      }
    }
  };

  // Real-time name input listeners for Individual, Husband, Wife
  const indivNameInput = document.getElementById("muhurtaNativeName");
  if (indivNameInput) {
    indivNameInput.addEventListener("input", () => {
      const val = indivNameInput.value;
      const feedback = document.getElementById("indivNameFeedback");
      const nakSelect = document.getElementById("muhurtamNativeNak");
      const rashiSelect = document.getElementById("muhurtamNativeRashi");

      const match = detectAvakahadaFromName(val);
      if (match && feedback) {
        feedback.innerHTML = `✨ నామాక్షరం: "<strong>${match.syllable}</strong>" ➔ నామ నక్షత్రం: <strong>${match.nakName}</strong> (${match.pada}వ పాదం) • నామ రాశి: <strong>${match.rashiName}</strong>`;
        feedback.style.color = "#2E7D32";
        feedback.style.display = "block";
        if (nakSelect) nakSelect.value = String(match.nakIdx);
        if (rashiSelect) rashiSelect.value = String(match.rashiIdx);
      } else if (feedback && val.trim().length > 0) {
        feedback.innerHTML = `ℹ️ నామాక్షరం సరిపోలలేదు. దయచేసి క్రింది డ్రాప్‌డౌన్ల నుండి నక్షత్రం ఎంచుకోండి లేదా సాధారణ పంచాంగ శుద్ధిని వాడండి.`;
        feedback.style.color = "#8D4004";
        feedback.style.display = "block";
      } else if (feedback) {
        feedback.style.display = "none";
      }
    });
  }

  const hNameInput = document.getElementById("muhurtaHusbandName");
  if (hNameInput) {
    hNameInput.addEventListener("input", () => {
      const val = hNameInput.value;
      const fb = document.getElementById("husbandNameFeedback");
      const nak = document.getElementById("muhurtaHusbandNak");
      const rashi = document.getElementById("muhurtaHusbandRashi");
      const match = detectAvakahadaFromName(val);
      if (match && fb) {
        fb.innerHTML = `✨ నామాక్షరం: "<strong>${match.syllable}</strong>" ➔ ${match.nakName} (${match.rashiName})`;
        fb.style.color = "#2E7D32";
        fb.style.display = "block";
        if (nak) nak.value = String(match.nakIdx);
        if (rashi) rashi.value = String(match.rashiIdx);
      } else if (fb) {
        fb.style.display = "none";
      }
    });
  }

  const wNameInput = document.getElementById("muhurtaWifeName");
  if (wNameInput) {
    wNameInput.addEventListener("input", () => {
      const val = wNameInput.value;
      const fb = document.getElementById("wifeNameFeedback");
      const nak = document.getElementById("muhurtaWifeNak");
      const rashi = document.getElementById("muhurtaWifeRashi");
      const match = detectAvakahadaFromName(val);
      if (match && fb) {
        fb.innerHTML = `✨ నామాక్షరం: "<strong>${match.syllable}</strong>" ➔ ${match.nakName} (${match.rashiName})`;
        fb.style.color = "#2E7D32";
        fb.style.display = "block";
        if (nak) nak.value = String(match.nakIdx);
        if (rashi) rashi.value = String(match.rashiIdx);
      } else if (fb) {
        fb.style.display = "none";
      }
    });
  }

  // 5. Form submit listener
  const form = document.getElementById("muhurtamForm");
  const resultContainer = document.getElementById("muhurtamResultContainer");
  if (form && resultContainer) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const submitBtn = document.getElementById("btnSubmitMuhurtam");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span>⏳</span> ముహూర్తాలు లెక్కింపబడుతున్నాయి...`;
      }

      resultContainer.style.display = "block";
      resultContainer.innerHTML = `
        <div style="text-align: center; padding: 40px 20px; background: #FFF; border-radius: 10px; border: 1px solid #EADBCE;">
          <div class="spinner" style="margin: 0 auto 15px auto;"></div>
          <h4 style="color: #4A0E17; margin: 0;">స్విస్ ఎఫెమెరిస్ ఖగోళ నిశిత ముహూర్త గణితం జరుగుతున్నది...</h4>
          <p style="color: #666; margin: 6px 0 0 0; font-size: 0.95rem;">రాహుకాలం, యమగండం, వర్జ్యం, అభిజిత్ ముహూర్తం, మరియు తారా/చంద్రబలాలు పరిశీలించబడుతున్నాయి...</p>
        </div>
      `;

      const mode = (modeInput ? modeInput.value : "individual") || "individual";
      let familyMembers = null;
      let primaryNak = null;
      let primaryRashi = null;

      if (mode === "individual") {
        const nakVal = document.getElementById("muhurtamNativeNak").value;
        const rashiVal = document.getElementById("muhurtamNativeRashi").value;
        primaryNak = nakVal !== "" ? parseInt(nakVal, 10) : null;
        primaryRashi = rashiVal !== "" ? parseInt(rashiVal, 10) : null;
      } else if (mode === "couple") {
        const hName = document.getElementById("muhurtaHusbandName")?.value || document.getElementById("coupleHusbandName")?.value || "భర్త (Husband)";
        const hNakVal = document.getElementById("muhurtaHusbandNak")?.value || document.getElementById("coupleHusbandNak")?.value;
        const hRashiVal = document.getElementById("muhurtaHusbandRashi")?.value || document.getElementById("coupleHusbandRashi")?.value;

        const wName = document.getElementById("muhurtaWifeName")?.value || document.getElementById("coupleWifeName")?.value || "భార్య (Wife)";
        const wNakVal = document.getElementById("muhurtaWifeNak")?.value || document.getElementById("coupleWifeNak")?.value;
        const wRashiVal = document.getElementById("muhurtaWifeRashi")?.value || document.getElementById("coupleWifeRashi")?.value;

        const hNak = hNakVal !== "" && hNakVal !== undefined && hNakVal !== null ? parseInt(hNakVal, 10) : null;
        const hRashi = hRashiVal !== "" && hRashiVal !== undefined && hRashiVal !== null ? parseInt(hRashiVal, 10) : null;
        const wNak = wNakVal !== "" && wNakVal !== undefined && wNakVal !== null ? parseInt(wNakVal, 10) : null;
        const wRashi = wRashiVal !== "" && wRashiVal !== undefined && wRashiVal !== null ? parseInt(wRashiVal, 10) : null;

        familyMembers = [
          { name: hName, role: "husband", nakshatra_index: hNak, rashi_index: hRashi },
          { name: wName, role: "wife", nakshatra_index: wNak, rashi_index: wRashi }
        ];
        primaryNak = hNak;
        primaryRashi = hRashi;
      } else if (mode === "family") {
        familyMembers = window.familyMembersData.map(m => ({
          name: m.name || "కుటుంబ సభ్యుడు",
          role: m.role || "member",
          nakshatra_index: m.nakshatra_index !== "" && m.nakshatra_index !== undefined ? parseInt(m.nakshatra_index, 10) : null,
          rashi_index: m.rashi_index !== "" && m.rashi_index !== undefined ? parseInt(m.rashi_index, 10) : null
        }));
        if (familyMembers.length > 0) {
          primaryNak = familyMembers[0].nakshatra_index;
          primaryRashi = familyMembers[0].rashi_index;
        }
      }

      const payload = {
        event_type: document.getElementById("muhurtamEventType").value,
        start_date: document.getElementById("muhurtamStartDate").value,
        days_range: parseInt(document.getElementById("muhurtamDaysRange").value, 10),
        latitude: parseFloat(document.getElementById("muhurtamLat").value) || 17.3850,
        longitude: parseFloat(document.getElementById("muhurtamLon").value) || 78.4867,
        timezone_offset: parseFloat(document.getElementById("muhurtamTz").value) || 5.5,
        native_nakshatra_index: primaryNak,
        native_rashi_index: primaryRashi,
        participant_mode: mode,
        family_members: familyMembers,
        limit: 8
      };

      try {
        const resp = await fetch("/api/v1/muhurtam/calculate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (!resp.ok) {
          const errData = await resp.json().catch(() => ({}));
          throw new Error(errData.detail || "ముహూర్త నిర్ణయంలో లోపం ఏర్పడింది.");
        }

        const resData = await resp.json();
        renderMuhurtamResults(resData.data);
      } catch (err) {
        resultContainer.innerHTML = `
          <div class="alert-guidance" style="background: #FFEBEE; border: 1px solid #FFCDD2; color: #B71C1C; padding: 20px; border-radius: 8px;">
            <h4 style="margin: 0 0 8px 0;">⚠️ ముహూర్త గణనలో లోపం ఏర్పడింది</h4>
            <p style="margin: 0;">${err.message || 'దయచేసి వివరాలను పరిశీలించి తిరిగి ప్రయత్నించండి.'}</p>
          </div>
        `;
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>⏱️</span> అత్యుత్తమ శుభ ముహూర్తాలను గణించండి (Calculate Optimal Muhurtams)`;
        }
      }
    });
  }
}

function renderMuhurtamResults(data) {
  const container = document.getElementById("muhurtamResultContainer");
  if (!container || !data) return;

  window.currentMuhurtaData = data;
  const picks = data.top_muhurtams || [];
  const isGeneralPanchanga = (data.native_nakshatra_index === null || data.native_nakshatra_index === undefined) && !data.is_family_mode;

  let candidatesHtml = "";
  if (picks.length === 0) {
    candidatesHtml = `
      <div style="background: #FFF; border: 1px solid #FFE082; padding: 20px; border-radius: 8px; text-align: center; color: #8D6E63;">
        ఈ కాల వ్యవధిలో నిర్దిష్ట నిబంధనలను పూర్తిస్థాయిలో సంతృప్తిపరిచే ముహూర్తాలు లభించలేదు. దయచేసి రోజుల పరిధిని పెంచండి (ఉదా: 60 లేదా 90 రోజులు).
      </div>
    `;
  } else {
    candidatesHtml = picks.map((m, idx) => {
      const badgeClass = m.badge === "success" ? "dignity-exalted" : (m.badge === "info" ? "dignity-friend" : "dignity-own");
      const cardBorder = m.badge === "success" ? "#4CAF50" : (m.badge === "info" ? "#2196F3" : "#FF9800");

      return `
        <div class="muhurtam-slot-card" style="background: #FFF; border: 1px solid #E0E0E0; border-left: 6px solid ${cardBorder}; border-radius: 10px; padding: 18px 20px; margin-bottom: 18px; box-shadow: 0 3px 10px rgba(0,0,0,0.04);">
          
          <!-- Card Header -->
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; border-bottom: 1px solid #F0F0F0; padding-bottom: 10px;">
            <div>
              <span style="background: #FAF5EB; color: #4A0E17; font-weight: 800; font-size: 0.85rem; padding: 4px 10px; border-radius: 4px; margin-right: 8px;">
                ర్యాంక్ #${idx + 1}
              </span>
              <strong style="font-size: 1.25rem; color: #2B2118;">
                📅 ${m.formatted_date} (${m.weekday_te})
              </strong>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="dignity-tag ${badgeClass}" style="font-size: 0.9rem; font-weight: bold;">
                ${m.classification} (స్కోరు: ${m.score})
              </span>
            </div>
          </div>

          <!-- Highlighted Best Window -->
          <div style="background: linear-gradient(135deg, #FFFDF0, #FFF8E1); border: 2px dashed #FFB300; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px; display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 2rem;">🌟</span>
            <div>
              <div style="font-size: 0.85rem; color: #996515; font-weight: 700; text-transform: uppercase;">
                ${m.best_window_label || 'ప్రశస్త ముహూర్త సమయం (Optimal Window)'}
              </div>
              <div style="font-size: 1.3rem; font-weight: 800; color: #B71C1C;">
                ${m.best_window}
              </div>
            </div>
          </div>

          <!-- Muhurta Lagna & Ashtama Shuddhi -->
          ${m.muhurta_lagna ? `
            <div style="background: linear-gradient(135deg, #F1F8E9, #E8F5E9); border: 1.5px solid #81C784; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.8rem;">🏛️</span>
                <div>
                  <div style="font-size: 0.82rem; color: #2E7D32; font-weight: 700; text-transform: uppercase;">
                    ముహూర్త లగ్నం & స్వభావం (Muhurta Lagna)
                  </div>
                  <div style="font-size: 1.15rem; font-weight: 800; color: #1B5E20;">
                    ${m.muhurta_lagna.rashi_name_te} (${m.muhurta_lagna.degree_formatted})
                    <span style="font-size: 0.82rem; font-weight: 700; color: #2E7D32; background: #C8E6C9; padding: 2px 8px; border-radius: 12px; margin-left: 6px;">
                      ${m.muhurta_lagna.nature_te}
                    </span>
                  </div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 6px;">
                <span class="dignity-tag ${m.muhurta_lagna.has_ashtama_shuddhi ? 'dignity-exalted' : 'dignity-debilitated'}" style="font-size: 0.86rem; font-weight: 700; padding: 5px 12px; border-radius: 20px;">
                  🛡️ ${m.muhurta_lagna.ashtama_shuddhi_desc}
                </span>
              </div>
            </div>
          ` : ''}

          <!-- Panchanga Details Grid -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; font-size: 0.93rem; margin-bottom: 14px; background: #FAFAFA; padding: 12px; border-radius: 6px;">
            <div>📜 తిథి: <strong>${m.tithi}</strong></div>
            <div>✨ నక్షత్రం: <strong>${m.nakshatra}</strong></div>
            <div>🌙 చంద్ర రాశి: <strong>${m.moon_rashi}</strong></div>
            <div>☀️ సూర్యోదయం: <strong>${m.sunrise}</strong></div>
            <div>🌅 సూర్యాస్తమయం: <strong>${m.sunset}</strong></div>
            <div>✨ అమృత కాలం: <strong>${m.amrita_kalam}</strong></div>
          </div>

          <!-- Inauspicious Avoidance Windows -->
          <div style="font-size: 0.88rem; color: #C62828; background: #FFEBEE; border: 1px solid #FFCDD2; padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 16px;">
            <span>🚫 రాహుకాలం: <strong>${m.rahu_kalam}</strong></span>
            <span>🚫 యమగండం: <strong>${m.yamagandam}</strong></span>
            <span>🚫 వర్జ్యం (విష ఘడియలు): <strong>${m.varjyam}</strong></span>
          </div>

          <!-- Joint Family / Couple Breakdown OR Single Native Tara & Chandra Bala -->
          ${m.family_compatibility && Array.isArray(m.family_compatibility.members) && m.family_compatibility.members.length > 0 ? `
            <div style="background: #FAFAFA; border: 1px solid #E0E0E0; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
                <div style="font-weight: 700; color: #4A0E17; font-size: 0.95rem; display: flex; align-items: center; gap: 6px;">
                  <span>👥</span> ${m.family_compatibility.members.length === 2 ? 'దంపతుల తారా-చంద్రబల సమన్వయం (Couple Harmony)' : 'కుటుంబ సభ్యుల సమగ్ర తారా-చంద్రబల పరిశీలన (Family Harmony)'}
                </div>
                <span class="dignity-tag ${m.family_compatibility.badge === 'success' ? 'dignity-exalted' : (m.family_compatibility.badge === 'danger' ? 'dignity-debilitated' : 'dignity-own')}" style="font-size: 0.85rem; font-weight: bold;">
                  ${m.family_compatibility.status_te}
                </span>
              </div>

              ${m.family_compatibility.has_ashtama_chandra ? `
                <div style="background: #FFEBEE; border: 1px solid #FFCDD2; color: #B71C1C; padding: 8px 12px; border-radius: 6px; font-size: 0.88rem; font-weight: 600; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                  <span>⚠️</span> శాస్త్ర నిషేధం: ఈ ముహూర్తంలో అష్టమ చంద్ర దోషం ఉన్నందున ఈ సమయంలో కార్యక్రమం జరపరాదు (*కాలామృతమ్*).
                </div>
              ` : ''}

              <div class="table-responsive">
                <table class="vedic-table" style="width: 100%; font-size: 0.86rem; background: #FFF;">
                  <thead>
                    <tr style="background: #F5F5F5;">
                      <th>సభ్యుడు (Member)</th>
                      <th>నక్షత్రం & తారాబలం</th>
                      <th>రాశి & చంద్రబలం</th>
                      <th style="text-align: center;">ఫలితం</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${m.family_compatibility.members.map(mem => `
                      <tr style="${mem.is_ashtama_chandra || mem.is_naidhana_tara ? 'background: #FFF5F5;' : ''}">
                        <td><strong>${mem.name}</strong></td>
                        <td>
                          ${mem.nakshatra_name} ➔ 
                          <span style="color: ${mem.tara_favorable ? '#2E7D32' : '#C62828'}; font-weight: 600;">
                            ${mem.tara_name} ${mem.tara_favorable ? '✅' : '🚫'}
                          </span>
                        </td>
                        <td>
                          ${mem.rashi_name} ➔ 
                          <span style="color: ${mem.chandra_favorable ? '#2E7D32' : '#C62828'}; font-weight: 600;">
                            ${mem.chandra_status} ${mem.chandra_favorable ? '✅' : (mem.is_ashtama_chandra ? '🔴' : '⚠️')}
                          </span>
                        </td>
                        <td style="text-align: center;">
                          ${mem.favorable_overall ? 
                            '<span style="background: #E8F5E9; color: #2E7D32; font-weight: 700; padding: 2px 8px; border-radius: 4px;">శుభకరం ✅</span>' : 
                            '<span style="background: #FFEBEE; color: #C62828; font-weight: 700; padding: 2px 8px; border-radius: 4px;">ప్రతికూలం ❌</span>'
                          }
                        </td>
                      </tr>
                    `).join("")}
                  </tbody>
                </table>
              </div>
            </div>
          ` : `
            <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
              <div style="background: ${m.tara_favorable ? '#E8F5E9' : '#FFF3E0'}; border: 1px solid ${m.tara_favorable ? '#A5D6A7' : '#FFE0B2'}; border-radius: 6px; padding: 6px 12px; font-size: 0.9rem;">
                <strong>🎯 జన్మ తారాబలం:</strong> <span style="color: ${m.tara_favorable ? '#2E7D32' : '#E65100'}; font-weight: 700;">${m.tara_bala}</span>
              </div>
              <div style="background: ${m.chandra_favorable ? '#E8F5E9' : '#FFEBEE'}; border: 1px solid ${m.chandra_favorable ? '#A5D6A7' : '#FFCDD2'}; border-radius: 6px; padding: 6px 12px; font-size: 0.9rem;">
                <strong>🌙 చంద్రబలం:</strong> <span style="color: ${m.chandra_favorable ? '#2E7D32' : '#C62828'}; font-weight: 700;">${m.chandra_bala}</span>
              </div>
              ${m.shiva_vasa ? `
                <div style="background: ${m.shiva_vasa.favorable ? '#E8F5E9' : '#FFF3E0'}; border: 1px solid #DDD; border-radius: 6px; padding: 6px 12px; font-size: 0.9rem;">
                  <strong>🔱 శివ వాసం:</strong> <span style="font-weight: 700;">${m.shiva_vasa.place} (${m.shiva_vasa.impact})</span>
                </div>
              ` : ''}
              ${m.agni_vasa ? `
                <div style="background: ${m.agni_vasa.favorable ? '#E8F5E9' : '#FFF3E0'}; border: 1px solid #DDD; border-radius: 6px; padding: 6px 12px; font-size: 0.9rem;">
                  <strong>🔥 అగ్ని వాసం:</strong> <span style="font-weight: 700;">${m.agni_vasa.place}</span>
                </div>
              ` : ''}
            </div>
          `}

          <!-- Reasons Checklist -->
          ${Array.isArray(m.reasons) && m.reasons.length > 0 ? `
            <div style="font-size: 0.88rem; color: #2E7D32; line-height: 1.5;">
              <strong>✅ శాస్త్రోక్త అనుకూలతలు:</strong> ${m.reasons.join(" • ")}
            </div>
          ` : ''}

        </div>
      `;
    }).join("");
  }

  container.innerHTML = `
    <!-- Top Action Bar for Priests & Clients: Print Patrika & Share WhatsApp -->
    <div style="display: flex; justify-content: flex-end; gap: 10px; margin-bottom: 14px; flex-wrap: wrap;">
      <button type="button" class="btn-submit" onclick="window.printMuhurtaPatrika()" style="padding: 8px 18px; font-size: 0.92rem; border-radius: 6px; background: linear-gradient(135deg, #4A0E17, #780016); color: white; border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; font-weight: 700; box-shadow: 0 2px 6px rgba(74,14,23,0.25);">
        <span>🖨️</span> ముహూర్త పత్రిక ముద్రణ (Print Patrika)
      </button>
      <button type="button" class="btn-submit" id="btnCopyWhatsApp" onclick="window.copyMuhurtaToWhatsApp()" style="padding: 8px 18px; font-size: 0.92rem; border-radius: 6px; background: linear-gradient(135deg, #1B5E20, #2E7D32); color: white; border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; font-weight: 700; box-shadow: 0 2px 6px rgba(27,94,32,0.25);">
        <span>📋</span> వాట్సాప్ సందేశం కాపీ (Copy WhatsApp)
      </button>
    </div>

    <!-- Event Banner -->
    <div style="background: #FAF5EB; border: 1px solid #EADBCE; border-radius: 10px; padding: 18px 20px; margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 8px;">
        <h3 style="color: #4A0E17; font-size: 1.35rem; margin: 0; display: flex; align-items: center; gap: 8px;">
          <span>⏱️</span> ${data.event_title_te}
        </h3>
        <span class="dignity-tag dignity-exalted" style="font-size: 0.85rem;">
          పరిశీలన వ్యవధి: ${data.search_period}
        </span>
      </div>
      <p style="color: #4A0E17; font-size: 1rem; margin: 0 0 10px 0; line-height: 1.6;">${data.description}</p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; font-size: 0.9rem; background: #FFF; padding: 10px 14px; border-radius: 6px; border: 1px solid #EADBCE;">
        <div><span>📜 <strong>ప్రామాణిక శాస్త్ర గ్రంథం:</strong></span> ${data.shastra_source}</div>
        <div><span>⚖️ <strong>శాస్త్ర నియమం:</strong></span> ${data.rule_note}</div>
      </div>

      ${isGeneralPanchanga ? `
        <div style="background: linear-gradient(135deg, #FFF9E6, #FFF3E0); border: 1.5px solid #FFE082; border-left: 6px solid #FF8F00; border-radius: 8px; padding: 12px 16px; margin-top: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <div>
            <div style="font-weight: 800; color: #8D4004; font-size: 0.98rem; display: flex; align-items: center; gap: 6px;">
              <span>☀️</span> సార్వత్రిక పంచాంగ & అభిజిత్ శుద్ధి ముహూర్తం (Universal Panchanga Shuddhi)
            </div>
            <div style="font-size: 0.88rem; color: #5D4037; margin-top: 4px;">
              జాతక వివరాలు (DOB/TOB) అవసరం లేకుండానే — సర్వదోషహర <strong>అభిజిత్ ముహూర్తం</strong>, అమృత ఘడియలు మరియు శుభ తిథి-వార-నక్షత్ర శుద్ధి ఆధారంగా గణింపబడినది.
            </div>
          </div>
          <span class="dignity-tag dignity-exalted" style="font-size: 0.82rem; font-weight: 700;">సార్వత్రిక శుభప్రదం</span>
        </div>
      ` : ''}

      ${data.is_family_mode ? `
        <div style="margin-top: 10px; background: #E8F5E9; border: 1px solid #A5D6A7; padding: 8px 12px; border-radius: 6px; color: #1B5E20; font-size: 0.92rem; font-weight: 600; display: flex; align-items: center; gap: 8px;">
          <span>👨‍👩‍👧‍👦</span> <strong>పరిశీలన విధానం:</strong> ${data.participants_count} మంది కుటుంబ సభ్యుల/దంపతుల ఉమ్మడి సమన్వయం (అందరికీ అష్టమ చంద్ర దోష రాహిత్యం & తారాబల సమగ్ర గణన).
        </div>
      ` : ''}
    </div>

    <!-- Candidates Header -->
    <h3 class="card-title" style="margin-bottom: 15px;">
      <span>🏆</span> గణించబడిన అత్యుత్తమ శుభ ముహూర్తాల పట్టిక (Ranked Auspicious Slots)
    </h3>

    <!-- Candidates List -->
    <div>
      ${candidatesHtml}
    </div>
  `;

  // Apply transliteration if active
  if (typeof applyTransliterationToPage === "function") {
    applyTransliterationToPage(container);
  }
}

window.printMuhurtaPatrika = function() {
  const data = window.currentMuhurtaData;
  if (!data || !data.top_muhurtams || data.top_muhurtams.length === 0) {
    alert("ముద్రించడానికి ముహూర్త ఫలితాలు అందుబాటులో లేవు.");
    return;
  }
  const place = document.getElementById("muhurtamPlace")?.value.trim() || "హైదరాబాద్";
  const indivName = document.getElementById("muhurtaNativeName")?.value.trim() || "";
  const hName = document.getElementById("muhurtaHusbandName")?.value.trim() || "";
  const wName = document.getElementById("muhurtaWifeName")?.value.trim() || "";
  const mode = document.getElementById("muhurtamParticipantMode")?.value || "individual";

  let clientInfo = "";
  if (mode === "individual" && indivName) {
    clientInfo = `సంకల్ప కర్త: <strong>${indivName}</strong>`;
  } else if (mode === "couple" && (hName || wName)) {
    clientInfo = `సంకల్ప దంపతులు: <strong>${hName || 'భర్త'}</strong> మరియు <strong>${wName || 'భార్య'}</strong>`;
  }

  const printWindow = window.open("", "_blank", "width=850,height=900");
  if (!printWindow) {
    alert("దయచేసి మీ బ్రౌజర్‌లో పాప్-అప్‌లను అనుమతించండి.");
    return;
  }

  const slotsHtml = data.top_muhurtams.map((m, idx) => `
    <div style="border: 1.5px solid #8D4004; border-radius: 8px; padding: 14px; margin-bottom: 14px; page-break-inside: avoid; background: #FFFDF9;">
      <div style="display: flex; justify-content: space-between; border-bottom: 1.5px solid #C49A45; padding-bottom: 6px; margin-bottom: 8px;">
        <span style="font-weight: 800; font-size: 1.15rem; color: #780016;">శుభ ముహూర్తం #${idx + 1}: ${m.formatted_date} (${m.weekday_te})</span>
        <span style="font-weight: 700; color: #1B5E20; font-size: 1rem;">${m.classification} (స్కోరు: ${m.score})</span>
      </div>
      <div style="background: #FFF8E1; border: 1px solid #FFE082; padding: 8px 12px; border-radius: 6px; margin-bottom: 10px; font-size: 1.05rem;">
        <strong style="color: #B71C1C;">🌟 ప్రశస్త ముహూర్త సమయం:</strong> <span style="font-size: 1.15rem; font-weight: 800; color: #4A0E17;">${m.best_window}</span>
      </div>
      ${m.muhurta_lagna ? `
        <div style="font-size: 0.95rem; margin-bottom: 8px; color: #1B5E20;">
          <strong>🏛️ ముహూర్త లగ్నం:</strong> ${m.muhurta_lagna.rashi_name_te} (${m.muhurta_lagna.degree_formatted}) — ${m.muhurta_lagna.nature_te} | <strong>అష్టమ శుద్ధి:</strong> ${m.muhurta_lagna.ashtama_shuddhi_desc}
        </div>
      ` : ''}
      <table style="width: 100%; border-collapse: collapse; font-size: 0.92rem; margin-bottom: 8px;">
        <tr>
          <td style="padding: 4px 8px; border: 1px solid #E0E0E0;"><strong>తిథి:</strong> ${m.tithi}</td>
          <td style="padding: 4px 8px; border: 1px solid #E0E0E0;"><strong>నక్షత్రం:</strong> ${m.nakshatra}</td>
          <td style="padding: 4px 8px; border: 1px solid #E0E0E0;"><strong>చంద్ర రాశి:</strong> ${m.moon_rashi}</td>
        </tr>
        <tr>
          <td style="padding: 4px 8px; border: 1px solid #E0E0E0;"><strong>సూర్యోదయం:</strong> ${m.sunrise}</td>
          <td style="padding: 4px 8px; border: 1px solid #E0E0E0;"><strong>సూర్యాస్తమయం:</strong> ${m.sunset}</td>
          <td style="padding: 4px 8px; border: 1px solid #E0E0E0;"><strong>అమృత కాలం:</strong> ${m.amrita_kalam}</td>
        </tr>
      </table>
      <div style="font-size: 0.88rem; color: #8D4004; background: #FFF3E0; padding: 6px 10px; border-radius: 4px;">
        <strong>వర్జిత సమయాలు (పరిత్యజించవలసినవి):</strong> రాహుకాలం: ${m.rahu_kalam} | యమగండం: ${m.yamagandam} | వర్జ్యం: ${m.varjyam}
      </div>
    </div>
  `).join("");

  printWindow.document.write(`
    <!DOCTYPE html>
    <html lang="te">
    <head>
      <meta charset="UTF-8">
      <title>శుభ ముహూర్త పత్రిక - ${data.event_title_te}</title>
      <style>
        body { font-family: 'Noto Sans Telugu', 'Gautami', 'Segoe UI', Tahoma, sans-serif; margin: 25px; color: #2B2118; line-height: 1.5; background: #fff; }
        .header { text-align: center; border-bottom: 3px double #780016; padding-bottom: 12px; margin-bottom: 18px; }
        .mangala { font-size: 1.15rem; font-weight: 700; color: #780016; margin-bottom: 4px; }
        .title { font-size: 1.5rem; font-weight: 800; color: #4A0E17; margin: 4px 0; }
        .sub { font-size: 0.95rem; color: #5D4037; }
        .footer { margin-top: 25px; border-top: 1.5px solid #C49A45; padding-top: 12px; display: flex; justify-content: space-between; font-size: 0.9rem; }
        @media print {
          body { margin: 15mm; }
          .no-print { display: none; }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="mangala">🕉️ శ్రీ గురుభ్యోనమః • శ్రీరస్తు శుభమస్తు అవిఘ్నమస్తు 🕉️</div>
        <div class="title">శ్రీ వైదిక శుభ ముహూర్త పత్రిక</div>
        <div class="sub"><strong>కార్యం:</strong> ${data.event_title_te} | <strong>స్థలం:</strong> ${place} ${clientInfo ? ' | ' + clientInfo : ''}</div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 4px;">శాస్త్ర ప్రమాణం: ${data.shastra_source} | ${data.rule_note}</div>
      </div>
      <div class="no-print" style="text-align: right; margin-bottom: 12px;">
        <button onclick="window.print()" style="padding: 8px 18px; font-size: 1rem; font-weight: bold; background: #780016; color: white; border: none; border-radius: 6px; cursor: pointer;">🖨️ ముద్రించండి (Print)</button>
      </div>
      ${slotsHtml}
      <div class="footer">
        <div><strong>సిద్ధాంతం:</strong> సూర్యసిద్ధాంత & స్విస్ ఎఫెమెరిస్ ఖగోళ శుద్ధి</div>
        <div style="text-align: right;"><strong>ఆశీర్వచనం:</strong> సర్వేజనాః సుఖినోభవంతు • శుభం భూయాత్ 🙏</div>
      </div>
    </body>
    </html>
  `);
  printWindow.document.close();
};

window.copyMuhurtaToWhatsApp = function() {
  const data = window.currentMuhurtaData;
  if (!data || !data.top_muhurtams || data.top_muhurtams.length === 0) {
    alert("కాపీ చేయడానికి ముహూర్త ఫలితాలు అందుబాటులో లేవు.");
    return;
  }
  const place = document.getElementById("muhurtamPlace")?.value.trim() || "హైదరాబాద్";
  const indivName = document.getElementById("muhurtaNativeName")?.value.trim() || "";
  const hName = document.getElementById("muhurtaHusbandName")?.value.trim() || "";
  const wName = document.getElementById("muhurtaWifeName")?.value.trim() || "";
  const mode = document.getElementById("muhurtamParticipantMode")?.value || "individual";

  let clientStr = "";
  if (mode === "individual" && indivName) clientStr = `\n👤 సంకల్పం: ${indivName}`;
  else if (mode === "couple" && (hName || wName)) clientStr = `\n👥 దంపతులు: ${hName || 'భర్త'} & ${wName || 'భార్య'}`;

  let text = `🕉️ *శ్రీరస్తు - శుభమస్తు* 🕉️\n✨ *శుభ ముహూర్త పత్రిక (Vedic Muhurtam)* ✨\n🎯 కార్యం: *${data.event_title_te}*\n📍 స్థలం: *${place}*${clientStr}\n\n`;

  data.top_muhurtams.slice(0, 3).forEach((m, idx) => {
    text += `*ముహూర్తం #${idx + 1}* (${m.classification}):\n`;
    text += `📅 తేది: *${m.formatted_date} (${m.weekday_te})*\n`;
    text += `⏰ ప్రశస్త సమయం: *${m.best_window}*\n`;
    if (m.muhurta_lagna) {
      text += `🏛️ లగ్నం: *${m.muhurta_lagna.rashi_name_te}* (${m.muhurta_lagna.nature_te})\n`;
    }
    text += `📜 తిథి: ${m.tithi} | నక్షత్రం: ${m.nakshatra}\n`;
    text += `✨ అమృత ఘడియలు: ${m.amrita_kalam}\n`;
    text += `🚫 రాహుకాలం: ${m.rahu_kalam} (పరిహరించబడింది)\n\n`;
  });

  text += `📖 శాస్త్ర ప్రమాణం: ${data.shastra_source}\nసర్వేజనాః సుఖినోభవంతు • శుభం భూయాత్ 🙏`;

  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById("btnCopyWhatsApp");
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = `<span>✅</span> వాట్సాప్ సందేశం కాపీ అయింది!`;
      setTimeout(() => { btn.innerHTML = orig; }, 3000);
    } else {
      alert("ముహూర్త వివరాలు వాట్సాప్ కొరకు కాపీ చేయబడ్డాయి! ✅");
    }
  }).catch(() => {
    alert("క్లిప్‌బోర్డ్‌కు కాపీ చేయడంలో లోపం. దయచేసి వివరాలను మాన్యువల్‌గా కాపీ చేసుకోండి.");
  });
};

// 1-Click Launch from Santana Dosha Parihara card into Muhurtam Module
window.launchMuhurtamForRemedy = function(eventType, encodedRemedyName) {
  const remedyName = decodeURIComponent(encodedRemedyName || "");
  
  // 1. Switch to Muhurtam module
  const muhurtamNavBtn = document.querySelector('.global-nav-btn[data-module="moduleMuhurtam"]');
  if (muhurtamNavBtn) {
    muhurtamNavBtn.click();
  }

  // 2. Pre-select event type
  const eventSelect = document.getElementById("muhurtamEventType");
  if (eventSelect) {
    eventSelect.value = eventType;
    if (typeof window.updateMuhurtamEventContextCard === "function") {
      window.updateMuhurtamEventContextCard(eventType);
    }
  }

  // Refresh assistant recommendations
  if (typeof window.renderMuhurtamJatakamAssistant === "function") {
    window.renderMuhurtamJatakamAssistant();
  }

  // 3. For Santana / Garbhasrava / Vivaha remedies, switch to Couple mode
  const isCoupleEvent = ["santana_gopala", "kuja_shanti_subrahmanya", "naga_pratishtha", "vivaha"].includes(eventType);
  if (isCoupleEvent) {
    const coupleBtn = document.querySelector('.participant-mode-btn[data-mode="couple"]');
    if (coupleBtn) {
      coupleBtn.click();
    }
  }

  // 4. Pre-fill native nakshatra & rashi if available from current Kundali
  if (window.currentKundaliData && window.currentKundaliData.panchangam) {
    const p = window.currentKundaliData.panchangam;
    const nakSelect = document.getElementById("muhurtamNativeNak");
    const rashiSelect = document.getElementById("muhurtamNativeRashi");
    if (nakSelect && p.nakshatra_index !== undefined) {
      nakSelect.value = String(p.nakshatra_index);
    }
    if (rashiSelect && p.rashi_index !== undefined) {
      rashiSelect.value = String(p.rashi_index);
    }

    // Also prefill into Couple inputs
    const gender = window.currentKundaliData.birth_details?.gender || window.currentKundaliData.input?.gender || "male";
    const name = window.currentKundaliData.birth_details?.name || window.currentKundaliData.input?.name || "";
    const nakIdx = p.nakshatra_index !== undefined ? p.nakshatra_index : p.moon_nakshatra_index;
    const rashiIdx = p.janma_rashi_index !== undefined ? p.janma_rashi_index : p.rashi_index;

    if (gender === "male") {
      const hNak = document.getElementById("muhurtaHusbandNak") || document.getElementById("coupleHusbandNak");
      const hRashi = document.getElementById("muhurtaHusbandRashi") || document.getElementById("coupleHusbandRashi");
      const hName = document.getElementById("muhurtaHusbandName") || document.getElementById("coupleHusbandName");
      if (hNak && nakIdx !== undefined) hNak.value = String(nakIdx);
      if (hRashi && rashiIdx !== undefined) hRashi.value = String(rashiIdx);
      if (hName && name) hName.value = `${name} (భర్త)`;
    } else {
      const wNak = document.getElementById("muhurtaWifeNak") || document.getElementById("coupleWifeNak");
      const wRashi = document.getElementById("muhurtaWifeRashi") || document.getElementById("coupleWifeRashi");
      const wName = document.getElementById("muhurtaWifeName") || document.getElementById("coupleWifeName");
      if (wNak && nakIdx !== undefined) wNak.value = String(nakIdx);
      if (wRashi && rashiIdx !== undefined) wRashi.value = String(rashiIdx);
      if (wName && name) wName.value = `${name} (భార్య)`;
    }
  }

  // 5. Pre-fill place if available from Kundali inputs
  const placeInput = document.getElementById("placeInput");
  const latInput = document.getElementById("latInput");
  const lonInput = document.getElementById("lonInput");
  const tzInput = document.getElementById("tzInput");
  
  if (placeInput && placeInput.value) {
    const mPlace = document.getElementById("muhurtamPlace");
    const mLat = document.getElementById("muhurtamLat");
    const mLon = document.getElementById("muhurtamLon");
    const mTz = document.getElementById("muhurtamTz");
    const mFeed = document.getElementById("muhurtamCityFeedback");
    if (mPlace) mPlace.value = placeInput.value;
    if (mLat && latInput) mLat.value = latInput.value;
    if (mLon && lonInput) mLon.value = lonInput.value;
    if (mTz && tzInput) mTz.value = tzInput.value;
    if (mFeed) mFeed.innerHTML = `📍 ప్రదేశం: <strong>${placeInput.value}</strong>`;
  }

  // 6. Scroll smoothly to Muhurtam Assistant and submit form
  const assistantEl = document.getElementById("muhurtamJatakamDoshaAssistant");
  if (assistantEl) {
    assistantEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  const form = document.getElementById("muhurtamForm");
  if (form) {
    setTimeout(() => {
      form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
    }, 350);
  }
};

/* ========================================================================== */
/* COUPLE & FAMILY HOROSCOPE AUDIT FRONTEND LOGIC                             */
/* ========================================================================== */

window.currentAnalysisMode = "individual";
window.currentCoupleData = null;
window.currentFamilyData = null;

function initAnalysisModeToggle() {
  const btns = document.querySelectorAll(".analysis-mode-btn");
  const indFormWrap = document.getElementById("individualFormWrapper");
  const coupleFormWrap = document.getElementById("coupleFormWrapper");
  const famFormWrap = document.getElementById("familyFormWrapper");

  const indResults = document.getElementById("resultsContainer");
  const coupleResults = document.getElementById("coupleResultsContainer");
  const famResults = document.getElementById("familyResultsContainer");

  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      btns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const mode = btn.dataset.mode;
      window.currentAnalysisMode = mode;

      if (mode === "individual") {
        if (indFormWrap) indFormWrap.style.display = "block";
        if (coupleFormWrap) coupleFormWrap.style.display = "none";
        if (famFormWrap) famFormWrap.style.display = "none";

        if (indResults && window.currentKundaliData) indResults.style.display = "block";
        if (coupleResults) coupleResults.style.display = "none";
        if (famResults) famResults.style.display = "none";
      } else if (mode === "couple") {
        if (indFormWrap) indFormWrap.style.display = "none";
        if (coupleFormWrap) coupleFormWrap.style.display = "block";
        if (famFormWrap) famFormWrap.style.display = "none";

        if (indResults) indResults.style.display = "none";
        if (coupleResults && window.currentCoupleData) coupleResults.style.display = "block";
        if (famResults) famResults.style.display = "none";
      } else if (mode === "family") {
        if (indFormWrap) indFormWrap.style.display = "none";
        if (coupleFormWrap) coupleFormWrap.style.display = "none";
        if (famFormWrap) famFormWrap.style.display = "block";

        if (indResults) indResults.style.display = "none";
        if (coupleResults) coupleResults.style.display = "none";
        if (famResults && window.currentFamilyData) famResults.style.display = "block";
      }
    });
  });
}

function initCoupleModule() {
  setupCityAutocomplete("coupleHusbandPlace", "coupleHusbandCitySuggestions", "coupleHusbandLat", "coupleHusbandLon", "coupleHusbandTz", "coupleHusbandPlaceFeedback");
  setupCityAutocomplete("coupleWifePlace", "coupleWifeCitySuggestions", "coupleWifeLat", "coupleWifeLon", "coupleWifeTz", "coupleWifePlaceFeedback");

  const form = document.getElementById("coupleForm");
  const btn = document.getElementById("btnCoupleGenerate");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    await ensureCityResolved("coupleHusbandPlace", "coupleHusbandLat", "coupleHusbandLon", "coupleHusbandTz", "coupleHusbandPlaceFeedback");
    await ensureCityResolved("coupleWifePlace", "coupleWifeLat", "coupleWifeLon", "coupleWifeTz", "coupleWifePlaceFeedback");

    const hName = document.getElementById("coupleHusbandName").value.trim() || "భర్త";
    const hDob = document.getElementById("coupleHusbandDob").value;
    const hTob = document.getElementById("coupleHusbandTob").value;
    const hPlace = document.getElementById("coupleHusbandPlace").value;
    const hLat = parseFloat(document.getElementById("coupleHusbandLat").value) || 16.3067;
    const hLon = parseFloat(document.getElementById("coupleHusbandLon").value) || 80.4365;
    const hTz = parseFloat(document.getElementById("coupleHusbandTz").value) || 5.5;

    const wName = document.getElementById("coupleWifeName").value.trim() || "భార్య";
    const wDob = document.getElementById("coupleWifeDob").value;
    const wTob = document.getElementById("coupleWifeTob").value;
    const wPlace = document.getElementById("coupleWifePlace").value;
    const wLat = parseFloat(document.getElementById("coupleWifeLat").value) || 17.3850;
    const wLon = parseFloat(document.getElementById("coupleWifeLon").value) || 78.4867;
    const wTz = parseFloat(document.getElementById("coupleWifeTz").value) || 5.5;

    const focusArea = document.getElementById("coupleFocusSelect").value || "general";
    const ayanamsa = document.getElementById("coupleAyanamsaSelect").value || "lahiri";

    if (!hDob || !hTob || !wDob || !wTob) {
      alert("దయచేసి భర్త మరియు భార్య ఇద్దరి జన్మ తేదీ, సమయాలను నమోదు చేయండి.");
      return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> దంపతుల జాతక చక్రాలు గణితం చేయబడుతున్నాయి...`;

    try {
      const resp = await fetch("/api/v1/kundali/couple-analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          husband: {
            name: hName,
            gender: "male",
            dob: hDob,
            tob: hTob,
            place_name: hPlace,
            latitude: hLat,
            longitude: hLon,
            timezone_offset: hTz,
            ayanamsa: ayanamsa
          },
          wife: {
            name: wName,
            gender: "female",
            dob: wDob,
            tob: wTob,
            place_name: wPlace,
            latitude: wLat,
            longitude: wLon,
            timezone_offset: wTz,
            ayanamsa: ayanamsa
          },
          focus_area: focusArea
        })
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.detail || "దంపతుల జాతక విశ్లేషణలో లోపం ఏర్పడింది.");
      }

      const data = await resp.json();
      window.currentCoupleData = data;

      renderCoupleResults(data);

      const coupleResults = document.getElementById("coupleResultsContainer");
      if (coupleResults) {
        coupleResults.style.display = "block";
        coupleResults.scrollIntoView({ behavior: "smooth" });
      }
    } catch (err) {
      alert(err.message || "విశ్లేషణలో లోపం సంభవించింది.");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span>👫</span> దంపతుల సంయుక్త జాతక విశ్లేషణ & దోష నిర్ణయం (Analyze Couple Charts)`;
    }
  });
}

function renderCoupleResults(data) {
  const hk = data.husband_kundali;
  const wk = data.wife_kundali;
  const ja = data.joint_analysis;

  function extractRashiText(k) {
    if (!k) return "--";
    if (k.panchangam) {
      if (k.panchangam.janma_rashi) return k.panchangam.janma_rashi;
      if (k.panchangam.janma_rashi_te) return k.panchangam.janma_rashi_te;
      if (k.panchangam.rashi_name_te) return k.panchangam.rashi_name_te;
    }
    if (k.planets) {
      const moon = k.planets.find(p => p.name_en === "Moon" || p.name_te === "చంద్రుడు");
      if (moon && moon.rashi_name_te) return moon.rashi_name_te;
    }
    return "--";
  }

  function extractDashaText(k) {
    if (!k || !k.dasha) return "--";
    const currM = k.dasha.current_mahadasha;
    const currB = k.dasha.current_bhukti;
    if (currM && currB) {
      return `${currM.lord_te} దశ / ${currB.lord_te} భుక్తి`;
    }
    if (currM && currM.lord_te) {
      return `${currM.lord_te} మహాదశ`;
    }
    if (k.dasha.current_dasha && k.dasha.current_dasha.mahadasha_te) {
      return `${k.dasha.current_dasha.mahadasha_te} దశ`;
    }
    return "--";
  }

  // 1. Summary Hero Boxes
  const hNameEl = document.getElementById("coupleHusbandSummaryName");
  const hLagnaEl = document.getElementById("coupleHusbandLagna");
  const hRashiEl = document.getElementById("coupleHusbandRashi");
  const hNakEl = document.getElementById("coupleHusbandNakshatra");
  const hDashaEl = document.getElementById("coupleHusbandDasha");

  if (hNameEl) hNameEl.textContent = hk.input.name;
  if (hLagnaEl) hLagnaEl.textContent = hk.lagna.rashi_name_te;
  if (hRashiEl) hRashiEl.textContent = extractRashiText(hk);
  if (hNakEl) hNakEl.textContent = `${hk.panchangam.nakshatra} (${hk.panchangam.pada})`;
  if (hDashaEl) hDashaEl.textContent = extractDashaText(hk);

  const wNameEl = document.getElementById("coupleWifeSummaryName");
  const wLagnaEl = document.getElementById("coupleWifeLagna");
  const wRashiEl = document.getElementById("coupleWifeRashi");
  const wNakEl = document.getElementById("coupleWifeNakshatra");
  const wDashaEl = document.getElementById("coupleWifeDasha");

  if (wNameEl) wNameEl.textContent = wk.input.name;
  if (wLagnaEl) wLagnaEl.textContent = wk.lagna.rashi_name_te;
  if (wRashiEl) wRashiEl.textContent = extractRashiText(wk);
  if (wNakEl) wNakEl.textContent = `${wk.panchangam.nakshatra} (${wk.panchangam.pada})`;
  if (wDashaEl) wDashaEl.textContent = extractDashaText(wk);

  const kartaBadge = document.getElementById("coupleKartaBadge");
  if (kartaBadge) {
    kartaBadge.innerHTML = `🪔 సంకల్ప కర్త: <strong>${ja.primary_action_karta}</strong>`;
  }

  // 2. Santana Section
  const santanaEl = document.getElementById("coupleSantanaSection");
  if (santanaEl) {
    const sj = ja.santana_joint;
    const badgeCol = sj.badge === "success" ? "#1B5E20" : (sj.badge === "warning" ? "#E65100" : "#B71C1C");
    const badgeBg = sj.badge === "success" ? "#E8F5E9" : (sj.badge === "warning" ? "#FFF3E0" : "#FFEBEE");

    santanaEl.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; border-bottom: 1.5px solid rgba(212, 175, 55, 0.3); padding-bottom: 12px;">
        <h3 class="card-title" style="margin: 0;">
          <span>👶</span> సంతాన యోగం & బీజ-క్షేత్ర స్పష్ట విశ్లేషణ (Santana & Beeja/Kshetra Sphuta)
        </h3>
        <span class="dignity-tag" style="background: ${badgeBg}; color: ${badgeCol}; font-weight: 800; font-size: 0.95rem; padding: 6px 14px; border: 1px solid ${badgeCol};">
          ${sj.verdict}
        </span>
      </div>

      <!-- Verdict Box -->
      <div style="background: ${badgeBg}; border-left: 5px solid ${badgeCol}; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
        <div style="font-weight: 800; font-size: 1.1rem; color: ${badgeCol}; margin-bottom: 4px;">
          🎯 దోష నిర్ధారణ: ${sj.who_carries_dosha}
        </div>
        <p style="margin: 0; color: #2B2118; font-size: 0.95rem; line-height: 1.7;">
          ${sj.description}
        </p>
      </div>

      <!-- Side by Side Sphutas -->
      <div class="side-by-side-sphutas">
        
        <!-- Husband Beeja Sphuta -->
        <div class="sphuta-box">
          <div class="sphuta-box-header">
            <span>👨 భర్త బీజ స్పష్టం (Male Seed Virility)</span>
            <span class="dignity-tag dignity-${sj.husband_beeja.badge}">${sj.husband_beeja.status}</span>
          </div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #4A0E17; margin: 8px 0;">
            ${sj.husband_beeja.rashi_name_te} రాశి (${sj.husband_beeja.degree}°)
          </div>
          <p style="font-size: 0.9rem; color: #5D4037; margin: 0; line-height: 1.6;">
            ${sj.husband_beeja.description}
          </p>
          <div style="margin-top: 10px; font-size: 0.85rem; color: #795548; background: #FAF7F2; padding: 8px; border-radius: 6px;">
            <strong>పంచమ స్థానం:</strong> ${hk.santana_analysis?.fifth_house_info?.rashi_name_te} (అధిపతి: ${hk.santana_analysis?.fifth_house_info?.lord_te})
          </div>
        </div>

        <!-- Wife Kshetra Sphuta -->
        <div class="sphuta-box">
          <div class="sphuta-box-header">
            <span>👩 భార్య క్షేత్ర స్పష్టం (Female Uterine Fertility)</span>
            <span class="dignity-tag dignity-${sj.wife_kshetra.badge}">${sj.wife_kshetra.status}</span>
          </div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #4A0E17; margin: 8px 0;">
            ${sj.wife_kshetra.rashi_name_te} రాశి (${sj.wife_kshetra.degree}°)
          </div>
          <p style="font-size: 0.9rem; color: #5D4037; margin: 0; line-height: 1.6;">
            ${sj.wife_kshetra.description}
          </p>
          <div style="margin-top: 10px; font-size: 0.85rem; color: #795548; background: #FAF7F2; padding: 8px; border-radius: 6px;">
            <strong>పంచమ స్థానం:</strong> ${wk.santana_analysis?.fifth_house_info?.rashi_name_te} (అధిపతి: ${wk.santana_analysis?.fifth_house_info?.lord_te})
          </div>
        </div>

      </div>
    `;
  }

  // 3. Kuja Dosha Samyam Section
  const kujaEl = document.getElementById("coupleKujaSamyaSection");
  if (kujaEl) {
    const ks = ja.kuja_samya;
    const kBadgeCol = ks.badge === "success" ? "#1B5E20" : "#E65100";
    const kBadgeBg = ks.badge === "success" ? "#E8F5E9" : "#FFF3E0";

    kujaEl.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; border-bottom: 1.5px solid rgba(212, 175, 55, 0.3); padding-bottom: 12px;">
        <h3 class="card-title" style="margin: 0;">
          <span>⚔️</span> కుజ దోష సామ్య విశ్లేషణ (Kuja Dosha Samyam & Cancellation)
        </h3>
        <span class="dignity-tag" style="background: ${kBadgeBg}; color: ${kBadgeCol}; font-weight: 800; font-size: 0.95rem; padding: 6px 14px; border: 1px solid ${kBadgeCol};">
          ${ks.title}
        </span>
      </div>

      <div style="background: ${kBadgeBg}; border-left: 5px solid ${kBadgeCol}; border-radius: 8px; padding: 16px;">
        <p style="margin: 0; color: #2B2118; font-size: 0.95rem; line-height: 1.7;">
          ${ks.description}
        </p>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
        <div style="background: #FFFDF9; border: 1px solid #E2D4B7; border-radius: 8px; padding: 12px;">
          <strong>👨 భర్త కుజ స్థితి:</strong> ${hk.kuja_dosha.status_te} (లగ్నం నుండి ${hk.kuja_dosha.kuja_from_lagna}వ ఇల్లు)
        </div>
        <div style="background: #FFFDF9; border: 1px solid #E2D4B7; border-radius: 8px; padding: 12px;">
          <strong>👩 భార్య కుజ స్థితి:</strong> ${wk.kuja_dosha.status_te} (లగ్నం నుండి ${wk.kuja_dosha.kuja_from_lagna}వ ఇల్లు)
        </div>
      </div>
    `;
  }

  // 4. Comparative Matrix Section
  const matrixEl = document.getElementById("coupleMatrixSection");
  if (matrixEl) {
    const rowsHtml = ja.comparative_matrix.map(row => {
      const badgeStyle = row.badge === "success" ? "badge-safe" : (row.badge === "warning" ? "badge-afflicted" : "dignity-friend");
      return `
        <tr>
          <td><strong>${row.dosha_name}</strong></td>
          <td>${row.husband_status}</td>
          <td>${row.wife_status}</td>
          <td><span class="${badgeStyle}">${row.joint_result}</span></td>
        </tr>
      `;
    }).join("");

    matrixEl.innerHTML = `
      <h3 class="card-title" style="margin-bottom: 14px;">
        <span>📊</span> దంపతుల దోష తులనాత్మక పట్టిక (Husband vs Wife Dosha Matrix)
      </h3>
      <div class="table-responsive">
        <table class="vedic-table">
          <thead>
            <tr>
              <th>దోష పరిశీలన</th>
              <th>భర్త (${hk.input.name}) స్థితి</th>
              <th>భార్య (${wk.input.name}) స్థితి</th>
              <th>సంయుక్త ఫలితం & తీర్పు</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;
  }

  // 5. Prescribed Pariharas Section
  const pariharasEl = document.getElementById("couplePariharasSection");
  if (pariharasEl) {
    const cardsHtml = ja.joint_pariharas.map((p, idx) => {
      return `
        <div style="background: #FFFDF9; border: 1.5px solid #D4AF37; border-radius: 12px; padding: 20px; margin-bottom: 18px; box-shadow: 0 3px 10px rgba(0,0,0,0.04);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; border-bottom: 1px solid #E2D4B7; padding-bottom: 10px;">
            <div>
              <span style="background: #4A0E17; color: #FFF8E7; font-size: 0.8rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; margin-right: 8px;">
                ప్రాధాన్యత: ${p.priority}
              </span>
              <strong style="font-size: 1.25rem; color: #4A0E17;">${p.title}</strong>
            </div>
            <div style="background: rgba(212, 175, 55, 0.2); color: #4A0E17; font-weight: 800; padding: 4px 12px; border-radius: 16px; font-size: 0.88rem;">
              🪔 సంకల్ప కర్త: ${p.karta}
            </div>
          </div>

          <!-- Permissible Shastric Timeframe & Urgency -->
          <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
            <span class="parihara-timeframe-chip">
              <span>⏱️</span> శాస్త్రోక్త కాల వ్యవధి: <strong>${p.timeframe_te || '3 నుండి 6 నెలల లోపు'}</strong>
            </span>
            <span style="background: #E8F5E9; color: #2E7D32; font-weight: 700; font-size: 0.82rem; padding: 3px 10px; border-radius: 12px; border: 1px solid #C8E6C9;">
              తీవ్రత: ${p.urgency || 'మధ్యమం'}
            </span>
          </div>

          <div style="font-size: 0.95rem; color: #3E2723; margin-bottom: 10px; line-height: 1.7;">
            <strong>విధి విధానం:</strong> ${p.procedure}
          </div>

          <div style="background: #FAF7F2; border-left: 4px solid #D4AF37; padding: 10px 14px; border-radius: 6px; margin-bottom: 14px;">
            <div style="font-size: 0.85rem; color: #795548; font-weight: 700;">మంత్ర సాధన:</div>
            <div style="font-size: 0.95rem; color: #2E7D32; font-weight: 600;">${p.mantra}</div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <span style="font-size: 0.85rem; color: #8D6E63; font-style: italic;">
              📜 ఆధార గ్రంథం: ${p.shastra_quote}
            </span>
            <button type="button" class="btn-calculate-muhurtam" onclick="window.launchMuhurtamForCoupleRemedy('${p.event_type}', '${hk.input.name}', '${wk.input.name}', null, null, ${p.ideal_days_range || 90})">
              <span>⏱️</span> ఈ పరిహారానికి ముహూర్తం నిర్ణయించండి
            </button>
          </div>
        </div>
      `;
    }).join("");

    pariharasEl.innerHTML = `
      <h3 class="card-title" style="margin-bottom: 16px;">
        <span>🪔</span> శాస్త్రోక్త దంపతుల సంయుక్త పరిహార కార్యాచరణ (Prescribed Couple Remedies)
      </h3>
      ${cardsHtml}
    `;
  }
}

window.switchCoupleView = function(viewType) {
  const btnJoint = document.getElementById("btnCoupleViewJoint");
  const btnHusband = document.getElementById("btnCoupleViewHusband");
  const btnWife = document.getElementById("btnCoupleViewWife");
  const coupleContent = document.getElementById("coupleReportContent");
  const resultsContainer = document.getElementById("resultsContainer");
  const coupleResults = document.getElementById("coupleResultsContainer");

  [btnJoint, btnHusband, btnWife].forEach(b => { if (b) b.classList.remove("active"); });

  if (viewType === "joint") {
    if (btnJoint) btnJoint.classList.add("active");
    if (coupleContent) coupleContent.style.display = "block";
    if (resultsContainer) resultsContainer.style.display = "none";
    if (coupleResults) coupleResults.scrollIntoView({ behavior: "smooth" });
  } else if (viewType === "husband") {
    if (btnHusband) btnHusband.classList.add("active");
    if (!window.currentCoupleData || !window.currentCoupleData.husband_kundali) return;
    if (coupleContent) coupleContent.style.display = "none";
    window.displayFullKundali(window.currentCoupleData.husband_kundali, {
      text: `<span>👨</span> <strong>భర్త (${window.currentCoupleData.husband_kundali.input.name})</strong> గారి సంపూర్ణ జాతకం (All 11 Tabs, SAV & Phalitalu)`,
      btnText: "దంపతుల ఉమ్మడి నివేదికకు తిరిగి వెళ్ళండి",
      returnAction: () => window.switchCoupleView('joint')
    });
  } else if (viewType === "wife") {
    if (btnWife) btnWife.classList.add("active");
    if (!window.currentCoupleData || !window.currentCoupleData.wife_kundali) return;
    if (coupleContent) coupleContent.style.display = "none";
    window.displayFullKundali(window.currentCoupleData.wife_kundali, {
      text: `<span>👩</span> <strong>భార్య (${window.currentCoupleData.wife_kundali.input.name})</strong> గారి సంపూర్ణ జాతకం (All 11 Tabs, SAV & Phalitalu)`,
      btnText: "దంపతుల ఉమ్మడి నివేదికకు తిరిగి వెళ్ళండి",
      returnAction: () => window.switchCoupleView('joint')
    });
  }
};

window.launchMuhurtamForCoupleRemedy = function(eventType, husbandName, wifeName, hNakIdx, wNakIdx, idealDaysRange = 90) {
  // 1. Switch to Muhurtam Tab
  const muhurtamNavBtn = document.querySelector('[data-module="moduleMuhurtam"]');
  if (muhurtamNavBtn) muhurtamNavBtn.click();

  // 2. Switch participant mode to Couple
  const coupleBtn = document.querySelector('.participant-mode-btn[data-mode="couple"]');
  if (coupleBtn) coupleBtn.click();

  // 3. Set Event Type
  const evSelect = document.getElementById("muhurtamEventType");
  if (evSelect && eventType) {
    evSelect.value = eventType;
    if (typeof window.updateMuhurtamEventContextCard === "function") {
      window.updateMuhurtamEventContextCard(eventType);
    }
  }

  // 4. Resolve exact Husband & Wife details
  const hk = window.currentCoupleData?.husband_kundali;
  const wk = window.currentCoupleData?.wife_kundali;

  function extractNakshatraIndex(k, fallback) {
    if (fallback !== null && fallback !== undefined && !isNaN(fallback)) return parseInt(fallback, 10);
    if (k?.panchangam?.nakshatra_index !== undefined) return parseInt(k.panchangam.nakshatra_index, 10);
    if (k?.panchangam?.moon_nakshatra_index !== undefined) return parseInt(k.panchangam.moon_nakshatra_index, 10);
    if (k?.planets) {
      const moon = k.planets.find(p => p.name_en === "Moon" || p.name_te === "చంద్రుడు");
      if (moon && moon.longitude !== undefined) return Math.floor((moon.longitude % 360) / (360 / 27));
    }
    return 0;
  }

  function extractRashiIndex(k) {
    if (k?.panchangam?.janma_rashi_index !== undefined) return parseInt(k.panchangam.janma_rashi_index, 10);
    if (k?.planets) {
      const moon = k.planets.find(p => p.name_en === "Moon" || p.name_te === "చంద్రుడు");
      if (moon && moon.rashi_index !== undefined) return parseInt(moon.rashi_index, 10);
      if (moon && moon.longitude !== undefined) return Math.floor((moon.longitude % 360) / 30);
    }
    return 0;
  }

  const finalHName = husbandName || hk?.input?.name || "భర్త";
  const finalWName = wifeName || wk?.input?.name || "భార్య";
  const finalHNak = extractNakshatraIndex(hk, hNakIdx);
  const finalWNak = extractNakshatraIndex(wk, wNakIdx);
  const finalHRashi = extractRashiIndex(hk);
  const finalWRashi = extractRashiIndex(wk);

  // 5. Fill Husband & Wife form fields (supporting both new and legacy IDs)
  const hNameEl = document.getElementById("muhurtaHusbandName") || document.getElementById("coupleHusbandName");
  const wNameEl = document.getElementById("muhurtaWifeName") || document.getElementById("coupleWifeName");
  const hNakEl = document.getElementById("muhurtaHusbandNak") || document.getElementById("coupleHusbandNak");
  const wNakEl = document.getElementById("muhurtaWifeNak") || document.getElementById("coupleWifeNak");
  const hRashiEl = document.getElementById("muhurtaHusbandRashi") || document.getElementById("coupleHusbandRashi");
  const wRashiEl = document.getElementById("muhurtaWifeRashi") || document.getElementById("coupleWifeRashi");

  if (hNameEl) hNameEl.value = `${finalHName} (భర్త)`;
  if (wNameEl) wNameEl.value = `${finalWName} (భార్య)`;
  if (hNakEl) hNakEl.value = String(finalHNak);
  if (wNakEl) wNakEl.value = String(finalWNak);
  if (hRashiEl) hRashiEl.value = String(finalHRashi);
  if (wRashiEl) wRashiEl.value = String(finalWRashi);

  // 6. Set Date Range based on permissible Shastric timeframe
  const rangeSelect = document.getElementById("muhurtamDaysRange");
  if (rangeSelect && idealDaysRange) {
    rangeSelect.value = String(idealDaysRange);
  }

  // 7. Scroll and execute search
  const form = document.getElementById("muhurtamForm");
  if (form) {
    setTimeout(() => {
      form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
    }, 350);
  }
};

/* ========================================================================== */
/* WHOLE FAMILY DOSHA AUDIT FRONTEND LOGIC                                    */
/* ========================================================================== */

window.familyMembersList = [
  {
    id: "fam_1",
    name: "వెంకటేశ్వరరావు",
    relation: "తండ్రి / గృహపతి",
    gender: "male",
    dob: "1968-04-12",
    tob: "06:15",
    place: "Vijayawada, Andhra Pradesh",
    lat: 16.5062,
    lon: 80.6480,
    tz: 5.5
  },
  {
    id: "fam_2",
    name: "సుమలత",
    relation: "తల్లి / గృహిణి",
    gender: "female",
    dob: "1972-08-20",
    tob: "11:45",
    place: "Vijayawada, Andhra Pradesh",
    lat: 16.5062,
    lon: 80.6480,
    tz: 5.5
  },
  {
    id: "fam_3",
    name: "కార్తీక్",
    relation: "పెద్ద కుమారుడు",
    gender: "male",
    dob: "1998-11-05",
    tob: "18:20",
    place: "Hyderabad, Telangana",
    lat: 17.3850,
    lon: 78.4867,
    tz: 5.5
  }
];

function initFamilyModule() {
  renderFamilyMemberInputs();

  const btnAdd = document.getElementById("btnAddFamilyMember");
  if (btnAdd) {
    btnAdd.addEventListener("click", () => {
      const newId = "fam_" + Date.now();
      window.familyMembersList.push({
        id: newId,
        name: "",
        relation: "కుటుంబ సభ్యుడు",
        gender: "male",
        dob: "2000-01-01",
        tob: "10:00",
        place: "Hyderabad, Telangana",
        lat: 17.3850,
        lon: 78.4867,
        tz: 5.5
      });
      renderFamilyMemberInputs();
    });
  }

  const form = document.getElementById("familyForm");
  const btnSubmit = document.getElementById("btnFamilyGenerate");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Read values from DOM into familyMembersList
    for (let i = 0; i < window.familyMembersList.length; i++) {
      const m = window.familyMembersList[i];
      const nameEl = document.getElementById(`famName_${m.id}`);
      const relEl = document.getElementById(`famRel_${m.id}`);
      const genEl = document.getElementById(`famGen_${m.id}`);
      const dobEl = document.getElementById(`famDob_${m.id}`);
      const tobEl = document.getElementById(`famTob_${m.id}`);
      const placeEl = document.getElementById(`famPlace_${m.id}`);
      const latEl = document.getElementById(`famLat_${m.id}`);
      const lonEl = document.getElementById(`famLon_${m.id}`);
      const tzEl = document.getElementById(`famTz_${m.id}`);

      if (nameEl) m.name = nameEl.value.trim() || `సభ్యుడు ${i + 1}`;
      if (relEl) m.relation = relEl.value;
      if (genEl) m.gender = genEl.value;
      if (dobEl) m.dob = dobEl.value;
      if (tobEl) m.tob = tobEl.value;
      if (placeEl) m.place = placeEl.value;
      if (latEl) m.lat = parseFloat(latEl.value) || 17.3850;
      if (lonEl) m.lon = parseFloat(lonEl.value) || 78.4867;
      if (tzEl) m.tz = parseFloat(tzEl.value) || 5.5;
    }

    const familyName = document.getElementById("familyDisplayName").value.trim() || "మా కుటుంబం";
    const purpose = document.getElementById("familyPurposeSelect").value || "all";

    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `<span class="spinner"></span> మొత్తం కుటుంబ సభ్యుల జాతకాలు పరిశీలించబడుతున్నాయి...`;

    try {
      const membersPayload = window.familyMembersList.map(m => ({
        id: m.id,
        name: m.name,
        relation: m.relation,
        gender: m.gender,
        dob: m.dob,
        tob: m.tob,
        place_name: m.place,
        latitude: m.lat,
        longitude: m.lon,
        timezone_offset: m.tz,
        ayanamsa: "lahiri"
      }));

      const resp = await fetch("/api/v1/kundali/family-audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          family_name: familyName,
          purpose: purpose,
          members: membersPayload
        })
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.detail || "సకుటుంబ దోష విశ్లేషణలో లోపం ఏర్పడింది.");
      }

      const data = await resp.json();
      window.currentFamilyData = data;

      renderFamilyResults(data);

      const famResults = document.getElementById("familyResultsContainer");
      if (famResults) {
        famResults.style.display = "block";
        famResults.scrollIntoView({ behavior: "smooth" });
      }
    } catch (err) {
      alert(err.message || "సకుటుంబ పరిశీలనలో లోపం సంభవించింది.");
    } finally {
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = `<span>👨‍👩‍👧‍👦</span> సకుటుంబ దోష సమగ్ర పరిశీలన & పరిహార నిర్ణయం (Audit Family Horoscopes)`;
    }
  });
}

function renderFamilyMemberInputs() {
  const container = document.getElementById("familyMembersListContainer");
  if (!container) return;

  container.innerHTML = "";

  window.familyMembersList.forEach((m, idx) => {
    const card = document.createElement("div");
    card.className = "family-member-card";
    card.id = `card_${m.id}`;

    const isRemovable = window.familyMembersList.length > 1;

    card.innerHTML = `
      <div class="family-member-header">
        <div class="family-member-title">
          <span>👤</span> కుటుంబ సభ్యుడు #${idx + 1}: <strong>${m.name || 'నూతన సభ్యుడు'}</strong>
        </div>
        ${isRemovable ? `
          <button type="button" class="btn-remove-member" onclick="window.removeFamilyMember('${m.id}')">
            ❌ తొలగించు
          </button>
        ` : ''}
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label>పూర్తి పేరు (Full Name)</label>
          <input type="text" id="famName_${m.id}" class="form-control" value="${m.name}" placeholder="సభ్యుని పేరు" required>
        </div>

        <div class="form-group">
          <label>కుటుంబంలో సంబంధం (Relation)</label>
          <select id="famRel_${m.id}" class="form-control">
            <option value="తండ్రి / గృహపతి" ${m.relation.includes("తండ్రి") ? 'selected' : ''}>తండ్రి / గృహపతి (Father/Head)</option>
            <option value="తల్లి / గృహిణి" ${m.relation.includes("తల్లి") ? 'selected' : ''}>తల్లి / గృహిణి (Mother/Wife)</option>
            <option value="పెద్ద కుమారుడు" ${m.relation.includes("పెద్ద కుమారుడు") ? 'selected' : ''}>పెద్ద కుమారుడు (Elder Son)</option>
            <option value="చిన్న కుమారుడు" ${m.relation.includes("చిన్న కుమారుడు") ? 'selected' : ''}>చిన్న కుమారుడు (Younger Son)</option>
            <option value="కుమార్తె" ${m.relation.includes("కుమార్తె") ? 'selected' : ''}>కుమార్తె (Daughter)</option>
            <option value="తాతగారు / పెద్దలు" ${m.relation.includes("తాతగారు") ? 'selected' : ''}>తాతగారు / పెద్దలు (Grandfather)</option>
            <option value="బామ్మగారు" ${m.relation.includes("బామ్మగారు") ? 'selected' : ''}>బామ్మగారు (Grandmother)</option>
            <option value="ఇతర సభ్యుడు" ${m.relation.includes("ఇతర") ? 'selected' : ''}>ఇతర కుటుంబ సభ్యుడు (Other Relative)</option>
          </select>
        </div>

        <div class="form-group">
          <label>లింగం (Gender)</label>
          <select id="famGen_${m.id}" class="form-control">
            <option value="male" ${m.gender === 'male' ? 'selected' : ''}>పురుషుడు (Male)</option>
            <option value="female" ${m.gender === 'female' ? 'selected' : ''}>స్త్రీ (Female)</option>
          </select>
        </div>

        <div class="form-group">
          <label>జన్మ తేదీ (DOB)</label>
          <input type="date" id="famDob_${m.id}" class="form-control" value="${m.dob}" required>
        </div>

        <div class="form-group">
          <label>జన్మ సమయం (TOB)</label>
          <input type="time" id="famTob_${m.id}" class="form-control" value="${m.tob}" step="1" required>
        </div>

        <div class="form-group" style="grid-column: span 2;">
          <label>జన్మ స్థలం / నగరం (Birth Place)</label>
          <input type="text" id="famPlace_${m.id}" class="form-control" value="${m.place}" placeholder="నగరం టైప్ చేయండి" autocomplete="off" required>
          <div id="famSuggestions_${m.id}" class="city-suggestions"></div>
          <div id="famFeedback_${m.id}" class="city-feedback-chip">📍 స్థలం: <strong>${m.place}</strong></div>
          <input type="hidden" id="famLat_${m.id}" value="${m.lat}">
          <input type="hidden" id="famLon_${m.id}" value="${m.lon}">
          <input type="hidden" id="famTz_${m.id}" value="${m.tz}">
        </div>
      </div>
    `;

    container.appendChild(card);

    // Setup autocomplete for this row
    setupCityAutocomplete(
      `famPlace_${m.id}`,
      `famSuggestions_${m.id}`,
      `famLat_${m.id}`,
      `famLon_${m.id}`,
      `famTz_${m.id}`,
      `famFeedback_${m.id}`
    );
  });
}

window.removeFamilyMember = function(memberId) {
  if (window.familyMembersList.length <= 1) return;
  window.familyMembersList = window.familyMembersList.filter(m => m.id !== memberId);
  renderFamilyMemberInputs();
};

function renderFamilyResults(data) {
  const fa = data.family_audit;
  if (!fa) return;

  const titleEl = document.getElementById("familySummaryTitle");
  const totEl = document.getElementById("familyTotalMembersCount");
  const affEl = document.getElementById("familyAfflictedCount");
  const safeEl = document.getElementById("familySafeCount");
  const kartaEl = document.getElementById("familyKartaName");

  if (titleEl) titleEl.textContent = fa.family_name;
  if (totEl) totEl.textContent = fa.total_members;
  if (affEl) affEl.textContent = fa.afflicted_count;
  if (safeEl) safeEl.textContent = fa.safe_count;
  if (kartaEl) kartaEl.textContent = fa.designated_karta;

  // Render Table
  const tbody = document.getElementById("familyAuditTableBody");
  if (tbody && fa.audit_table) {
    tbody.innerHTML = fa.audit_table.map((row, idx) => {
      const vBadgeClass = row.verdict_badge === "danger" ? "badge-afflicted" : (row.verdict_badge === "warning" ? "dignity-friend" : "badge-safe");
      const memberIdx = row.member_index !== undefined ? row.member_index : idx;
      return `
        <tr>
          <td>
            <strong>${row.name}</strong><br>
            <small style="color: #795548;">${row.relation}</small>
          </td>
          <td>
            <strong>${row.rashi}</strong> / ${row.nakshatra}<br>
            <small style="color: #996515;">లగ్నం: ${row.lagna}</small>
          </td>
          <td><span class="${row.sarpa_badge === 'danger' ? 'badge-afflicted' : 'badge-safe'}">${row.sarpa_dosha}</span></td>
          <td><span class="${row.kuja_badge === 'warning' ? 'badge-afflicted' : 'badge-safe'}">${row.kuja_dosha}</span></td>
          <td><span class="${row.kalasarpa_badge === 'warning' ? 'badge-afflicted' : 'badge-safe'}">${row.kalasarpa_dosha}</span></td>
          <td><span class="${row.pitru_badge === 'warning' ? 'badge-afflicted' : 'badge-safe'}">${row.pitru_dosha}</span></td>
          <td><span class="dignity-tag dignity-own">${row.shani_dosha}</span></td>
          <td>${row.gandanta}</td>
          <td>
            <span class="${vBadgeClass}">${row.verdict}</span><br>
            <small style="color: #4A0E17; font-weight: 600;">${row.primary_remedy}</small>
          </td>
          <td>
            <button type="button" class="btn-view-member-kundali" onclick="window.viewFamilyMemberFullKundali(${memberIdx})" title="${row.name} గారి సంపూర్ణ 11 చక్రాల జాతకం చూడండి">
              <span>👁️</span> జాతకం
            </button>
          </td>
        </tr>
      `;
    }).join("");
  }

  // Render Family Pariharas
  const pariharasEl = document.getElementById("familyPariharasSection");
  if (pariharasEl && fa.family_remedies) {
    const remediesHtml = fa.family_remedies.map(r => {
      return `
        <div style="background: #FFFDF9; border: 1.5px solid #D4AF37; border-radius: 12px; padding: 20px; margin-bottom: 18px; box-shadow: 0 3px 10px rgba(0,0,0,0.04);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; border-bottom: 1px solid #E2D4B7; padding-bottom: 10px;">
            <strong style="font-size: 1.25rem; color: #4A0E17;">${r.title}</strong>
            <div style="background: rgba(212, 175, 55, 0.2); color: #4A0E17; font-weight: 800; padding: 4px 12px; border-radius: 16px; font-size: 0.88rem;">
              🪔 సంకల్ప కర్త: ${r.karta}
            </div>
          </div>

          <!-- Permissible Shastric Timeframe & Urgency -->
          <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
            <span class="parihara-timeframe-chip">
              <span>⏱️</span> శాస్త్రోక్త కాల వ్యవధి: <strong>${r.timeframe_te || '3 నుండి 6 నెలల లోపు'}</strong>
            </span>
            <span style="background: #E8F5E9; color: #2E7D32; font-weight: 700; font-size: 0.82rem; padding: 3px 10px; border-radius: 12px; border: 1px solid #C8E6C9;">
              తీవ్రత: ${r.urgency || 'మధ్యమం'}
            </span>
          </div>

          <div style="font-size: 0.95rem; color: #3E2723; margin-bottom: 10px; line-height: 1.7;">
            <strong>లక్ష్యం:</strong> ${r.target}<br>
            <strong>విధానం:</strong> ${r.procedure}
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <span style="font-size: 0.85rem; color: #8D6E63; font-style: italic;">
              📜 ఆధార గ్రంథం: ${r.shastra_quote}
            </span>
            <button type="button" class="btn-calculate-muhurtam" onclick="window.launchMuhurtamForFamilyRemedy('${r.event_type}', '${fa.family_name}', ${r.ideal_days_range || 90})">
              <span>⏱️</span> సకుటుంబ ముహూర్తం నిర్ణయించండి
            </button>
          </div>
        </div>
      `;
    }).join("");

    pariharasEl.innerHTML = `
      <h3 class="card-title" style="margin-bottom: 16px;">
        <span>🪔</span> సకుటుంబ శాంతి & పరిహార కార్యాచరణ (Recommended Family Pariharas)
      </h3>
      ${remediesHtml}
    `;
  }
}

window.viewFamilyMemberFullKundali = function(memberIndex) {
  if (!window.currentFamilyData || !window.currentFamilyData.members_data) {
    alert("కుటుంబ సభ్యుల జాతక వివరాలు అందుబాటులో లేవు.");
    return;
  }
  const member = window.currentFamilyData.members_data[memberIndex];
  if (!member || !member.kundali) {
    alert("ఈ సభ్యుని జాతక వివరాలు లభించలేదు.");
    return;
  }

  const famResults = document.getElementById("familyResultsContainer");
  if (famResults) famResults.style.display = "none";

  window.displayFullKundali(member.kundali, {
    text: `<span>👨‍👩‍👧‍👦</span> సకుటుంబ పరిశీలన: <strong>${member.member_info.name} (${member.member_info.relation})</strong> గారి సంపూర్ణ జాతకం (All 11 Tabs, SAV & Predictions)`,
    btnText: "సకుటుంబ నివేదికకు తిరిగి వెళ్ళండి",
    returnAction: () => {
      const resultsContainer = document.getElementById("resultsContainer");
      if (resultsContainer) resultsContainer.style.display = "none";
      if (famResults) {
        famResults.style.display = "block";
        famResults.scrollIntoView({ behavior: "smooth" });
      }
    }
  });
};

window.launchMuhurtamForFamilyRemedy = function(eventType, familyName, idealDaysRange = 90) {
  // 1. Switch to Muhurtam Tab
  const muhurtamNavBtn = document.querySelector('[data-module="moduleMuhurtam"]');
  if (muhurtamNavBtn) muhurtamNavBtn.click();

  // 2. Switch participant mode to Family
  const familyBtn = document.querySelector('.participant-mode-btn[data-mode="family"]');
  if (familyBtn) familyBtn.click();

  // 3. Set Event Type
  const evSelect = document.getElementById("muhurtamEventType");
  if (evSelect && eventType) {
    evSelect.value = eventType;
    if (typeof window.updateMuhurtamEventContextCard === "function") {
      window.updateMuhurtamEventContextCard(eventType);
    }
  }

  // 4. Set Date Range based on permissible Shastric timeframe
  const rangeSelect = document.getElementById("muhurtamDaysRange");
  if (rangeSelect && idealDaysRange) {
    rangeSelect.value = String(idealDaysRange);
  }

  // 5. Scroll and execute search
  const form = document.getElementById("muhurtamForm");
  if (form) {
    setTimeout(() => {
      form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
    }, 350);
  }
};




