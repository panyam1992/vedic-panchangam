/**
 * Interactive SVG Kundali Chart Renderer.
 * Supports:
 * 1. Traditional South Indian Chart (Fixed Signs)
 * 2. North Indian Diamond Chart (Fixed Houses)
 * 3. D1 (Rashi) and D9 (Navamsha) Charts
 * 4. Multi-Language Indic Script Support (Aksharamukha Parity):
 *    Telugu, Devanagari (Hindi/Sanskrit), Tamil, Kannada, Malayalam, Bengali, Gujarati, Odia, Gurmukhi, IAST
 */

const SOUTH_INDIAN_SIGN_BOXES = {
  11: { r: 0, c: 0, name_te: 'మీనం', name_en: 'Pisces' },
  0:  { r: 0, c: 1, name_te: 'మేషం', name_en: 'Aries' },
  1:  { r: 0, c: 2, name_te: 'వృషభం', name_en: 'Taurus' },
  2:  { r: 0, c: 3, name_te: 'మిథునం', name_en: 'Gemini' },
  3:  { r: 1, c: 3, name_te: 'కర్కాటకం', name_en: 'Cancer' },
  4:  { r: 2, c: 3, name_te: 'సింహం', name_en: 'Leo' },
  5:  { r: 3, c: 3, name_te: 'కన్య', name_en: 'Virgo' },
  6:  { r: 3, c: 2, name_te: 'తుల', name_en: 'Libra' },
  7:  { r: 3, c: 1, name_te: 'వృశ్చికం', name_en: 'Scorpio' },
  8:  { r: 3, c: 0, name_te: 'ధనుస్సు', name_en: 'Sagittarius' },
  9:  { r: 2, c: 0, name_te: 'మకరం', name_en: 'Capricorn' },
  10: { r: 1, c: 0, name_te: 'కుంభం', name_en: 'Aquarius' }
};

const INDIC_SIGN_NAMES = {
  Telugu: ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"],
  Devanagari: ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन"],
  Tamil: ["மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி", "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"],
  Kannada: ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕಾಟಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"],
  Malayalam: ["മേടം", "ഇടവം", "മിഥുനം", "കർക്കടകം", "ചിങ്ങം", "കന്നി", "തുലാം", "വൃശ്ചികം", "ധനു", "മകരം", "കുംഭം", "മീനം"],
  Bengali: ["মেষ", "বৃষ", "মিথুন", "কর্কট", "সিংহ", "কন্যা", "তুলা", "বৃশ্চিক", "ধনু", "মকর", "কুম্ভ", "মীন"],
  Gujarati: ["મેષ", "વૃષભ", "મિથુન", "કર્ક", "સિંહ", "કન્યા", "તુલા", "વૃશ્ચિક", "ધન", "મકર", "કુંભ", "મીન"],
  Oriya: ["ମେଷ", "ବୃଷ", "ମିଥୁନ", "କର୍କଟ", "ସିଂହ", "କନ୍ୟା", "ତୁଳା", "ବିଛା", "ଧନୁ", "ମକର", "କୁମ୍ଭ", "ମୀନ"],
  Gurmukhi: ["ਮੇਖ", "ਬ੍ਰਿਖ", "ਮਿਥੁਨ", "ਕਰਕ", "ਸਿੰਘ", "ਕੰਨਿਆ", "ਤੁਲਾ", "ਬ੍ਰਿਸ਼ਚਕ", "ਧਨੁ", "ਮਕਰ", "ਕੁੰਭ", "ਮੀਨ"],
  IAST: ["Meṣa", "Vṛṣabha", "Mithuna", "Karka", "Siṃha", "Kanyā", "Tulā", "Vṛścika", "Dhanu", "Makara", "Kumbha", "Mīna"]
};

const INDIC_PLANET_SHORT = {
  Telugu: { "Sun": "రవి", "Moon": "చం", "Mars": "కు", "Mercury": "బు", "Jupiter": "గు", "Venus": "శు", "Saturn": "శని", "Rahu": "రా", "Ketu": "కే", "Lagna": "లగ్నం" },
  Devanagari: { "Sun": "सूर्य", "Moon": "चन्द्र", "Mars": "मंगल", "Mercury": "बुध", "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु", "Lagna": "लग्न" },
  Tamil: { "Sun": "சூரி", "Moon": "சந்", "Mars": "செவ்", "Mercury": "புத", "Jupiter": "குரு", "Venus": "சுக்", "Saturn": "சனி", "Rahu": "ராகு", "Ketu": "கேது", "Lagna": "லக்" },
  Kannada: { "Sun": "ರವಿ", "Moon": "ಚಂ", "Mars": "ಕುಜ", "Mercury": "ಬುಧ", "Jupiter": "ಗುರು", "Venus": "ಶುಕ್ರ", "Saturn": "ಶನಿ", "Rahu": "ರಾಹು", "Ketu": "ಕೇತು", "Lagna": "ಲಗ್ನ" },
  Malayalam: { "Sun": "സൂ", "Moon": "ച", "Mars": "കു", "Mercury": "ബു", "Jupiter": "ഗു", "Venus": "ശു", "Saturn": "ശ", "Rahu": "രാ", "Ketu": "കേ", "Lagna": "ല" },
  Bengali: { "Sun": "রবি", "Moon": "চন্দ্র", "Mars": "মঙ্গল", "Mercury": "বুধ", "Jupiter": "বৃহ", "Venus": "শুক্র", "Saturn": "শনি", "Rahu": "রাহু", "Ketu": "কেতু", "Lagna": "লগ্ন" },
  Gujarati: { "Sun": "સૂર્ય", "Moon": "ચંદ્ર", "Mars": "મંગળ", "Mercury": "બુધ", "Jupiter": "ગુરુ", "Venus": "શુક્ર", "Saturn": "શનિ", "Rahu": "રાહુ", "Ketu": "કેતુ", "Lagna": "લગ્ન" },
  Oriya: { "Sun": "ରବି", "Moon": "ଚନ୍ଦ୍ର", "Mars": "ମଙ୍ଗଳ", "Mercury": "ବୁଧ", "Jupiter": "ଗୁରୁ", "Venus": "ଶୁକ୍ର", "Saturn": "ଶନି", "Rahu": "ରାହୁ", "Ketu": "କେତୁ", "Lagna": "ଲଗ୍ନ" },
  Gurmukhi: { "Sun": "ਸੂਰਜ", "Moon": "ਚੰਨ", "Mars": "ਮੰਗਲ", "Mercury": "ਬੁੱਧ", "Jupiter": "ਗੁਰੂ", "Venus": "ਸ਼ੁੱਕਰ", "Saturn": "ਸ਼ਨੀ", "Rahu": "ਰਾਹੂ", "Ketu": "ਕੇਤੂ", "Lagna": "ਲਗਨ" },
  IAST: { "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke", "Lagna": "LAG" }
};

function getCurrentScript() {
  return window.currentScript || "Telugu";
}

function getSignLabel(signIdx, script = getCurrentScript()) {
  const list = INDIC_SIGN_NAMES[script] || INDIC_SIGN_NAMES["Telugu"];
  return list[signIdx % 12];
}

function getPlanetShortLabel(pNameEn, script = getCurrentScript()) {
  const map = INDIC_PLANET_SHORT[script] || INDIC_PLANET_SHORT["Telugu"];
  return map[pNameEn] || pNameEn;
}

/**
 * Render South Indian Chart SVG.
 */
function renderSouthIndianChart(chartData, titleText = "రాశి చక్రం (D1)") {
  const size = 520;
  const cellSize = size / 4;
  const script = getCurrentScript();

  let svg = `<svg viewBox="0 0 ${size} ${size}" class="kundali-svg" xmlns="http://www.w3.org/2000/svg">`;
  svg += `<defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.1"/>
    </filter>
  </defs>`;

  // Background
  svg += `<rect width="${size}" height="${size}" fill="#FFFDF8" stroke="#D4AF37" stroke-width="3"/>`;

  // Draw 12 sign boxes (outer perimeter)
  for (let sIdx = 0; sIdx < 12; sIdx++) {
    const box = SOUTH_INDIAN_SIGN_BOXES[sIdx];
    const x = box.c * cellSize;
    const y = box.r * cellSize;

    const occupants = chartData[sIdx] || [];
    const hasLagna = occupants.some(o => o.is_lagna);

    // Box border & fill
    const boxBg = hasLagna ? "#FFF8E7" : "#FFFFFF";
    svg += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" fill="${boxBg}" stroke="#B8860B" stroke-width="1.5"/>`;

    // Sign Name Label (top-left) in current Indic script
    const signName = getSignLabel(sIdx, script);
    svg += `<text x="${x + 6}" y="${y + 16}" font-size="11" font-weight="700" fill="#6B1426">${signName}</text>`;

    // Render Occupants (Lagna and Planets)
    let textY = y + 36;
    occupants.forEach(occ => {
      if (occ.is_lagna) {
        // Lagna Badge
        const lagnaStr = getPlanetShortLabel("Lagna", script);
        svg += `<rect x="${x + 6}" y="${textY - 12}" width="${cellSize - 12}" height="18" rx="4" fill="#4A0E17"/>`;
        svg += `<text x="${x + 10}" y="${textY + 1}" font-size="11" font-weight="bold" fill="#F3E5AB">${lagnaStr}</text>`;
        textY += 20;
      } else {
        const shortName = getPlanetShortLabel(occ.name_en, script);
        const vakra = occ.is_retrograde ? "(R)" : "";
        const deg = occ.degree_in_rashi !== undefined ? `${Math.floor(occ.degree_in_rashi)}°` : "";

        // Text Color based on dignity
        const pColor = occ.dignity_en === "Exalted" ? "#1B5E20" :
                       occ.dignity_en === "Debilitated" ? "#B71C1C" : "#1C2541";

        svg += `<text x="${x + 8}" y="${textY}" font-size="12" font-weight="600" fill="${pColor}">
          ${shortName}${vakra} <tspan font-size="10" fill="#666">${deg}</tspan>
        </text>`;
        textY += 17;
      }
    });
  }

  // Center Area (Title and Info)
  const centerSize = cellSize * 2;
  const centerX = cellSize;
  const centerY = cellSize;

  svg += `<rect x="${centerX}" y="${centerY}" width="${centerSize}" height="${centerSize}" fill="#FFF8E7" stroke="#D4AF37" stroke-width="2"/>`;
  svg += `<circle cx="${size/2}" cy="${size/2}" r="35" fill="#FAF0D7" stroke="#B8860B" stroke-width="1.5"/>`;
  svg += `<text x="${size/2}" y="${size/2 - 5}" font-size="20" text-anchor="middle" fill="#996515">🕉</text>`;
  svg += `<text x="${size/2}" y="${size/2 + 16}" font-size="12" font-weight="bold" text-anchor="middle" fill="#4A0E17">${titleText}</text>`;
  svg += `<text x="${size/2}" y="${size/2 + 55}" font-size="11" text-anchor="middle" fill="#7A6021">దక్షిణ భారత చక్రం</text>`;

  svg += `</svg>`;
  return svg;
}

/**
 * Render North Indian Diamond Chart SVG.
 */
function renderNorthIndianChart(chartData, lagnaRashiIdx, titleText = "రాశి చక్రం (D1)") {
  const size = 520;
  const h = size / 2;
  const script = getCurrentScript();

  let svg = `<svg viewBox="0 0 ${size} ${size}" class="kundali-svg" xmlns="http://www.w3.org/2000/svg">`;

  // Outer border & background
  svg += `<rect width="${size}" height="${size}" fill="#FFFDF8" stroke="#D4AF37" stroke-width="3"/>`;

  // Diamond lines
  svg += `<line x1="0" y1="0" x2="${size}" y2="${size}" stroke="#B8860B" stroke-width="1.5"/>`;
  svg += `<line x1="${size}" y1="0" x2="0" y2="${size}" stroke="#B8860B" stroke-width="1.5"/>`;
  svg += `<polygon points="${h},0 ${size},${h} ${h},${size} 0,${h}" fill="none" stroke="#B8860B" stroke-width="1.5"/>`;

  // Centers of 12 Houses in North Indian Chart
  const houseCenters = [
    { h: 1,  x: h, y: h * 0.48 },          // 1st house (top center diamond)
    { h: 2,  x: h * 0.5, y: h * 0.25 },    // 2nd house (top left triangle)
    { h: 3,  x: h * 0.25, y: h * 0.5 },    // 3rd house (left top triangle)
    { h: 4,  x: h * 0.48, y: h },          // 4th house (left center diamond)
    { h: 5,  x: h * 0.25, y: h * 1.5 },    // 5th house (left bottom triangle)
    { h: 6,  x: h * 0.5, y: h * 1.75 },    // 6th house (bottom left triangle)
    { h: 7,  x: h, y: h * 1.52 },          // 7th house (bottom center diamond)
    { h: 8,  x: h * 1.5, y: h * 1.75 },    // 8th house (bottom right triangle)
    { h: 9,  x: h * 1.75, y: h * 1.5 },    // 9th house (right bottom triangle)
    { h: 10, x: h * 1.52, y: h },          // 10th house (right center diamond)
    { h: 11, x: h * 1.75, y: h * 0.5 },    // 11th house (right top triangle)
    { h: 12, x: h * 1.5, y: h * 0.25 }     // 12th house (top right triangle)
  ];

  houseCenters.forEach(item => {
    // In North Indian chart:
    // House 1 always holds sign = lagnaRashiIdx + 1
    const signNum = ((lagnaRashiIdx + (item.h - 1)) % 12) + 1;
    const signIdx = signNum - 1;
    const occupants = chartData[signIdx] || [];

    // House sign number label
    svg += `<text x="${item.x}" y="${item.y - 18}" font-size="11" font-weight="bold" fill="#6B1426" text-anchor="middle">${signNum}</text>`;

    // Planets in this house in current Indic script
    let pY = item.y - 2;
    occupants.forEach(occ => {
      const nameStr = occ.is_lagna ? getPlanetShortLabel("Lagna", script) : getPlanetShortLabel(occ.name_en, script);
      const vakra = occ.is_retrograde ? "(R)" : "";
      svg += `<text x="${item.x}" y="${pY}" font-size="11" font-weight="600" fill="#1C2541" text-anchor="middle">${nameStr}${vakra}</text>`;
      pY += 15;
    });
  });

  svg += `</svg>`;
  return svg;
}

/**
 * Render Sarvashtakavarga (SAV) South Indian Chart SVG.
 * Displays 337-point distribution across 12 signs.
 */
function renderAshtakavargaChart(savRashiList, totalPoints = 337) {
  const size = 520;
  const cellSize = size / 4;
  const script = getCurrentScript();

  // Create sign to points lookup map
  const ptsMap = {};
  if (Array.isArray(savRashiList)) {
    savRashiList.forEach(item => {
      ptsMap[item.rashi_index] = item.points;
    });
  }

  let svg = `<svg viewBox="0 0 ${size} ${size}" class="kundali-svg sav-chart-svg" xmlns="http://www.w3.org/2000/svg">`;

  // Background
  svg += `<rect width="${size}" height="${size}" fill="#FFFDF8" stroke="#D4AF37" stroke-width="3"/>`;

  // Draw 12 sign boxes
  for (let sIdx = 0; sIdx < 12; sIdx++) {
    const box = SOUTH_INDIAN_SIGN_BOXES[sIdx];
    const x = box.c * cellSize;
    const y = box.r * cellSize;

    const points = ptsMap[sIdx] !== undefined ? ptsMap[sIdx] : 28;
    const isStrong = points >= 28;
    const isHigh = points >= 32;

    // Color coding
    const boxBg = isHigh ? "#E8F5E9" : (isStrong ? "#F1F8E9" : "#FFF8E1");
    const ptsColor = isStrong ? "#1B5E20" : "#B71C1C";

    svg += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" fill="${boxBg}" stroke="#B8860B" stroke-width="1.5"/>`;

    // Sign Name Label in current Indic script
    const signName = getSignLabel(sIdx, script);
    svg += `<text x="${x + 6}" y="${y + 16}" font-size="11" font-weight="700" fill="#6B1426">${signName}</text>`;

    // SAV Points Circle & Number
    const circleX = x + (cellSize / 2);
    const circleY = y + (cellSize / 2) + 6;

    svg += `<circle cx="${circleX}" cy="${circleY}" r="22" fill="#FFFFFF" stroke="${ptsColor}" stroke-width="2" filter="url(#shadow)"/>`;
    svg += `<text x="${circleX}" y="${circleY + 6}" font-size="18" font-weight="bold" fill="${ptsColor}" text-anchor="middle">${points}</text>`;

    // Mini Strength Badge
    const statusText = isHigh ? "అత్యుత్తమం" : (isStrong ? "శుభం" : "మధ్యమం");
    svg += `<text x="${circleX}" y="${circleY + 32}" font-size="9" font-weight="600" fill="#555" text-anchor="middle">${statusText}</text>`;
  }

  // Center Box (Sarvashtakavarga 337 Total)
  const centerSize = cellSize * 2;
  const centerX = cellSize;
  const centerY = cellSize;

  svg += `<rect x="${centerX}" y="${centerY}" width="${centerSize}" height="${centerSize}" fill="#FFFDF4" stroke="#D4AF37" stroke-width="2.5"/>`;
  svg += `<circle cx="${size/2}" cy="${size/2}" r="45" fill="#FAF0D7" stroke="#B8860B" stroke-width="2"/>`;
  svg += `<text x="${size/2}" y="${size/2 - 10}" font-size="22" font-weight="bold" text-anchor="middle" fill="#4A0E17">${totalPoints}</text>`;
  svg += `<text x="${size/2}" y="${size/2 + 10}" font-size="10" font-weight="bold" text-anchor="middle" fill="#996515">సర్వాష్టకవర్గ బిందువులు</text>`;
  svg += `<text x="${size/2}" y="${size/2 + 24}" font-size="9" text-anchor="middle" fill="#666">పరాశర శాస్త్ర సిద్ధాంతం (SAV)</text>`;

  svg += `</svg>`;
  return svg;
}
