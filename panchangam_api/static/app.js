/**
 * Vedic Panchangam Client Application.
 * Full reactive orchestration for Daily View, Monthly Calendar,
 * GPS Detection, Multi-language switcher, and Vedic Sankalpa Generator.
 */

const STATE = {
  lang: localStorage.getItem('vp_lang') || 'telugu',
  city: localStorage.getItem('vp_city') || 'Frisco',
  country: localStorage.getItem('vp_country') || 'USA',
  lat: parseFloat(localStorage.getItem('vp_lat')) || 33.1507,
  lon: parseFloat(localStorage.getItem('vp_lon')) || -96.8236,
  tz: localStorage.getItem('vp_tz') || 'America/Chicago',
  date: localStorage.getItem('vp_date') || '2026-03-19', // Default to Parabhava Ugadi for rich experience
  year: 2026,
  month: 3,
  activeTab: 'daily', // 'daily', 'monthly', 'sankalpa', 'rashi', 'intercalary', 'kandadayam'
  intercalarySystem: 'surya_siddhanta',
  intercalaryData: null,
  kandadayamData: null,
  selectedNakshatraIdx: 0,
  rashiKdViewMode: 'cards',
  activeRashiPeriod: 'daily', // 'daily', 'monthly', 'yearly'
  selectedRashiIdx: 0,
  rashiData: { daily: null, monthly: null, yearly: null },
  dailyData: null,
  monthlyData: null,
  sankalpaData: null
};

// UI Translations for all 8 supported languages
const UI_TEXT = {
  telugu: {
    appTitle: "వేద సంహిత • పంచాంగం",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ సిద్ధాంతకర్త:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">రామచంద్ర శాస్త్రి మునిమడుగు</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ రూపకర్త: రామచంద్ర శాస్త్రి మునిమడుగు",
    dailyTab: "రోజువారీ పంచాంగం",
    monthlyTab: "మాస క్యాలెండర్",
    sankalpaTab: "వైదిక సంకల్పం",
    rashiTab: "రాశి ఫలాలు",
    intercalaryTab: "అధిక / క్షయ మాసములు",
    kandadayamTab: "కందదాయ ఫలాలు",
    rashiDaily: "☀️ దిన ఫలాలు",
    rashiMonthly: "🌙 మాస ఫలాలు",
    rashiYearly: "🪐 వార్షిక ఫలాలు",
    rashiSelectPrompt: "✨ మీ రాశిని ఎంచుకోండి (Select Your Rashi)",
    searchPlaceholder: "నగరం పేరును వెతకండి (ఉదా: Frisco, Hyderabad)...",
    gpsBtn: "నా లొకేషన్",
    todayBtn: "ఈరోజు",
    heroEra: "ప్రభవాది షష్టి సంవత్సరం",
    heroVaraLabel: "వారం",
    angasTitle: "పంచాంగం",
    samvatsaraLabel: "సంవత్సరం",
    ayanaLabel: "ఆయనం",
    rituLabel: "ఋతువు",
    masaLabel: "మాసం",
    pakshaLabel: "పక్షం",
    tithi: "తిథి",
    vara: "వారం",
    nakshatra: "నక్షత్రం",
    yoga: "యోగం",
    karana: "కరణం",
    chandramanaTitle: "చాంద్రమానం (Chandramana)",
    labelCmAmanta: "అమాంత మాసం:",
    labelCmPurnimanta: "పూర్ణిమాంత మాసం:",
    labelCmPaksha: "పక్షము:",
    sauramanaTitle: "సౌరమానం (Sauramana)",
    labelSmSolarMonth: "సౌర రాశి/మాసం:",
    labelSmTamil: "తమిళ మాసం:",
    labelSmMalayalam: "మలయాళ కొల్లాం:",
    labelSmSankranti: "సంక్రాంతి:",
    barhaspatyamanaTitle: "బార్హస్పత్యమానం (Jovian)",
    labelBmRashi: "గురు రాశి:",
    labelBmNakshatra: "నక్షత్రం:",
    labelBmStatus: "గతి:",
    labelBmMahaMasa: "మహా-మాసం:",
    labelBmPushkaram: "పుష్కరం:",
    sunMoonTitle: "సూర్యోదయ & చంద్రోదయ కాలాలు",
    labelTimeSunrise: "సూర్యోదయం",
    labelTimeSunset: "సూర్యాస్తమయం",
    labelTimeBrahma: "బ్రహ్మ ముహూర్తం",
    labelTimeMidday: "మధ్యాహ్నం",
    labelTimePratah: "ప్రాతః సంధ్య",
    labelTimeSayan: "సాయం సంధ్య",
    labelTimeMoonrise: "చంద్రోదయం",
    labelTimeMoonset: "చంద్రాస్తమయం",
    labelTimeMoonPhase: "చంద్ర స్థితి:",
    muhurthasTitle: "ముహూర్తాలు & వర్జ్య కాలాలు",
    labelAbhijit: "అభిజిత్ ముహూర్తం",
    labelAmrita: "అమృత కాలం",
    labelRahu: "రాహుకాలం",
    labelYama: "యమగండం",
    labelGulika: "గుళిక కాలం",
    labelDurmuhurtham: "దుర్ముహూర్తం",
    labelVarjyam: "వర్జ్యం",
    lagnasTitle: "24-గంటల లగ్న పట్టిక (Daily Lagnas)",
    festivalsTitle: "ఈ రోజు పండుగలు & వ్రతాలు (Festivals & Vratas)",
    monthlyGridTitle: "మాస క్యాలెండర్",
    monthlyHint: "ఏదైనా తేదీపై క్లిక్ చేస్తే ఆ రోజు పంచాంగ వివరాలు ఓపెన్ అవుతాయి",
    calDays: ["ఆది", "సోమ", "మంగళ", "బుధ", "గురు", "శుక్ర", "శని"],
    sankalpaTitle: "🪔 వైదిక దేశ-కాల సంకల్పం (Vedic Deśa-Kāla Sankalpa)",
    sankalpaSubtitle: "పూజ, హోమం, వ్రతాలలో చదివేందుకు మీరు ఉన్న దేశం, నగర భౌగోళిక నిరూపకాలు మరియు ఖగోళ కాల సమన్వయంతో రూపొందించబడిన శాస్త్రీయ సంకల్పం.",
    labelGotra: "మీ గోత్రం (Gotra):",
    sankalpaGotraPlaceholder: "ఉదా: కాశ్యప, భారద్వాజ, కౌండిన్య...",
    labelSharma: "మీ పేరు / శర్మ (Name):",
    sankalpaSharmaPlaceholder: "ఉదా: రామ శర్మ...",
    labelDeity: "పూజించు దైవం / కులదైవం (Deity):",
    sankalpaDeityPlaceholder: "ఉదా: శ్రీ వేంకటేశ్వర స్వామి...",
    sankalpaSubmitBtn: "సంకల్పం సిద్ధం చేయండి",
    sankalpaLangBadge: "సంకల్ప మంత్రం (ప్రస్తుత భాషలో)",
    sankalpaSaBadge: "मूल-संस्कृत-सङ्कल्पः (Original Sanskrit Devanagari)",
    copyBtnText: "కాపీ చేయండి",
    copied: "కాపీ చేయబడింది! ✔️",
    endLabel: "ముగింపు:",
    nextDayLabel: "మరుసటి రోజు",
    fullDay: "రోజంతా",
    pushkaraLabel: "పుష్కరాంశ",
    pada: "పాదం",
    timeSpanLabel: "సమయం",
    noAbhijit: "ఈ రోజు లేదు",
    noVarjyam: "వర్జ్యం లేదు",
    noFestivals: "ఈ రోజు ప్రత్యేక పండుగలు ఏవీ లేవు.",
    noLagnas: "లగ్న వివరాలు అందుబాటులో లేవు.",
    loaderText: "పంచాంగ వివరాలు లోడ్ అవుతున్నాయి...",
    geoCoordLabel: "భౌగోళిక స్థానం",
    dveepaLabel: "ద్వీపం",
    khandaLabel: "ఖండం"
  },
  english: {
    appTitle: "Vedic Samhita • Panchangam",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ Created by:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">Ramachandra Sastry Munimadugu</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ Created by: Ramachandra Sastry Munimadugu",
    dailyTab: "Daily Panchangam",
    monthlyTab: "Monthly Calendar",
    sankalpaTab: "Vedic Sankalpa",
    rashiTab: "Rashi Phalalu",
    intercalaryTab: "Adhika & Kshaya Masas",
    kandadayamTab: "Kandadayam & Trimesters",
    rashiDaily: "☀️ Daily Horoscope",
    rashiMonthly: "🌙 Monthly Horoscope",
    rashiYearly: "🪐 Yearly Horoscope",
    rashiSelectPrompt: "✨ Select Your Rashi",
    searchPlaceholder: "Search city (e.g. Frisco, Hyderabad, London)...",
    gpsBtn: "My Location",
    todayBtn: "Today",
    heroEra: "Prabhavadi 60 Samvatsara",
    heroVaraLabel: "Weekday",
    angasTitle: "Panchangam",
    samvatsaraLabel: "Samvatsaram",
    ayanaLabel: "Ayanam",
    rituLabel: "Rutu",
    masaLabel: "Masam",
    pakshaLabel: "Paksham",
    tithi: "Tithi",
    vara: "Vara",
    nakshatra: "Nakshatra",
    yoga: "Yoga",
    karana: "Karana",
    chandramanaTitle: "Chandramana (Lunar Calendar)",
    labelCmAmanta: "Amanta Month:",
    labelCmPurnimanta: "Purnimanta Month:",
    labelCmPaksha: "Paksha:",
    sauramanaTitle: "Sauramana (Solar Calendar)",
    labelSmSolarMonth: "Solar Sign/Month:",
    labelSmTamil: "Tamil Month:",
    labelSmMalayalam: "Malayalam Kollam:",
    labelSmSankranti: "Sankranti:",
    barhaspatyamanaTitle: "Barhaspatyamana (Jovian Calendar)",
    labelBmRashi: "Jupiter Sign:",
    labelBmNakshatra: "Nakshatra:",
    labelBmStatus: "Motion:",
    labelBmMahaMasa: "Maha-Masa:",
    labelBmPushkaram: "Pushkaram River:",
    sunMoonTitle: "Sun & Moon Timings",
    labelTimeSunrise: "Sunrise",
    labelTimeSunset: "Sunset",
    labelTimeBrahma: "Brahma Muhurtham",
    labelTimeMidday: "Midday (Madhyahna)",
    labelTimePratah: "Pratah Sandhya",
    labelTimeSayan: "Sayan Sandhya",
    labelTimeMoonrise: "Moonrise",
    labelTimeMoonset: "Moonset",
    labelTimeMoonPhase: "Moon Phase:",
    muhurthasTitle: "Auspicious & Inauspicious Periods",
    labelAbhijit: "Abhijit Muhurtham",
    labelAmrita: "Amrita Kalam",
    labelRahu: "Rahu Kalam",
    labelYama: "Yama Gandam",
    labelGulika: "Gulika Kalam",
    labelDurmuhurtham: "Durmuhurtham",
    labelVarjyam: "Varjyam",
    lagnasTitle: "24-Hour Lagna Schedule (Ascendants)",
    festivalsTitle: "Festivals & Vratas",
    monthlyGridTitle: "Monthly Calendar Grid",
    monthlyHint: "Click on any date to view detailed Panchangam",
    calDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    sankalpaTitle: "🪔 Vedic Deśa-Kāla Sankalpa",
    sankalpaSubtitle: "Classical, authoritative Sankalpa crafted with your exact global geographic coordinates and sidereal celestial alignment.",
    labelGotra: "Your Gotra:",
    sankalpaGotraPlaceholder: "e.g. Kashyapa, Bharadwaja, Kaundinya...",
    labelSharma: "Your Name / Sharma:",
    sankalpaSharmaPlaceholder: "e.g. Rama Sharma...",
    labelDeity: "Family Deity / Ishta Devata:",
    sankalpaDeityPlaceholder: "e.g. Sri Venkateswara Swamy...",
    sankalpaSubmitBtn: "Generate Sankalpa",
    sankalpaLangBadge: "Sankalpa Mantra (English Transliteration)",
    sankalpaSaBadge: "मूल-संस्कृत-सङ्कल्पः (Original Sanskrit Devanagari)",
    copyBtnText: "Copy",
    copied: "Copied! ✔️",
    endLabel: "End:",
    nextDayLabel: "Next Day",
    fullDay: "Full Day",
    pushkaraLabel: "Pushkara Navamsha",
    pada: "Pada",
    timeSpanLabel: "Time",
    noAbhijit: "None today",
    noVarjyam: "No Varjyam",
    noFestivals: "No major festival for today.",
    noLagnas: "Lagna details not available.",
    loaderText: "Loading Panchangam details...",
    geoCoordLabel: "Geographic Location",
    dveepaLabel: "Dveepa",
    khandaLabel: "Khanda"
  },
  devanagari: {
    appTitle: "वैदिक संहिता • पञ्चाङ्गम्",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ सिद्धान्तकार:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">रामचन्द्र शास्त्री मुनिमडुगु</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ निर्माता: रामचन्द्र शास्त्री मुनिमडुगु",
    dailyTab: "दैनिक पञ्चाङ्ग",
    monthlyTab: "मासिक पञ्चाङ्ग",
    sankalpaTab: "वैदिक सङ्कल्प",
    rashiTab: "राशि फल",
    intercalaryTab: "अधिक / क्षय मास",
    kandadayamTab: "कन्ददाय फलानि",
    rashiDaily: "☀️ दैनिक राशिफल",
    rashiMonthly: "🌙 मासिक राशिफल",
    rashiYearly: "🪐 वार्षिक राशिफल",
    rashiSelectPrompt: "✨ अपनी राशि चुनें",
    searchPlaceholder: "नगर खोजें (उदा: Frisco, Kashi, Delhi)...",
    gpsBtn: "मेरा स्थान",
    todayBtn: "आज",
    heroEra: "प्रभवादि षष्टि संवत्सर",
    heroVaraLabel: "वार",
    angasTitle: "पञ्चाङ्गम्",
    samvatsaraLabel: "संवत्सर",
    ayanaLabel: "अयन",
    rituLabel: "ऋतु",
    masaLabel: "मास",
    pakshaLabel: "पक्ष",
    tithi: "तिथि",
    vara: "वार",
    nakshatra: "नक्षत्र",
    yoga: "योग",
    karana: "करण",
    chandramanaTitle: "चान्द्रमान (Lunar Calendar)",
    labelCmAmanta: "अमान्त मास:",
    labelCmPurnimanta: "पूर्णिमान्त मास:",
    labelCmPaksha: "पक्ष:",
    sauramanaTitle: "सौरमान (Solar Calendar)",
    labelSmSolarMonth: "सौर राशि/मास:",
    labelSmTamil: "तमिल मास:",
    labelSmMalayalam: "मलयालम कोल्लम:",
    labelSmSankranti: "संक्रान्ति:",
    barhaspatyamanaTitle: "बार्हस्पत्यमान (Jovian Calendar)",
    labelBmRashi: "गुरु राशि:",
    labelBmNakshatra: "नक्षत्र:",
    labelBmStatus: "गति:",
    labelBmMahaMasa: "महा-मास:",
    labelBmPushkaram: "पुष्कर नदी:",
    sunMoonTitle: "सूर्योदय एवं चन्द्रोदय समय",
    labelTimeSunrise: "सूर्योदय",
    labelTimeSunset: "सूर्यास्त",
    labelTimeBrahma: "ब्रह्म मुहूर्त",
    labelTimeMidday: "मध्याह्न",
    labelTimePratah: "प्रातः सन्ध्या",
    labelTimeSayan: "सायं सन्ध्या",
    labelTimeMoonrise: "चन्द्रोदय",
    labelTimeMoonset: "चन्द्रास्त",
    labelTimeMoonPhase: "चन्द्र कला:",
    muhurthasTitle: "शुभ एवं अशुभ मुहूर्त",
    labelAbhijit: "अभिजित् मुहूर्त",
    labelAmrita: "अमृत काल",
    labelRahu: "राहुकाल",
    labelYama: "यमगण्ड",
    labelGulika: "गुलिक काल",
    labelDurmuhurtham: "दुर्मुहूर्त",
    labelVarjyam: "वर्ज्यम्",
    lagnasTitle: "२४-घंटे लग्न सारणी (Daily Lagnas)",
    festivalsTitle: "आज के पर्व एवं व्रत",
    monthlyGridTitle: "मासिक पञ्चाङ्ग (Monthly Grid)",
    monthlyHint: "किसी भी तिथि पर क्लिक करके उस दिन का पञ्चाङ्ग देखें",
    calDays: ["रवि", "सोम", "मङ्गल", "बुध", "गुरु", "शुक्र", "शनि"],
    sankalpaTitle: "🪔 वैदिक देश-काल सङ्कल्प",
    sankalpaSubtitle: "पूजा, हवन एवं व्रतों के लिए आपकी भौगोलिक स्थिति एवं खगोलीय काल-गणना से सुसज्जित शास्त्रीय सङ्कल्प।",
    labelGotra: "आपका गोत्र:",
    sankalpaGotraPlaceholder: "उदा: काश्यप, भारद्वाज, कौण्डिन्य...",
    labelSharma: "आपका नाम / शर्मा:",
    sankalpaSharmaPlaceholder: "उदा: राम शर्मा...",
    labelDeity: "इष्टदेव / कुलदेवता:",
    sankalpaDeityPlaceholder: "उदा: श्री वेङ्कटेश्वर स्वामी...",
    sankalpaSubmitBtn: "सङ्कल्प बनाएं",
    sankalpaLangBadge: "सङ्कल्प मन्त्र (देवनागरी)",
    sankalpaSaBadge: "मूल-संस्कृत-सङ्कल्पः (Original Sanskrit Devanagari)",
    copyBtnText: "कॉपी करें",
    copied: "कॉपी हो गया! ✔️",
    endLabel: "समाप्ति:",
    nextDayLabel: "अगले दिन",
    fullDay: "दिनभर",
    pushkaraLabel: "पुष्करांश",
    pada: "पाद",
    timeSpanLabel: "समय",
    noAbhijit: "आज नहीं है",
    noVarjyam: "वर्ज्य नहीं है",
    noFestivals: "आज कोई विशेष पर्व नहीं है।",
    noLagnas: "लग्न विवरण उपलब्ध नहीं है।",
    loaderText: "पञ्चाङ्ग विवरण लोड हो रहा है...",
    geoCoordLabel: "भौगोलिक स्थिति",
    dveepaLabel: "द्वीप",
    khandaLabel: "खण्ड"
  },
  tamil: {
    appTitle: "வேத சம்ஹிதை • பஞ்சாங்கம்",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ கணிப்பாளர்:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">ராமசந்திர சாஸ்திரி முனிமடுகு</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ உருவாக்கியவர்: ராமசந்திர சாஸ்திரி முனிமடுகு",
    dailyTab: "தினசரி பஞ்சாங்கம்",
    monthlyTab: "மாதாந்திர காலண்டர்",
    sankalpaTab: "வைதிக சங்கல்பம்",
    rashiTab: "ராசி பலன்",
    intercalaryTab: "அதிக / க்ஷய மாதங்கள்",
    kandadayamTab: "கந்ததாய பலன்கள்",
    rashiDaily: "☀️ தினசரி ராசிபலன்",
    rashiMonthly: "🌙 மாத ராசிபலன்",
    rashiYearly: "🪐 வருடாந்திர ராசிபலன்",
    rashiSelectPrompt: "✨ உங்கள் ராசியைத் தேர்ந்தெடுக்கவும்",
    searchPlaceholder: "நகரத்தைத் தேடுங்கள் (எ.கா: Frisco, Chennai)...",
    gpsBtn: "என் இடம்",
    todayBtn: "இன்று",
    heroEra: "பிரபவாதி 60 வருடம்",
    heroVaraLabel: "வாரம்",
    angasTitle: "பஞ்சாங்கம்",
    samvatsaraLabel: "வருடம்",
    ayanaLabel: "அயனம்",
    rituLabel: "ருது",
    masaLabel: "மாதம்",
    pakshaLabel: "பட்சம்",
    tithi: "திதி",
    vara: "வாரம்",
    nakshatra: "நட்சத்திரம்",
    yoga: "யோகம்",
    karana: "கரணம்",
    chandramanaTitle: "சாந்திரமானம் (Lunar Calendar)",
    labelCmAmanta: "அமாந்த மாதம்:",
    labelCmPurnimanta: "பூர்ணிமாந்த மாதம்:",
    labelCmPaksha: "பட்சம்:",
    sauramanaTitle: "சௌரமானம் (Solar Calendar)",
    labelSmSolarMonth: "சூரிய ராசி/மாதம்:",
    labelSmTamil: "தமிழ் மாதம்:",
    labelSmMalayalam: "மலையாள கொல்லம்:",
    labelSmSankranti: "சங்கிராந்தி:",
    barhaspatyamanaTitle: "பார்ஹஸ்பத்யமானம் (Jovian Calendar)",
    labelBmRashi: "குரு ராசி:",
    labelBmNakshatra: "நட்சத்திரம்:",
    labelBmStatus: "கதி:",
    labelBmMahaMasa: "மகா-மாதம்:",
    labelBmPushkaram: "புஷ்கர நதி:",
    sunMoonTitle: "சூரியோதயம் மற்றும் சந்திரோதய நேரம்",
    labelTimeSunrise: "சூரியோதயம்",
    labelTimeSunset: "சூரியாஸ்தமனம்",
    labelTimeBrahma: "பிரம்ம முகூர்த்தம்",
    labelTimeMidday: "நண்பகல்",
    labelTimePratah: "பிராத சந்தியா",
    labelTimeSayan: "சாயங்கால சந்தியா",
    labelTimeMoonrise: "சந்திரோதயம்",
    labelTimeMoonset: "சந்திராஸ்தமனம்",
    labelTimeMoonPhase: "சந்திர நிலை:",
    muhurthasTitle: "முகூர்த்தங்கள் மற்றும் வர்ஜ்ய காலங்கள்",
    labelAbhijit: "அபிஜித் முகூர்த்தம்",
    labelAmrita: "அமிர்த காலம்",
    labelRahu: "இராகு காலம்",
    labelYama: "எமகண்டம்",
    labelGulika: "குளிகை காலம்",
    labelDurmuhurtham: "துர்முகூர்த்தம்",
    labelVarjyam: "வர்ஜ்யம்",
    lagnasTitle: "24 மணி நேர லக்ன அட்டவணை (Daily Lagnas)",
    festivalsTitle: "இன்றைய பண்டிகைகள் மற்றும் விரதங்கள்",
    monthlyGridTitle: "மாதாந்திர காலண்டர் (Monthly Grid)",
    monthlyHint: "தினசரி பஞ்சாங்க விவரங்களைக் காண எந்த தேதியையும் கிளிக் செய்யவும்",
    calDays: ["ஞாயிறு", "திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்", "வெள்ளி", "சனி"],
    sankalpaTitle: "🪔 வைதிக தேச-கால சங்கல்பம் (Vedic Deśa-Kāla Sankalpa)",
    sankalpaSubtitle: "பூஜை, ஹோமம் மற்றும் விரதங்களுக்காக உங்கள் புவியியல் இருப்பிடத்திற்கேற்ப வடிவமைக்கப்பட்ட சாஸ்திர சங்கல்பம்.",
    labelGotra: "உங்கள் கோத்திரம்:",
    sankalpaGotraPlaceholder: "எ.கா: காஷ்யப, பரத்வாஜ, கௌண்டின்ய...",
    labelSharma: "உங்கள் பெயர் / சர்மா:",
    sankalpaSharmaPlaceholder: "எ.கா: ராம சர்மா...",
    labelDeity: "வழிபடும் தெய்வம் / குலதெய்வம்:",
    sankalpaDeityPlaceholder: "எ.கா: ஸ்ரீ வெங்கடேஸ்வர சுவாமி...",
    sankalpaSubmitBtn: "சங்கல்பத்தை உருவாக்கவும்",
    sankalpaLangBadge: "சங்கல்ப மந்திரம் (தமிழ் எழுத்துக்களில்)",
    sankalpaSaBadge: "மூல-சமஸ்கிருத-சங்கல்பம் (Original Sanskrit Devanagari)",
    copyBtnText: "நகலெடு",
    copied: "நகலெடுக்கப்பட்டது! ✔️",
    endLabel: "முடிவு:",
    nextDayLabel: "அடுத்த நாள்",
    fullDay: "நாள் முழுவதும்",
    pushkaraLabel: "புஷ்கராம்சம்",
    pada: "பாதம்",
    timeSpanLabel: "நேரம்",
    noAbhijit: "இன்று இல்லை",
    noVarjyam: "வர்ஜ்யம் இல்லை",
    noFestivals: "இன்று சிறப்பு பண்டிகைகள் ஏதுமில்லை.",
    noLagnas: "லக்ன விவரங்கள் கிடைக்கவில்லை.",
    loaderText: "பஞ்சாங்க விவரங்கள் ஏற்றப்படுகின்றன...",
    geoCoordLabel: "புவியியல் இருப்பிடம்",
    dveepaLabel: "த்வீபம்",
    khandaLabel: "கண்டம்"
  },
  kannada: {
    appTitle: "ವೇದ ಸಂಹಿತಾ • ಪಂಚಾಂಗ",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ ಸಿದ್ಧಾಂತಕರ್ತ:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">ರಾಮಚಂದ್ರ ಶಾಸ್ತ್ರಿ ಮುನಿಮಡುಗು</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ ಕರ್ತೃ: ರಾಮಚಂದ್ರ ಶಾಸ್ತ್ರಿ ಮುನಿಮಡುಗು",
    dailyTab: "ದೈನಂದಿನ ಪಂಚಾಂಗ",
    monthlyTab: "ಮಾಸಿಕ ಕ್ಯಾಲೆಂಡರ್",
    sankalpaTab: "ವೈದಿಕ ಸಂಕಲ್ಪ",
    rashiTab: "ರಾಶಿ ಫಲ",
    intercalaryTab: "ಅಧಿಕ / ಕ್ಷಯ ಮಾಸಗಳು",
    kandadayamTab: "ಕಂದದಾಯ ಫಲಗಳು",
    rashiDaily: "☀️ ದಿನ ಭವಿಷ್ಯ",
    rashiMonthly: "🌙 ಮಾಸಿಕ ಭವಿಷ್ಯ",
    rashiYearly: "🪐 ವಾರ್ಷಿಕ ಭವಿಷ್ಯ",
    rashiSelectPrompt: "✨ ನಿಮ್ಮ ರಾಶಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    searchPlaceholder: "ನಗರವನ್ನು ಹುಡುಕಿ (ಉದಾ: Frisco, Bengaluru)...",
    gpsBtn: "ನನ್ನ ಸ್ಥಳ",
    todayBtn: "ಇಂದು",
    heroEra: "ಪ್ರಭವಾದಿ 60 ಸಂವತ್ಸರ",
    heroVaraLabel: "ವಾರ",
    angasTitle: "ಪಂಚಾಂಗ",
    samvatsaraLabel: "ಸಂವತ್ಸರ",
    ayanaLabel: "ಅಯನ",
    rituLabel: "ಋತು",
    masaLabel: "ಮಾಸ",
    pakshaLabel: "ಪಕ್ಷ",
    tithi: "ತಿಥಿ",
    vara: "ವಾರ",
    nakshatra: "ನಕ್ಷತ್ರ",
    yoga: "ಯೋಗ",
    karana: "ಕರಣ",
    chandramanaTitle: "ಚಾಂದ್ರಮಾನ (Lunar Calendar)",
    labelCmAmanta: "ಅಮಾಂತ ಮಾಸ:",
    labelCmPurnimanta: "ಪೂರ್ಣಿಮಾಂತ ಮಾಸ:",
    labelCmPaksha: "ಪಕ್ಷ:",
    sauramanaTitle: "ಸೌರಮಾನ (Solar Calendar)",
    labelSmSolarMonth: "ಸೌರ ರಾಶಿ/ಮಾಸ:",
    labelSmTamil: "ತಮಿಳು ಮಾಸ:",
    labelSmMalayalam: "ಮಲಯಾಳಂ ಕೊಲ್ಲಂ:",
    labelSmSankranti: "ಸಂಕ್ರಾಂತಿ:",
    barhaspatyamanaTitle: "ಬಾರ್ಹಸ್ಪತ್ಯಮಾನ (Jovian Calendar)",
    labelBmRashi: "ಗುರು ರಾಶಿ:",
    labelBmNakshatra: "ನಕ್ಷತ್ರ:",
    labelBmStatus: "ಗತಿ:",
    labelBmMahaMasa: "ಮಹಾ-ಮಾಸ:",
    labelBmPushkaram: "ಪುಷ್ಕರ ನದಿ:",
    sunMoonTitle: "ಸೂರ್ಯೋದಯ ಮತ್ತು ಚಂದ್ರೋದಯ ಸಮಯ",
    labelTimeSunrise: "ಸೂರ್ಯೋದಯ",
    labelTimeSunset: "ಸೂರ್ಯಾಸ್ತ",
    labelTimeBrahma: "ಬ್ರಹ್ಮ ಮುಹೂರ್ತ",
    labelTimeMidday: "ಮಧ್ಯಾಹ್ನ",
    labelTimePratah: "ಪ್ರಾತಃ ಸಂಧ್ಯಾ",
    labelTimeSayan: "ಸಾಯಂ ಸಂಧ್ಯಾ",
    labelTimeMoonrise: "ಚಂದ್ರೋದಯ",
    labelTimeMoonset: "ಚಂದ್ರಾಸ್ತ",
    labelTimeMoonPhase: "ಚಂದ್ರ ಸ್ಥಿತಿ:",
    muhurthasTitle: "ಮುಹೂರ್ತಗಳು ಮತ್ತು ವರ್ಜ್ಯ ಕಾಲಗಳು",
    labelAbhijit: "ಅಭಿಜಿತ್ ಮುಹೂರ್ತ",
    labelAmrita: "ಅಮೃತ ಕಾಲ",
    labelRahu: "ರಾಹುಕಾಲ",
    labelYama: "ಯಮಗಂಡ",
    labelGulika: "ಗುಳಿಕ ಕಾಲ",
    labelDurmuhurtham: "ದುರ್ಮುಹೂರ್ತ",
    labelVarjyam: "ವರ್ಜ್ಯ",
    lagnasTitle: "24-ಗಂಟೆಗಳ ಲಗ್ನ ಕೋಷ್ಟಕ (Daily Lagnas)",
    festivalsTitle: "ಇಂದಿನ ಹಬ್ಬಗಳು ಮತ್ತು ವ್ರತಗಳು",
    monthlyGridTitle: "ಮಾಸಿಕ ಕ್ಯಾಲೆಂಡರ್ (Monthly Grid)",
    monthlyHint: "ದೈನಂದಿನ ಪಂಚಾಂಗ ವಿವರಗಳನ್ನು ತೆರೆಯಲು ಯಾವುದೇ ದಿನಾಂಕವನ್ನು ಕ್ಲಿಕ್ ಮಾಡಿ",
    calDays: ["ಭಾನು", "ಸೋಮ", "ಮಂಗಳ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ"],
    sankalpaTitle: "🪔 ವೈದಿಕ ದೇಶ-ಕಾಲ ಸಂಕಲ್ಪ (Vedic Deśa-Kāla Sankalpa)",
    sankalpaSubtitle: "ಪೂಜೆ, ಹೋಮ, ವ್ರತಗಳಿಗಾಗಿ ನಿಮ್ಮ ಭೌಗೋಳಿಕ ನಿರ್ದೇಶಾಂಕಗಳು ಮತ್ತು ಖಗೋಳ ಕಾಲಕ್ಕೆ ಅನುಗುಣವಾಗಿ ರೂಪಿಸಲಾದ ಶಾಸ್ತ್ರೀಯ ಸಂಕಲ್ಪ.",
    labelGotra: "ನಿಮ್ಮ ಗೋತ್ರ:",
    sankalpaGotraPlaceholder: "ಉದಾ: ಕಾಶ್ಯಪ, ಭಾರದ್ವಾಜ, ಕೌಂಡಿನ್ಯ...",
    labelSharma: "ನಿಮ್ಮ ಹೆಸರು / ಶರ್ಮ:",
    sankalpaSharmaPlaceholder: "ಉದಾ: ರಾಮ ಶರ್ಮ...",
    labelDeity: "ಪೂಜಿಸುವ ದೇವರು / ಕುಲದೇವರು:",
    sankalpaDeityPlaceholder: "ಉದಾ: ಶ್ರೀ ವೇಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ...",
    sankalpaSubmitBtn: "ಸಂಕಲ್ಪ ಸಿದ್ಧಪಡಿಸಿ",
    sankalpaLangBadge: "ಸಂಕಲ್ಪ ಮಂತ್ರ (ಕನ್ನಡದಲ್ಲಿ)",
    sankalpaSaBadge: "ಮೂಲ-ಸಂಸ್ಕೃತ-ಸಂಕಲ್ಪಃ (Original Sanskrit Devanagari)",
    copyBtnText: "ಕಾಪಿ ಮಾಡಿ",
    copied: "ಕಾಪಿ ಮಾಡಲಾಗಿದೆ! ✔️",
    endLabel: "ಮುಕ್ತಾಯ:",
    nextDayLabel: "ಮರುದಿನ",
    fullDay: "ದಿನವಿಡೀ",
    pushkaraLabel: "ಪುಷ್ಕರಾಂಶ",
    pada: "ಪಾದ",
    timeSpanLabel: "ಸಮಯ",
    noAbhijit: "ಇಂದು ಇಲ್ಲ",
    noVarjyam: "ವರ್ಜ್ಯವಿಲ್ಲ",
    noFestivals: "ಇಂದು ಯಾವುದೇ ಪ್ರಮುಖ ಹಬ್ಬಗಳಿಲ್ಲ.",
    noLagnas: "ಲಗ್ನ ವಿವರಗಳು ಲಭ್ಯವಿಲ್ಲ.",
    loaderText: "ಪಂಚಾಂಗ ವಿವರಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ...",
    geoCoordLabel: "ಭೌಗೋಳಿಕ ಸ್ಥಾನ",
    dveepaLabel: "ದ್ವೀಪ",
    khandaLabel: "ಖಂಡ"
  },
  malayalam: {
    appTitle: "വേദ സംഹിത • പഞ്ചാംഗം",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ സിദ്ധാന്തകാരൻ:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">രാമചന്ദ്ര ശാസ്ത്രി മുനിമഡുഗു</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ നിർമ്മാതാവ്: രാമചന്ദ്ര ശാസ്ത്രി മുനിമഡുഗു",
    dailyTab: "ദിവസേന പഞ്ചാംഗം",
    monthlyTab: "മാസ കലണ്ടർ",
    sankalpaTab: "വൈദിക സങ്കൽപ്പം",
    rashiTab: "രാശി ഫലം",
    intercalaryTab: "അധിക / ക്ഷയ മാസങ്ങൾ",
    kandadayamTab: "കന്ദദായ ഫലങ്ങൾ",
    rashiDaily: "☀️ ദിവസേന രാശിഫലം",
    rashiMonthly: "🌙 പ്രതിമാസ രാശിഫലം",
    rashiYearly: "🪐 വാർഷിക രാശിഫലം",
    rashiSelectPrompt: "✨ നിങ്ങളുടെ രാശി തിരഞ്ഞെടുക്കുക",
    searchPlaceholder: "നഗരം തിരയുക (ഉദാ: Frisco, Kochi)...",
    gpsBtn: "എന്റെ സ്ഥലം",
    todayBtn: "ഇന്ന്",
    heroEra: "പ്രഭവാദി 60 സംവത്സരം",
    heroVaraLabel: "വാരം",
    angasTitle: "പഞ്ചാംഗം",
    samvatsaraLabel: "സംവത്സരം",
    ayanaLabel: "അയനം",
    rituLabel: "ഋതു",
    masaLabel: "മാസം",
    pakshaLabel: "പക്ഷം",
    tithi: "തിഥി",
    vara: "വാരം",
    nakshatra: "നക്ഷത്രം",
    yoga: "യോഗം",
    karana: "കരണം",
    chandramanaTitle: "ചാന്ദ്രമാനം (Lunar Calendar)",
    labelCmAmanta: "അമാന്ത മാസം:",
    labelCmPurnimanta: "പൂർണ്ണിമാന്ത മാസം:",
    labelCmPaksha: "പക്ഷം:",
    sauramanaTitle: "സൗരമാനം (Solar Calendar)",
    labelSmSolarMonth: "സൗര രാശി/മാസം:",
    labelSmTamil: "തമിഴ് മാസം:",
    labelSmMalayalam: "മലയാളം കൊല്ലം:",
    labelSmSankranti: "സംക്രാന്തി:",
    barhaspatyamanaTitle: "ബാർഹസ്പത്യമാനം (Jovian Calendar)",
    labelBmRashi: "ഗുരു രാശി:",
    labelBmNakshatra: "നക്ഷത്രം:",
    labelBmStatus: "ഗതി:",
    labelBmMahaMasa: "മഹാ-മാസം:",
    labelBmPushkaram: "പുഷ്കര നദി:",
    sunMoonTitle: "സൂര്യോദയവും ചന്ദ്രോദയ സമയവും",
    labelTimeSunrise: "സൂര്യോദയം",
    labelTimeSunset: "സൂര്യാസ്തമയം",
    labelTimeBrahma: "ബ്രഹ്മ മുഹൂർത്തം",
    labelTimeMidday: "മദ്ധ്യാഹ്നം",
    labelTimePratah: "പ്രാതഃ സന്ധ്യ",
    labelTimeSayan: "സായം സന്ധ്യ",
    labelTimeMoonrise: "ചന്ദ്രോദയം",
    labelTimeMoonset: "ചന്ദ്രാസ്തമയം",
    labelTimeMoonPhase: "ചന്ദ്ര അവസ്ഥ:",
    muhurthasTitle: "മുഹൂർത്തങ്ങളും വർജ്യ കാലങ്ങളും",
    labelAbhijit: "അഭിജിത്ത് മുഹൂർത്തം",
    labelAmrita: "അമൃത കാലം",
    labelRahu: "രാഹുകാലം",
    labelYama: "യമഗണ്ഡം",
    labelGulika: "ഗുളിക കാലം",
    labelDurmuhurtham: "ദുർമുഹൂർത്തം",
    labelVarjyam: "വർജ്യം",
    lagnasTitle: "24-മണിക്കൂർ ലഗ്ന പട്ടിക (Daily Lagnas)",
    festivalsTitle: "ഇന്നത്തെ ഉത്സവങ്ങളും വ്രതങ്ങളും",
    monthlyGridTitle: "മാസ കലണ്ടർ (Monthly Grid)",
    monthlyHint: "ദിവസേന പഞ്ചാംഗ വിവരങ്ങൾ കാണാൻ ഏതെങ്കിലും തീയതിയിൽ ക്ലിക്ക് ചെയ്യുക",
    calDays: ["ഞായർ", "തിങ്കൾ", "ചൊവ്വ", "ബുധൻ", "വ്യാഴം", "വെള്ളി", "ശനി"],
    sankalpaTitle: "🪔 വൈദിക ദേശ-കാല സങ്കൽപ്പം (Vedic Deśa-Kāla Sankalpa)",
    sankalpaSubtitle: "പൂജ, ഹോമം, വ്രതങ്ങൾ എന്നിവയ്ക്കായി നിങ്ങളുടെ ഭൂമിശാസ്ത്രപരമായ സ്ഥാനവും കാലഗണനയും അനുസരിച്ച് തയ്യാറാക്കിയ ശാസ്ത്രീയ സങ്കൽപ്പം.",
    labelGotra: "നിങ്ങളുടെ ഗോത്രം:",
    sankalpaGotraPlaceholder: "ഉദാ: കാശ്യപ, ഭാരദ്വാജ, കൗണ്ഡിന്യ...",
    labelSharma: "നിങ്ങളുടെ പേര് / ശർമ്മ:",
    sankalpaSharmaPlaceholder: "ഉദാ: രാമ ശർമ്മ...",
    labelDeity: "ഇഷ്ടദേവൻ / കുലദൈവം:",
    sankalpaDeityPlaceholder: "ഉദാ: ശ്രീ വെങ്കടേശ്വര സ്വാമി...",
    sankalpaSubmitBtn: "സങ്കൽപ്പം തയ്യാറാക്കുക",
    sankalpaLangBadge: "സങ്കൽപ്പ മന്ത്രം (മലയാളത്തിൽ)",
    sankalpaSaBadge: "മൂല-സംസ്കൃത-സങ്കൽപ്പഃ (Original Sanskrit Devanagari)",
    copyBtnText: "പകർപ്പുക",
    copied: "പകർത്തി! ✔️",
    endLabel: "സമാപ്തി:",
    nextDayLabel: "അടുത്ത ദിവസം",
    fullDay: "മുഴുവൻ ദിവസം",
    pushkaraLabel: "പുഷ്കരാംശം",
    pada: "പാദം",
    timeSpanLabel: "സമയം",
    noAbhijit: "ഇന്ന് ഇല്ല",
    noVarjyam: "വർജ്യം ഇല്ല",
    noFestivals: "ഇന്ന് പ്രത്യേക ഉത്സവങ്ങളൊന്നുമില്ല.",
    noLagnas: "ലഗ്ന വിവരങ്ങൾ ലഭ്യമല്ല.",
    loaderText: "പഞ്ചാംഗ വിവരങ്ങൾ ലോഡ് ചെയ്യുന്നു...",
    geoCoordLabel: "ഭൂമിശാസ്ത്രപരമായ സ്ഥാനം",
    dveepaLabel: "ദ്വീപ്",
    khandaLabel: "ഖണ്ഡം"
  },
  gujarati: {
    appTitle: "વૈદિક સંહિતા • પંચાંગ",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ સિદ્ધાંતકર્તા:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">રામચંદ્ર શાસ્ત્રી મુનિમડુગુ</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ નિર્માતા: રામચંદ્ર શાસ્ત્રી મુનિમડુગુ",
    dailyTab: "દૈનિક પંચાંગ",
    monthlyTab: "માસિક કેલેન્ડર",
    sankalpaTab: "વૈદિક સંકલ્પ",
    rashiTab: "રાશિ ફળ",
    intercalaryTab: "અધિક / ક્ષય માસ",
    kandadayamTab: "કંદદાય ફળ",
    rashiDaily: "☀️ દૈનિક રાશિફળ",
    rashiMonthly: "🌙 માસિક રાશિફળ",
    rashiYearly: "🪐 વાર્ષિક રાશિફળ",
    rashiSelectPrompt: "✨ તમારી રાશિ પસંદ કરો",
    searchPlaceholder: "શહેર શોધો (દા.ત: Frisco, Ahmedabad)...",
    gpsBtn: "મારું સ્થાન",
    todayBtn: "આજે",
    heroEra: "પ્રભવાદિ 60 સંવત્સર",
    heroVaraLabel: "વાર",
    angasTitle: "પંચાંગ",
    samvatsaraLabel: "સંવત્સર",
    ayanaLabel: "અયન",
    rituLabel: "ઋતુ",
    masaLabel: "માસ",
    pakshaLabel: "પક્ષ",
    tithi: "તિથિ",
    vara: "વાર",
    nakshatra: "નક્ષત્ર",
    yoga: "યોગ",
    karana: "કરણ",
    chandramanaTitle: "ચાંદ્રમાન (Lunar Calendar)",
    labelCmAmanta: "અમાંત માસ:",
    labelCmPurnimanta: "પૂર્ણિમાંત માસ:",
    labelCmPaksha: "પક્ષ:",
    sauramanaTitle: "સૌરમાન (Solar Calendar)",
    labelSmSolarMonth: "સૌર રાશિ/માસ:",
    labelSmTamil: "તમિલ માસ:",
    labelSmMalayalam: "મલયાલમ કોલ્લમ:",
    labelSmSankranti: "સંક્રાંતિ:",
    barhaspatyamanaTitle: "બાર્હસ્પત્યમાન (Jovian Calendar)",
    labelBmRashi: "ગુરુ રાશિ:",
    labelBmNakshatra: "નક્ષત્ર:",
    labelBmStatus: "ગતિ:",
    labelBmMahaMasa: "મહા-માસ:",
    labelBmPushkaram: "પુષ્કર નદી:",
    sunMoonTitle: "સૂર્યોદય અને ચંદ્રોદય સમય",
    labelTimeSunrise: "સૂર્યોદય",
    labelTimeSunset: "સૂર્યાસ્ત",
    labelTimeBrahma: "બ્રહ્મ મુહૂર્ત",
    labelTimeMidday: "મધ્યાહ્ન",
    labelTimePratah: "પ્રાતઃ સંધ્યા",
    labelTimeSayan: "સાયં સંધ્યા",
    labelTimeMoonrise: "ચંદ્રોદય",
    labelTimeMoonset: "ચંદ્રાસ્ત",
    labelTimeMoonPhase: "ચંદ્ર કલા:",
    muhurthasTitle: "મુહૂર્ત અને વર્જ્ય કાળ",
    labelAbhijit: "અભિજિત મુહૂર્ત",
    labelAmrita: "અમૃત કાળ",
    labelRahu: "રાહુકાળ",
    labelYama: "યમગંડ",
    labelGulika: "ગુલિક કાળ",
    labelDurmuhurtham: "દુર્મુહૂર્ત",
    labelVarjyam: "વર્જ્ય",
    lagnasTitle: "24 કલાક લગ્ન સમયપત્રક (Daily Lagnas)",
    festivalsTitle: "આજના તહેવારો અને વ્રત",
    monthlyGridTitle: "માસિક કેલેન્ડર (Monthly Grid)",
    monthlyHint: "દૈનિક પંચાંગ વિગતો ખોલવા માટે કોઈપણ તારીખ પર ક્લિક કરો",
    calDays: ["રવિ", "સોમ", "મંગળ", "બુધ", "ગુરુ", "શુક્ર", "શનિ"],
    sankalpaTitle: "🪔 વૈદિક દેશ-કાળ સંકલ્પ (Vedic Deśa-Kāla Sankalpa)",
    sankalpaSubtitle: "પૂજા, હવન અને વ્રત માટે તમારા ભૌગોલિક સ્થાન અને ખગોળીય સમય અનુસાર તૈયાર કરાયેલ શાસ્ત્રીય સંકલ્પ.",
    labelGotra: "તમારું ગોત્ર:",
    sankalpaGotraPlaceholder: "દા.ત: કાશ્યપ, ભારદ્વાજ, કૌંડિન્ય...",
    labelSharma: "તમારું નામ / શર્મા:",
    sankalpaSharmaPlaceholder: "દા.ત: રામ શર્મા...",
    labelDeity: "ઇષ્ટદેવ / કુલદેવતા:",
    sankalpaDeityPlaceholder: "દા.ત: શ્રી વેંકટેશ્વર સ્વામી...",
    sankalpaSubmitBtn: "સંકલ્પ તૈયાર કરો",
    sankalpaLangBadge: "સંકલ્પ મંત્ર (ગુજરાતીમાં)",
    sankalpaSaBadge: "મૂળ-સંસ્કૃત-સંકલ્પઃ (Original Sanskrit Devanagari)",
    copyBtnText: "કૉપિ કરો",
    copied: "કૉપિ થઈ ગયું! ✔️",
    endLabel: "સમાપ્તિ:",
    nextDayLabel: "બીજા દિવસે",
    fullDay: "આખો દિવસ",
    pushkaraLabel: "પુષ્કરાંશ",
    pada: "પાદ",
    timeSpanLabel: "સમય",
    noAbhijit: "આજે નથી",
    noVarjyam: "વર્જ્ય નથી",
    noFestivals: "આજે કોઈ વિશેષ તહેવાર નથી.",
    noLagnas: "લગ્ન વિગતો ઉપલબ્ધ નથી.",
    loaderText: "પંચાંગ વિગતો લોડ થઈ રહી છે...",
    geoCoordLabel: "ભૌગોલિક સ્થાન",
    dveepaLabel: "દ્વીપ",
    khandaLabel: "ખંડ"
  },
  bengali: {
    appTitle: "বৈদিক সংহিতা • পঞ্চাঙ্গ",
    appSubtitle: "Vedic Astronomy & Dharma Shastra Computation System • www.vedicsamhita.com",
    headerCreatorCreditHtml: '<span>✨ সিদ্ধান্তকার:</span> <span class="text-white font-extrabold tracking-wide drop-shadow">রামচন্দ্র শাস্ত্রী মুনিমডুগু</span> <span class="text-[10px] text-amber-200/80 font-normal hidden sm:inline">(RAMACHANDRA SASTRY MUNIMADUGU)</span>',
    heroAuthor: "✍️ নির্মাতা: রামচন্দ্র শাস্ত্রী মুনিমডুগু",
    dailyTab: "দৈনিক পঞ্চাঙ্গ",
    monthlyTab: "মাসিক ক্যালেন্ডার",
    sankalpaTab: "বৈদিক সংকল্প",
    rashiTab: "রাশি ফল",
    intercalaryTab: "অধিক / ক্ষয় মাস",
    kandadayamTab: "কন্দদায় ফল",
    rashiDaily: "☀️ দৈনিক রাশিফল",
    rashiMonthly: "🌙 মাসিক রাশিফল",
    rashiYearly: "🪐 বার্ষিক রাশিফল",
    rashiSelectPrompt: "✨ আপনার রাশি নির্বাচন করুন",
    searchPlaceholder: "শহর খুঁজুন (যেমন: Frisco, Kolkata)...",
    gpsBtn: "আমার অবস্থান",
    todayBtn: "আজ",
    heroEra: "প্রভবাদি ৬০ সংবৎসর",
    heroVaraLabel: "বার",
    angasTitle: "পঞ্চাঙ্গ",
    samvatsaraLabel: "সংবৎসর",
    ayanaLabel: "অয়ন",
    rituLabel: "ঋতু",
    masaLabel: "মাস",
    pakshaLabel: "পক্ষ",
    tithi: "তিথি",
    vara: "বার",
    nakshatra: "নক্ষত্র",
    yoga: "যোগ",
    karana: "করণ",
    chandramanaTitle: "চন্দ্রমান (Lunar Calendar)",
    labelCmAmanta: "অমান্ত মাস:",
    labelCmPurnimanta: "পূর্ণিমান্ত মাস:",
    labelCmPaksha: "পক্ষ:",
    sauramanaTitle: "সৌরমান (Solar Calendar)",
    labelSmSolarMonth: "সৌর রাশি/মাস:",
    labelSmTamil: "তামিল মাস:",
    labelSmMalayalam: "মালয়ালম কোল্লম:",
    labelSmSankranti: "সংক্রান্তি:",
    barhaspatyamanaTitle: "বার্হস্পত্যমান (Jovian Calendar)",
    labelBmRashi: "বৃহস্পতি রাশি:",
    labelBmNakshatra: "নক্ষত্র:",
    labelBmStatus: "গতি:",
    labelBmMahaMasa: "মহা-মাস:",
    labelBmPushkaram: "পুষ্কর নদী:",
    sunMoonTitle: "সূর্যোদয় ও চন্দ্রোদয় সময়",
    labelTimeSunrise: "সূর্যোদয়",
    labelTimeSunset: "সূর্যাস্ত",
    labelTimeBrahma: "ব্রহ্ম মুহূর্ত",
    labelTimeMidday: "মধ্যাহ্ন",
    labelTimePratah: "প্রাতঃ সন্ধ্যা",
    labelTimeSayan: "সায়ং সন্ধ্যা",
    labelTimeMoonrise: "চন্দ্রোদয়",
    labelTimeMoonset: "চন্দ্রাস্ত",
    labelTimeMoonPhase: "চন্দ্র কলা:",
    muhurthasTitle: "মুহূর্ত ও বর্জ্য সময়",
    labelAbhijit: "অভিজিৎ মুহূর্ত",
    labelAmrita: "অমৃত কাল",
    labelRahu: "রাহুকাল",
    labelYama: "যমগণ্ড",
    labelGulika: "গুলিক কাল",
    labelDurmuhurtham: "দুর্মুহূর্ত",
    labelVarjyam: "বর্জ্য",
    lagnasTitle: "২৪ ঘণ্টার লগ্ন সারণী (Daily Lagnas)",
    festivalsTitle: "আজকের উৎসব ও ব্রত",
    monthlyGridTitle: "মাসিক ক্যালেন্ডার (Monthly Grid)",
    monthlyHint: "দৈনিক পঞ্চাঙ্গ দেখতে যে কোনো তারিখে ক্লিক করুন",
    calDays: ["রবি", "সোম", "মঙ্গল", "বুধ", "বৃহস্পতি", "শুক্র", "শনি"],
    sankalpaTitle: "🪔 বৈদিক দেশ-কাল সংকল্প (Vedic Deśa-Kāla Sankalpa)",
    sankalpaSubtitle: "পূজা, হোম ও ব্রতের জন্য আপনার ভৌগোলিক অবস্থান এবং জ্যোতির্বিজ্ঞানসম্মত সময় অনুসারে প্রণীত বৈদিক সংকল্প।",
    labelGotra: "আপনার গোত্র:",
    sankalpaGotraPlaceholder: "যেমন: কাশ্যপ, ভরদ্বাজ, কৌণ্ডিন্য...",
    labelSharma: "আপনার নাম / শর্মা:",
    sankalpaSharmaPlaceholder: "যেমন: রাম শর্মা...",
    labelDeity: "ইষ্টদেবতা / কুলদেবতা:",
    sankalpaDeityPlaceholder: "যেমন: শ্রী ভেঙ্কটেশ্বর স্বামী...",
    sankalpaSubmitBtn: "সংকল্প প্রস্তুত করুন",
    sankalpaLangBadge: "সংকল্প মন্ত্র (বাংলা হরফে)",
    sankalpaSaBadge: "মূল-সংস্কৃত-সংকল্পঃ (Original Sanskrit Devanagari)",
    copyBtnText: "কপি করুন",
    copied: "কপি হয়েছে! ✔️",
    endLabel: "সমাপ্তি:",
    nextDayLabel: "পরের দিন",
    fullDay: "সারাদিন",
    pushkaraLabel: "পুষ্করাংশ",
    pada: "পাদ",
    timeSpanLabel: "সময়",
    noAbhijit: "আজ নেই",
    noVarjyam: "বর্জ্য নেই",
    noFestivals: "আজ কোন বিশেষ উৎসব নেই।",
    noLagnas: "লগ্ন বিবরণ পাওয়া যায়নি।",
    loaderText: "পঞ্চাঙ্গ বিবরণ লোড হচ্ছে...",
    geoCoordLabel: "ভৌগোলিক অবস্থান",
    dveepaLabel: "দ্বীপ",
    khandaLabel: "খণ্ড"
  }
};

function t(key) {
  const langKey = UI_TEXT[STATE.lang] ? STATE.lang : 'telugu';
  return (UI_TEXT[langKey] && UI_TEXT[langKey][key] !== undefined)
    ? UI_TEXT[langKey][key]
    : ((UI_TEXT['telugu'] && UI_TEXT['telugu'][key] !== undefined) ? UI_TEXT['telugu'][key] : key);
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  initUI();
  setupEventListeners();
  loadData();
});

function initUI() {
  const selDesktop = document.getElementById('langSelect');
  const selMobile = document.getElementById('langSelectMobile');
  if (selDesktop) selDesktop.value = STATE.lang;
  if (selMobile) selMobile.value = STATE.lang;
  document.getElementById('datePicker').value = STATE.date;
  updateStaticLabels();
}

function handleLangChange(newLang) {
  STATE.lang = newLang;
  localStorage.setItem('vp_lang', STATE.lang);
  const selDesktop = document.getElementById('langSelect');
  const selMobile = document.getElementById('langSelectMobile');
  if (selDesktop) selDesktop.value = STATE.lang;
  if (selMobile) selMobile.value = STATE.lang;
  STATE.monthlyData = null;
  STATE.sankalpaData = null;
  STATE.rashiData = { daily: null, monthly: null, yearly: null };
  updateStaticLabels();
  loadData();
}

function updateStaticLabels() {
  const setTxt = (id, val) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.innerText = val;
  };
  const setHtml = (id, val) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.innerHTML = val;
  };
  const setPh = (id, val) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.placeholder = val;
  };
  const setTitle = (id, val) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.title = val;
  };

  setTxt('appTitle', t('appTitle'));
  setTxt('appSubtitle', t('appSubtitle'));
  setHtml('headerCreatorCredit', t('headerCreatorCreditHtml'));
  document.title = `${t('appTitle')} | Vedic Astronomy & Dharma Shastra Computation System by Ramachandra Sastry Munimadugu • www.vedicsamhita.com`;
  setTxt('dailyTabBtn', t('dailyTab'));
  setTxt('monthlyTabBtn', t('monthlyTab'));
  setTxt('sankalpaTabBtn', t('sankalpaTab'));
  setTxt('rashiTabBtn', t('rashiTab'));
  setTxt('intercalaryTabBtn', t('intercalaryTab'));
  setTxt('kandadayamTabBtn', t('kandadayamTab'));
  setTxt('rashiPeriodDailyBtn', t('rashiDaily'));
  setTxt('rashiPeriodMonthlyBtn', t('rashiMonthly'));
  setTxt('rashiPeriodYearlyBtn', t('rashiYearly'));
  setTxt('rashiGridTitle', t('rashiSelectPrompt'));
  setPh('citySearchInput', t('searchPlaceholder'));
  setTxt('gpsBtnText', t('gpsBtn'));
  setTxt('todayBtn', t('todayBtn'));
  setTitle('prevDayBtn', STATE.lang === 'english' ? 'Previous Day' : (STATE.lang === 'devanagari' ? 'पिछला दिन' : 'మునుపటి రోజు'));
  setTitle('nextDayBtn', STATE.lang === 'english' ? 'Next Day' : (STATE.lang === 'devanagari' ? 'अगला दिन' : 'తరువాति రోజు'));

  // Hero Card
  setTxt('heroEraBadge', t('heroEra'));
  setTxt('heroAuthorBadge', t('heroAuthor'));
  setTxt('heroVaraLabel', t('heroVaraLabel'));

  // 3 Mana Systems
  setTxt('cmTitle', t('chandramanaTitle'));
  setTxt('labelCmAmanta', t('labelCmAmanta'));
  setTxt('labelCmPurnimanta', t('labelCmPurnimanta'));
  setTxt('labelCmPaksha', t('labelCmPaksha'));

  setTxt('smTitle', t('sauramanaTitle'));
  setTxt('labelSmSolarMonth', t('labelSmSolarMonth'));
  setTxt('labelSmTamil', t('labelSmTamil'));
  setTxt('labelSmMalayalam', t('labelSmMalayalam'));
  setTxt('labelSmSankranti', t('labelSmSankranti'));

  setTxt('bmTitle', t('barhaspatyamanaTitle'));
  setTxt('labelBmRashi', t('labelBmRashi'));
  setTxt('labelBmNakshatra', t('labelBmNakshatra'));
  setTxt('labelBmStatus', t('labelBmStatus'));
  setTxt('labelBmMahaMasa', t('labelBmMahaMasa'));
  setTxt('labelBmPushkaram', t('labelBmPushkaram'));

  // Panchangam Card & Attribute Labels
  setTxt('panchangaCardTitle', t('angasTitle'));
  setTxt('labelPanchangaSamvatsara', t('samvatsaraLabel'));
  setTxt('labelPanchangaAyanam', t('ayanaLabel'));
  setTxt('labelPanchangaRutu', t('rituLabel'));
  setTxt('labelPanchangaMasam', t('masaLabel'));
  setTxt('labelPanchangaPaksham', t('pakshaLabel'));

  setTxt('labelAngaTithi', `${t('tithi')} (Tithi)`);
  setTxt('labelAngaVara', `${t('vara')} (Vara)`);
  setTxt('labelAngaNakshatra', `${t('nakshatra')} (Nakshatra)`);
  setTxt('labelAngaYoga', `${t('yoga')} (Yoga)`);
  setTxt('labelAngaKarana', `${t('karana')} (Karana)`);

  // Sun & Moon
  setTxt('sunMoonTitle', t('sunMoonTitle'));
  setTxt('labelTimeSunrise', t('labelTimeSunrise'));
  setTxt('labelTimeSunset', t('labelTimeSunset'));
  setTxt('labelTimeBrahma', t('labelTimeBrahma'));
  setTxt('labelTimeMidday', t('labelTimeMidday'));
  setTxt('labelTimePratah', t('labelTimePratah'));
  setTxt('labelTimeSayan', t('labelTimeSayan'));
  setTxt('labelTimeMoonrise', t('labelTimeMoonrise'));
  setTxt('labelTimeMoonset', t('labelTimeMoonset'));
  setTxt('labelTimeMoonPhase', t('labelTimeMoonPhase'));

  // Muhurthams
  setTxt('muhurthasTitle', t('muhurthasTitle'));
  setTxt('labelAbhijit', t('labelAbhijit'));
  setTxt('labelAmrita', t('labelAmrita'));
  setTxt('labelRahu', t('labelRahu'));
  setTxt('labelYama', t('labelYama'));
  setTxt('labelGulika', t('labelGulika'));
  setTxt('labelDurmuhurtham', t('labelDurmuhurtham'));
  setTxt('labelVarjyam', t('labelVarjyam'));

  // Lagnas & Festivals
  setTxt('lagnasTitle', t('lagnasTitle'));
  setTxt('festivalsTitle', t('festivalsTitle'));

  // Monthly View
  setTxt('monthlyHint', t('monthlyHint'));
  const daysArr = t('calDays');
  if (Array.isArray(daysArr) && daysArr.length === 7) {
    for (let i = 0; i < 7; i++) {
      setTxt(`calDay${i}`, daysArr[i]);
    }
  }

  // Sankalpam View
  setTxt('sankalpaTitle', t('sankalpaTitle'));
  setTxt('sankalpaSubtitle', t('sankalpaSubtitle'));
  setTxt('labelGotra', t('labelGotra'));
  setPh('sankalpaGotra', t('sankalpaGotraPlaceholder'));
  setTxt('labelSharma', t('labelSharma'));
  setPh('sankalpaSharma', t('sankalpaSharmaPlaceholder'));
  setTxt('labelDeity', t('labelDeity'));
  setPh('sankalpaDeity', t('sankalpaDeityPlaceholder'));
  setTxt('sankalpaSubmitBtnText', t('sankalpaSubmitBtn'));
  setTxt('sankalpaLangBadge', t('sankalpaLangBadge'));
  setTxt('copySankalpaBtnText', t('copyBtnText'));
  setTxt('sankalpaSaBadge', t('sankalpaSaBadge'));

  // Loader
  setTxt('loaderText', t('loaderText'));
}

function setupEventListeners() {
  // Language Switch (Desktop & Mobile)
  const langDesktop = document.getElementById('langSelect');
  if (langDesktop) langDesktop.addEventListener('change', (e) => handleLangChange(e.target.value));

  const langMobile = document.getElementById('langSelectMobile');
  if (langMobile) langMobile.addEventListener('change', (e) => handleLangChange(e.target.value));

  // Date Change
  document.getElementById('datePicker').addEventListener('change', (e) => {
    STATE.date = e.target.value;
    const parts = STATE.date.split('-');
    STATE.year = parseInt(parts[0]);
    STATE.month = parseInt(parts[1]);
    localStorage.setItem('vp_date', STATE.date);
    loadData();
  });

  // Today Button
  document.getElementById('todayBtn').addEventListener('click', () => {
    const today = new Date().toISOString().split('T')[0];
    STATE.date = today;
    document.getElementById('datePicker').value = today;
    const parts = today.split('-');
    STATE.year = parseInt(parts[0]);
    STATE.month = parseInt(parts[1]);
    localStorage.setItem('vp_date', STATE.date);
    loadData();
  });

  // Prev / Next Day
  document.getElementById('prevDayBtn').addEventListener('click', () => adjustDate(-1));
  document.getElementById('nextDayBtn').addEventListener('click', () => adjustDate(1));

  // Tabs
  document.getElementById('dailyTabBtn').addEventListener('click', () => switchTab('daily'));
  document.getElementById('monthlyTabBtn').addEventListener('click', () => switchTab('monthly'));
  document.getElementById('sankalpaTabBtn').addEventListener('click', () => switchTab('sankalpa'));
  const rashiBtn = document.getElementById('rashiTabBtn');
  if (rashiBtn) rashiBtn.addEventListener('click', () => switchTab('rashi'));
  const interBtn = document.getElementById('intercalaryTabBtn');
  if (interBtn) interBtn.addEventListener('click', () => switchTab('intercalary'));
  const kdBtn = document.getElementById('kandadayamTabBtn');
  if (kdBtn) kdBtn.addEventListener('click', () => switchTab('kandadayam'));
  setupKandadayamControls();

  const sysSurya = document.getElementById('systemSuryaBtn');
  if (sysSurya) sysSurya.addEventListener('click', () => switchIntercalarySystem('surya_siddhanta'));
  const sysDrik = document.getElementById('systemDrikBtn');
  if (sysDrik) sysDrik.addEventListener('click', () => switchIntercalarySystem('drik'));

  // Rashi Period Toggle Buttons
  const rDaily = document.getElementById('rashiPeriodDailyBtn');
  if (rDaily) rDaily.addEventListener('click', () => fetchRashi('daily'));
  const rMonthly = document.getElementById('rashiPeriodMonthlyBtn');
  if (rMonthly) rMonthly.addEventListener('click', () => fetchRashi('monthly'));
  const rYearly = document.getElementById('rashiPeriodYearlyBtn');
  if (rYearly) rYearly.addEventListener('click', () => fetchRashi('yearly'));

  // City Search Autocomplete
  const searchInput = document.getElementById('citySearchInput');
  const searchResults = document.getElementById('searchResults');
  let searchTimer = null;

  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimer);
    const query = e.target.value.trim();
    if (query.length < 2) {
      searchResults.classList.add('hidden');
      return;
    }
    searchTimer = setTimeout(() => {
      fetchCities(query);
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.classList.add('hidden');
    }
  });

  // GPS Auto-detect Button
  document.getElementById('gpsBtn').addEventListener('click', handleGPSDetect);

  // Sankalpa Form Submit
  document.getElementById('sankalpaForm').addEventListener('submit', (e) => {
    e.preventDefault();
    fetchSankalpa();
  });

  // Copy Sankalpa Button
  document.getElementById('copySankalpaBtn').addEventListener('click', copySankalpaMantra);
}

function adjustDate(days) {
  const cur = new Date(STATE.date);
  cur.setDate(cur.getDate() + days);
  const nextDateStr = cur.toISOString().split('T')[0];
  STATE.date = nextDateStr;
  document.getElementById('datePicker').value = nextDateStr;
  const parts = nextDateStr.split('-');
  STATE.year = parseInt(parts[0]);
  STATE.month = parseInt(parts[1]);
  localStorage.setItem('vp_date', STATE.date);
  loadData();
}

function switchTab(tab) {
  STATE.activeTab = tab;
  ['daily', 'monthly', 'sankalpa', 'rashi', 'intercalary', 'kandadayam'].forEach((t) => {
    const el = document.getElementById(`${t}View`);
    const btn = document.getElementById(`${t}TabBtn`);
    if (t === tab) {
      if (el) el.classList.remove('hidden');
      if (btn) btn.className = "px-5 py-2.5 rounded-full font-semibold text-white bg-amber-700 shadow-md transition-all";
    } else {
      if (el) el.classList.add('hidden');
      if (btn) btn.className = "px-5 py-2.5 rounded-full font-semibold text-stone-300 hover:bg-amber-900/60 transition-all";
    }
  });

  if (tab === 'monthly' && !STATE.monthlyData) {
    fetchMonthly();
  } else if (tab === 'sankalpa' && !STATE.sankalpaData) {
    fetchSankalpa();
  } else if (tab === 'rashi') {
    fetchRashi();
  } else if (tab === 'intercalary') {
    fetchIntercalary();
  } else if (tab === 'kandadayam') {
    fetchKandadayam();
  }
}

// Load Data orchestrator
function loadData() {
  fetchDaily();
  if (STATE.activeTab === 'monthly') {
    fetchMonthly();
  } else if (STATE.activeTab === 'sankalpa') {
    fetchSankalpa();
  } else if (STATE.activeTab === 'rashi') {
    fetchRashi();
  } else if (STATE.activeTab === 'intercalary') {
    fetchIntercalary();
  } else if (STATE.activeTab === 'kandadayam') {
    fetchKandadayam();
  }
}

// Fetch Daily Panchangam
async function fetchDaily() {
  showLoader(true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);
  try {
    const url = `/api/v1/panchangam/daily?city=${encodeURIComponent(STATE.city)}&lat=${STATE.lat}&lon=${STATE.lon}&tz=${encodeURIComponent(STATE.tz)}&date=${STATE.date}&language=${STATE.lang}`;
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error(`Failed to fetch daily panchangam (${res.status})`);
    const data = await res.json();
    STATE.dailyData = data;
    renderDaily(data);
  } catch (err) {
    clearTimeout(timeoutId);
    console.error("Daily Panchangam error:", err);
  } finally {
    showLoader(false);
  }
}

// Render Daily View
function renderDaily(data) {
  // 1. Hero Summary
  const cm = data.chandramana;
  const sm = data.sauramana;
  const bm = data.barhaspatyamana;

  document.getElementById('heroSamvatsara').innerText = (data.angas && data.angas.samvatsara) || cm.samvatsara.name;
  document.getElementById('heroSubDetails').innerText = cm.description;
  document.getElementById('heroCityBadge').innerText = `📍 ${data.city}, ${data.country} (${data.latitude.toFixed(2)}°, ${data.longitude.toFixed(2)}°) • ${data.timezone}`;

  // 2. 3 Traditional Mana Systems
  // Chandramana
  document.getElementById('cmAmanta').innerText = cm.amanta_masa.name;
  document.getElementById('cmPurnimanta').innerText = cm.purnimanta_masa.name;
  const pakshaRaw = cm.paksha_name || cm.paksha || '';
  let pakshaDisplay = pakshaRaw;
  if (STATE.lang === 'telugu' || !STATE.lang) {
    if (pakshaRaw === 'Shukla') pakshaDisplay = 'శుక్ల పక్షము';
    else if (pakshaRaw === 'Krishna') pakshaDisplay = 'కృష్ణ పక్షము';
    else if (!pakshaRaw.includes('పక్షము') && (pakshaRaw === 'శుక్ల' || pakshaRaw === 'కృష్ణ')) pakshaDisplay = `${pakshaRaw} పక్షము`;
  }
  document.getElementById('cmPaksha').innerText = pakshaDisplay || '---';

  const cmBadge = document.getElementById('cmMasaBadge');
  const cmStatus = document.getElementById('cmMasaStatus');
  if (cmBadge) {
    const classification = cm.amanta_masa.masa_classification || (cm.amanta_masa.is_adhika ? 'ADHIKA' : 'NIJA');
    const badgeText = cm.amanta_masa.badge_label || (classification === 'ADHIKA' ? 'అధిక మాసం' : 'సాధారణ మాసం');
    cmBadge.innerText = badgeText;
    if (classification === 'KSHAYA') {
      cmBadge.className = 'text-[11px] font-extrabold px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-900 border border-rose-300 shadow-2xs animate-pulse';
    } else if (classification === 'SAMSARPA' || classification === 'ADHIKA') {
      cmBadge.className = 'text-[11px] font-extrabold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300 shadow-2xs';
    } else {
      cmBadge.className = 'text-[11px] font-extrabold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-2xs';
    }
  }
  if (cmStatus) {
    const sc = cm.amanta_masa.sankranti_count !== undefined ? cm.amanta_masa.sankranti_count : (cm.amanta_masa.is_adhika ? 0 : 1);
    cmStatus.innerText = `${cm.amanta_masa.badge_label || (sc === 0 ? 'అధిక' : (sc === 2 ? 'క్షయ' : 'నిజ'))} (${sc} సంక్రాంతి${sc === 1 ? '' : 'లు'})`;
  }

  // Sauramana
  const regSolar = sm.regional_solar_calendars || {};
  const smSolar = sm.solar_month || {};
  let smSolarText = smSolar.name;
  if (!smSolarText) {
    const rName = smSolar.rashi_name || '';
    const dayVal = smSolar.day ? `${smSolar.day}వ రోజు` : '';
    smSolarText = (rName && dayVal) ? `${rName} (${dayVal})` : (rName || '---');
  }
  document.getElementById('smSolarMonth').innerText = smSolarText || '---';
  document.getElementById('smTamil').innerText = regSolar.tamil ? regSolar.tamil.month_name : "---";
  document.getElementById('smMalayalam').innerText = regSolar.malayalam_kollam ? regSolar.malayalam_kollam.month_name : "---";
  document.getElementById('smSankranti').innerText = sm.sankranti_transition ? `${sm.sankranti_transition.to_month}: ${sm.sankranti_transition.transition_time}` : "---";

  // Barhaspatyamana
  document.getElementById('bmRashi').innerText = `${bm.jupiter_position.rashi_name} (${bm.jupiter_position.rashi_degrees})`;
  const padaText = STATE.lang === 'telugu'
    ? `${bm.jupiter_position.pada}వ ${t('pada')}`
    : (STATE.lang === 'english' ? `${t('pada')} ${bm.jupiter_position.pada}` : `${bm.jupiter_position.pada} ${t('pada')}`);
  document.getElementById('bmNakshatra').innerText = `${bm.jupiter_position.nakshatra_name} (${padaText})`;
  document.getElementById('bmStatus').innerText = bm.jupiter_position.motion_status;
  document.getElementById('bmMahaMasa').innerText = bm.jovian_cycle_12_year.maha_masa;
  document.getElementById('bmPushkaram').innerText = bm.sacred_river_pushkaram.active_river;

  // 3. 5 Angas & Panchanga Values
  const angas = data.angas;

  // Samvatsaram, Ayanam, Rutu, Masam, Paksham in Panchangam Card
  const samEl = document.getElementById('panchangaSamvatsara');
  if (samEl) samEl.innerText = angas.samvatsara || (cm.samvatsara ? cm.samvatsara.name : '---');

  const ayaEl = document.getElementById('panchangaAyanam');
  if (ayaEl) ayaEl.innerText = angas.ayanam || (sm.solar_month ? sm.solar_month.ayana : '---');

  const rutuEl = document.getElementById('panchangaRutu');
  if (rutuEl) rutuEl.innerText = angas.rutu || (cm.ritu_name || '---');

  const masEl = document.getElementById('panchangaMasam');
  if (masEl) masEl.innerText = angas.masam || (cm.amanta_masa ? cm.amanta_masa.name : '---');

  const pakEl = document.getElementById('panchangaPaksham');
  if (pakEl) pakEl.innerText = angas.paksham || (cm.paksha_name || cm.paksha || '---');

  // Vara in Panchangam Card & Quick Pill
  const cardVaraEl = document.getElementById('angaCardVara');
  if (cardVaraEl) cardVaraEl.innerText = angas.vara;

  const cardVaraEnEl = document.getElementById('angaCardVaraEnglish');
  if (cardVaraEnEl) {
    if (STATE.lang === 'english') {
      cardVaraEnEl.innerText = '';
    } else {
      cardVaraEnEl.innerText = angas.vara_english || '';
    }
  }

  if (document.getElementById('angaVara')) {
    document.getElementById('angaVara').innerText = angas.vara;
  }

  function formatAngaEndTime(anga) {
    if (!anga.end_time) {
      return t('fullDay');
    }
    const dStr = anga.end_date || '';
    const endLbl = t('endLabel');
    if (anga.is_next_day) {
      return `${endLbl} ${anga.end_time} (${dStr}, ${t('nextDayLabel')})`;
    } else {
      return `${endLbl} ${anga.end_time} (${dStr})`;
    }
  }

  // Tithis
  const tithisHtml = angas.tithis.map(t => `
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center py-2 border-b border-amber-100 last:border-0 gap-1">
      <span class="font-bold text-stone-900">${t.name}</span>
      <span class="text-xs px-2.5 py-1 ${t.is_next_day ? 'bg-amber-200 text-amber-950 font-bold border border-amber-300' : 'bg-amber-100 text-amber-800 font-medium'} rounded-full">
        ${formatAngaEndTime(t)}
      </span>
    </div>
  `).join('');
  document.getElementById('angaTithis').innerHTML = tithisHtml;

  // Nakshatras
  const nakshatrasHtml = angas.nakshatras.map(n => `
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center py-2 border-b border-amber-100 last:border-0 gap-1">
      <span class="font-bold text-stone-900">${n.name}</span>
      <span class="text-xs px-2.5 py-1 ${n.is_next_day ? 'bg-amber-200 text-amber-950 font-bold border border-amber-300' : 'bg-amber-100 text-amber-800 font-medium'} rounded-full">
        ${formatAngaEndTime(n)}
      </span>
    </div>
  `).join('');
  document.getElementById('angaNakshatras').innerHTML = nakshatrasHtml;

  // Yogas
  const yogasHtml = angas.yogas.map(y => `
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center py-2 border-b border-amber-100 last:border-0 gap-1">
      <span class="font-bold text-stone-900">${y.name}</span>
      <span class="text-xs px-2.5 py-1 ${y.is_next_day ? 'bg-amber-200 text-amber-950 font-bold border border-amber-300' : 'bg-stone-100 text-stone-700 font-medium'} rounded-full">
        ${formatAngaEndTime(y)}
      </span>
    </div>
  `).join('');
  document.getElementById('angaYogas').innerHTML = yogasHtml;

  // Karanas
  const karanasHtml = angas.karanas.map(k => `
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center py-2 border-b border-amber-100 last:border-0 gap-1">
      <span class="font-bold text-stone-900">${k.name}</span>
      <span class="text-xs px-2.5 py-1 ${k.is_next_day ? 'bg-amber-200 text-amber-950 font-bold border border-amber-300' : 'bg-stone-100 text-stone-700 font-medium'} rounded-full">
        ${formatAngaEndTime(k)}
      </span>
    </div>
  `).join('');
  document.getElementById('angaKaranas').innerHTML = karanasHtml;

  // 4. Sun & Moon Timings
  const smt = data.sun_moon;
  document.getElementById('timeSunrise').innerText = smt.sunrise;
  document.getElementById('timeSunset').innerText = smt.sunset;
  document.getElementById('timeMidday').innerText = smt.midday;
  document.getElementById('timeBrahma').innerText = smt.brahma_muhurtham || '---';
  document.getElementById('timePratah').innerText = smt.pratahsandhya || '---';
  document.getElementById('timeSayan').innerText = smt.sayansandhya || '---';
  document.getElementById('timeMoonrise').innerText = smt.moonrise;
  document.getElementById('timeMoonset').innerText = smt.moonset;
  document.getElementById('timeMoonPhase').innerText = `${smt.moon_phase_name} (${(smt.moon_illumination * 100).toFixed(1)}%)`;

  // 5. Muhurthams
  const m = data.muhurthams;
  document.getElementById('timeRahu').innerText = m.rahu_kalam;
  document.getElementById('timeYama').innerText = m.yama_gandam;
  document.getElementById('timeGulika').innerText = m.gulika_kalam;
  document.getElementById('timeAbhijit').innerText = m.abhijit_muhurtham || t('noAbhijit');
  document.getElementById('timeDurmuhurtham').innerText = m.durmuhurtham.join(', ') || '---';
  document.getElementById('timeVarjyam').innerText = m.varjyam.join(', ') || t('noVarjyam');
  document.getElementById('timeAmrita').innerText = m.amrita_kalam.join(', ') || '---';

  // 6. 24-Hour Lagna Schedule with Pushkara Navamsha
  const lagnasContainer = document.getElementById('lagnasContainer');
  if (data.lagnas && data.lagnas.length > 0) {
    lagnasContainer.innerHTML = data.lagnas.map(l => {
      const nextDayBadge = l.is_next_day ? `
        <span class="text-[10px] text-purple-700 bg-purple-50 border border-purple-200 rounded px-1.5 py-0.5 font-semibold inline-block">
          ${t('nextDayLabel')}
        </span>` : '';

      const pushkaraHtml = l.pushkara_amsha ? `
        <div class="mt-2 pt-2 border-t border-amber-200/60 flex items-center justify-between text-xs bg-amber-100/60 -mx-3 -mb-3 px-3 py-1.5 rounded-b-xl">
          <span class="text-amber-900 font-bold flex items-center gap-1">
            ✨ ${t('pushkaraLabel')}:
          </span>
          <span class="font-mono font-bold text-amber-950">
            ${l.pushkara_amsha}
            ${l.pushkara_is_next_day ? `<span class="text-[9px] text-purple-700 font-normal">(${t('nextDayLabel')})</span>` : ''}
          </span>
        </div>` : '';

      return `
        <div class="p-3 bg-gradient-to-b from-amber-50/70 via-white to-amber-50/40 border border-amber-200/90 rounded-xl shadow-xs hover:shadow-md transition-all flex flex-col justify-between relative">
          <div>
            <div class="flex justify-between items-start mb-1.5">
              <span class="font-bold text-sm md:text-base text-amber-950 font-serif-te">
                ${l.rashi_name}
              </span>
              ${l.duration ? `<span class="text-[10px] bg-amber-100/80 text-amber-900 border border-amber-200 px-1.5 py-0.5 rounded-md font-medium">${l.duration}</span>` : ''}
            </div>

            <div class="text-xs space-y-1 my-1.5">
              <div class="flex items-center justify-between text-stone-700">
                <span class="text-stone-500 text-[11px]">${t('timeSpanLabel')}:</span>
                <span class="font-bold font-mono text-stone-900">${l.start_time || '---'} – ${l.end_time}</span>
              </div>
              ${nextDayBadge ? `<div class="text-right">${nextDayBadge}</div>` : ''}
            </div>
          </div>

          ${pushkaraHtml}
        </div>
      `;
    }).join('');
  } else {
    lagnasContainer.innerHTML = `<div class="col-span-full text-stone-500 text-center py-2">${t('noLagnas')}</div>`;
  }

  // 7. Festivals & Vratams
  const festContainer = document.getElementById('festivalsContainer');
  if (data.festivals && data.festivals.length > 0) {
    festContainer.innerHTML = data.festivals.map(f => {
      const name = typeof f === 'string' ? f : f.name;
      return `
        <span class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-sm font-semibold bg-amber-50 text-amber-900 border border-amber-200/80 shadow-2xs">
          <span class="text-amber-600">🪔</span>
          <span>${name}</span>
        </span>
      `;
    }).join('');
  } else {
    festContainer.innerHTML = `<span class="text-stone-500 italic text-sm">${t('noFestivals')}</span>`;
  }
}

// Fetch Monthly Calendar
async function fetchMonthly() {
  showLoader(true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);
  try {
    const url = `/api/v1/panchangam/monthly?city=${encodeURIComponent(STATE.city)}&lat=${STATE.lat}&lon=${STATE.lon}&tz=${encodeURIComponent(STATE.tz)}&year=${STATE.year}&month=${STATE.month}&language=${STATE.lang}`;
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error("Failed to fetch monthly calendar");
    const data = await res.json();
    STATE.monthlyData = data;
    renderMonthly(data);
  } catch (err) {
    clearTimeout(timeoutId);
    console.error("Monthly fetch error:", err);
  } finally {
    showLoader(false);
  }
}

// Render Monthly Grid
function renderMonthly(data) {
  document.getElementById('monthlyTitle').innerText = `${STATE.year} - ${STATE.month} ${t('monthlyGridTitle')} (${data.city})`;
  const grid = document.getElementById('calendarDaysGrid');
  grid.innerHTML = '';

  if (!data.days || data.days.length === 0) return;

  // Compute offset for the 1st day of the month
  const firstDate = new Date(`${STATE.year}-${String(STATE.month).padStart(2, '0')}-01`);
  const startDayIndex = firstDate.getDay(); // 0 = Sunday, 1 = Monday...

  // Blank slots for previous month
  for (let i = 0; i < startDayIndex; i++) {
    const blank = document.createElement('div');
    blank.className = "bg-stone-50/50 border border-stone-100 rounded-lg p-2 min-h-[85px] opacity-40";
    grid.appendChild(blank);
  }

  // Render Days
  data.days.forEach(day => {
    const cell = document.createElement('div');
    const isToday = day.date === new Date().toISOString().split('T')[0];
    const isSelected = day.date === STATE.date;

    cell.className = `cal-day-cell vedic-card p-2 rounded-lg border flex flex-col justify-between ${isToday ? 'cal-day-today' : 'border-amber-200'} ${isSelected ? 'cal-day-selected' : ''}`;
    
    let festsHtml = '';
    if (day.festivals && day.festivals.length > 0) {
      festsHtml = `
        <div class="mt-1 flex flex-wrap gap-1">
          <span class="text-[10px] bg-amber-200 text-amber-900 px-1.5 py-0.5 rounded font-bold truncate max-w-full" title="${day.festivals.join(', ')}">
            🪔 ${day.festivals[0]}
          </span>
        </div>
      `;
    }

    const tithiTooltip = `${day.tithi_name} ${t('endLabel')} ${day.tithi_end_time || ''} ${day.tithi_is_next_day ? '(' + t('nextDayLabel') + ')' : ''}`;
    const tithiEndDisplay = day.tithi_end_time ? (day.tithi_is_next_day ? t('nextDayLabel') + ' ' : '') + day.tithi_end_time : '';

    cell.innerHTML = `
      <div>
        <div class="flex justify-between items-center">
          <span class="font-bold text-base ${isToday ? 'text-amber-800' : 'text-stone-800'}">${day.day}</span>
          <span class="text-[11px] text-stone-500 font-medium">${day.weekday.split(' ')[0]}</span>
        </div>
        <div class="text-[12px] font-semibold text-amber-950 mt-1 truncate" title="${tithiTooltip}">
          ${day.tithi_name}
        </div>
        <div class="text-[10px] text-amber-800 font-mono">
          ${tithiEndDisplay}
        </div>
        <div class="text-[11px] text-stone-600 truncate mt-0.5">${day.nakshatra_name}</div>
      </div>
      ${festsHtml}
    `;

    cell.addEventListener('click', () => {
      STATE.date = day.date;
      document.getElementById('datePicker').value = day.date;
      localStorage.setItem('vp_date', STATE.date);
      switchTab('daily');
      loadData();
    });

    grid.appendChild(cell);
  });
}

// Fetch Custom Vedic Sankalpam
async function fetchSankalpa() {
  showLoader(true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);
  try {
    const gotra = document.getElementById('sankalpaGotra').value.trim();
    const sharma = document.getElementById('sankalpaSharma').value.trim();
    const deity = document.getElementById('sankalpaDeity').value.trim();

    let url = `/api/v1/sankalpam/generate?city=${encodeURIComponent(STATE.city)}&lat=${STATE.lat}&lon=${STATE.lon}&tz=${encodeURIComponent(STATE.tz)}&date=${STATE.date}&language=${STATE.lang}`;
    if (gotra) url += `&gotra=${encodeURIComponent(gotra)}`;
    if (sharma) url += `&sharma_name=${encodeURIComponent(sharma)}`;
    if (deity) url += `&kula_devata=${encodeURIComponent(deity)}`;

    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error("Failed to generate sankalpam");
    const data = await res.json();
    STATE.sankalpaData = data;
    renderSankalpa(data);
  } catch (err) {
    clearTimeout(timeoutId);
    console.error("Sankalpa fetch error:", err);
  } finally {
    showLoader(false);
  }
}

function renderSankalpa(data) {
  const sk = data.sankalpam;
  document.getElementById('sankalpaTeluguText').innerText = sk.sankalpam_text;
  document.getElementById('sankalpaSanskritText').innerText = sk.sankalpam_sanskrit_devanagari;
  document.getElementById('sankalpaGeoInfo').innerText = `${t('geoCoordLabel')}: ${sk.location_context.city}, ${sk.location_context.country} • ${t('dveepaLabel')}: ${sk.location_context.dveepa} • ${t('khandaLabel')}: ${sk.location_context.khanda}`;
}

function copySankalpaMantra() {
  const text = document.getElementById('sankalpaTeluguText').innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('copySankalpaBtn');
    const labelSpan = document.getElementById('copySankalpaBtnText');
    const originalText = labelSpan ? labelSpan.innerText : btn.innerText;
    if (labelSpan) labelSpan.innerText = t('copied');
    else btn.innerText = t('copied');
    btn.classList.replace('bg-amber-700', 'bg-emerald-700');
    setTimeout(() => {
      if (labelSpan) labelSpan.innerText = originalText;
      else btn.innerText = originalText;
      btn.classList.replace('bg-emerald-700', 'bg-amber-700');
    }, 2000);
  });
}

// Fetch Cities Autocomplete
async function fetchCities(query) {
  try {
    const res = await fetch(`/api/v1/cities/search?q=${encodeURIComponent(query)}&limit=10`);
    const data = await res.json();
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    if (data.cities && data.cities.length > 0) {
      data.cities.forEach(c => {
        const item = document.createElement('div');
        item.className = "px-4 py-2.5 hover:bg-amber-50 cursor-pointer border-b border-stone-100 last:border-0 flex justify-between items-center text-sm";
        item.innerHTML = `
          <div>
            <span class="font-bold text-stone-800">${c.name}</span>
            <span class="text-xs text-stone-500 ml-1">(${c.state || ''}, ${c.country})</span>
          </div>
          <span class="text-[11px] bg-stone-100 text-stone-600 px-2 py-0.5 rounded font-mono">${c.tz}</span>
        `;
        item.addEventListener('click', () => {
          selectCity(c);
          resultsContainer.classList.add('hidden');
          document.getElementById('citySearchInput').value = '';
        });
        resultsContainer.appendChild(item);
      });
      resultsContainer.classList.remove('hidden');
    } else {
      resultsContainer.classList.add('hidden');
    }
  } catch (err) {
    console.error(err);
  }
}

function selectCity(cityObj) {
  STATE.city = cityObj.name;
  STATE.country = cityObj.country;
  STATE.lat = cityObj.lat;
  STATE.lon = cityObj.lon;
  STATE.tz = cityObj.tz;
  localStorage.setItem('vp_city', STATE.city);
  localStorage.setItem('vp_country', STATE.country);
  localStorage.setItem('vp_lat', STATE.lat);
  localStorage.setItem('vp_lon', STATE.lon);
  localStorage.setItem('vp_tz', STATE.tz);
  loadData();
}

// GPS Auto-detect
function handleGPSDetect() {
  if (!navigator.geolocation) {
    alert("మీ బ్రౌజర్‌లో GPS జియోలొకేషన్ సపోర్ట్ లేదు.");
    return;
  }
  const btn = document.getElementById('gpsBtn');
  btn.classList.add('opacity-50');
  
  navigator.geolocation.getCurrentPosition(async (pos) => {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    try {
      const res = await fetch(`/api/v1/cities/nearest?lat=${lat}&lon=${lon}`);
      if (res.ok) {
        const nearestCity = await res.json();
        selectCity(nearestCity);
        alert(`లొకేషన్ విజయవంతంగా గుర్తించబడింది: ${nearestCity.name}, ${nearestCity.country}`);
      }
    } catch (err) {
      console.error(err);
    } finally {
      btn.classList.remove('opacity-50');
    }
  }, (err) => {
    btn.classList.remove('opacity-50');
    alert("లొకేషన్ అనుమతి లభించలేదు: " + err.message);
  });
}

// ==================== RASHI PHALALU (HOROSCOPE) ====================

async function fetchRashi(period = null) {
  if (period) {
    STATE.activeRashiPeriod = period;
  }
  const curPeriod = STATE.activeRashiPeriod; // 'daily', 'monthly', 'yearly'

  // Update Period toggle button styles
  const pMap = { daily: 'Daily', monthly: 'Monthly', yearly: 'Yearly' };
  ['daily', 'monthly', 'yearly'].forEach(p => {
    const btn = document.getElementById(`rashiPeriod${pMap[p]}Btn`);
    if (btn) {
      if (p === curPeriod) {
        btn.className = "px-4 py-1.5 rounded-lg text-xs font-bold text-white bg-amber-600 shadow transition-all";
      } else {
        btn.className = "px-4 py-1.5 rounded-lg text-xs font-bold text-amber-200 hover:text-white transition-all";
      }
    }
  });

  // If already cached in STATE, render immediately
  if (STATE.rashiData[curPeriod]) {
    renderRashiView();
    return;
  }

  showLoader(true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);
  try {
    let url = '';
    if (curPeriod === 'daily') {
      url = `/api/v1/rashi/daily?date=${STATE.date}&language=${STATE.lang}`;
    } else if (curPeriod === 'monthly') {
      url = `/api/v1/rashi/monthly?year=${STATE.year}&month=${STATE.month}&language=${STATE.lang}`;
    } else {
      url = `/api/v1/rashi/yearly?year=${STATE.year}&language=${STATE.lang}`;
    }

    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error("Failed to fetch rashi phalalu");
    const data = await res.json();
    STATE.rashiData[curPeriod] = data;

    renderRashiView();
  } catch (err) {
    clearTimeout(timeoutId);
    console.error("Error fetching Rashi Phalalu:", err);
  } finally {
    showLoader(false);
  }
}

function renderRashiView() {
  const curPeriod = STATE.activeRashiPeriod;
  const data = STATE.rashiData[curPeriod];
  if (!data || !data.rashis || data.rashis.length === 0) return;

  // 1. Update Info Badge
  const infoBadge = document.getElementById('rashiPeriodInfoBadge');
  const activePlanet = document.getElementById('rashiActivePlanetBadge');
  if (infoBadge) {
    if (curPeriod === 'daily') {
      infoBadge.innerText = `📅 ${data.date} (${data.weekday})`;
      if (activePlanet) activePlanet.innerText = `🌙 చంద్ర సంచారం: ${data.moon_rashi}`;
    } else if (curPeriod === 'monthly') {
      infoBadge.innerText = `🗓️ ${data.year} / ${String(data.month).padStart(2, '0')} (${data.solar_month})`;
      if (activePlanet) activePlanet.innerText = `☀️ సౌర మాసం: ${data.solar_month}`;
    } else {
      infoBadge.innerText = `🪐 ${data.samvatsara} (${data.year})`;
      if (activePlanet) activePlanet.innerText = `✨ పంచాంగ కందాయ పట్టిక`;
    }
  }

  // 2. Render 12 Cards Grid
  renderRashiCardsGrid(data.rashis);

  // 3. Render Selected Rashi Details
  const selectedRashi = data.rashis[STATE.selectedRashiIdx] || data.rashis[0];
  renderRashiDetails(selectedRashi, curPeriod);
}

function renderRashiCardsGrid(rashis) {
  const container = document.getElementById('rashiCardsGrid');
  if (!container) return;

  let html = '';
  rashis.forEach((item, idx) => {
    const isSelected = idx === STATE.selectedRashiIdx;
    const isChandrashtama = item.is_chandrashtama;
    const score = item.score_percent;

    // Mini pill badge
    let miniBadge = '';
    if (STATE.activeRashiPeriod === 'daily') {
      if (isChandrashtama) {
        miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 border border-rose-300">⚠️ చంద్రాష్టమం</span>`;
      } else {
        const bgCls = score >= 75 ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : 'bg-amber-100 text-amber-800 border-amber-300';
        miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded ${bgCls}">${score}%</span>`;
      }
    } else if (STATE.activeRashiPeriod === 'monthly') {
      miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300">${score}% అనుకూలం</span>`;
    } else {
      // Yearly: show aadhayam / vyayam
      const kd = item.kandadayam;
      miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300 font-mono">ఆ:${kd.aadhayam} వ్య:${kd.vyayam}</span>`;
    }

    const cardClasses = isSelected
      ? "p-3 rounded-2xl bg-gradient-to-br from-amber-100/90 to-orange-50 border-2 border-amber-600 ring-2 ring-amber-400/60 shadow-md cursor-pointer transition-all transform scale-[1.02]"
      : "p-3 rounded-2xl bg-white hover:bg-amber-50/70 border border-amber-200/80 shadow-xs hover:border-amber-400 cursor-pointer transition-all";

    html += `
      <div onclick="selectRashiCard(${idx})" class="${cardClasses}">
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-2xl">${item.rashi.symbol}</span>
          ${miniBadge}
        </div>
        <div class="font-extrabold text-stone-900 text-sm leading-tight">${item.rashi.name}</div>
        <div class="text-[11px] text-stone-500 font-medium">${item.rashi.name_english}</div>
        <div class="text-[10px] text-amber-800 mt-1 flex justify-between font-medium">
          <span>${item.rashi.lord}</span>
          <span class="text-stone-400">•</span>
          <span>${item.rashi.element.split(' ')[0]}</span>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function selectRashiCard(idx) {
  STATE.selectedRashiIdx = idx;
  renderRashiView();
}

function renderRashiDetails(item, curPeriod) {
  const container = document.getElementById('selectedRashiDetailContainer');
  if (!container) return;

  const rashi = item.rashi;
  const score = item.score_percent;

  // Header progress bar color
  const scoreColor = score >= 75 ? 'text-emerald-700 bg-emerald-100 border-emerald-300' : (score >= 55 ? 'text-amber-800 bg-amber-100 border-amber-300' : 'text-rose-700 bg-rose-100 border-rose-300');
  const barColor = score >= 75 ? 'bg-emerald-500' : (score >= 55 ? 'bg-amber-500' : 'bg-rose-500');

  // Transit Alert HTML
  let transitAlertHtml = '';
  if (curPeriod === 'daily') {
    if (item.is_chandrashtama) {
      transitAlertHtml = `
        <div class="p-4 rounded-xl bg-gradient-to-r from-rose-50 to-red-100 border-l-4 border-rose-600 text-rose-900 shadow-sm flex items-start gap-3">
          <span class="text-2xl">⚠️</span>
          <div>
            <div class="font-bold text-sm text-rose-900 uppercase tracking-wide">చంద్రాష్టమ హెచ్చరిక (Chandrashtama Active)</div>
            <div class="text-xs text-rose-800 mt-0.5 leading-relaxed">
              ఈ రోజు చంద్రుడు మీ జన్మ రాశి నుండి 8వ స్థానంలో సంచరిస్తున్నారు. ఆందోళనలు, ఆర్థిక లావాదేవీలు, వాదనలు మరియు ముఖ్యమైన నూతన ఒప్పందాల ప్రారంభాలలో అత్యంత జాగ్రత్త అవసరం. శివారాధన శుభప్రదం.
            </div>
          </div>
        </div>
      `;
    }

    // Daily Status Badges & Lucky info
    transitAlertHtml += `
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5">
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">చంద్ర స్థానం</div>
          <div class="text-xs font-extrabold text-amber-950 mt-0.5">${item.moon_house}వ ఇల్లు</div>
          <div class="text-[10px] text-amber-700 mt-0.5">${item.chandra_bala_status.split('(')[0]}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">తారాబలం</div>
          <div class="text-xs font-extrabold text-amber-950 mt-0.5">${item.tara_bala_name.split('(')[0]}</div>
          <div class="text-[10px] ${item.is_tara_bala_good ? 'text-emerald-600' : 'text-rose-600'} font-bold mt-0.5">${item.is_tara_bala_good ? 'శుభ తార ✔️' : 'అప్రమత్తత ⚠️'}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">అదృష్ట సంఖ్య</div>
          <div class="text-lg font-extrabold text-amber-800 leading-tight mt-0.5 font-mono">${item.lucky_number}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">అదృష్ట రంగు</div>
          <div class="text-xs font-bold text-stone-800 mt-1">${item.lucky_color}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center col-span-2 sm:col-span-1">
          <div class="text-[10px] text-stone-500 font-bold uppercase">అనుకూల దిశ</div>
          <div class="text-xs font-bold text-stone-800 mt-1">${item.lucky_direction}</div>
        </div>
      </div>
    `;
  } else if (curPeriod === 'monthly') {
    // Monthly Transit Info
    transitAlertHtml = `
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="p-3.5 bg-white rounded-xl border border-amber-200 shadow-xs">
          <div class="text-[10px] text-stone-500 font-bold uppercase">సూర్య సంక్రమణం</div>
          <div class="text-sm font-extrabold text-amber-950 mt-1">${item.sun_house}వ స్థానం</div>
          <div class="text-xs text-amber-800 mt-0.5">${item.is_sun_favorable ? 'అనుకూల సూర్య బలం (ఉపచయం) ☀️' : 'సూర్య ప్రతికూలత (ఓపిక అవసరం)'}</div>
        </div>
        <div class="p-3.5 bg-white rounded-xl border border-amber-200 shadow-xs sm:col-span-2">
          <div class="text-[10px] text-stone-500 font-bold uppercase mb-1">మాస ముఖ్యాంశాలు</div>
          <ul class="text-xs text-stone-700 space-y-1">
            ${item.highlights.map(h => `<li class="flex items-center gap-1.5"><span class="text-amber-500 font-bold">•</span> <span>${h}</span></li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  } else {
    // Yearly: Kandadayam Grid & Saturn/Jupiter status
    const kd = item.kandadayam;
    transitAlertHtml = `
      <div class="space-y-4">
        <!-- Kandadayam 4-card metric -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="p-4 rounded-2xl bg-gradient-to-br from-emerald-50 to-emerald-100/60 border border-emerald-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-emerald-800 uppercase tracking-wide">💰 ఆదాయం (Income)</div>
            <div class="text-3xl font-extrabold text-emerald-950 font-mono mt-1">${kd.aadhayam}</div>
            <div class="text-[10px] text-emerald-700 mt-1">గరిష్టం: 14</div>
          </div>
          <div class="p-4 rounded-2xl bg-gradient-to-br from-amber-50 to-orange-100/60 border border-amber-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-amber-800 uppercase tracking-wide">💸 వ్యయం (Expenditure)</div>
            <div class="text-3xl font-extrabold text-amber-950 font-mono mt-1">${kd.vyayam}</div>
            <div class="text-[10px] text-amber-700 mt-1">గరిష్టం: 14</div>
          </div>
          <div class="p-4 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-100/60 border border-blue-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-blue-800 uppercase tracking-wide">👑 రాజపూజ్యం (Honor)</div>
            <div class="text-3xl font-extrabold text-blue-950 font-mono mt-1">${kd.rajapujyam}</div>
            <div class="text-[10px] text-blue-700 mt-1">గరిష్టం: 8</div>
          </div>
          <div class="p-4 rounded-2xl bg-gradient-to-br from-rose-50 to-rose-100/60 border border-rose-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-rose-800 uppercase tracking-wide">🛡️ అవమానం (Disgrace)</div>
            <div class="text-3xl font-extrabold text-rose-950 font-mono mt-1">${kd.avamanam}</div>
            <div class="text-[10px] text-rose-700 mt-1">గరిష్టం: 8</div>
          </div>
        </div>

        <!-- Kandadayam Insight Pill Bar -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs flex items-center gap-2.5">
            <span class="text-xl">📊</span>
            <div>
              <div class="text-[10px] text-stone-500 font-bold uppercase">ఆర్థిక స్థితి విశ్లేషణ</div>
              <div class="text-xs font-extrabold text-amber-900">${kd.finance_status}</div>
            </div>
          </div>
          <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs flex items-center gap-2.5">
            <span class="text-xl">🎖️</span>
            <div>
              <div class="text-[10px] text-stone-500 font-bold uppercase">సామాజిక హోదా విశ్లేషణ</div>
              <div class="text-xs font-extrabold text-amber-900">${kd.social_status}</div>
            </div>
          </div>
        </div>

        <!-- Planetary Positions -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200 text-center">
            <div class="text-[10px] text-stone-500 font-bold uppercase">గురు బలం (${item.jupiter_house}వ స్థానం)</div>
            <div class="text-xs font-bold text-amber-950 mt-0.5">${item.has_guru_balam ? 'గురు బలం కలదు ✨' : 'గురు శాంతి అవసరం'}</div>
          </div>
          <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200 text-center">
            <div class="text-[10px] text-stone-500 font-bold uppercase">శని గోచారం (${item.saturn_house}వ స్థానం)</div>
            <div class="text-xs font-bold text-amber-950 mt-0.5">${item.sade_sati_status}</div>
          </div>
          <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200 text-center">
            <div class="text-[10px] text-stone-500 font-bold uppercase">రాహు-కేతు సంచారం</div>
            <div class="text-xs font-bold text-amber-950 mt-0.5">${item.rahu_ketu_status}</div>
          </div>
        </div>
      </div>
    `;
  }

  // 5 Category Predictions
  const preds = item.predictions;
  const categoriesHtml = `
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">🔮</span>
          <h4>సాధారణ సమీక్ష (General Overview)</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.general}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">💼</span>
          <h4>ఉద్యోగం & వ్యాపారం (Career & Profession)</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.career}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">💰</span>
          <h4>ఆర్థిక స్థితి & ధన యోగం (Finance & Wealth)</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.finance}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">🩺</span>
          <h4>ఆరోగ్యం & శక్తి (Health & Well-being)</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.health}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs md:col-span-2">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">👨‍👩‍👧</span>
          <h4>కుటుంబం & దాంపత్యం (Family & Relationships)</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.family}</p>
      </div>
    </div>
  `;

  // Remedy Section
  const remedyHtml = `
    <div class="p-5 rounded-2xl bg-gradient-to-br from-amber-900 via-amber-950 to-stone-950 text-amber-100 border border-amber-500/40 shadow-md">
      <div class="flex items-center gap-2.5 mb-2">
        <span class="text-2xl">🪔</span>
        <h4 class="font-extrabold text-sm text-amber-200 uppercase tracking-wide">శాంతి / దైవ పరిహారము (Remedies & Prayers)</h4>
      </div>
      <p class="text-xs text-stone-300 leading-relaxed font-normal">${item.remedy}</p>
    </div>
  `;

  // Main Detail Assembly
  container.innerHTML = `
    <div class="vedic-card p-6 bg-white border-2 border-amber-300 shadow-md space-y-6">
      
      <!-- Top Title Bar -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-amber-200 pb-5">
        <div class="flex items-center gap-3.5">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-amber-500 to-amber-700 text-white flex items-center justify-center text-3xl font-extrabold shadow-md border-2 border-amber-300">
            ${rashi.symbol}
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-2xl md:text-3xl font-extrabold text-amber-950 font-serif-te leading-tight">
                ${rashi.name}
              </h3>
              <span class="text-xs font-semibold text-stone-500">(${rashi.name_english})</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-stone-600 mt-1 font-medium">
              <span>అధిపతి: <strong class="text-amber-900">${rashi.lord}</strong></span>
              <span>•</span>
              <span>తత్త్వం: <strong class="text-amber-900">${rashi.element}</strong></span>
            </div>
          </div>
        </div>

        <!-- Score Meter -->
        <div class="flex flex-col items-end sm:items-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase tracking-wider mb-1">అనుకూలత స్కోర్</div>
          <div class="flex items-center gap-2">
            <span class="text-2xl font-black font-mono text-amber-950">${score}%</span>
            <span class="text-xs font-extrabold px-2.5 py-1 rounded-full border ${scoreColor}">
              ${item.score_rating}
            </span>
          </div>
          <div class="w-28 bg-stone-200 h-2 rounded-full mt-1.5 overflow-hidden shadow-inner">
            <div class="${barColor} h-full transition-all duration-500" style="width: ${score}%;"></div>
          </div>
        </div>
      </div>

      <!-- Transit Alerts & Status Grid -->
      ${transitAlertHtml}

      <!-- Predictions Grid -->
      ${categoriesHtml}

      <!-- Remedy Box -->
      ${remedyHtml}

    </div>
  `;
}

// Intercalary (Adhika, Kshaya, Samsarpa) Functions
async function fetchIntercalary() {
  const sys = STATE.intercalarySystem || 'surya_siddhanta';
  showLoader(true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(`/api/v1/panchangam/intercalary-months?start_year=2026&end_year=2036&system=${sys}&language=${STATE.lang}`, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    STATE.intercalaryData = data;
    renderIntercalary(data);
  } catch (err) {
    clearTimeout(timeoutId);
    console.error('Error fetching intercalary months:', err);
  } finally {
    showLoader(false);
  }
}

function switchIntercalarySystem(sys) {
  STATE.intercalarySystem = sys;
  const btnSurya = document.getElementById('systemSuryaBtn');
  const btnDrik = document.getElementById('systemDrikBtn');
  const badge = document.getElementById('activeSystemBadge');
  const keelakaCallout = document.getElementById('keelakaCallout');

  if (sys === 'surya_siddhanta') {
    if (btnSurya) btnSurya.className = "px-4 py-2 rounded-xl text-xs font-bold text-white bg-amber-600 shadow transition-all";
    if (btnDrik) btnDrik.className = "px-4 py-2 rounded-xl text-xs font-bold text-amber-200 hover:text-white transition-all";
    if (badge) {
      badge.innerText = "సూర్యసిద్ధాంత / ధర్మశాస్త్ర పద్ధతి";
      badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300";
    }
    if (keelakaCallout) keelakaCallout.classList.remove('hidden');
  } else {
    if (btnDrik) btnDrik.className = "px-4 py-2 rounded-xl text-xs font-bold text-white bg-amber-600 shadow transition-all";
    if (btnSurya) btnSurya.className = "px-4 py-2 rounded-xl text-xs font-bold text-amber-200 hover:text-white transition-all";
    if (badge) {
      badge.innerText = "దృక్సిద్ధాంత పద్ధతి (Swiss Ephemeris)";
      badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-sky-100 text-sky-900 border border-sky-300";
    }
    if (keelakaCallout) keelakaCallout.classList.add('hidden');
  }

  fetchIntercalary();
}

function renderIntercalary(data) {
  const tbody = document.getElementById('intercalaryTableBody');
  if (!tbody || !data || !data.months) return;

  const rowsHtml = data.months.map(m => {
    let typeBadge = '';
    let rowBg = '';
    if (m.classification === 'KSHAYA') {
      typeBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-900 border border-rose-300 shadow-2xs">${m.classification_name}</span>`;
      rowBg = 'bg-rose-50/60 hover:bg-rose-100/50';
    } else if (m.classification === 'SAMSARPA') {
      typeBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-orange-100 text-orange-900 border border-orange-300 shadow-2xs">${m.classification_name}</span>`;
      rowBg = 'bg-orange-50/50 hover:bg-orange-100/40';
    } else {
      typeBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300 shadow-2xs">${m.classification_name}</span>`;
      rowBg = 'hover:bg-amber-50/50';
    }

    return `
      <tr class="${rowBg} transition border-b border-stone-200 last:border-0">
        <td class="p-3 font-bold text-stone-900 whitespace-nowrap">${m.year}</td>
        <td class="p-3 font-semibold text-amber-950 whitespace-nowrap font-serif-te">${m.samvatsara_name_telugu || m.samvatsara_name}</td>
        <td class="p-3 font-bold text-amber-900">${m.full_display_name}</td>
        <td class="p-3 text-center whitespace-nowrap">${typeBadge}</td>
        <td class="p-3 text-center font-mono font-bold text-stone-800">${m.sankranti_count}</td>
        <td class="p-3 font-mono text-stone-700 whitespace-nowrap">${m.start_date} నుండి ${m.end_date}</td>
        <td class="p-3 text-xs text-stone-600 max-w-xs">
          <div>${m.description}</div>
          ${m.shastra_verse ? `<div class="mt-1 text-[11px] font-serif-te font-semibold text-amber-800 italic">"${m.shastra_verse}"</div>` : ''}
        </td>
      </tr>
    `;
  }).join('');

  tbody.innerHTML = rowsHtml;
}

// ==========================================
// KANDADAYAM & NAKSHATRA TRIMESTERS LOGIC
// ==========================================

async function fetchKandadayam() {
  showLoader(true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(`/api/v1/rashi/kandadayam-all?year=${STATE.year}&language=${STATE.lang}`, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    STATE.kandadayamData = data;
    renderKandadayam(data);
  } catch (err) {
    clearTimeout(timeoutId);
    console.error('Error fetching Kandadayam data:', err);
  } finally {
    showLoader(false);
  }
}

function renderKandadayam(data) {
  if (!data) return;

  // 1. Update Badges & Titles
  const badge = document.getElementById('kdSamvatsaraBadge');
  if (badge) badge.innerText = data.samvatsara;

  // 2. Render 12 Rashi Kandadayam (Cards & Table)
  renderRashiKandadayam(data.rashis);

  // 3. Populate 27 Nakshatras Dropdown & Pills
  setupNakshatraPicker(data.nakshatras);

  // 4. Render Spotlight Nakshatra Details
  if (data.nakshatras && data.nakshatras.length > 0) {
    const activeNak = data.nakshatras[STATE.selectedNakshatraIdx] || data.nakshatras[0];
    renderNakshatraSpotlight(activeNak);
  }

  // 5. Render 27 Nakshatras Master Table
  renderNakshatrasMasterTable(data.nakshatras);
}

function renderRashiKandadayam(rashis) {
  if (!rashis) return;

  // Render Cards Grid
  const cardsContainer = document.getElementById('rashiKdCardsGrid');
  if (cardsContainer) {
    cardsContainer.innerHTML = rashis.map((item, idx) => {
      const isFinSurplus = item.aadhayam > item.vyayam;
      const isFinEqual = item.aadhayam === item.vyayam;
      const isSocHigh = item.rajapujyam > item.avamanam;
      const isSocEqual = item.rajapujyam === item.avamanam;

      const finBadgeClass = isFinSurplus 
        ? "bg-emerald-100 text-emerald-900 border-emerald-300" 
        : (isFinEqual ? "bg-amber-100 text-amber-900 border-amber-300" : "bg-rose-100 text-rose-900 border-rose-300");

      const socBadgeClass = isSocHigh
        ? "bg-purple-100 text-purple-900 border-purple-300"
        : (isSocEqual ? "bg-stone-100 text-stone-800 border-stone-300" : "bg-orange-100 text-orange-900 border-orange-300");

      return `
        <div class="vedic-card p-4 bg-white border border-amber-200 hover:border-amber-400 shadow-sm flex flex-col justify-between transition group">
          <div>
            <!-- Header: Symbol + Name + Lord -->
            <div class="flex items-center justify-between border-b border-amber-100 pb-2.5 mb-3">
              <div class="flex items-center gap-2">
                <span class="text-2xl">${item.rashi.symbol}</span>
                <div>
                  <h4 class="font-extrabold text-amber-950 text-base font-serif-te leading-tight">${item.rashi.name}</h4>
                  <span class="text-[11px] text-stone-500 font-medium">${item.rashi.name_english}</span>
                </div>
              </div>
              <span class="text-[11px] px-2 py-0.5 rounded-full font-bold bg-amber-50 text-amber-800 border border-amber-200">
                ${item.rashi.lord}
              </span>
            </div>

            <!-- Scores: Income vs Expense -->
            <div class="space-y-2 text-xs">
              <div>
                <div class="flex justify-between font-bold mb-1">
                  <span class="text-emerald-800">ఆదాయం: <span class="font-mono text-sm">${item.aadhayam}</span>/14</span>
                  <span class="text-rose-800">వ్యయం: <span class="font-mono text-sm">${item.vyayam}</span>/14</span>
                </div>
                <!-- Dual Comparative Progress Bar -->
                <div class="h-2 w-full bg-stone-100 rounded-full overflow-hidden flex">
                  <div class="bg-emerald-500 h-full" style="width: ${(item.aadhayam / 14) * 100}%"></div>
                  <div class="bg-rose-400 h-full ml-auto" style="width: ${(item.vyayam / 14) * 100}%"></div>
                </div>
              </div>

              <!-- Scores: Honor vs Disgrace -->
              <div class="pt-1">
                <div class="flex justify-between font-bold mb-1">
                  <span class="text-purple-800">రాజపూజ్యం: <span class="font-mono text-sm">${item.rajapujyam}</span>/8</span>
                  <span class="text-orange-800">అవమానం: <span class="font-mono text-sm">${item.avamanam}</span>/8</span>
                </div>
                <div class="h-2 w-full bg-stone-100 rounded-full overflow-hidden flex">
                  <div class="bg-purple-500 h-full" style="width: ${(item.rajapujyam / 8) * 100}%"></div>
                  <div class="bg-orange-400 h-full ml-auto" style="width: ${(item.avamanam / 8) * 100}%"></div>
                </div>
              </div>
            </div>

            <!-- Status Badges -->
            <div class="mt-3.5 space-y-1.5">
              <div class="px-2.5 py-1 rounded-lg border text-[11px] font-bold ${finBadgeClass} flex items-center gap-1.5">
                <span>${isFinSurplus ? '📈' : (isFinEqual ? '⚖️' : '📉')}</span>
                <span>${item.finance_status}</span>
              </div>
              <div class="px-2.5 py-1 rounded-lg border text-[11px] font-bold ${socBadgeClass} flex items-center gap-1.5">
                <span>${isSocHigh ? '👑' : (isSocEqual ? '🛡️' : '⚠️')}</span>
                <span>${item.social_status}</span>
              </div>
            </div>
          </div>

          <!-- Shastric Verdict -->
          <div class="mt-3 pt-2.5 border-t border-amber-100/80 text-[11px] font-semibold text-amber-950 italic">
            ✨ ${item.verdict}
          </div>
        </div>
      `;
    }).join('');
  }

  // Render Table View
  const tableBody = document.getElementById('rashiKdTableBody');
  if (tableBody) {
    tableBody.innerHTML = rashis.map(item => {
      const isFinSurplus = item.aadhayam > item.vyayam;
      const isSocHigh = item.rajapujyam > item.avamanam;

      return `
        <tr class="hover:bg-amber-50/50 transition border-b border-stone-200 last:border-0">
          <td class="p-3 font-extrabold text-amber-950 font-serif-te whitespace-nowrap">
            ${item.rashi.symbol} ${item.rashi.name} <span class="text-xs font-normal text-stone-500">(${item.rashi.name_english})</span>
          </td>
          <td class="p-3 font-medium text-stone-700 whitespace-nowrap">${item.rashi.lord}</td>
          <td class="p-3 text-center font-mono font-extrabold text-emerald-800 text-sm bg-emerald-50/40">${item.aadhayam}</td>
          <td class="p-3 text-center font-mono font-extrabold text-rose-800 text-sm bg-rose-50/40">${item.vyayam}</td>
          <td class="p-3 text-center font-mono font-extrabold text-purple-800 text-sm bg-purple-50/40">${item.rajapujyam}</td>
          <td class="p-3 text-center font-mono font-extrabold text-orange-800 text-sm bg-orange-50/40">${item.avamanam}</td>
          <td class="p-3 text-xs font-bold ${isFinSurplus ? 'text-emerald-800' : 'text-stone-700'}">${item.finance_status}</td>
          <td class="p-3 text-xs font-bold ${isSocHigh ? 'text-purple-800' : 'text-stone-700'}">${item.social_status}</td>
          <td class="p-3 text-xs font-semibold text-amber-900">${item.verdict}</td>
        </tr>
      `;
    }).join('');
  }
}

function setupNakshatraPicker(nakshatras) {
  if (!nakshatras) return;

  const dropdown = document.getElementById('nakshatraSelectDropdown');
  if (dropdown) {
    dropdown.innerHTML = nakshatras.map((n, idx) => `
      <option value="${idx}" ${idx === STATE.selectedNakshatraIdx ? 'selected' : ''}>
        ${n.id}. ${n.name}
      </option>
    `).join('');
  }

  const pillsContainer = document.getElementById('nakshatraQuickPills');
  if (pillsContainer) {
    pillsContainer.innerHTML = nakshatras.map((n, idx) => {
      const isSelected = idx === STATE.selectedNakshatraIdx;
      return `
        <button 
          onclick="selectNakshatra(${idx})" 
          class="shrink-0 px-3 py-1 rounded-full text-xs font-bold transition-all ${
            isSelected 
              ? 'bg-amber-700 text-white shadow-sm ring-2 ring-amber-400' 
              : 'bg-stone-100 text-stone-700 hover:bg-amber-100 hover:text-amber-900'
          }"
        >
          ${n.name}
        </button>
      `;
    }).join('');
  }
}

function selectNakshatra(idx) {
  STATE.selectedNakshatraIdx = idx;
  const dropdown = document.getElementById('nakshatraSelectDropdown');
  if (dropdown) dropdown.value = idx;

  if (STATE.kandadayamData && STATE.kandadayamData.nakshatras) {
    renderNakshatraSpotlight(STATE.kandadayamData.nakshatras[idx]);
    setupNakshatraPicker(STATE.kandadayamData.nakshatras);
    const searchInput = document.getElementById('nakshatraTableSearchInput');
    renderNakshatrasMasterTable(STATE.kandadayamData.nakshatras, searchInput ? searchInput.value.trim().toLowerCase() : '');
  }
}

function renderNakshatraSpotlight(item) {
  const container = document.getElementById('selectedNakshatraSpotlight');
  if (!container || !item) return;

  const getStatusBadge = (status) => {
    if (status.includes("ఉత్తమం") || status.includes("Excellent")) {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-emerald-100 text-emerald-900 border border-emerald-300">ఉత్తమం (Auspicious)</span>`;
    } else if (status.includes("అనుకూలం") || status.includes("Good")) {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-sky-100 text-sky-900 border border-sky-300">అనుకూలం (Favorable)</span>`;
    } else if (status.includes("మధ్యమం") || status.includes("Moderate")) {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-amber-100 text-amber-900 border border-amber-300">మధ్యమం (Moderate)</span>`;
    } else {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-rose-100 text-rose-900 border border-rose-300">అప్రమత్తత (Caution)</span>`;
    }
  };

  container.innerHTML = `
    <!-- Top Header for Selected Nakshatra -->
    <div class="p-4 rounded-2xl bg-gradient-to-r from-amber-100/80 via-amber-50 to-orange-50 border border-amber-300 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs px-2.5 py-0.5 rounded-full font-extrabold bg-amber-900 text-white font-mono">
            #${item.id}
          </span>
          <h3 class="text-xl md:text-2xl font-extrabold text-amber-950 font-serif-te">
            ${item.name} నక్షత్రం
          </h3>
        </div>
        <p class="text-xs font-semibold text-stone-600 mt-1 flex items-center gap-1">
          <span>వ్యాపించిన రాశులు / పాదాలు:</span>
          <span class="font-bold text-amber-900">${item.rashi_names.join(', ')}</span>
        </p>
      </div>

      <!-- Composite Annual Status -->
      <div class="bg-white px-4 py-2.5 rounded-xl border border-amber-200 shadow-sm text-left md:text-right">
        <div class="text-[10px] text-stone-500 font-bold uppercase tracking-wider">సంవత్సర సమగ్ర స్థితి</div>
        <div class="font-extrabold text-amber-950 text-sm mt-0.5">${item.overall_rating}</div>
      </div>
    </div>

    <!-- 3 Trimester Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Trimester 1 -->
      <div class="vedic-card p-5 bg-white border-2 border-amber-300 flex flex-col justify-between shadow-sm hover:shadow-md transition">
        <div>
          <div class="flex items-center justify-between border-b border-amber-100 pb-2 mb-3">
            <div>
              <h4 class="font-extrabold text-amber-950 text-sm">ప్రథమ కందాయం</h4>
              <p class="text-[11px] font-semibold text-stone-500">చైత్రం – ఆషాఢం (నెలలు 1–4)</p>
            </div>
            <div class="w-10 h-10 rounded-full bg-amber-50 border border-amber-300 flex items-center justify-center font-mono font-extrabold text-amber-900 text-lg shadow-2xs">
              ${item.trimester_1.score}
            </div>
          </div>
          <div class="mb-3">
            ${getStatusBadge(item.trimester_1.status)}
          </div>
          <p class="text-xs text-stone-700 leading-relaxed font-normal">
            ${item.trimester_1.prediction}
          </p>
        </div>
        <div class="mt-4 pt-2 border-t border-stone-100 text-[10px] font-semibold text-stone-400">
          గరిష్ట పరిమితి: 8 భాగాలు
        </div>
      </div>

      <!-- Trimester 2 -->
      <div class="vedic-card p-5 bg-white border-2 border-orange-300 flex flex-col justify-between shadow-sm hover:shadow-md transition">
        <div>
          <div class="flex items-center justify-between border-b border-orange-100 pb-2 mb-3">
            <div>
              <h4 class="font-extrabold text-amber-950 text-sm">ద్వితీయ కందాయం</h4>
              <p class="text-[11px] font-semibold text-stone-500">శ్రావణం – కార్తీకం (నెలలు 5–8)</p>
            </div>
            <div class="w-10 h-10 rounded-full bg-orange-50 border border-orange-300 flex items-center justify-center font-mono font-extrabold text-orange-950 text-lg shadow-2xs">
              ${item.trimester_2.score}
            </div>
          </div>
          <div class="mb-3">
            ${getStatusBadge(item.trimester_2.status)}
          </div>
          <p class="text-xs text-stone-700 leading-relaxed font-normal">
            ${item.trimester_2.prediction}
          </p>
        </div>
        <div class="mt-4 pt-2 border-t border-stone-100 text-[10px] font-semibold text-stone-400">
          గరిష్ట పరిమితి: 3 భాగాలు
        </div>
      </div>

      <!-- Trimester 3 -->
      <div class="vedic-card p-5 bg-white border-2 border-emerald-300 flex flex-col justify-between shadow-sm hover:shadow-md transition">
        <div>
          <div class="flex items-center justify-between border-b border-emerald-100 pb-2 mb-3">
            <div>
              <h4 class="font-extrabold text-amber-950 text-sm">తృతీయ కందాయం</h4>
              <p class="text-[11px] font-semibold text-stone-500">మార్గశిరం – ఫాల్గుణం (నెలలు 9–12)</p>
            </div>
            <div class="w-10 h-10 rounded-full bg-emerald-50 border border-emerald-300 flex items-center justify-center font-mono font-extrabold text-emerald-950 text-lg shadow-2xs">
              ${item.trimester_3.score}
            </div>
          </div>
          <div class="mb-3">
            ${getStatusBadge(item.trimester_3.status)}
          </div>
          <p class="text-xs text-stone-700 leading-relaxed font-normal">
            ${item.trimester_3.prediction}
          </p>
        </div>
        <div class="mt-4 pt-2 border-t border-stone-100 text-[10px] font-semibold text-stone-400">
          గరిష్ట పరిమితి: 5 భాగాలు
        </div>
      </div>
    </div>

    <!-- Overall Summary Callout -->
    <div class="p-4 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-950 font-medium leading-relaxed flex items-start gap-2.5">
      <span class="text-xl">💡</span>
      <div>
        <strong class="font-bold">సంవత్సర ఫలిత సారాంశం & సూచన:</strong> ${item.overall_status}
      </div>
    </div>
  `;
}

function renderNakshatrasMasterTable(nakshatras, filterTerm = '') {
  const tbody = document.getElementById('nakshatraKdTableBody');
  if (!tbody || !nakshatras) return;

  const filtered = filterTerm 
    ? nakshatras.filter(n => n.name.toLowerCase().includes(filterTerm) || n.rashi_names.some(r => r.toLowerCase().includes(filterTerm)))
    : nakshatras;

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="p-6 text-center text-stone-400 italic">నక్షత్ర ఫలితాలు ఏవీ కనుగొనబడలేదు</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(n => {
    return `
      <tr class="hover:bg-amber-50/50 transition border-b border-stone-200 last:border-0 cursor-pointer ${n.id === (STATE.selectedNakshatraIdx + 1) ? 'bg-amber-100/50 font-bold' : ''}" onclick="selectNakshatra(${n.id - 1})">
        <td class="p-3 font-mono text-center text-stone-500 font-bold">${n.id}</td>
        <td class="p-3 font-extrabold text-amber-950 font-serif-te whitespace-nowrap">${n.name}</td>
        <td class="p-3 text-xs text-stone-600 whitespace-nowrap">${n.rashi_names.join(', ')}</td>
        <td class="p-3 text-center whitespace-nowrap">
          <span class="font-mono font-extrabold text-amber-900 text-sm mr-1.5">${n.trimester_1.score}</span>
          <span class="text-[11px] px-2 py-0.5 rounded-full font-bold bg-amber-50 text-amber-800 border border-amber-200">${n.trimester_1.status}</span>
        </td>
        <td class="p-3 text-center whitespace-nowrap">
          <span class="font-mono font-extrabold text-orange-900 text-sm mr-1.5">${n.trimester_2.score}</span>
          <span class="text-[11px] px-2 py-0.5 rounded-full font-bold bg-orange-50 text-orange-800 border border-orange-200">${n.trimester_2.status}</span>
        </td>
        <td class="p-3 text-center whitespace-nowrap">
          <span class="font-mono font-extrabold text-emerald-900 text-sm mr-1.5">${n.trimester_3.score}</span>
          <span class="text-[11px] px-2 py-0.5 rounded-full font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">${n.trimester_3.status}</span>
        </td>
        <td class="p-3 text-center whitespace-nowrap text-xs font-bold text-amber-900">
          ${n.overall_rating}
        </td>
      </tr>
    `;
  }).join('');
}

function setupKandadayamControls() {
  const btnCards = document.getElementById('rashiKdViewCardsBtn');
  const btnTable = document.getElementById('rashiKdViewTableBtn');
  const containerCards = document.getElementById('rashiKdCardsGrid');
  const containerTable = document.getElementById('rashiKdTableContainer');

  if (btnCards && btnTable && containerCards && containerTable) {
    btnCards.addEventListener('click', () => {
      btnCards.className = "px-3 py-1 rounded-lg text-xs font-bold text-white bg-amber-700 shadow transition";
      btnTable.className = "px-3 py-1 rounded-lg text-xs font-bold text-stone-600 hover:text-stone-900 transition";
      containerCards.classList.remove('hidden');
      containerTable.classList.add('hidden');
    });

    btnTable.addEventListener('click', () => {
      btnTable.className = "px-3 py-1 rounded-lg text-xs font-bold text-white bg-amber-700 shadow transition";
      btnCards.className = "px-3 py-1 rounded-lg text-xs font-bold text-stone-600 hover:text-stone-900 transition";
      containerTable.classList.remove('hidden');
      containerCards.classList.add('hidden');
    });
  }

  // Jump buttons
  const jumpRashi = document.getElementById('jumpToRashiKdBtn');
  if (jumpRashi) jumpRashi.addEventListener('click', () => {
    document.getElementById('sectionRashiKd')?.scrollIntoView({ behavior: 'smooth' });
  });

  const jumpNakshatra = document.getElementById('jumpToNakshatraKdBtn');
  if (jumpNakshatra) jumpNakshatra.addEventListener('click', () => {
    document.getElementById('sectionNakshatraKd')?.scrollIntoView({ behavior: 'smooth' });
  });

  const jumpShastra = document.getElementById('jumpToShastraKdBtn');
  if (jumpShastra) jumpShastra.addEventListener('click', () => {
    document.getElementById('sectionShastraKd')?.scrollIntoView({ behavior: 'smooth' });
  });

  // Nakshatra dropdown
  const dropdown = document.getElementById('nakshatraSelectDropdown');
  if (dropdown) {
    dropdown.addEventListener('change', (e) => {
      selectNakshatra(parseInt(e.target.value));
    });
  }

  // Table search
  const searchInput = document.getElementById('nakshatraTableSearchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      if (STATE.kandadayamData && STATE.kandadayamData.nakshatras) {
        renderNakshatrasMasterTable(STATE.kandadayamData.nakshatras, e.target.value.trim().toLowerCase());
      }
    });
  }
}

let loaderWatchdogTimer = null;
function showLoader(show) {
  const loader = document.getElementById('globalLoader');
  if (!loader) return;
  if (loaderWatchdogTimer) {
    clearTimeout(loaderWatchdogTimer);
    loaderWatchdogTimer = null;
  }
  if (show) {
    loader.classList.remove('hidden');
    // Safety watchdog: auto-hide after 5 seconds under any circumstance
    loaderWatchdogTimer = setTimeout(() => {
      loader.classList.add('hidden');
      console.warn("Global loader watchdog triggered: auto-dismissed after 5s limit.");
    }, 5000);
  } else {
    loader.classList.add('hidden');
  }
}

// Register PWA Service Worker with auto-update
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/sw.js')
      .then(reg => {
        reg.update();
        console.log('ServiceWorker registered with scope:', reg.scope);
      })
      .catch(err => console.log('ServiceWorker registration failed:', err));
  });
}
