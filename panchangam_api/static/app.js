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
  sankalpaData: null,
  annualMoudhyamData: null
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
    khandaLabel: "ఖండం",

    prevDayTitle: "మునుపటి రోజు",
    nextDayTitle: "తరువాతి రోజు",
    maxWord: "గరిష్టం",
    bannerPurePeriod: "శుద్ధ కాలం",
    bannerTabooAuspicious: "శుభకార్యములు వర్జ్యం",
    bannerTabooConstruction: "గృహారంభం నిషిద్ధం",
    bannerAnnualScheduleBtn: "సంవత్సర పట్టిక & శాస్త్ర నియమాలు",
    modalMoudhyamTitle: "🪔 సంవత్సర మౌఢ్య & కర్తరి నిర్ణయ పట్టిక",
    modalMoudhyamSubtitle: "ఖగోళ నిరయణ గణితం • ధర్మశాస్త్ర ముహూర్త నిషేధాలు & ప్రాశస్త్యాలు",
    timezoneLabel: "సమయ మండలం",
    moudhyamTimesSubtitle: "🕒 సమయాలు: మీ స్థానిక సమయం & (IST భారత ప్రామాణిక సమయం)",
    thPhase: "విభాగం (Phase)",
    thTransit: "సూర్య సంచారం (Transit)",
    thTiming: "ఖచ్చితమైన సమయం (Timing)",
    thSignificance: "ప్రాముఖ్యత (Significance)",
    moudhyamSectionTitle: "మౌఢ్యములు (గురు & శుక్ర అస్తమయాలు)",
    moudhyamSectionSubtitle: "దేవగురు బృహస్పతి, దైత్యగురు శుక్రులు సూర్య సామీప్యంచే అస్తంగతులయ్యే కాలాలు.",
    durationLabel: "వ్యవధి",
    daysLabel: "రోజులు",
    moudhyamStartLabel: "ఆరంభం (అస్తమయం):",
    moudhyamEndLabel: "సమాప్తి (ఉదయం):",
    vardhakyaLabel: "వార్ధక్య దోషం:",
    balyaLabel: "బాల్య దోషం:",
    prohibitionLabel: "నిషేధం:",
    shastraDecisionsTitle: "ధర్మశాస్త్ర ముహూర్త నిర్ణయాలు (ఏవి చేయవచ్చు? ఏవి నిషిద్ధం?)",
    moudhyamTaboosTitle: "మౌఢ్యంలో నిషిద్ధాలు:",
    kartariTaboosTitle: "కర్తరిలో నిషిద్ధాలు:",
    permittedKarmasTitle: "ఆచరించదగినవి:",
    moudhyamLoading: "మౌఢ్య & కర్తరి నిర్ణయ పట్టిక లోడ్ అవుతోంది...",
    moudhyamError: "పట్టిక లోడ్ చేయడంలో లోపం ఏర్పడింది. దయచేసి మళ్ళీ ప్రయత్నించండి.",
    adhikaMasaBadge: "అధిక మాసం",
    nijaMasaBadge: "సాధారణ మాసం",
    kshayaMasaBadge: "క్షయ మాసం",
    sankrantiWord: "సంక్రాంతులు",
    shuklaPaksha: "శుక్ల పక్షము",
    krishnaPaksha: "కృష్ణ పక్షము",
    solarDaySuffix: "వ రోజు",
    intercalaryHeroBadge: "🏛️ ధర్మశాస్త్రం & ఖగోళ సిద్ధాంతం • కాలమాధవీయం",
    intercalaryHeroTitle: "అధిక మాసం & క్షయ మాస ఖగోళ-ధర్మశాస్త్ర విజ్ఞానం",
    intercalaryHeroSubtitle: "సూర్యసిద్ధాంత స్పష్టగతి మరియు కాలమాధవీయ సూత్రాల ప్రకారం అధిక, క్షయ, సంసర్ప, మరియు అంహస్పతి మాసాల సమగ్ర కాలగణన.",
    systemSuryaBtn: "📜 సూర్యసిద్ధాంతం (శాస్త్రం)",
    systemDrikBtn: "🔭 దృక్సిద్ధాంతం (Swiss Ephemeris)",
    suryaSystemBadge: "సూర్యసిద్ధాంత / ధర్మశాస్త్ర పద్ధతి",
    drikSystemBadge: "దృక్సిద్ధాంత పద్ధతి (Swiss Ephemeris)",
    kalamadhavaHeader: "కాలమాధవీయ పరమ ప్రామాణిక శ్లోకం (Kalamadhava Canonical Verse)",
    kalamadhavaRuleDesc: "<strong>ధర్మశాస్త్ర నియమం:</strong> ఒకే సౌర సంవత్సరంలో రెండు అసంక్రాంత మాసాలు వస్తే, మొదటి దానిని <strong>సంసర్పం</strong> అంటారు. మధ్యలో వచ్చే ద్విసంక్రాంత మాసమే <strong>క్షయ మాసం (అంహస్పతి)</strong>. సంవత్సరాంతంలో వచ్చే రెండవ అసంక్రాంత మాసం <strong>అధిక మాసం</strong> అవుతుంది. సంసర్పంలో నిత్య నైమిత్తిక కర్మలు చేయవచ్చు; అంహస్పతి (క్షయ) మాసంలో వివాహాది శుభకార్యాలు వర్జ్యం.",
    adhikaCardTitle: "అధిక మాసం (Asankranta)",
    adhikaCardBadge: "0 సంక్రాంతులు",
    adhikaCardFormula: "Ingresses = 0 (అసంక్రాంతం)",
    adhikaCardDesc: "ఒక అమావాస్య నుండి తర్వాతి అమావాస్య వరకు సూర్యుడు ఏ రాశి లోకీ ప్రవేశించకపోతే అది అధిక మాసం (మలమాసం). ప్రతి ~32.5 నెలలకు ఒకసారి వస్తుంది.",
    nijaCardTitle: "సాధారణ మాసం (Nija Masa)",
    nijaCardBadge: "1 సంక్రాంతి",
    nijaCardFormula: "Ingresses = 1 (సంక్రాంతం)",
    nijaCardDesc: "ఒక చాంద్రమాసంలో ఖచ్చితంగా ఒకే సూర్య సంక్రమణం సంభవిస్తే అది నిజ లేదా శుద్ధ మాసం. అన్ని శుభకార్యాలకు ప్రశస్తమైన కాలం.",
    kshayaCardTitle: "క్షయ మాసం (Dvi-Sankranta)",
    kshayaCardBadge: "2 సంక్రాంతులు",
    kshayaCardFormula: "Ingresses = 2 (ద్విసంక్రాంతం)",
    kshayaCardDesc: "ఒకే చాంద్రమాసంలో సూర్యుని 2 సంక్రాంతులు సంభవిస్తే అది క్షయ మాసం (అంహస్పతి). రెండు నెలలు యుగళీభూతమై ఒకటిగా మారుతాయి.",
    driftTitle: "📐 సౌర-చాంద్ర కాలగణన సూత్రాలు (Calendar Drift)",
    driftSolarYr: "సౌర సంవత్సరం:",
    driftLunarYr: "చాంద్ర సంవత్సరం (12 × 29.5):",
    driftAnnual: "వార్షిక లోటు (Annual Drift):",
    drift3Yr: "3 సంవత్సరాలలో చేరే లోటు:",
    driftLagadhaRule: "✨ <strong>వేదాంగ జ్యోతిష నియమం (లగధ మహర్షి):</strong> పంచసంవత్సరాత్మక యుగంలో 60 సౌర మాసాలు = 62 చాంద్ర మాసాలు. అంటే ప్రతి 5 సంవత్సరాలకు సరిగ్గా 2 అధిక మాసాలు వస్తాయి.",
    kaliyugaTitle: "🪐 కలియుగ మహాయుగ సమతుల్యత & క్షయ చక్రం",
    perihelionRule: "💡 <strong>ఖగోళ పెరిహిలియన్ నియమం:</strong> సూర్యుడు భూమికి దగ్గరగా ఉండి పరమోచ్ఛ వేగంతో ధనుస్సు, మకర, కుంభ రాశులను దాటినప్పుడు మాత్రమే చాంద్రమాసంలో 2 సంక్రాంతులు వచ్చే అవకాశం ఉంటుంది.",
    keelakaBadge: "ప్రత్యేక పరిశీలన",
    keelakaTitle: "శ్రీ కీలక నామ సంవత్సరం (2028 – 2029) • క్షయ & సంసర్ప మాసాలు",
    keelakaDesc: "హైదరాబాద్‌లోని గాంధీనగర్‌లో 23 మంది ప్రసిద్ధ సిద్ధాంతులు మరియు ధర్మశాస్త్ర పండితులతో జరిగిన <strong>'తెలంగాణ విద్వత్సభ' విద్వద్గోష్ఠి</strong> (ఆగస్టు 30, 2026) తీర్మానం ప్రకారం: <em>\"పూర్వసిద్ధాంతం సదా ఆచరణీయం\"</em> అనే సూత్రంపై, శ్రీ కీలక నామ సంవత్సరంలో <strong>సంసర్ప కార్తిక మాసం (అధికం)</strong> మరియు <strong>మార్గశిర-పుష్య యుగళీభూత అంహస్పతి మాసం (క్షయ మాసం)</strong> గా ఏకగ్రీవంగా నిర్ణయించబడింది.",
    intercalaryTableTitle: "📅 రాబోయే 10 సంవత్సరాల అధిక / క్షయ మాసాల పట్టిక (2026 – 2036)",
    intercalaryTableSubtitle: "ఎంచుకున్న సిద్ధాంత పద్ధతి ప్రకారం అమావాస్యాంత చాంద్రమాసాల ఫలితాలు",
    thInterYr: "సంవత్సరం",
    thInterSamvat: "తెలుగు సంవత్సరం",
    thInterMasa: "మాసం పేరు",
    thInterType: "రకం / హోదా",
    thInterSankranti: "సంక్రాంతులు",
    thInterSpan: "కాలం (ప్రారంభం – సమాప్తి)",
    thInterRule: "శాస్త్ర వివరణ",
    toDateSpan: "నుండి",
    kdHeroBadge: "📊 వార్షిక కందదాయ గణితం",
    kdMainHeading: "కందదాయ ఫలాలు & ఆదాయ వ్యయాలు",
    kdMainSubtitle: "ద్వాదశ రాశుల ఆదాయ-వ్యయ, రాజపూజ్య-అవమానాలు మరియు 27 నక్షత్రాల త్రైమాసిక (ప్రథమ, ద్వితీయ, తృతీయ కందాయాల) ప్రామాణిక ఫలితాలు.",
    kdCreatorBadge: "✍️ రూపకర్త: రామచంద్ర శాస్త్రి మునిమడుగు",
    jumpToRashiKdBtn: "💰 రాశి కందదాయం",
    jumpToNakshatraKdBtn: "⭐ నక్షత్ర కందాయాలు",
    jumpToShastraKdBtn: "📜 శాస్త్ర గణన సూత్రాలు",
    kdQuickT1Title: "🌱 ప్రథమ కందాయం",
    kdQuickT1Span: "మొదటి 4 నెలలు",
    kdQuickT1Months: "చైత్రం, వైశాఖం, జ్యేష్ఠం, ఆషాఢం",
    kdQuickT1Max: "గరిష్ట పరిమితి: 8 భాగాలు (0–7 శేషం)",
    kdQuickT2Title: "🌧️ ద్వితీయ కందాయం",
    kdQuickT2Span: "రెండవ 4 నెలలు",
    kdQuickT2Months: "శ్రావణం, భాద్రపదం, ఆశ్వయుజం, కార్తీకం",
    kdQuickT2Max: "గరిష్ట పరిమితి: 3 భాగాలు (0–2 శేషం)",
    kdQuickT3Title: "❄️ తృతీయ కందాయం",
    kdQuickT3Span: "మూడవ 4 నెలలు",
    kdQuickT3Months: "మార్గశిరం, పుష్యం, మాఘం, ఫాల్గుణం",
    kdQuickT3Max: "గరిష్ట పరిమితి: 5 భాగాలు (0–4 శేషం)",
    rashiKdSectionTitle: "💰 ద్వాదశ రాశి కందదాయం (ఆదాయం, వ్యయం, రాజపూజ్యం, అవమానం)",
    rashiKdSectionSubtitle: "శ్రీ పరాభవ నామ సంవత్సర ద్వాదశ రాశుల సంపూర్ణ ఆర్థిక & సామాజిక గౌరవ స్థితిగతులు",
    rashiKdViewCardsBtn: "కార్డులు",
    rashiKdViewTableBtn: "పట్టిక",
    thKdRashi: "రాశి",
    thKdLord: "అధిపతి",
    thKdAdayam: "ఆదాయం",
    thKdVyayam: "వ్యయం",
    thKdRajapujyam: "రాజపూజ్యం",
    thKdAvamanam: "అవమానం",
    thKdFinStatus: "ఆర్థిక స్థితి",
    thKdSocStatus: "సామాజిక గౌరవం",
    thKdVerdict: "సమగ్ర నిర్ణయం",
    nakshatraSectionTitle: "⭐ 27 నక్షత్ర కందాయ ఫలాలు (త్రైమాసిక విభజన)",
    nakshatraSectionSubtitle: "సంవత్సరంలోని 3 కందాయాల ప్రకారం మీ జన్మ నక్షత్ర ఫలితాలు తెలుసుకోండి",
    nakshatraSelectLabel: "నక్షత్రం:",
    nakshatraMasterTableTitle: "📋 సమగ్ర 27 నక్షత్రాల కందాయ పట్టిక (Master Table)",
    nakshatraTableSearchInput: "నక్షత్రం పేరుతో వెతకండి...",
    thNId: "క్ర.సం.",
    thNName: "నక్షత్రం",
    thNRashis: "రాశులు",
    thNT1: "ప్రథమ (1–4 నెలలు)",
    thNT2: "ద్వితీయ (5–8 నెలలు)",
    thNT3: "తృతీయ (9–12 నెలలు)",
    thNOverall: "వార్షిక స్థితి",
    shastraKdTitle: "📜 కందదాయ గణిత విజ్ఞానము & శాస్త్ర ప్రమాణాలు (Shastric Rules & Trimester Science)",
    shastraKdT1Title: "📅 సంవత్సర కాల విభజన (3 కందాయాలు)",
    shastraKdT2Title: "⚖️ ద్వాదశ రాశి కందదాయ గణితం",
    nakshatraWord: "నక్షత్రం",
    spreadRashisPadasLabel: "వ్యాపించిన రాశులు / పాదాలు:",
    annualCompositeStatusLabel: "సంవత్సర సమగ్ర స్థితి",
    trimester1Title: "ప్రథమ కందాయం",
    trimester1Months: "చైత్రం – ఆషాఢం (నెలలు 1–4)",
    trimester1MaxLimit: "గరిష్ట పరిమితి: 8 భాగాలు",
    trimester2Title: "ద్వితీయ కందాయం",
    trimester2Months: "శ్రావణం – కార్తీకం (నెలలు 5–8)",
    trimester2MaxLimit: "గరిష్ట పరిమితి: 3 భాగాలు",
    trimester3Title: "తృతీయ కందాయం",
    trimester3Months: "మార్గశిరం – ఫాల్గుణం (నెలలు 9–12)",
    trimester3MaxLimit: "గరిష్ట పరిమితి: 5 భాగాలు",
    annualSummaryAdviceLabel: "సంవత్సర ఫలిత సారాంశం & సూచన:",
    noNakshatraFound: "నక్షత్ర ఫలితాలు ఏవీ కనుగొనబడలేదు",
    rashiHeading: "రాశి ఫలాలు (Gochara Horoscope)",
    rashiSubtitle: "ఖగోళ గోచార సంచారం, చంద్రబలం, తారాబలం మరియు పంచాంగ కందాయ సూత్రాల ఆధారిత ప్రామాణిక ఫలితాలు.",
    rashiGocharaBadge: "♈ ద్వాదశ రాశి గోచారం",
    moonTransitLabel: "చంద్ర సంచారం",
    solarMonthLabel: "సౌర మాసం",
    kandadayamTableLabel: "పంచాంగ కందాయ పట్టిక",
    kdAdayam: "ఆదాయం",
    kdVyayam: "వ్యయం",
    kdRajapujyam: "రాజపూజ్యం",
    kdAvamanam: "అవమానం",
    statusAuspicious: "ఉత్తమం (Auspicious)",
    statusFavorable: "అనుకూలం (Favorable)",
    statusModerate: "మధ్యమం (Moderate)",
    statusCaution: "అప్రమత్తత (Caution)",
    footerOrgTitle: "వేద సంహిత • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "సిద్ధాంత & ఖగోళ కంప్యుటేషన్ రూపకర్త (System Architect & Creator)",
    footerCreatorName: "రామచంద్ర శాస్త్రి మునిమడుగు",
    footerCreatorDesc: "ఈ పంచాంగ గణనలు, వైదిక ఖగోళ సూత్రాలు, ధర్మశాస్త్ర నిర్ణయాలు మరియు సాంకేతిక క్రోడీకరణ సమగ్రంగా <strong class=\"text-amber-200 font-bold\">శ్రీ రామచంద్ర శాస్త్రి మునిమడుగు</strong> గారి పరిశోధన & రూపకల్పన ద్వారా రూపొందించబడినవి. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "అధికారిక వెబ్‌సైట్:",
    footerPoweredBy: "Swiss Ephemeris ఖగోళ గణనలు, జ్యోతిష ఇంజిన్ మరియు అక్షరముఖ బహుభాషా పరివర్తన ఆధారితం.",
    chandrashtamaAlertTitle: "చంద్రాష్టమ హెచ్చరిక (Chandrashtama Active)",
    chandrashtamaAlertDesc: "${t('chandrashtamaAlertDesc')}",
    moonHouseLabel: "చంద్ర స్థానం",
    houseSuffix: "వ ఇల్లు",
    tarabalamLabel: "తారాబలం",
    taraGood: "శుభ తార ✔️",
    taraCaution: "అప్రమత్తత ⚠️",
    luckyNumberLabel: "అదృష్ట సంఖ్య",
    luckyColorLabel: "అదృష్ట రంగు",
    luckyDirectionLabel: "అనుకూల దిశ",
    sunTransitLabel: "సూర్య సంక్రమణం",
    placeSuffix: "వ స్థానం",
    sunFavorable: "అనుకూల సూర్య బలం (ఉపచయం) ☀️",
    sunUnfavorable: "సూర్య ప్రతికూలత (ఓపిక అవసరం)",
    monthlyHighlightsLabel: "మాస ముఖ్యాంశాలు",
    guruBalamLabel: "గురు బలం",
    guruBalamYes: "గురు బలం కలదు ✨",
    guruBalamNo: "గురు శాంతి అవసరం",
    shaniGocharaLabel: "శని గోచారం",
    rahuKetuTransitLabel: "రాహు-కేతు సంచారం",
    financialAnalysisLabel: "ఆర్థిక స్థితి విశ్లేషణ",
    socialAnalysisLabel: "సామాజిక హోదా విశ్లేషణ",
    rashiOverviewTitle: "సాధారణ సమీక్ష (General Overview)",
    rashiCareerTitle: "ఉద్యోగం & వ్యాపారం (Career & Profession)",
    rashiFinanceTitle: "ఆర్థిక స్థితి & ధన యోగం (Finance & Wealth)",
    rashiHealthTitle: "ఆరోగ్యం & శక్తి (Health & Well-being)",
    rashiFamilyTitle: "కుటుంబం & దాంపత్యం (Family & Relationships)",
    rashiRemediesTitle: "శాంతి / దైవ పరిహారము (Remedies & Prayers)",
    lordLabel: "అధిపతి:",
    elementLabel: "తత్త్వం:",
    compatibilityScoreLabel: "అనుకూలత స్కోర్",
    chandrashtamaMiniBadge: "చంద్రాష్టమం",
    sunShortLabel: "రవి",
    incomeShort: "ఆ",
    expenseShort: "వ్య",
    gpsNotSupported: "మీ బ్రౌజర్‌లో GPS జియోలొకేషన్ సపోర్ట్ లేదు.",
    gpsSuccess: "లొకేషన్ విజయవంతంగా గుర్తించబడింది",
    gpsDenied: "లొకేషన్ అనుమతి లభించలేదు"
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
    khandaLabel: "Khanda",

    prevDayTitle: "Previous Day",
    nextDayTitle: "Next Day",
    maxWord: "Max",
    bannerPurePeriod: "Pure Period",
    bannerTabooAuspicious: "Auspicious Ceremonies Prohibited",
    bannerTabooConstruction: "Construction / Housewarming Prohibited",
    bannerAnnualScheduleBtn: "Annual Schedule & Shastric Rules",
    modalMoudhyamTitle: "🪔 Annual Moudhyam & Kartari Schedule",
    modalMoudhyamSubtitle: "Nirayana Ephemeris Computation • Muhurtha Dharma Shastra Prohibitions & Allowances",
    timezoneLabel: "Timezone",
    moudhyamTimesSubtitle: "🕒 Timings: Your Local Time & (IST Indian Standard Time)",
    thPhase: "Phase",
    thTransit: "Solar Transit",
    thTiming: "Exact Timing",
    thSignificance: "Significance",
    moudhyamSectionTitle: "Moudhyam Periods (Combustion of Jupiter & Venus)",
    moudhyamSectionSubtitle: "Inauspicious periods when Jupiter or Venus are in deep celestial conjunction with the Sun.",
    durationLabel: "Duration",
    daysLabel: "days",
    moudhyamStartLabel: "Start (Combustion / Set):",
    moudhyamEndLabel: "End (Helical Rise):",
    vardhakyaLabel: "Vardhakya Dosha:",
    balyaLabel: "Balya Dosha:",
    prohibitionLabel: "Prohibition:",
    shastraDecisionsTitle: "Dharma Shastra Muhurtha Rules (Permitted vs Prohibited)",
    moudhyamTaboosTitle: "Taboos in Moudhyam:",
    kartariTaboosTitle: "Taboos in Kartari:",
    permittedKarmasTitle: "Permitted Karmas:",
    moudhyamLoading: "Loading Moudhyam & Kartari schedule...",
    moudhyamError: "Error loading schedule. Please try again.",
    adhikaMasaBadge: "Adhika Masa",
    nijaMasaBadge: "Nija Masa",
    kshayaMasaBadge: "Kshaya Masa",
    sankrantiWord: "Sankrantis",
    shuklaPaksha: "Shukla Paksha",
    krishnaPaksha: "Krishna Paksha",
    solarDaySuffix: "day",
    intercalaryHeroBadge: "🏛️ Dharma Shastra & Astronomy • Kalamadhaviyam",
    intercalaryHeroTitle: "Adhika & Kshaya Masas: Astronomy & Dharma Shastra Computation",
    intercalaryHeroSubtitle: "Comprehensive calculation of Adhika, Kshaya, Samsarpa, and Amhaspati months according to Surya Siddhanta and Kalamadhaviya shastric canons.",
    systemSuryaBtn: "📜 Surya Siddhanta (Shastra)",
    systemDrikBtn: "🔭 Drik Siddhanta (Swiss Ephemeris)",
    suryaSystemBadge: "Surya Siddhanta / Dharma Shastra Method",
    drikSystemBadge: "Drik Siddhanta Method (Swiss Ephemeris)",
    kalamadhavaHeader: "Kalamadhava Canonical Verse (Kalamadhaviyam)",
    kalamadhavaRuleDesc: "<strong>Dharma Shastra Rule:</strong> When two asankranta (no solar ingress) months occur in a single solar year, the first is <strong>Samsarpa</strong>. The intermediate month with two ingresses is the <strong>Kshaya Masa (Amhaspati)</strong>. The subsequent asankranta month is the <strong>Adhika Masa</strong>. Routine (Nitya/Naimittika) rites are permitted in Samsarpa; auspicious events like weddings are strictly taboo in Amhaspati (Kshaya).",
    adhikaCardTitle: "Adhika Masa (Asankranta)",
    adhikaCardBadge: "0 Ingresses",
    adhikaCardFormula: "Ingresses = 0 (Asankranta)",
    adhikaCardDesc: "When the Sun does not transit into any new zodiac sign between two successive Amavasyas (New Moons), it is an Adhika Masa. Occurs every ~32.5 lunar months.",
    nijaCardTitle: "Nija Masa (Normal Lunar Month)",
    nijaCardBadge: "1 Ingress",
    nijaCardFormula: "Ingresses = 1 (Sankranta)",
    nijaCardDesc: "A standard lunar month containing exactly one solar ingress. Propitious for all auspicious events and Vedic sacraments.",
    kshayaCardTitle: "Kshaya Masa (Dvi-Sankranta)",
    kshayaCardBadge: "2 Ingresses",
    kshayaCardFormula: "Ingresses = 2 (Dvi-Sankranta)",
    kshayaCardDesc: "When two solar ingresses occur within a single lunar month, it is an expunged or Kshaya month (Amhaspati), fusing two months into one.",
    driftTitle: "📐 Solar-Lunar Calendar Principles (Calendar Drift)",
    driftSolarYr: "Solar Year:",
    driftLunarYr: "Lunar Year (12 × 29.5):",
    driftAnnual: "Annual Drift:",
    drift3Yr: "Drift accumulated in 3 years:",
    driftLagadhaRule: "✨ <strong>Vedanga Jyotisha Canon (Sage Lagadha):</strong> In a 5-year Yuga cycle, 60 Solar months equal 62 Lunar months. Exactly 2 Adhika Masas occur every 5 years.",
    kaliyugaTitle: "🪐 Kaliyuga Cosmic Balance & Kshaya Recurrence Cycle",
    perihelionRule: "💡 <strong>Astronomical Perihelion Rule:</strong> Two solar ingresses within one lunar month can only occur when Earth is near perihelion and the Sun transits rapidly through Sagittarius, Capricorn, or Aquarius.",
    keelakaBadge: "Special Case Study",
    keelakaTitle: "Sri Keelaka Samvatsara (2028–2029) • Kshaya & Samsarpa Months",
    keelakaDesc: "According to the unanimous resolution of the <strong>'Telangana Vidwatsabha' Conference</strong> of 23 eminent Siddhantis and Vedic Scholars (Aug 30, 2026): In Sri Keelaka Samvatsara, Kartika is established as <strong>Samsarpa Kartika (Adhika)</strong>, followed by the combined Margashira-Pushya <strong>Amhaspati Masa (Kshaya Masa)</strong>.",
    intercalaryTableTitle: "📅 10-Year Adhika & Kshaya Masas Schedule (2026–2036)",
    intercalaryTableSubtitle: "Amanta lunar month calculations computed under the selected siddhanta system",
    thInterYr: "Year",
    thInterSamvat: "Samvatsara Name",
    thInterMasa: "Month Name",
    thInterType: "Type / Status",
    thInterSankranti: "Ingresses",
    thInterSpan: "Span (Start – End)",
    thInterRule: "Shastric Rule",
    toDateSpan: "to",
    kdHeroBadge: "📊 Annual Kandadayam Computation",
    kdMainHeading: "Kandadayam Results & Income-Expenditure",
    kdMainSubtitle: "Canonical results for 12 Rashis (Income, Expense, Honor, Disgrace) and 27 Nakshatras across 3 Trimesters (Prathama, Dvitiya, Tritiya Kandayams).",
    kdCreatorBadge: "✍️ Created by: Ramachandra Sastry Munimadugu",
    jumpToRashiKdBtn: "💰 Rashi Kandadayam",
    jumpToNakshatraKdBtn: "⭐ Nakshatra Trimesters",
    jumpToShastraKdBtn: "📜 Shastric Computation Rules",
    kdQuickT1Title: "🌱 First Trimester (Prathama)",
    kdQuickT1Span: "Months 1–4",
    kdQuickT1Months: "Chaitra, Vaishakha, Jyeshtha, Ashadha",
    kdQuickT1Max: "Max Limit: 8 Units (Remainder 0–7)",
    kdQuickT2Title: "🌧️ Second Trimester (Dvitiya)",
    kdQuickT2Span: "Months 5–8",
    kdQuickT2Months: "Shravana, Bhadrapada, Ashwayuja, Kartika",
    kdQuickT2Max: "Max Limit: 3 Units (Remainder 0–2)",
    kdQuickT3Title: "❄️ Third Trimester (Tritiya)",
    kdQuickT3Span: "Months 9–12",
    kdQuickT3Months: "Margashira, Pushya, Magha, Phalguna",
    kdQuickT3Max: "Max Limit: 5 Units (Remainder 0–4)",
    rashiKdSectionTitle: "💰 12 Rashi Kandadayam (Income, Expense, Honor, Disgrace)",
    rashiKdSectionSubtitle: "Comprehensive financial and social status evaluation of all 12 Rashis",
    rashiKdViewCardsBtn: "Cards",
    rashiKdViewTableBtn: "Table",
    thKdRashi: "Rashi",
    thKdLord: "Lord",
    thKdAdayam: "Income (Adayam)",
    thKdVyayam: "Expense (Vyayam)",
    thKdRajapujyam: "Honor (Rajapujyam)",
    thKdAvamanam: "Disgrace (Avamanam)",
    thKdFinStatus: "Financial Status",
    thKdSocStatus: "Social Honor",
    thKdVerdict: "Verdict",
    nakshatraSectionTitle: "⭐ 27 Nakshatra Kandayam Results (Trimester Breakdown)",
    nakshatraSectionSubtitle: "Discover your birth star results across the 3 trimester periods of the year",
    nakshatraSelectLabel: "Nakshatra:",
    nakshatraMasterTableTitle: "📋 Master Table: 27 Nakshatras Trimester Kandayam",
    nakshatraTableSearchInput: "Search by star name...",
    thNId: "S.No",
    thNName: "Nakshatra",
    thNRashis: "Rashis",
    thNT1: "First (Months 1–4)",
    thNT2: "Second (Months 5–8)",
    thNT3: "Third (Months 9–12)",
    thNOverall: "Annual Rating",
    shastraKdTitle: "📜 Shastric Rules & Trimester Science of Kandadayam",
    shastraKdT1Title: "📅 Year Division (3 Trimesters / Kandayams)",
    shastraKdT2Title: "⚖️ 12 Rashi Kandadayam Mathematical Principles",
    nakshatraWord: "Nakshatra",
    spreadRashisPadasLabel: "Spread Rashis / Padas:",
    annualCompositeStatusLabel: "Annual Composite Status",
    trimester1Title: "First Trimester",
    trimester1Months: "Chaitra – Ashadha (Months 1–4)",
    trimester1MaxLimit: "Max limit: 8 units",
    trimester2Title: "Second Trimester",
    trimester2Months: "Shravana – Kartika (Months 5–8)",
    trimester2MaxLimit: "Max limit: 3 units",
    trimester3Title: "Third Trimester",
    trimester3Months: "Margashira – Phalguna (Months 9–12)",
    trimester3MaxLimit: "Max limit: 5 units",
    annualSummaryAdviceLabel: "Annual Summary & Guidance:",
    noNakshatraFound: "No nakshatra results found",
    rashiHeading: "Rashi Phalalu (Gochara Horoscope)",
    rashiSubtitle: "Authoritative predictions based on celestial transits, Chandrabalam, Tarabalam, and Panchangam Kandadayam principles.",
    rashiGocharaBadge: "♈ 12 Rashis Gochara",
    moonTransitLabel: "Moon Transit",
    solarMonthLabel: "Solar Month",
    kandadayamTableLabel: "Panchangam Kandadayam Table",
    kdAdayam: "Income",
    kdVyayam: "Expense",
    kdRajapujyam: "Honor",
    kdAvamanam: "Disgrace",
    statusAuspicious: "Auspicious",
    statusFavorable: "Favorable",
    statusModerate: "Moderate",
    statusCaution: "Caution",
    footerOrgTitle: "Vedic Samhita • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "System Architect & Creator (Astronomical Siddhanta Computation)",
    footerCreatorName: "Ramachandra Sastry Munimadugu",
    footerCreatorDesc: "These panchangam algorithms, Vedic astronomical models, Dharma Shastra canons, and computational systems are authored and architected by <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "Official Website:",
    footerPoweredBy: "Powered by Swiss Ephemeris astronomical computation engine and Aksharamukha script transliteration.",
    chandrashtamaAlertTitle: "Chandrashtama Warning (Chandrashtama Active)",
    chandrashtamaAlertDesc: "Today the Moon transits the 8th house from your Janma Rashi. Exercise utmost caution in arguments, financial dealings, and launching major new agreements. Worship of Lord Shiva is recommended.",
    moonHouseLabel: "Moon House",
    houseSuffix: "th House",
    tarabalamLabel: "Tarabalam",
    taraGood: "Auspicious Tara ✔️",
    taraCaution: "Caution ⚠️",
    luckyNumberLabel: "Lucky Number",
    luckyColorLabel: "Lucky Color",
    luckyDirectionLabel: "Lucky Direction",
    sunTransitLabel: "Solar Transit",
    placeSuffix: "th House",
    sunFavorable: "Favorable Sun Strength (Upachaya) ☀️",
    sunUnfavorable: "Sun Adversity (Patience required)",
    monthlyHighlightsLabel: "Monthly Highlights",
    guruBalamLabel: "Guru Balam",
    guruBalamYes: "Guru Balam Present ✨",
    guruBalamNo: "Guru Shanti Recommended",
    shaniGocharaLabel: "Saturn Transit",
    rahuKetuTransitLabel: "Rahu-Ketu Transit",
    financialAnalysisLabel: "Financial Status Analysis",
    socialAnalysisLabel: "Social Status Analysis",
    rashiOverviewTitle: "General Overview",
    rashiCareerTitle: "Career & Profession",
    rashiFinanceTitle: "Finance & Wealth",
    rashiHealthTitle: "Health & Well-being",
    rashiFamilyTitle: "Family & Relationships",
    rashiRemediesTitle: "Remedies & Prayers",
    lordLabel: "Lord:",
    elementLabel: "Element:",
    compatibilityScoreLabel: "Compatibility Score",
    chandrashtamaMiniBadge: "Chandrashtama",
    sunShortLabel: "Sun",
    incomeShort: "Inc",
    expenseShort: "Exp",
    gpsNotSupported: "GPS Geolocation is not supported by your browser.",
    gpsSuccess: "Location detected successfully",
    gpsDenied: "Location permission denied"
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
    khandaLabel: "खण्ड",

    prevDayTitle: "पिछला दिन",
    nextDayTitle: "अगला दिन",
    maxWord: "अधिकतम",
    bannerPurePeriod: "शुद्ध काल",
    bannerTabooAuspicious: "शुभकार्य वर्ज्य",
    bannerTabooConstruction: "गृहारम्भ निषिद्ध",
    bannerAnnualScheduleBtn: "वार्षिक सारणी एवं शास्त्रीय नियम",
    modalMoudhyamTitle: "🪔 वार्षिक मौढ्य एवं कर्तरी निर्णय सारणी",
    modalMoudhyamSubtitle: "खगोलीय निरयण गणित • धर्मशास्त्र मुहूर्त निषेध एवं प्राशस्त्य",
    timezoneLabel: "समय मण्डल",
    moudhyamTimesSubtitle: "🕒 समय: आपका स्थानीय समय एवं (IST भारतीय मानक समय)",
    thPhase: "विभाग (Phase)",
    thTransit: "सूर्य सञ्चार (Transit)",
    thTiming: "सटीक समय (Timing)",
    thSignificance: "महत्त्व (Significance)",
    moudhyamSectionTitle: "मौढ्य काल (गुरु एवं शुक्र अस्त)",
    moudhyamSectionSubtitle: "देवगुरु बृहस्पति एवं दैत्यगुरु शुक्र के सूर्य सान्निध्य से अस्त होने का काल।",
    durationLabel: "अवधि",
    daysLabel: "दिन",
    moudhyamStartLabel: "आरम्भ (अस्त):",
    moudhyamEndLabel: "समाप्ति (उदय):",
    vardhakyaLabel: "वार्धक्य दोष:",
    balyaLabel: "बाल्य दोष:",
    prohibitionLabel: "निषेध:",
    shastraDecisionsTitle: "धर्मशास्त्र मुहूर्त निर्णय (क्या करें? क्या वर्जित है?)",
    moudhyamTaboosTitle: "मौढ्य में निषिद्ध:",
    kartariTaboosTitle: "कर्तरी में निषिद्ध:",
    permittedKarmasTitle: "अनुमोदित कर्म:",
    moudhyamLoading: "मौढ्य एवं कर्तरी सारणी लोड हो रही है...",
    moudhyamError: "सारणी लोड करने में त्रुटि हुई। कृपया पुनः प्रयास करें।",
    adhikaMasaBadge: "अधिक मास",
    nijaMasaBadge: "सामान्य मास",
    kshayaMasaBadge: "क्षय मास",
    sankrantiWord: "संक्रान्तियां",
    shuklaPaksha: "शुक्ल पक्ष",
    krishnaPaksha: "कृष्ण पक्ष",
    solarDaySuffix: "वां दिन",
    intercalaryHeroBadge: "🏛️ धर्मशास्त्र एवं खगोल सिद्धान्त • कालमाधवीयम्",
    intercalaryHeroTitle: "अधिक मास एवं क्षय मास: खगोल-धर्मशास्त्र विज्ञान",
    intercalaryHeroSubtitle: "सूर्यसिद्धान्त स्पष्टगति एवं कालमाधवीय सूत्रों के अनुसार अधिक, क्षय, संसर्प एवं अंहस्पति मासों की गणना।",
    systemSuryaBtn: "📜 सूर्यसिद्धान्त (शास्त्र)",
    systemDrikBtn: "🔭 दृक्सिद्धान्त (Swiss Ephemeris)",
    suryaSystemBadge: "सूर्यसिद्धान्त / धर्मशास्त्र पद्धति",
    drikSystemBadge: "दृक्सिद्धान्त पद्धति (Swiss Ephemeris)",
    kalamadhavaHeader: "कालमाधवीय परम प्रामाणिक श्लोक",
    kalamadhavaRuleDesc: "<strong>धर्मशास्त्र नियम:</strong> एक सौर वर्ष में यदि दो असंक्रान्त मास आएं, तो प्रथम को <strong>संसर्प</strong> कहते हैं। मध्य में आने वाला द्विसंक्रान्त मास <strong>क्षय मास (अंहस्पति)</strong> है। वर्षान्त में आने वाला द्वितीय असंक्रान्त मास <strong>अधिक मास</strong> होता है। संसर्प में नित्य-नैमित्तिक कर्म मान्य हैं; अंहस्पति (क्षय) मास में विवाहादि शुभकार्य वर्जित हैं।",
    adhikaCardTitle: "अधिक मास (असंक्रान्त)",
    adhikaCardBadge: "० संक्रान्ति",
    adhikaCardFormula: "Ingresses = 0 (असंक्रान्त)",
    adhikaCardDesc: "एक अमावस्या से अगली अमावस्या तक जब सूर्य किसी भी राशि में प्रवेश नहीं करता, वह अधिक मास (मलमास) कहलाता है। प्रति ~३२.५ चान्द्रमासों में आता है।",
    nijaCardTitle: "सामान्य मास (निज मास)",
    nijaCardBadge: "१ संक्रान्ति",
    nijaCardFormula: "Ingresses = 1 (संक्रान्त)",
    nijaCardDesc: "एक चान्द्रमास में जब ठीक एक ही सूर्य संक्रान्ति होती है, वह निज या शुद्ध मास कहलाता है। सभी शुभ कार्यों के लिए उपयुक्त।",
    kshayaCardTitle: "क्षय मास (द्विसंक्रान्त)",
    kshayaCardBadge: "२ संक्रान्तियां",
    kshayaCardFormula: "Ingresses = 2 (द्विसंक्रान्त)",
    kshayaCardDesc: "एक ही चान्द्रमास में जब सूर्य की दो संक्रान्तियां घटित हों, वह क्षय मास (अंहस्पति) कहलाता है। दो मास मिलकर एक हो जाते हैं।",
    driftTitle: "📐 सौर-चान्द्र कालगणना सिद्धान्त (Calendar Drift)",
    driftSolarYr: "सौर वर्ष:",
    driftLunarYr: "चान्द्र वर्ष (12 × 29.5):",
    driftAnnual: "वार्षिक अन्तर (Annual Drift):",
    drift3Yr: "३ वर्षों में एकत्रित अन्तर:",
    driftLagadhaRule: "✨ <strong>वेदाङ्ग ज्योतिष नियम (लगध महर्षि):</strong> पञ्चसंवत्सरात्मक युग में ६० सौर मास = ६२ चान्द्र मास। अर्थात् प्रति ५ वर्षों में ठीक २ अधिक मास आते हैं।",
    kaliyugaTitle: "🪐 कलियुग महायुग सन्तुलन एवं क्षय चक्र",
    perihelionRule: "💡 <strong>खगोलीय उपसौर (Perihelion) नियम:</strong> सूर्य जब पृथ्वी के निकटतम होकर तीव्र गति से धनु, मकर या कुम्भ राशियों को पार करता है, तभी एक चान्द्रमास में २ संक्रान्तियां संभव होती हैं।",
    keelakaBadge: "विशेष अनुशीलन",
    keelakaTitle: "श्री कीलक संवत्सर (2028–2029) • क्षय एवं संसर्प मास",
    keelakaDesc: "२३ प्रसिद्ध सिद्धान्तियों एवं धर्मशास्त्र पण्डितों की 'तेलंगाना विद्वत्सभा' संगोष्ठी के सर्वसम्मत निर्णय के अनुसार: श्री कीलक संवत्सर में <strong>संसर्प कार्तिक मास (अधिक)</strong> तथा <strong>मार्गशीर्ष-पौष युगल अंहस्पति मास (क्षय मास)</strong> निश्चित किया गया है।",
    intercalaryTableTitle: "📅 आगामी १० वर्षों की अधिक / क्षय मास सारणी (2026–2036)",
    intercalaryTableSubtitle: "चयनित सिद्धान्त के अनुसार अमान्त चान्द्रमासों के परिणाम",
    thInterYr: "वर्ष",
    thInterSamvat: "संवत्सर नाम",
    thInterMasa: "मास नाम",
    thInterType: "प्रकार / स्थिति",
    thInterSankranti: "संक्रान्तियां",
    thInterSpan: "अवधि (आरम्भ – समाप्ति)",
    thInterRule: "शास्त्र व्याख्या",
    toDateSpan: "से",
    kdHeroBadge: "📊 वार्षिक कन्ददाय गणित",
    kdMainHeading: "कन्ददाय फलानि एवं आय-व्यय",
    kdMainSubtitle: "द्वादश राशियों के आय-व्यय, राजपूज्य-अपमान एवं २७ नक्षत्रों के त्रैमासिक (प्रथम, द्वितीय, तृतीय कन्ददाय) प्रामाणिक फल।",
    kdCreatorBadge: "✍️ निर्माता: रामचन्द्र शास्त्री मुनिमडुगु",
    jumpToRashiKdBtn: "💰 राशि कन्ददाय",
    jumpToNakshatraKdBtn: "⭐ नक्षत्र कन्ददाय",
    jumpToShastraKdBtn: "📜 शास्त्रीय गणना सूत्र",
    kdQuickT1Title: "🌱 प्रथम कन्ददाय",
    kdQuickT1Span: "प्रथम ४ मास",
    kdQuickT1Months: "चैत्र, वैशाख, ज्येष्ठ, आषाढ",
    kdQuickT1Max: "अधिकतम सीमा: ८ भाग (शेष ०-७)",
    kdQuickT2Title: "🌧️ द्वितीय कन्ददाय",
    kdQuickT2Span: "द्वितीय ४ मास",
    kdQuickT2Months: "श्रावण, भाद्रपद, आश्विन, कार्तिक",
    kdQuickT2Max: "अधिकतम सीमा: ३ भाग (शेष ०-२)",
    kdQuickT3Title: "❄️ तृतीय कन्ददाय",
    kdQuickT3Span: "तृतीय ४ मास",
    kdQuickT3Months: "मार्गशीर्ष, पौष, माघ, फाल्गुन",
    kdQuickT3Max: "अधिकतम सीमा: ५ भाग (शेष ०-४)",
    rashiKdSectionTitle: "💰 द्वादश राशि कन्ददाय (आय, व्यय, राजपूज्य, अपमान)",
    rashiKdSectionSubtitle: "द्वादश राशियों की सम्पूर्ण आर्थिक एवं सामाजिक स्थिति",
    rashiKdViewCardsBtn: "कार्ड",
    rashiKdViewTableBtn: "सारणी",
    thKdRashi: "राशि",
    thKdLord: "स्वामी",
    thKdAdayam: "आय",
    thKdVyayam: "व्यय",
    thKdRajapujyam: "राजपूज्य",
    thKdAvamanam: "अपमान",
    thKdFinStatus: "आर्थिक स्थिति",
    thKdSocStatus: "सामाजिक प्रतिष्ठा",
    thKdVerdict: "समग्र निर्णय",
    nakshatraSectionTitle: "⭐ २७ नक्षत्र कन्ददाय फल (त्रैमासिक विभाजन)",
    nakshatraSectionSubtitle: "वर्ष के ३ कन्ददायों के अनुसार अपने जन्म नक्षत्र का फल जानें",
    nakshatraSelectLabel: "नक्षत्र:",
    nakshatraMasterTableTitle: "📋 सम्पूर्ण २७ नक्षत्र कन्ददाय सारणी (Master Table)",
    nakshatraTableSearchInput: "नक्षत्र नाम से खोजें...",
    thNId: "क्र.सं.",
    thNName: "नक्षत्र",
    thNRashis: "राशियां",
    thNT1: "प्रथम (१–४ मास)",
    thNT2: "द्वितीय (५–८ मास)",
    thNT3: "तृतीय (९–१२ मास)",
    thNOverall: "वार्षिक स्थिति",
    shastraKdTitle: "📜 कन्ददाय गणित विज्ञान एवं शास्त्रीय प्रमाण",
    shastraKdT1Title: "📅 संवत्सर काल विभाजन (३ कन्ददाय)",
    shastraKdT2Title: "⚖️ द्वादश राशि कन्ददाय गणित",
    nakshatraWord: "नक्षत्र",
    spreadRashisPadasLabel: "विस्तृत राशियां / पाद:",
    annualCompositeStatusLabel: "वार्षिक समग्र स्थिति",
    trimester1Title: "प्रथम कन्ददाय",
    trimester1Months: "चैत्र – आषाढ (मास १–४)",
    trimester1MaxLimit: "अधिकतम सीमा: ८ भाग",
    trimester2Title: "द्वितीय कन्ददाय",
    trimester2Months: "श्रावण – कार्तिक (मास ५–८)",
    trimester2MaxLimit: "अधिकतम सीमा: ३ भाग",
    trimester3Title: "तृतीय कन्ददाय",
    trimester3Months: "मार्गशीर्ष – फाल्गुन (मास ९–१२)",
    trimester3MaxLimit: "अधिकतम सीमा: ५ भाग",
    annualSummaryAdviceLabel: "वार्षिक फल सारांश एवं मार्गदर्शन:",
    noNakshatraFound: "कोई नक्षत्र परिणाम नहीं मिला",
    rashiHeading: "राशि फल (गोचर होरोस्कोप)",
    rashiSubtitle: "खगोलीय गोचर सञ्चार, चन्द्रबल, ताराबल एवं कन्ददाय सूत्रों पर आधारित प्रामाणिक फल।",
    rashiGocharaBadge: "♈ द्वादश राशि गोचर",
    moonTransitLabel: "चन्द्र सञ्चार",
    solarMonthLabel: "सौर मास",
    kandadayamTableLabel: "पञ्चाङ्ग कन्ददाय सारणी",
    kdAdayam: "आय",
    kdVyayam: "व्यय",
    kdRajapujyam: "राजपूज्य",
    kdAvamanam: "अपमान",
    statusAuspicious: "उत्तम (Auspicious)",
    statusFavorable: "अनुकूल (Favorable)",
    statusModerate: "मध्यम (Moderate)",
    statusCaution: "सावधानी (Caution)",
    footerOrgTitle: "वैदिक संहिता • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "सिद्धान्त एवं खगोल संगणना निर्माता (System Architect & Creator)",
    footerCreatorName: "रामचन्द्र शास्त्री मुनिमडुगु",
    footerCreatorDesc: "ये पञ्चाङ्ग गणनाएं, वैदिक खगोलीय सूत्र, धर्मशास्त्र निर्णय एवं तकनीकी प्रणालियां <strong class=\"text-amber-200 font-bold\">श्री रामचन्द्र शास्त्री मुनिमडुगु</strong> के अनुसन्धान एवं रचना द्वारा निर्मित हैं। <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "आधिकारिक वेबसाइट:",
    footerPoweredBy: "Swiss Ephemeris खगोलीय गणना, ज्योतिषीय इंजन एवं अक्षरामुख बहुभाषी लिप्यन्तरण पर आधारित।",
    chandrashtamaAlertTitle: "चन्द्राष्टम चेतावनी (Chandrashtama Active)",
    chandrashtamaAlertDesc: "आज चन्द्रमा आपकी जन्म राशि से ८वें भाव में गोचर कर रहे हैं। वाद-विवाद, वित्तीय लेन-देन तथा नए समझौतों में विशेष सावधानी बरतें। शिवोपासना शुभप्रद है।",
    moonHouseLabel: "चन्द्र भाव",
    houseSuffix: "वां भाव",
    tarabalamLabel: "ताराबल",
    taraGood: "शुभ तारा ✔️",
    taraCaution: "सावधानी ⚠️",
    luckyNumberLabel: "शुभ अंक",
    luckyColorLabel: "शुभ रंग",
    luckyDirectionLabel: "शुभ दिशा",
    sunTransitLabel: "सूर्य संक्रान्ति",
    placeSuffix: "वां स्थान",
    sunFavorable: "अनुकूल सूर्य बल (उपचय) ☀️",
    sunUnfavorable: "सूर्य प्रतिकूलता (धैर्य अपेक्षित)",
    monthlyHighlightsLabel: "मासिक मुख्य बिन्दु",
    guruBalamLabel: "गुरु बल",
    guruBalamYes: "गुरु बल प्राप्त ✨",
    guruBalamNo: "गुरु शान्ति अपेक्षित",
    shaniGocharaLabel: "शनि गोचर",
    rahuKetuTransitLabel: "राहु-केतु सञ्चार",
    financialAnalysisLabel: "आर्थिक स्थिति विश्लेषण",
    socialAnalysisLabel: "सामाजिक प्रतिष्ठा विश्लेषण",
    rashiOverviewTitle: "सामान्य समीक्षा (General Overview)",
    rashiCareerTitle: "आजीविका एवं व्यवसाय (Career & Profession)",
    rashiFinanceTitle: "आर्थिक स्थिति एवं धन योग (Finance & Wealth)",
    rashiHealthTitle: "स्वास्थ्य एवं ऊर्जा (Health & Well-being)",
    rashiFamilyTitle: "परिवार एवं दाम्पत्य (Family & Relationships)",
    rashiRemediesTitle: "शान्ति / दैवीय परिहार (Remedies & Prayers)",
    lordLabel: "स्वामी:",
    elementLabel: "तत्व:",
    compatibilityScoreLabel: "अनुकूलता अंक",
    chandrashtamaMiniBadge: "चन्द्राष्टम",
    sunShortLabel: "सूर्य",
    incomeShort: "आय",
    expenseShort: "व्यय",
    gpsNotSupported: "आपके ब्राउज़र में GPS जियोलोकेशन समर्थित नहीं है।",
    gpsSuccess: "स्थान सफलतापूर्वक प्राप्त हुआ",
    gpsDenied: "स्थान की अनुमति नहीं मिली"
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
    khandaLabel: "கண்டம்",

    prevDayTitle: "முந்தைய நாள்",
    nextDayTitle: "அடுத்த நாள்",
    maxWord: "அதிகபட்சம்",
    bannerPurePeriod: "சுத்த காலம்",
    bannerTabooAuspicious: "சுபகாரியங்கள் நிஷித்தம்",
    bannerTabooConstruction: "கிருஹாரம்பம் நிஷித்தம்",
    bannerAnnualScheduleBtn: "வருடாந்திர அட்டவணை & சாஸ்திர விதிகள்",
    modalMoudhyamTitle: "🪔 வருடாந்திர மௌட்ய & கர்த்தரி அட்டவணை",
    modalMoudhyamSubtitle: "வானியல் நிரயண கணிதம் • தர்மசாஸ்திர முகூர்த்த தடைகள் & சிறப்புக்கள்",
    timezoneLabel: "நேர மண்டலம்",
    moudhyamTimesSubtitle: "🕒 நேரங்கள்: உங்கள் உள்ளூர் நேரம் & (IST இந்திய நிலையான நேரம்)",
    thPhase: "பிரிவு (Phase)",
    thTransit: "சூரியப் பெயர்ச்சி (Transit)",
    thTiming: "துல்லியமான நேரம் (Timing)",
    thSignificance: "முக்கியத்துவம் (Significance)",
    moudhyamSectionTitle: "மௌட்ய காலங்கள் (குரு & சுக்கிர அஸ்தமனம்)",
    moudhyamSectionSubtitle: "தேவகுரு பிரகஸ்பதி, அசுரகுரு சுக்கிரன் சூரியனின் அருகாமையால் அஸ்தமனமாகும் காலங்கள்.",
    durationLabel: "கால அளவு",
    daysLabel: "நாட்கள்",
    moudhyamStartLabel: "ஆரம்பம் (அஸ்தமனம்):",
    moudhyamEndLabel: "முடிவு (உதயம்):",
    vardhakyaLabel: "வார்த்தக்ய தோஷம்:",
    balyaLabel: "பால்ய தோஷம்:",
    prohibitionLabel: "தடை:",
    shastraDecisionsTitle: "தர்மசாஸ்திர முகூர்த்த முடிவுகள் (செய்யத்தக்கவை & தவிர்க்கவேண்டியவை)",
    moudhyamTaboosTitle: "மௌட்யத்தில் தவிர்க்கவேண்டியவை:",
    kartariTaboosTitle: "கர்த்தரியில் தவிர்க்கவேண்டியவை:",
    permittedKarmasTitle: "செய்யத்தக்க கர்மங்கள்:",
    moudhyamLoading: "மௌட்ய & கர்த்தரி அட்டவணை ஏற்றப்படுகிறது...",
    moudhyamError: "அட்டவணையை ஏற்றுவதில் பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
    adhikaMasaBadge: "அதிக மாதம்",
    nijaMasaBadge: "நிஜ மாதம்",
    kshayaMasaBadge: "க்ஷய மாதம்",
    sankrantiWord: "சங்கிராந்திகள்",
    shuklaPaksha: "சுக்ல பக்ஷம்",
    krishnaPaksha: "கிருஷ்ண பக்ஷம்",
    solarDaySuffix: "ஆம் நாள்",
    intercalaryHeroBadge: "🏛️ தர்மசாஸ்திரம் & வானியல் கோட்பாடு • காலமாதவீயம்",
    intercalaryHeroTitle: "அதிக மாதம் & க்ஷய மாத வானியல்-தர்மசாஸ்திர அறிவு",
    intercalaryHeroSubtitle: "சூரியசித்தாந்தம் மற்றும் காலமாதவீய சூத்திரங்களின்படி அதிக, க்ஷய, சம்சர்ப்ப மற்றும் அங்ஹஸ்பதி மாதங்களின் துல்லியக் கணக்கீடு.",
    systemSuryaBtn: "📜 சூரியசித்தாந்தம் (சாஸ்திரம்)",
    systemDrikBtn: "🔭 திருக்கணக்கணிதம் (Swiss Ephemeris)",
    suryaSystemBadge: "சூரியசித்தாந்த / தர்மசாஸ்திர முறை",
    drikSystemBadge: "திருக்கணித முறை (Swiss Ephemeris)",
    kalamadhavaHeader: "காலமாதவீய மூலப் பிரமாண சுலோகம்",
    kalamadhavaRuleDesc: "<strong>தர்மசாஸ்திர விதி:</strong> ஒரே சௌர வருடத்தில் இரு அசங்கிராந்தி மாதங்கள் வந்தால், முதலாவது <strong>சம்சர்ப்பம்</strong> எனப்படும். நடுவில் வரும் இரு சங்கிராந்திகள் கொண்ட மாதம் <strong>க்ஷய மாதம் (அங்ஹஸ்பதி)</strong>. ஆண்டின் முடிவில் வரும் இரண்டாவது அசங்கிராந்தி மாதம் <strong>அதிக மாதம்</strong> ஆகும். சம்சர்ப்பத்தில் நித்ய நைமித்திக கர்மங்கள் செய்யலாம்; அங்ஹஸ்பதி (க்ஷய) மாதத்தில் விவாகம் உள்ளிட்ட சுபகாரியங்கள் நிஷித்தம்.",
    adhikaCardTitle: "அதிக மாதம் (அசங்கிராந்தி)",
    adhikaCardBadge: "0 சங்கிராந்திகள்",
    adhikaCardFormula: "Ingresses = 0 (அசங்கிராந்தி)",
    adhikaCardDesc: "ஒரு அமாவாசையிலிருந்து அடுத்த அமாவாசைக்குள் சூரியன் எந்த ராசியிலும் பிரவேசிக்காவிட்டால் அது அதிக மாதம் (மலமாதம்) ஆகும். ஒவ்வொரு ~32.5 மாதங்களுக்கும் ஒருமுறை வரும்.",
    nijaCardTitle: "நிஜ மாதம் (இயல்பான மாதம்)",
    nijaCardBadge: "1 சங்கிராந்தி",
    nijaCardFormula: "Ingresses = 1 (சங்கிராந்தி)",
    nijaCardDesc: "ஒரு சாந்திர மாதத்தில் சரியாக ஒரே ஒரு சூரிய சங்கிரமணம் நிகழ்ந்தால் அது நிஜ அல்லது சுத்த மாதம். அனைத்து சுபகாரியங்களுக்கும் ஏற்ற காலம்.",
    kshayaCardTitle: "க்ஷய மாதம் (துவி-சங்கிராந்தி)",
    kshayaCardBadge: "2 சங்கிராந்திகள்",
    kshayaCardFormula: "Ingresses = 2 (துவி-சங்கிராந்தி)",
    kshayaCardDesc: "ஒரே சாந்திர மாதத்தில் சூரியனின் 2 சங்கிராந்திகள் நிகழ்ந்தால் அது க்ஷய மாதம் (அங்ஹஸ்பதி). இரு மாதங்கள் இணைந்து ஒன்றாக மாறும்.",
    driftTitle: "📐 சௌர-சாந்திர காலக்கணக்கீட்டு விதிகள் (Calendar Drift)",
    driftSolarYr: "சௌர வருடம்:",
    driftLunarYr: "சாந்திர வருடம் (12 × 29.5):",
    driftAnnual: "வருடாந்திர இடைவெளி (Annual Drift):",
    drift3Yr: "3 ஆண்டுகளில் சேரும் இடைவெளி:",
    driftLagadhaRule: "✨ <strong>வேதாங்க ஜோதிட விதி (லகத மகரிஷி):</strong> ஐந்தாண்டு யுக சுழற்சியில் 60 சௌர மாதங்கள் = 62 சாந்திர மாதங்கள். அதாவது ஒவ்வொரு 5 ஆண்டுகளுக்கும் சரியாக 2 அதிக மாதங்கள் வருகின்றன.",
    kaliyugaTitle: "🪐 கலியுக சமநிலை & க்ஷய சுழற்சி",
    perihelionRule: "💡 <strong>வானியல் பெரிஹிலியன் விதி:</strong> சூரியன் பூமிக்கு மிக அருகில் இருந்து அதிவேகமாக தனுசு, மகரம், கும்ப ராசிகளைக் கடக்கும் போது மட்டுமே ஒரே சாந்திர மாதத்தில் 2 சங்கிராந்திகள் வர வாய்ப்புள்ளது.",
    keelakaBadge: "சிறப்பு ஆய்வு",
    keelakaTitle: "ஸ்ரீ கீலக நாம வருடம் (2028 – 2029) • க்ஷய & சம்சர்ப்ப மாதங்கள்",
    keelakaDesc: "23 புகழ்பெற்ற சித்தாந்திகள் மற்றும் தர்மசாஸ்திர பண்டிதர்கள் கலந்து கொண்ட <strong>'தெலங்கானா வித்வத் சபை' மாநாட்டு</strong> தீர்மானத்தின்படி: ஸ்ரீ கீலக நாம வருடத்தில் <strong>சம்சர்ப்ப கார்த்திகை மாதம் (அதிகம்)</strong> மற்றும் <strong>மார்கழி-தை இணைந்த அங்ஹஸ்பதி மாதம் (க்ஷய மாதம்)</strong> என ஏகமனதாகத் தீர்மானிக்கப்பட்டது.",
    intercalaryTableTitle: "📅 அடுத்த 10 ஆண்டுகளுக்கான அதிக / க்ஷய மாதங்கள் அட்டவணை (2026 – 2036)",
    intercalaryTableSubtitle: "தேர்ந்தெடுக்கப்பட்ட சித்தாந்த முறைப்படியான அமாந்த சாந்திர மாதங்களின் கணக்கீடு",
    thInterYr: "வருடம்",
    thInterSamvat: "வருடப் பெயர்",
    thInterMasa: "மாதப் பெயர்",
    thInterType: "வகை / அந்தஸ்து",
    thInterSankranti: "சங்கிராந்திகள்",
    thInterSpan: "காலம் (தொடக்க – முடிவு)",
    thInterRule: "சாஸ்திர விளக்கம்",
    toDateSpan: "முதல்",
    kdHeroBadge: "📊 வருடாந்திர கந்ததாயக் கணிதம்",
    kdMainHeading: "கந்ததாய பலன்கள் & வரவு செலவுகள்",
    kdMainSubtitle: "12 ராசிகளின் வரவு-செலவு, ராஜபூஜ்யம்-அவமானம் மற்றும் 27 நட்சத்திரங்களின் 3 பருவ (முதல், இரண்டாம், மூன்றாம் கந்ததாய) துல்லியப் பலன்கள்.",
    kdCreatorBadge: "✍️ உருவாக்கியவர்: ராமசந்திர சாஸ்திரி முனிமடுகு",
    jumpToRashiKdBtn: "💰 ராசி கந்ததாயம்",
    jumpToNakshatraKdBtn: "⭐ நட்சத்திரக் கந்ததாயம்",
    jumpToShastraKdBtn: "📜 சாஸ்திரக் கணக்கீட்டு விதிகள்",
    kdQuickT1Title: "🌱 முதலாம் கந்ததாயம்",
    kdQuickT1Span: "முதல் 4 மாதங்கள்",
    kdQuickT1Months: "சித்திரை, வைகாசி, ஆனி, ஆடி",
    kdQuickT1Max: "அதிகபட்ச அளவு: 8 பகுதிகள் (மீதி 0–7)",
    kdQuickT2Title: "🌧️ இரண்டாம் கந்ததாயம்",
    kdQuickT2Span: "இரண்டாம் 4 மாதங்கள்",
    kdQuickT2Months: "ஆவணி, புரட்டாசி, ஐப்பசி, கார்த்திகை",
    kdQuickT2Max: "அதிகபட்ச அளவு: 3 பகுதிகள் (மீதி 0–2)",
    kdQuickT3Title: "❄️ மூன்றாம் கந்ததாயம்",
    kdQuickT3Span: "மூன்றாம் 4 மாதங்கள்",
    kdQuickT3Months: "மார்கழி, தை, மாசி, பங்குனி",
    kdQuickT3Max: "அதிகபட்ச அளவு: 5 பகுதிகள் (மீதி 0–4)",
    rashiKdSectionTitle: "💰 பன்னிரு ராசி கந்ததாயம் (வரவு, செலவு, ராஜபூஜ்யம், அவமானம்)",
    rashiKdSectionSubtitle: "பன்னிரு ராசிகளின் முழுமையான நிதி மற்றும் சமூக கௌரவ நிலை",
    rashiKdViewCardsBtn: "அட்டைகள்",
    rashiKdViewTableBtn: "அட்டவணை",
    thKdRashi: "ராசி",
    thKdLord: "அதிபதி",
    thKdAdayam: "வரவு",
    thKdVyayam: "செலவு",
    thKdRajapujyam: "ராஜபூஜ்யம்",
    thKdAvamanam: "அவமானம்",
    thKdFinStatus: "நிதி நிலை",
    thKdSocStatus: "சமூக கௌரவம்",
    thKdVerdict: "முழுமையான முடிவு",
    nakshatraSectionTitle: "⭐ 27 நட்சத்திரக் கந்ததாய பலன்கள் (3 பருவப் பகுப்பு)",
    nakshatraSectionSubtitle: "ஆண்டின் 3 பருவங்களின்படி உங்கள் ஜென்ம நட்சத்திர பலன்களை அறிந்துகொள்ளுங்கள்",
    nakshatraSelectLabel: "நட்சத்திரம்:",
    nakshatraMasterTableTitle: "📋 27 நட்சத்திரங்களின் முழுமையான கந்ததாய அட்டவணை (Master Table)",
    nakshatraTableSearchInput: "நட்சத்திரப் பெயரால் தேடுங்கள்...",
    thNId: "வ.எண்",
    thNName: "நட்சத்திரம்",
    thNRashis: "ராசிகள்",
    thNT1: "முதலாம் (1–4 மாதங்கள்)",
    thNT2: "இரண்டாம் (5–8 மாதங்கள்)",
    thNT3: "மூன்றாம் (9–12 மாதங்கள்)",
    thNOverall: "வருடாந்திர நிலை",
    shastraKdTitle: "📜 கந்ததாயக் கணித அறிவும் சாஸ்திர பிரமாணங்களும்",
    shastraKdT1Title: "📅 வருடப் பகுப்பு (3 கந்ததாயங்கள்)",
    shastraKdT2Title: "⚖️ பன்னிரு ராசி கந்ததாயக் கணிதம்",
    nakshatraWord: "நட்சத்திரம்",
    spreadRashisPadasLabel: "வியாபித்துள்ள ராசிகள் / பாதங்கள்:",
    annualCompositeStatusLabel: "வருடாந்திர ஒட்டுமொத்த நிலை",
    trimester1Title: "முதலாம் கந்ததாயம்",
    trimester1Months: "சித்திரை – ஆடி (மாதங்கள் 1–4)",
    trimester1MaxLimit: "அதிகபட்ச அளவு: 8 பகுதிகள்",
    trimester2Title: "இரண்டாம் கந்ததாயம்",
    trimester2Months: "ஆவணி – கார்த்திகை (மாதங்கள் 5–8)",
    trimester2MaxLimit: "அதிகபட்ச அளவு: 3 பகுதிகள்",
    trimester3Title: "மூன்றாம் கந்ததாயம்",
    trimester3Months: "மார்கழி – பங்குனி (மாதங்கள் 9–12)",
    trimester3MaxLimit: "அதிகபட்ச அளவு: 5 பகுதிகள்",
    annualSummaryAdviceLabel: "வருடாந்திர பலன் சுருக்கம் & வழிகாட்டல்:",
    noNakshatraFound: "நட்சத்திரப் பலன்கள் எதுவும் காணப்படவில்லை",
    rashiHeading: "ராசி பலன் (கோசார பலன்கள்)",
    rashiSubtitle: "வானியல் கிரகப் பெயர்ச்சி, சந்திரபலம், தாராபலம் மற்றும் கந்ததாய விதிகள் அடிப்படையிலான துல்லியப் பலன்கள்.",
    rashiGocharaBadge: "♈ பன்னிரு ராசி கோசாரம்",
    moonTransitLabel: "சந்திர சஞ்சாரம்",
    solarMonthLabel: "சூரிய மாதம்",
    kandadayamTableLabel: "பஞ்சாங்கக் கந்ததாய அட்டவணை",
    kdAdayam: "வரவு",
    kdVyayam: "செலவு",
    kdRajapujyam: "ராஜபூஜ்யம்",
    kdAvamanam: "அவமானம்",
    statusAuspicious: "உத்தமம் (Auspicious)",
    statusFavorable: "அனுகூலம் (Favorable)",
    statusModerate: "மத்திமம் (Moderate)",
    statusCaution: "எச்சரிக்கை (Caution)",
    footerOrgTitle: "வேத சம்ஹிதை • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "சித்தாந்த & வானியல் கணக்கீட்டு வடிவமைப்பாளர் (System Architect & Creator)",
    footerCreatorName: "ராமசந்திர சாஸ்திரி முனிமடுகு",
    footerCreatorDesc: "இந்த பஞ்சாங்கக் கணிதங்கள், வைதிக வானியல் விதிகள், தர்மசாஸ்திர முடிவுகள் மற்றும் தொழில்நுட்ப அமைப்புகள் அனைத்தும் <strong class=\"text-amber-200 font-bold\">ஸ்ரீ ராமசந்திர சாஸ்திரி முனிமடுகு</strong> அவர்களின் ஆராய்ச்சி மற்றும் வடிவமைப்பினால் உருவாக்கப்பட்டவை. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "அதிகாரப்பூர்வ வலைத்தளம்:",
    footerPoweredBy: "Swiss Ephemeris வானியல் கணக்கீடு, ஜோதிட எஞ்சின் மற்றும் அக்ஷரமுக பன்மொழி எழுத்துப்பெயர்ப்பு சார்ந்தது.",
    chandrashtamaAlertTitle: "சந்திராஷ்டம எச்சரிக்கை (Chandrashtama Active)",
    chandrashtamaAlertDesc: "இன்று சந்திரன் உங்கள் ஜென்ம ராசியிலிருந்து 8வது வீட்டில் சஞ்சரிக்கிறார். விவாதங்கள், நிதி பரிவர்த்தனைகள் மற்றும் புதிய ஒப்பந்தங்களைத் தொடங்குவதில் மிகுந்த எச்சரிக்கை தேவை. சிவ வழிபாடு நலம் தரும்.",
    moonHouseLabel: "சந்திர நிலை",
    houseSuffix: "ஆம் இடம்",
    tarabalamLabel: "தாராபலம்",
    taraGood: "சுப தாரை ✔️",
    taraCaution: "எச்சரிக்கை ⚠️",
    luckyNumberLabel: "அதிர்ஷ்ட எண்",
    luckyColorLabel: "அதிர்ஷ்ட நிறம்",
    luckyDirectionLabel: "அனுகூல திசை",
    sunTransitLabel: "சூரியப் பெயர்ச்சி",
    placeSuffix: "ஆம் இடம்",
    sunFavorable: "அனுகூல சூரிய பலம் (உபசயம்) ☀️",
    sunUnfavorable: "சூரியப் பின்னடைவு (பொறுமை தேவை)",
    monthlyHighlightsLabel: "மாத முக்கிய அம்சங்கள்",
    guruBalamLabel: "குரு பலம்",
    guruBalamYes: "குரு பலம் உண்டு ✨",
    guruBalamNo: "குரு சாந்தி தேவை",
    shaniGocharaLabel: "சனி கோசாரம்",
    rahuKetuTransitLabel: "ராகு-கேது சஞ்சாரம்",
    financialAnalysisLabel: "நிதி நிலை பகுப்பாய்வு",
    socialAnalysisLabel: "சமூக அந்தஸ்து பகுப்பாய்வு",
    rashiOverviewTitle: "பொதுவான பார்வை (General Overview)",
    rashiCareerTitle: "வேலை & தொழில் (Career & Profession)",
    rashiFinanceTitle: "நிதி நிலை & தன யோகம் (Finance & Wealth)",
    rashiHealthTitle: "உடல்நலம் & ஆற்றல் (Health & Well-being)",
    rashiFamilyTitle: "குடும்பம் & தாம்பத்யம் (Family & Relationships)",
    rashiRemediesTitle: "சாந்தி / தெய்வீகப் பரிகாரம் (Remedies & Prayers)",
    lordLabel: "அதிபதி:",
    elementLabel: "தத்துவம்:",
    compatibilityScoreLabel: "பொருத்த மதிப்பெண்",
    chandrashtamaMiniBadge: "சந்திராஷ்டமம்",
    sunShortLabel: "சூரியன்",
    incomeShort: "வர",
    expenseShort: "செ",
    gpsNotSupported: "உங்கள் உலாவியில் GPS இருப்பிட வசதி இல்லை.",
    gpsSuccess: "இருப்பிடம் வெற்றிகரமாகக் கண்டறியப்பட்டது",
    gpsDenied: "இருப்பிட அனுமதி கிடைக்கவில்லை"
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
    khandaLabel: "ಖಂಡ",

    prevDayTitle: "ಹಿಂದಿನ ದಿನ",
    nextDayTitle: "ಮುಂದಿನ ದಿನ",
    maxWord: "ಗರಿಷ್ಠ",
    bannerPurePeriod: "ಶುದ್ಧ ಕಾಲ",
    bannerTabooAuspicious: "ಶುಭಕಾರ್ಯಗಳು ನಿಷಿದ್ಧ",
    bannerTabooConstruction: "ಗೃಹಾರಂಭ ನಿಷಿದ್ಧ",
    bannerAnnualScheduleBtn: "ವಾರ್ಷಿಕ ಪಟ್ಟಿ & ಶಾಸ್ತ್ರ ನಿಯಮಗಳು",
    modalMoudhyamTitle: "🪔 ವಾರ್ಷಿಕ ಮೌಢ್ಯ & ಕರ್ತರಿ ನಿರ್ಣಯ ಪಟ್ಟಿ",
    modalMoudhyamSubtitle: "ಖಗೋಳ ನಿರಯಣ ಗಣಿತ • ಧರ್ಮಶಾಸ್ತ್ರ ಮುಹೂರ್ತ ನಿಷೇಧಗಳು & ಪ್ರಾಶಸ್ತ್ಯಗಳು",
    timezoneLabel: "ಸಮಯ ವಲಯ",
    moudhyamTimesSubtitle: "🕒 ಸಮಯಗಳು: ನಿಮ್ಮ ಸ್ಥಳೀಯ ಸಮಯ & (IST ಭಾರತೀಯ ಪ್ರಮಾಣಿತ ಸಮಯ)",
    thPhase: "ವಿಭಾಗ (Phase)",
    thTransit: "ಸೂರ್ಯ ಸಂಚಾರ (Transit)",
    thTiming: "ನಿಖರವಾದ ಸಮಯ (Timing)",
    thSignificance: "ಪ್ರಾಮುಖ್ಯತೆ (Significance)",
    moudhyamSectionTitle: "ಮೌಢ್ಯಗಳು (ಗುರು & ಶುಕ್ರ ಅಸ್ತಂಗತಗಳು)",
    moudhyamSectionSubtitle: "ದೇವಗುರು ಬೃಹಸ್ಪತಿ ಮತ್ತು ಶುಕ್ರರು ಸೂರ್ಯನ ಸಾಮೀಪ್ಯದಿಂದ ಅಸ್ತಂಗತರಾಗುವ ಅವಧಿಗಳು.",
    durationLabel: "ಅವಧಿ",
    daysLabel: "ದಿನಗಳು",
    moudhyamStartLabel: "ಆರಂಭ (ಅಸ್ತಂಗತ):",
    moudhyamEndLabel: "ಸಮಾಪ್ತಿ (ಉದಯ):",
    vardhakyaLabel: "ವಾರ್ಧಕ್ಯ ದೋಷ:",
    balyaLabel: "ಬಾಲ್ಯ ದೋಷ:",
    prohibitionLabel: "ನಿಷೇಧ:",
    shastraDecisionsTitle: "ಧರ್ಮಶಾಸ್ತ್ರ ಮುಹೂರ್ತ ನಿರ್ಣಯಗಳು (ಯಾವುವು ಮಾಡಬಹುದು? ಯಾವುವು ನಿಷಿದ್ಧ?)",
    moudhyamTaboosTitle: "ಮೌಢ್ಯದಲ್ಲಿ ನಿಷಿದ್ಧಗಳು:",
    kartariTaboosTitle: "ಕರ್ತರಿಯಲ್ಲಿ ನಿಷಿದ್ಧಗಳು:",
    permittedKarmasTitle: "ಆಚರಿಸಬಹುದಾದ ಕಾರ್ಯಗಳು:",
    moudhyamLoading: "ಮೌಢ್ಯ & ಕರ್ತರಿ ನಿರ್ಣಯ ಪಟ್ಟಿ ಲೋಡ್ ಆಗುತ್ತಿದೆ...",
    moudhyamError: "ಪಟ್ಟಿ ಲೋಡ್ ಮಾಡುವಲ್ಲಿ ದೋಷ ಉಂಟಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    adhikaMasaBadge: "ಅಧಿಕ ಮಾಸ",
    nijaMasaBadge: "ಸಾಮಾನ್ಯ ಮಾಸ",
    kshayaMasaBadge: "ಕ್ಷಯ ಮಾಸ",
    sankrantiWord: "ಸಂಕ್ರಾಂತಿಗಳು",
    shuklaPaksha: "ಶುಕ್ಲ ಪಕ್ಷ",
    krishnaPaksha: "ಕೃಷ್ಣ ಪಕ್ಷ",
    solarDaySuffix: "ನೇ ದಿನ",
    intercalaryHeroBadge: "🏛️ ಧರ್ಮಶಾಸ್ತ್ರ & ಖಗೋಳ ಸಿದ್ಧಾಂತ • ಕಾಲಮಾಧವೀಯಂ",
    intercalaryHeroTitle: "ಅಧಿಕ ಮಾಸ & ಕ್ಷಯ ಮಾಸ ಖಗೋಳ-ಧರ್ಮಶಾಸ್ತ್ರ ವಿಜ್ಞಾನ",
    intercalaryHeroSubtitle: "ಸೂರ್ಯಸಿದ್ಧಾಂತ ಮತ್ತು ಕಾಲಮಾಧವೀಯ ಸೂತ್ರಗಳ ಪ್ರಕಾರ ಅಧಿಕ, ಕ್ಷಯ, ಸಂಸರ್ಪ ಮತ್ತು ಅಂಹಸ್ಪತಿ ಮಾಸಗಳ ಸಮಗ್ರ ಗಣನೆ.",
    systemSuryaBtn: "📜 ಸೂರ್ಯಸಿದ್ಧಾಂತ (ಶಾಸ್ತ್ರ)",
    systemDrikBtn: "🔭 ದೃಕ್ಸಿದ್ಧಾಂತ (Swiss Ephemeris)",
    suryaSystemBadge: "ಸೂರ್ಯಸಿದ್ಧಾಂತ / ಧರ್ಮಶಾಸ್ತ್ರ ಪದ್ಧತಿ",
    drikSystemBadge: "ದೃಕ್ಸಿದ್ಧಾಂತ ಪದ್ಧತಿ (Swiss Ephemeris)",
    kalamadhavaHeader: "ಕಾಲಮಾಧವೀಯ ಪರಮ ಪ್ರಾಮಾಣಿಕ ಶ್ಲೋಕ",
    kalamadhavaRuleDesc: "<strong>ಧರ್ಮಶಾಸ್ತ್ರ ನಿಯಮ:</strong> ಒಂದೇ ಸೌರ ವರ್ಷದಲ್ಲಿ ಎರಡು ಅಸಂಕ್ರಾಂತ ಮಾಸಗಳು ಬಂದರೆ, ಮೊದಲನೆಯದನ್ನು <strong>ಸಂಸರ್ಪ</strong> ಎನ್ನುತ್ತಾರೆ. ಮಧ್ಯದಲ್ಲಿ ಬರುವ ದ್ವಿಸಂಕ್ರಾಂತ ಮಾಸವೇ <strong>ಕ್ಷಯ ಮಾಸ (ಅಂಹಸ್ಪತಿ)</strong>. ವರ್ಷಾಂತ್ಯದಲ್ಲಿ ಬರುವ ಎರಡನೇ ಅಸಂಕ್ರಾಂತ ಮಾಸ <strong>ಅಧಿಕ ಮಾಸ</strong>ವಾಗುತ್ತದೆ. ಸಂಸರ್ಪದಲ್ಲಿ ನಿತ್ಯ ನೈಮಿತ್ತಿಕ ಕರ್ಮಗಳನ್ನು ಮಾಡಬಹುದು; ಅಂಹಸ್ಪತಿ (ಕ್ಷಯ) ಮಾಸದಲ್ಲಿ ವಿವಾಹಾದಿ ಶುಭಕಾರ್ಯಗಳು ನಿಷಿದ್ಧ.",
    adhikaCardTitle: "ಅಧಿಕ ಮಾಸ (ಅಸಂಕ್ರಾಂತ)",
    adhikaCardBadge: "0 ಸಂಕ್ರಾಂತಿಗಳು",
    adhikaCardFormula: "Ingresses = 0 (ಅಸಂಕ್ರಾಂತ)",
    adhikaCardDesc: "ಒಂದು ಅಮಾವಾಸ್ಯೆಯಿಂದ ಮುಂದಿನ ಅಮಾವಾಸ್ಯೆಯವರೆಗೆ ಸೂರ್ಯನು ಯಾವುದೇ ರಾಶಿಗೆ ಪ್ರವೇಶಿಸದಿದ್ದರೆ ಅದು ಅಧಿಕ ಮಾಸ (ಮಲಮಾಸ). ಪ್ರತಿ ~32.5 ತಿಂಗಳಿಗೊಮ್ಮೆ ಬರುತ್ತದೆ.",
    nijaCardTitle: "ಸಾಮಾನ್ಯ ಮಾಸ (ನಿಜ ಮಾಸ)",
    nijaCardBadge: "1 ಸಂಕ್ರಾಂತಿ",
    nijaCardFormula: "Ingresses = 1 (ಸಂಕ್ರಾಂತ)",
    nijaCardDesc: "ಒಂದು ಚಾಂದ್ರಮಾಸದಲ್ಲಿ ಕರಾರುವಕ್ಕಾಗಿ ಒಂದೇ ಸೂರ್ಯ ಸಂಕ್ರಮಣ ಸಂಭವಿಸಿದರೆ ಅದು ನಿಜ ಅಥವಾ ಶುದ್ಧ ಮಾಸ. ಎಲ್ಲಾ ಶುಭಕಾರ್ಯಗಳಿಗೆ ಪ್ರಶಸ್ತವಾದ ಕಾಲ.",
    kshayaCardTitle: "ಕ್ಷಯ ಮಾಸ (ದ್ವಿಸಂಕ್ರಾಂತ)",
    kshayaCardBadge: "2 ಸಂಕ್ರಾಂತಿಗಳು",
    kshayaCardFormula: "Ingresses = 2 (ದ್ವಿಸಂಕ್ರಾಂತ)",
    kshayaCardDesc: "ಒಂದೇ ಚಾಂದ್ರಮಾಸದಲ್ಲಿ ಸೂರ್ಯನ 2 ಸಂಕ್ರಾಂತಿಗಳು ಸಂಭವಿಸಿದರೆ ಅದು ಕ್ಷಯ ಮಾಸ (ಅಂಹಸ್ಪತಿ). ಎರಡು ತಿಂಗಳುಗಳು ಒಂದಾಗಿ ಬೆರೆಯುತ್ತವೆ.",
    driftTitle: "📐 ಸೌರ-ಚಾಂದ್ರ ಕಾಲಗಣನೆ ಸೂತ್ರಗಳು (Calendar Drift)",
    driftSolarYr: "ಸೌರ ವರ್ಷ:",
    driftLunarYr: "ಚಾಂದ್ರ ವರ್ಷ (12 × 29.5):",
    driftAnnual: "ವಾರ್ಷಿಕ ವ್ಯತ್ಯಾಸ (Annual Drift):",
    drift3Yr: "3 ವರ್ಷಗಳಲ್ಲಿ ಸೇರುವ ವ್ಯತ್ಯಾಸ:",
    driftLagadhaRule: "✨ <strong>ವೇದಾಂಗ ಜ್ಯೋತಿಷ ನಿಯಮ (ಲಗಧ ಮಹರ್ಷಿ):</strong> ಪಂಚಸಂವತ್ಸರಾತ್ಮಕ ಯುಗದಲ್ಲಿ 60 ಸೌರ ಮಾಸಗಳು = 62 ಚಾಂದ್ರ ಮಾಸಗಳು. ಅಂದರೆ ಪ್ರತಿ 5 ವರ್ಷಗಳಿಗೆ ಸರಿಯಾಗಿ 2 ಅಧಿಕ ಮಾಸಗಳು ಬರುತ್ತವೆ.",
    kaliyugaTitle: "🪐 ಕಲಿಯುಗ ಮಹಾಯುಗ ಸಮತೋಲನ & ಕ್ಷಯ ಚಕ್ರ",
    perihelionRule: "💡 <strong>ಖಗೋಳ ಪೆರಿಹಿಲಿಯನ್ ನಿಯಮ:</strong> ಸೂರ್ಯನು ಭೂಮಿಗೆ ಹತ್ತಿರವಿದ್ದು ಅತಿವೇಗವಾಗಿ ಧನು, ಮಕರ, ಕುಂಭ ರಾಶಿಗಳನ್ನು ದಾಟಿದಾಗ ಮಾತ್ರ ಚಾಂದ್ರಮಾಸದಲ್ಲಿ 2 ಸಂಕ್ರಾಂತಿಗಳು ಬರುವ ಸಾಧ್ಯತೆ ಇರುತ್ತದೆ.",
    keelakaBadge: "ವಿಶೇಷ ಪರಿಶೀಲನೆ",
    keelakaTitle: "ಶ್ರೀ ಕೀಲಕ ನಾಮ ಸಂವತ್ಸರ (2028 – 2029) • ಕ್ಷಯ & ಸಂಸರ್ಪ ಮಾಸಗಳು",
    keelakaDesc: "23 ಪ್ರಸಿದ್ಧ ಸಿದ್ಧಾಂತಿಗಳು ಮತ್ತು ಧರ್ಮಶಾಸ್ತ್ರ ವಿದ್ವಾಂಸರನ್ನೊಳಗೊಂಡ <strong>'ತೆಲಂಗಾಣ ವಿದ್ವತ್ಸಭೆ' ಗೋಷ್ಠಿ</strong> ನಿರ್ಣಯದ ಪ್ರಕಾರ: ಶ್ರೀ ಕೀಲಕ ನಾಮ ಸಂವತ್ಸರದಲ್ಲಿ <strong>ಸಂಸರ್ಪ ಕಾರ್ತಿಕ ಮಾಸ (ಅಧಿಕ)</strong> ಮತ್ತು <strong>ಮಾರ್ಗಶಿರ-ಪುಷ್ಯ ಯುಗಳ ಅಂಹಸ್ಪತಿ ಮಾಸ (ಕ್ಷಯ ಮಾಸ)</strong> ಎಂದು ಸರ್ವಾನುಮತದಿಂದ ನಿರ್ಣಯಿಸಲಾಗಿದೆ.",
    intercalaryTableTitle: "📅 ಮುಂದಿನ 10 ವರ್ಷಗಳ ಅಧಿಕ / ಕ್ಷಯ ಮಾಸಗಳ ಪಟ್ಟಿ (2026 – 2036)",
    intercalaryTableSubtitle: "ಆಯ್ಕೆಮಾಡಿದ ಸಿದ್ಧಾಂತ ಪದ್ಧತಿಯ ಪ್ರಕಾರ ಅಮಾಂತ ಚಾಂದ್ರಮಾಸಗಳ ಫಲಿತಾಂಶಗಳು",
    thInterYr: "ವರ್ಷ",
    thInterSamvat: "ಸಂವತ್ಸರದ ಹೆಸರು",
    thInterMasa: "ಮಾಸದ ಹೆಸರು",
    thInterType: "ವಿಧ / ಸ್ಥಾನಮಾನ",
    thInterSankranti: "ಸಂಕ್ರಾಂತಿಗಳು",
    thInterSpan: "ಅವಧಿ (ಆರಂಭ – ಮುಕ್ತಾಯ)",
    thInterRule: "ಶಾಸ್ತ್ರ ವಿವರಣೆ",
    toDateSpan: "ಇಂದ",
    kdHeroBadge: "📊 ವಾರ್ಷಿಕ ಕಂದದಾಯ ಗಣಿತ",
    kdMainHeading: "ಕಂದದಾಯ ಫಲಗಳು & ಆದಾಯ ವ್ಯಯಗಳು",
    kdMainSubtitle: "ದ್ವಾದಶ ರಾಶಿಗಳ ಆದಾಯ-ವ್ಯಯ, ರಾಜಪೂಜ್ಯ-ಅವಮಾನ ಮತ್ತು 27 ನಕ್ಷತ್ರಗಳ ತ್ರೈಮಾಸಿಕ (ಪ್ರಥಮ, ದ್ವಿತೀಯ, ತೃತೀಯ ಕಂದಾಯಗಳ) ಪ್ರಮಾಣಿತ ಫಲಗಳು.",
    kdCreatorBadge: "✍️ ಕರ್ತೃ: ರಾಮಚಂದ್ರ ಶಾಸ್ತ್ರಿ ಮುನಿಮಡುಗು",
    jumpToRashiKdBtn: "💰 ರಾಶಿ ಕಂದದಾಯ",
    jumpToNakshatraKdBtn: "⭐ ನಕ್ಷತ್ರ ಕಂದಾಯಗಳು",
    jumpToShastraKdBtn: "📜 ಶಾಸ್ತ್ರ ಗಣನೆ ಸೂತ್ರಗಳು",
    kdQuickT1Title: "🌱 ಪ್ರಥಮ ಕಂದಾಯ",
    kdQuickT1Span: "ಮೊದಲ 4 ತಿಂಗಳುಗಳು",
    kdQuickT1Months: "ಚೈತ್ರ, ವೈಶಾಖ, ಜ್ಯೇಷ್ಠ, ಆಷಾಢ",
    kdQuickT1Max: "ಗರಿಷ್ಠ ಮಿತಿ: 8 ಭಾಗಗಳು (ಶೇಷ 0–7)",
    kdQuickT2Title: "🌧️ ದ್ವಿತೀಯ ಕಂದಾಯ",
    kdQuickT2Span: "ಎರಡನೇ 4 ತಿಂಗಳುಗಳು",
    kdQuickT2Months: "ಶ್ರಾವಣ, ಭಾದ್ರಪದ, ಆಶ್ವಯುಜ, ಕಾರ್ತಿಕ",
    kdQuickT2Max: "ಗರಿಷ್ಠ ಮಿತಿ: 3 ಭಾಗಗಳು (ಶೇಷ 0–2)",
    kdQuickT3Title: "❄️ ತೃತೀಯ ಕಂದಾಯ",
    kdQuickT3Span: "ಮೂರನೇ 4 ತಿಂಗಳುಗಳು",
    kdQuickT3Months: "ಮಾರ್ಗಶಿರ, ಪುಷ್ಯ, ಮಾಘ, ಫಾಲ್ಗುಣ",
    kdQuickT3Max: "ಗರಿಷ್ಠ ಮಿತಿ: 5 ಭಾಗಗಳು (ಶೇಷ 0–4)",
    rashiKdSectionTitle: "💰 ದ್ವಾದಶ ರಾಶಿ ಕಂದದಾಯ (ಆದಾಯ, ವ್ಯಯ, ರಾಜಪೂಜ್ಯ, ಅವಮಾನ)",
    rashiKdSectionSubtitle: "ದ್ವಾದಶ ರಾಶಿಗಳ ಸಂಪೂರ್ಣ ಆರ್ಥಿಕ ಮತ್ತು ಸಾಮಾಜಿಕ ಗೌರವ ಸ್ಥಿತಿಗತಿಗಳು",
    rashiKdViewCardsBtn: "ಕಾರ್ಡ್‌ಗಳು",
    rashiKdViewTableBtn: "ಕೋಷ್ಟಕ",
    thKdRashi: "ರಾಶಿ",
    thKdLord: "ಅಧಿಪತಿ",
    thKdAdayam: "ಆದಾಯ",
    thKdVyayam: "ವ್ಯಯ",
    thKdRajapujyam: "ರಾಜಪೂಜ್ಯ",
    thKdAvamanam: "ಅವಮಾನ",
    thKdFinStatus: "ಆರ್ಥಿಕ ಸ್ಥಿತಿ",
    thKdSocStatus: "ಸಾಮಾಜಿಕ ಗೌರವ",
    thKdVerdict: "ಸಮಗ್ರ ತೀರ್ಮಾನ",
    nakshatraSectionTitle: "⭐ 27 ನಕ್ಷತ್ರ ಕಂದಾಯ ಫಲಗಳು (ತ್ರೈಮಾಸಿಕ ವಿಭಜನೆ)",
    nakshatraSectionSubtitle: "ವರ್ಷದ 3 ಕಂದಾಯಗಳ ಪ್ರಕಾರ ನಿಮ್ಮ ಜನ್ಮ ನಕ್ಷತ್ರದ ಫಲಗಳನ್ನು ತಿಳಿದುಕೊಳ್ಳಿ",
    nakshatraSelectLabel: "ನಕ್ಷತ್ರ:",
    nakshatraMasterTableTitle: "📋 ಸಮಗ್ರ 27 ನಕ್ಷತ್ರಗಳ ಕಂದಾಯ ಕೋಷ್ಟಕ (Master Table)",
    nakshatraTableSearchInput: "ನಕ್ಷತ್ರದ ಹೆಸರಿನಿಂದ ಹುಡುಕಿ...",
    thNId: "ಕ್ರ.ಸಂ.",
    thNName: "ನಕ್ಷತ್ರ",
    thNRashis: "ರಾಶಿಗಳು",
    thNT1: "ಪ್ರಥಮ (1–4 ತಿಂಗಳು)",
    thNT2: "ದ್ವಿತೀಯ (5–8 ತಿಂಗಳು)",
    thNT3: "ತೃತೀಯ (9–12 ತಿಂಗಳು)",
    thNOverall: "ವಾರ್ಷಿಕ ಸ್ಥಿತಿ",
    shastraKdTitle: "📜 ಕಂದದಾಯ ಗಣಿತ ವಿಜ್ಞಾನ ಮತ್ತು ಶಾಸ್ತ್ರ ಪ್ರಮಾಣಗಳು",
    shastraKdT1Title: "📅 ವರ್ಷದ ಕಾಲ ವಿಭಜನೆ (3 ಕಂದಾಯಗಳು)",
    shastraKdT2Title: "⚖️ ದ್ವಾದಶ ರಾಶಿ ಕಂದದಾಯ ಗಣಿತ",
    nakshatraWord: "ನಕ್ಷತ್ರ",
    spreadRashisPadasLabel: "ವ್ಯಾಪಿಸಿದ ರಾಶಿಗಳು / ಪಾದಗಳು:",
    annualCompositeStatusLabel: "ವಾರ್ಷಿಕ ಸಮಗ್ರ ಸ್ಥಿತಿ",
    trimester1Title: "ಪ್ರಥಮ ಕಂದಾಯ",
    trimester1Months: "ಚೈತ್ರ – ಆಷಾಢ (ತಿಂಗಳು 1–4)",
    trimester1MaxLimit: "ಗರಿಷ್ಠ ಮಿತಿ: 8 ಭಾಗಗಳು",
    trimester2Title: "ದ್ವಿತೀಯ ಕಂದಾಯ",
    trimester2Months: "ಶ್ರಾವಣ – ಕಾರ್ತಿಕ (ತಿಂಗಳು 5–8)",
    trimester2MaxLimit: "ಗರಿಷ್ಠ ಮಿತಿ: 3 ಭಾಗಗಳು",
    trimester3Title: "ತೃತೀಯ ಕಂದಾಯ",
    trimester3Months: "ಮಾರ್ಗಶಿರ – ಫಾಲ್ಗುಣ (ತಿಂಗಳು 9–12)",
    trimester3MaxLimit: "ಗರಿಷ್ಠ ಮಿತಿ: 5 ಭಾಗಗಳು",
    annualSummaryAdviceLabel: "ವಾರ್ಷಿಕ ಫಲ ಸಾರಾಂಶ & ಮಾರ್ಗದರ್ಶನ:",
    noNakshatraFound: "ಯಾವುದೇ ನಕ್ಷತ್ರ ಫಲಗಳು ಕಂಡುಬಂದಿಲ್ಲ",
    rashiHeading: "ರಾಶಿ ಫಲ (ಗೋಚಾರ ಫಲಗಳು)",
    rashiSubtitle: "ಖಗೋಳ ಗೋಚಾರ ಸಂಚಾರ, ಚಂದ್ರಬಲ, ತಾರಾಬಲ ಮತ್ತು ಪಂಚಾಂಗ ಕಂದಾಯ ಸೂತ್ರಗಳ ಆಧಾರಿತ ಪ್ರಮಾಣಿತ ಫಲಗಳು.",
    rashiGocharaBadge: "♈ ದ್ವಾದಶ ರಾಶಿ ಗೋಚಾರ",
    moonTransitLabel: "ಚಂದ್ರ ಸಂಚಾರ",
    solarMonthLabel: "ಸೌರ ಮಾಸ",
    kandadayamTableLabel: "ಪಂಚಾಂಗ ಕಂದಾಯ ಕೋಷ್ಟಕ",
    kdAdayam: "ಆದಾಯ",
    kdVyayam: "ವ್ಯಯ",
    kdRajapujyam: "ರಾಜಪೂಜ್ಯ",
    kdAvamanam: "ಅವಮಾನ",
    statusAuspicious: "ಉತ್ತಮ (Auspicious)",
    statusFavorable: "ಅನುಕೂಲ (Favorable)",
    statusModerate: "ಮಧ್ಯಮ (Moderate)",
    statusCaution: "ಎಚ್ಚರಿಕೆ (Caution)",
    footerOrgTitle: "ವೇದ ಸಂಹಿತಾ • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "ಸಿದ್ಧಾಂತ & ಖಗೋಳ ಕಂಪ್ಯೂಟೇಶನ್ ಕರ್ತೃ (System Architect & Creator)",
    footerCreatorName: "ರಾಮಚಂದ್ರ ಶಾಸ್ತ್ರಿ ಮುನಿಮಡುಗು",
    footerCreatorDesc: "ಈ ಪಂಚಾಂಗ ಗಣನೆಗಳು, ವೈದಿಕ ಖಗೋಳ ಸೂತ್ರಗಳು, ಧರ್ಮಶಾಸ್ತ್ರ ನಿರ್ಣಯಗಳು ಮತ್ತು ತಾಂತ್ರಿಕ ಕ್ರೋಡೀಕರಣವು ಸಮಗ್ರವಾಗಿ <strong class=\"text-amber-200 font-bold\">ಶ್ರೀ ರಾಮಚಂದ್ರ ಶಾಸ್ತ್ರಿ ಮುನಿಮಡುಗು</strong> ಅವರ ಸಂಶೋಧನೆ ಮತ್ತು ವಿನ್ಯಾಸದಿಂದ ರಚಿತವಾಗಿದೆ. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್:",
    footerPoweredBy: "Swiss Ephemeris ಖಗೋಳ ಗಣನೆಗಳು, ಜ್ಯೋತಿಷ ಎಂಜಿನ್ ಮತ್ತು ಅಕ್ಷರಮುಖ ಬಹುಭಾಷಾ ಲಿಪ್ಯಂತರ ಆಧಾರಿತ.",
    chandrashtamaAlertTitle: "ಚಂದ್ರಾಷ್ಟಮ ಎಚ್ಚರಿಕೆ (Chandrashtama Active)",
    chandrashtamaAlertDesc: "ಇಂದು ಚಂದ್ರನು ನಿಮ್ಮ ಜನ್ಮ ರಾಶಿಯಿಂದ 8ನೇ ಮನೆಯಲ್ಲಿ ಸಂಚರಿಸುತ್ತಿದ್ದಾನೆ. ವಾದ-ವಿವಾದಗಳು, ಹಣಕಾಸು ವ್ಯವಹಾರಗಳು ಮತ್ತು ಹೊಸ ಒಪ್ಪಂದಗಳನ್ನು ಪ್ರಾರಂಭಿಸುವಲ್ಲಿ ಹೆಚ್ಚಿನ ಎಚ್ಚರಿಕೆ ಅಗತ್ಯ. ಶಿವಾರಾಧನೆ ಶುಭಪ್ರದ.",
    moonHouseLabel: "ಚಂದ್ರ ಸ್ಥಾನ",
    houseSuffix: "ನೇ ಮನೆ",
    tarabalamLabel: "ತಾರಾಬಲ",
    taraGood: "ಶುಭ ತಾರೆ ✔️",
    taraCaution: "ಎಚ್ಚರಿಕೆ ⚠️",
    luckyNumberLabel: "ಅದೃಷ್ಟ ಸಂಖ್ಯೆ",
    luckyColorLabel: "ಅದೃಷ್ಟ ಬಣ್ಣ",
    luckyDirectionLabel: "ಅನುಕೂಲ ದಿಕ್ಕು",
    sunTransitLabel: "ಸೂರ್ಯ ಸಂಕ್ರಮಣ",
    placeSuffix: "ನೇ ಸ್ಥಾನ",
    sunFavorable: "ಅನುಕೂಲ ಸೂರ್ಯ ಬಲ (ಉಪಚಯ) ☀️",
    sunUnfavorable: "ಸೂರ್ಯ ಪ್ರತಿಕೂಲತೆ (ತಾಳ್ಮೆ ಅಗತ್ಯ)",
    monthlyHighlightsLabel: "ಮಾಸಿಕ ಮುಖ್ಯಾಂಶಗಳು",
    guruBalamLabel: "ಗುರು ಬಲ",
    guruBalamYes: "ಗುರು ಬಲವಿದೆ ✨",
    guruBalamNo: "ಗುರು ಶಾಂತಿ ಅಗತ್ಯ",
    shaniGocharaLabel: "ಶನಿ ಗೋಚಾರ",
    rahuKetuTransitLabel: "ರಾಹು-ಕೇತು ಸಂಚಾರ",
    financialAnalysisLabel: "ಆರ್ಥಿಕ ಸ್ಥಿತಿ ವಿಶ್ಲೇಷಣೆ",
    socialAnalysisLabel: "ಸಾಮಾಜಿಕ ಸ್ಥಾನಮಾನ ವಿಶ್ಲೇಷಣೆ",
    rashiOverviewTitle: "ಸಾಮಾನ್ಯ ಅವಲೋಕನ (General Overview)",
    rashiCareerTitle: "ಉದ್ಯೋಗ & ವ್ಯವಹಾರ (Career & Profession)",
    rashiFinanceTitle: "ಆರ್ಥಿಕ ಸ್ಥಿತಿ & ಧನ ಯೋಗ (Finance & Wealth)",
    rashiHealthTitle: "ಆರೋಗ್ಯ & ಚೈತನ್ಯ (Health & Well-being)",
    rashiFamilyTitle: "ಕುಟುಂಬ & ದಾಂಪತ್ಯ (Family & Relationships)",
    rashiRemediesTitle: "ಶಾಂತಿ / ದೈವಿಕ ಪರಿಹಾರ (Remedies & Prayers)",
    lordLabel: "ಅಧಿಪತಿ:",
    elementLabel: "ತತ್ತ್ವ:",
    compatibilityScoreLabel: "ಹೊಂದಾಣಿಕೆ ಅಂಕ",
    chandrashtamaMiniBadge: "ಚಂದ್ರಾಷ್ಟಮ",
    sunShortLabel: "ರವಿ",
    incomeShort: "ಆ",
    expenseShort: "ವ್ಯ",
    gpsNotSupported: "ನಿಮ್ಮ ಬ್ರೌಸರ್‌ನಲ್ಲಿ GPS ಜಿಯೋಲೊಕೇಶನ್ ಬೆಂಬಲವಿಲ್ಲ.",
    gpsSuccess: "ಸ್ಥಳವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಗುರುತಿಸಲಾಗಿದೆ",
    gpsDenied: "ಸ್ಥಳದ ಅನುಮತಿ ನಿರಾಕರಿಸಲಾಗಿದೆ"
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
    khandaLabel: "ഖണ്ഡം",

    prevDayTitle: "Previous Day",
    nextDayTitle: "Next Day",
    maxWord: "Max",
    bannerPurePeriod: "Pure Period",
    bannerTabooAuspicious: "Auspicious Ceremonies Prohibited",
    bannerTabooConstruction: "Construction / Housewarming Prohibited",
    bannerAnnualScheduleBtn: "Annual Schedule & Shastric Rules",
    modalMoudhyamTitle: "🪔 Annual Moudhyam & Kartari Schedule",
    modalMoudhyamSubtitle: "Nirayana Ephemeris Computation • Muhurtha Dharma Shastra Prohibitions & Allowances",
    timezoneLabel: "Timezone",
    moudhyamTimesSubtitle: "🕒 Timings: Your Local Time & (IST Indian Standard Time)",
    thPhase: "Phase",
    thTransit: "Solar Transit",
    thTiming: "Exact Timing",
    thSignificance: "Significance",
    moudhyamSectionTitle: "Moudhyam Periods (Combustion of Jupiter & Venus)",
    moudhyamSectionSubtitle: "Inauspicious periods when Jupiter or Venus are in deep celestial conjunction with the Sun.",
    durationLabel: "Duration",
    daysLabel: "days",
    moudhyamStartLabel: "Start (Combustion / Set):",
    moudhyamEndLabel: "End (Helical Rise):",
    vardhakyaLabel: "Vardhakya Dosha:",
    balyaLabel: "Balya Dosha:",
    prohibitionLabel: "Prohibition:",
    shastraDecisionsTitle: "Dharma Shastra Muhurtha Rules (Permitted vs Prohibited)",
    moudhyamTaboosTitle: "Taboos in Moudhyam:",
    kartariTaboosTitle: "Taboos in Kartari:",
    permittedKarmasTitle: "Permitted Karmas:",
    moudhyamLoading: "Loading Moudhyam & Kartari schedule...",
    moudhyamError: "Error loading schedule. Please try again.",
    adhikaMasaBadge: "Adhika Masa",
    nijaMasaBadge: "Nija Masa",
    kshayaMasaBadge: "Kshaya Masa",
    sankrantiWord: "Sankrantis",
    shuklaPaksha: "Shukla Paksha",
    krishnaPaksha: "Krishna Paksha",
    solarDaySuffix: "day",
    intercalaryHeroBadge: "🏛️ Dharma Shastra & Astronomy • Kalamadhaviyam",
    intercalaryHeroTitle: "Adhika & Kshaya Masas: Astronomy & Dharma Shastra Computation",
    intercalaryHeroSubtitle: "Comprehensive calculation of Adhika, Kshaya, Samsarpa, and Amhaspati months according to Surya Siddhanta and Kalamadhaviya shastric canons.",
    systemSuryaBtn: "📜 Surya Siddhanta (Shastra)",
    systemDrikBtn: "🔭 Drik Siddhanta (Swiss Ephemeris)",
    suryaSystemBadge: "Surya Siddhanta / Dharma Shastra Method",
    drikSystemBadge: "Drik Siddhanta Method (Swiss Ephemeris)",
    kalamadhavaHeader: "Kalamadhava Canonical Verse (Kalamadhaviyam)",
    kalamadhavaRuleDesc: "<strong>Dharma Shastra Rule:</strong> When two asankranta (no solar ingress) months occur in a single solar year, the first is <strong>Samsarpa</strong>. The intermediate month with two ingresses is the <strong>Kshaya Masa (Amhaspati)</strong>. The subsequent asankranta month is the <strong>Adhika Masa</strong>. Routine (Nitya/Naimittika) rites are permitted in Samsarpa; auspicious events like weddings are strictly taboo in Amhaspati (Kshaya).",
    adhikaCardTitle: "Adhika Masa (Asankranta)",
    adhikaCardBadge: "0 Ingresses",
    adhikaCardFormula: "Ingresses = 0 (Asankranta)",
    adhikaCardDesc: "When the Sun does not transit into any new zodiac sign between two successive Amavasyas (New Moons), it is an Adhika Masa. Occurs every ~32.5 lunar months.",
    nijaCardTitle: "Nija Masa (Normal Lunar Month)",
    nijaCardBadge: "1 Ingress",
    nijaCardFormula: "Ingresses = 1 (Sankranta)",
    nijaCardDesc: "A standard lunar month containing exactly one solar ingress. Propitious for all auspicious events and Vedic sacraments.",
    kshayaCardTitle: "Kshaya Masa (Dvi-Sankranta)",
    kshayaCardBadge: "2 Ingresses",
    kshayaCardFormula: "Ingresses = 2 (Dvi-Sankranta)",
    kshayaCardDesc: "When two solar ingresses occur within a single lunar month, it is an expunged or Kshaya month (Amhaspati), fusing two months into one.",
    driftTitle: "📐 Solar-Lunar Calendar Principles (Calendar Drift)",
    driftSolarYr: "Solar Year:",
    driftLunarYr: "Lunar Year (12 × 29.5):",
    driftAnnual: "Annual Drift:",
    drift3Yr: "Drift accumulated in 3 years:",
    driftLagadhaRule: "✨ <strong>Vedanga Jyotisha Canon (Sage Lagadha):</strong> In a 5-year Yuga cycle, 60 Solar months equal 62 Lunar months. Exactly 2 Adhika Masas occur every 5 years.",
    kaliyugaTitle: "🪐 Kaliyuga Cosmic Balance & Kshaya Recurrence Cycle",
    perihelionRule: "💡 <strong>Astronomical Perihelion Rule:</strong> Two solar ingresses within one lunar month can only occur when Earth is near perihelion and the Sun transits rapidly through Sagittarius, Capricorn, or Aquarius.",
    keelakaBadge: "Special Case Study",
    keelakaTitle: "Sri Keelaka Samvatsara (2028–2029) • Kshaya & Samsarpa Months",
    keelakaDesc: "According to the unanimous resolution of the <strong>'Telangana Vidwatsabha' Conference</strong> of 23 eminent Siddhantis and Vedic Scholars (Aug 30, 2026): In Sri Keelaka Samvatsara, Kartika is established as <strong>Samsarpa Kartika (Adhika)</strong>, followed by the combined Margashira-Pushya <strong>Amhaspati Masa (Kshaya Masa)</strong>.",
    intercalaryTableTitle: "📅 10-Year Adhika & Kshaya Masas Schedule (2026–2036)",
    intercalaryTableSubtitle: "Amanta lunar month calculations computed under the selected siddhanta system",
    thInterYr: "Year",
    thInterSamvat: "Samvatsara Name",
    thInterMasa: "Month Name",
    thInterType: "Type / Status",
    thInterSankranti: "Ingresses",
    thInterSpan: "Span (Start – End)",
    thInterRule: "Shastric Rule",
    toDateSpan: "to",
    kdHeroBadge: "📊 Annual Kandadayam Computation",
    kdMainHeading: "Kandadayam Results & Income-Expenditure",
    kdMainSubtitle: "Canonical results for 12 Rashis (Income, Expense, Honor, Disgrace) and 27 Nakshatras across 3 Trimesters (Prathama, Dvitiya, Tritiya Kandayams).",
    kdCreatorBadge: "✍️ Created by: Ramachandra Sastry Munimadugu",
    jumpToRashiKdBtn: "💰 Rashi Kandadayam",
    jumpToNakshatraKdBtn: "⭐ Nakshatra Trimesters",
    jumpToShastraKdBtn: "📜 Shastric Computation Rules",
    kdQuickT1Title: "🌱 First Trimester (Prathama)",
    kdQuickT1Span: "Months 1–4",
    kdQuickT1Months: "Chaitra, Vaishakha, Jyeshtha, Ashadha",
    kdQuickT1Max: "Max Limit: 8 Units (Remainder 0–7)",
    kdQuickT2Title: "🌧️ Second Trimester (Dvitiya)",
    kdQuickT2Span: "Months 5–8",
    kdQuickT2Months: "Shravana, Bhadrapada, Ashwayuja, Kartika",
    kdQuickT2Max: "Max Limit: 3 Units (Remainder 0–2)",
    kdQuickT3Title: "❄️ Third Trimester (Tritiya)",
    kdQuickT3Span: "Months 9–12",
    kdQuickT3Months: "Margashira, Pushya, Magha, Phalguna",
    kdQuickT3Max: "Max Limit: 5 Units (Remainder 0–4)",
    rashiKdSectionTitle: "💰 12 Rashi Kandadayam (Income, Expense, Honor, Disgrace)",
    rashiKdSectionSubtitle: "Comprehensive financial and social status evaluation of all 12 Rashis",
    rashiKdViewCardsBtn: "Cards",
    rashiKdViewTableBtn: "Table",
    thKdRashi: "Rashi",
    thKdLord: "Lord",
    thKdAdayam: "Income (Adayam)",
    thKdVyayam: "Expense (Vyayam)",
    thKdRajapujyam: "Honor (Rajapujyam)",
    thKdAvamanam: "Disgrace (Avamanam)",
    thKdFinStatus: "Financial Status",
    thKdSocStatus: "Social Honor",
    thKdVerdict: "Verdict",
    nakshatraSectionTitle: "⭐ 27 Nakshatra Kandayam Results (Trimester Breakdown)",
    nakshatraSectionSubtitle: "Discover your birth star results across the 3 trimester periods of the year",
    nakshatraSelectLabel: "Nakshatra:",
    nakshatraMasterTableTitle: "📋 Master Table: 27 Nakshatras Trimester Kandayam",
    nakshatraTableSearchInput: "Search by star name...",
    thNId: "S.No",
    thNName: "Nakshatra",
    thNRashis: "Rashis",
    thNT1: "First (Months 1–4)",
    thNT2: "Second (Months 5–8)",
    thNT3: "Third (Months 9–12)",
    thNOverall: "Annual Rating",
    shastraKdTitle: "📜 Shastric Rules & Trimester Science of Kandadayam",
    shastraKdT1Title: "📅 Year Division (3 Trimesters / Kandayams)",
    shastraKdT2Title: "⚖️ 12 Rashi Kandadayam Mathematical Principles",
    nakshatraWord: "Nakshatra",
    spreadRashisPadasLabel: "Spread Rashis / Padas:",
    annualCompositeStatusLabel: "Annual Composite Status",
    trimester1Title: "First Trimester",
    trimester1Months: "Chaitra – Ashadha (Months 1–4)",
    trimester1MaxLimit: "Max limit: 8 units",
    trimester2Title: "Second Trimester",
    trimester2Months: "Shravana – Kartika (Months 5–8)",
    trimester2MaxLimit: "Max limit: 3 units",
    trimester3Title: "Third Trimester",
    trimester3Months: "Margashira – Phalguna (Months 9–12)",
    trimester3MaxLimit: "Max limit: 5 units",
    annualSummaryAdviceLabel: "Annual Summary & Guidance:",
    noNakshatraFound: "No nakshatra results found",
    rashiHeading: "Rashi Phalalu (Gochara Horoscope)",
    rashiSubtitle: "Authoritative predictions based on celestial transits, Chandrabalam, Tarabalam, and Panchangam Kandadayam principles.",
    rashiGocharaBadge: "♈ 12 Rashis Gochara",
    moonTransitLabel: "Moon Transit",
    solarMonthLabel: "Solar Month",
    kandadayamTableLabel: "Panchangam Kandadayam Table",
    kdAdayam: "Income",
    kdVyayam: "Expense",
    kdRajapujyam: "Honor",
    kdAvamanam: "Disgrace",
    statusAuspicious: "Auspicious",
    statusFavorable: "Favorable",
    statusModerate: "Moderate",
    statusCaution: "Caution",
    footerOrgTitle: "Vedic Samhita • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "System Architect & Creator (Astronomical Siddhanta Computation)",
    footerCreatorName: "Ramachandra Sastry Munimadugu",
    footerCreatorDesc: "These panchangam algorithms, Vedic astronomical models, Dharma Shastra canons, and computational systems are authored and architected by <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "Official Website:",
    footerPoweredBy: "Powered by Swiss Ephemeris astronomical computation engine and Aksharamukha script transliteration.",
    chandrashtamaAlertTitle: "Chandrashtama Warning (Chandrashtama Active)",
    chandrashtamaAlertDesc: "Today the Moon transits the 8th house from your Janma Rashi. Exercise utmost caution in arguments, financial dealings, and launching major new agreements. Worship of Lord Shiva is recommended.",
    moonHouseLabel: "Moon House",
    houseSuffix: "th House",
    tarabalamLabel: "Tarabalam",
    taraGood: "Auspicious Tara ✔️",
    taraCaution: "Caution ⚠️",
    luckyNumberLabel: "Lucky Number",
    luckyColorLabel: "Lucky Color",
    luckyDirectionLabel: "Lucky Direction",
    sunTransitLabel: "Solar Transit",
    placeSuffix: "th House",
    sunFavorable: "Favorable Sun Strength (Upachaya) ☀️",
    sunUnfavorable: "Sun Adversity (Patience required)",
    monthlyHighlightsLabel: "Monthly Highlights",
    guruBalamLabel: "Guru Balam",
    guruBalamYes: "Guru Balam Present ✨",
    guruBalamNo: "Guru Shanti Recommended",
    shaniGocharaLabel: "Saturn Transit",
    rahuKetuTransitLabel: "Rahu-Ketu Transit",
    financialAnalysisLabel: "Financial Status Analysis",
    socialAnalysisLabel: "Social Status Analysis",
    rashiOverviewTitle: "General Overview",
    rashiCareerTitle: "Career & Profession",
    rashiFinanceTitle: "Finance & Wealth",
    rashiHealthTitle: "Health & Well-being",
    rashiFamilyTitle: "Family & Relationships",
    rashiRemediesTitle: "Remedies & Prayers",
    lordLabel: "Lord:",
    elementLabel: "Element:",
    compatibilityScoreLabel: "Compatibility Score",
    chandrashtamaMiniBadge: "Chandrashtama",
    sunShortLabel: "Sun",
    incomeShort: "Inc",
    expenseShort: "Exp",
    gpsNotSupported: "GPS Geolocation is not supported by your browser.",
    gpsSuccess: "Location detected successfully",
    gpsDenied: "Location permission denied"
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
    khandaLabel: "ખંડ",

    prevDayTitle: "Previous Day",
    nextDayTitle: "Next Day",
    maxWord: "Max",
    bannerPurePeriod: "Pure Period",
    bannerTabooAuspicious: "Auspicious Ceremonies Prohibited",
    bannerTabooConstruction: "Construction / Housewarming Prohibited",
    bannerAnnualScheduleBtn: "Annual Schedule & Shastric Rules",
    modalMoudhyamTitle: "🪔 Annual Moudhyam & Kartari Schedule",
    modalMoudhyamSubtitle: "Nirayana Ephemeris Computation • Muhurtha Dharma Shastra Prohibitions & Allowances",
    timezoneLabel: "Timezone",
    moudhyamTimesSubtitle: "🕒 Timings: Your Local Time & (IST Indian Standard Time)",
    thPhase: "Phase",
    thTransit: "Solar Transit",
    thTiming: "Exact Timing",
    thSignificance: "Significance",
    moudhyamSectionTitle: "Moudhyam Periods (Combustion of Jupiter & Venus)",
    moudhyamSectionSubtitle: "Inauspicious periods when Jupiter or Venus are in deep celestial conjunction with the Sun.",
    durationLabel: "Duration",
    daysLabel: "days",
    moudhyamStartLabel: "Start (Combustion / Set):",
    moudhyamEndLabel: "End (Helical Rise):",
    vardhakyaLabel: "Vardhakya Dosha:",
    balyaLabel: "Balya Dosha:",
    prohibitionLabel: "Prohibition:",
    shastraDecisionsTitle: "Dharma Shastra Muhurtha Rules (Permitted vs Prohibited)",
    moudhyamTaboosTitle: "Taboos in Moudhyam:",
    kartariTaboosTitle: "Taboos in Kartari:",
    permittedKarmasTitle: "Permitted Karmas:",
    moudhyamLoading: "Loading Moudhyam & Kartari schedule...",
    moudhyamError: "Error loading schedule. Please try again.",
    adhikaMasaBadge: "Adhika Masa",
    nijaMasaBadge: "Nija Masa",
    kshayaMasaBadge: "Kshaya Masa",
    sankrantiWord: "Sankrantis",
    shuklaPaksha: "Shukla Paksha",
    krishnaPaksha: "Krishna Paksha",
    solarDaySuffix: "day",
    intercalaryHeroBadge: "🏛️ Dharma Shastra & Astronomy • Kalamadhaviyam",
    intercalaryHeroTitle: "Adhika & Kshaya Masas: Astronomy & Dharma Shastra Computation",
    intercalaryHeroSubtitle: "Comprehensive calculation of Adhika, Kshaya, Samsarpa, and Amhaspati months according to Surya Siddhanta and Kalamadhaviya shastric canons.",
    systemSuryaBtn: "📜 Surya Siddhanta (Shastra)",
    systemDrikBtn: "🔭 Drik Siddhanta (Swiss Ephemeris)",
    suryaSystemBadge: "Surya Siddhanta / Dharma Shastra Method",
    drikSystemBadge: "Drik Siddhanta Method (Swiss Ephemeris)",
    kalamadhavaHeader: "Kalamadhava Canonical Verse (Kalamadhaviyam)",
    kalamadhavaRuleDesc: "<strong>Dharma Shastra Rule:</strong> When two asankranta (no solar ingress) months occur in a single solar year, the first is <strong>Samsarpa</strong>. The intermediate month with two ingresses is the <strong>Kshaya Masa (Amhaspati)</strong>. The subsequent asankranta month is the <strong>Adhika Masa</strong>. Routine (Nitya/Naimittika) rites are permitted in Samsarpa; auspicious events like weddings are strictly taboo in Amhaspati (Kshaya).",
    adhikaCardTitle: "Adhika Masa (Asankranta)",
    adhikaCardBadge: "0 Ingresses",
    adhikaCardFormula: "Ingresses = 0 (Asankranta)",
    adhikaCardDesc: "When the Sun does not transit into any new zodiac sign between two successive Amavasyas (New Moons), it is an Adhika Masa. Occurs every ~32.5 lunar months.",
    nijaCardTitle: "Nija Masa (Normal Lunar Month)",
    nijaCardBadge: "1 Ingress",
    nijaCardFormula: "Ingresses = 1 (Sankranta)",
    nijaCardDesc: "A standard lunar month containing exactly one solar ingress. Propitious for all auspicious events and Vedic sacraments.",
    kshayaCardTitle: "Kshaya Masa (Dvi-Sankranta)",
    kshayaCardBadge: "2 Ingresses",
    kshayaCardFormula: "Ingresses = 2 (Dvi-Sankranta)",
    kshayaCardDesc: "When two solar ingresses occur within a single lunar month, it is an expunged or Kshaya month (Amhaspati), fusing two months into one.",
    driftTitle: "📐 Solar-Lunar Calendar Principles (Calendar Drift)",
    driftSolarYr: "Solar Year:",
    driftLunarYr: "Lunar Year (12 × 29.5):",
    driftAnnual: "Annual Drift:",
    drift3Yr: "Drift accumulated in 3 years:",
    driftLagadhaRule: "✨ <strong>Vedanga Jyotisha Canon (Sage Lagadha):</strong> In a 5-year Yuga cycle, 60 Solar months equal 62 Lunar months. Exactly 2 Adhika Masas occur every 5 years.",
    kaliyugaTitle: "🪐 Kaliyuga Cosmic Balance & Kshaya Recurrence Cycle",
    perihelionRule: "💡 <strong>Astronomical Perihelion Rule:</strong> Two solar ingresses within one lunar month can only occur when Earth is near perihelion and the Sun transits rapidly through Sagittarius, Capricorn, or Aquarius.",
    keelakaBadge: "Special Case Study",
    keelakaTitle: "Sri Keelaka Samvatsara (2028–2029) • Kshaya & Samsarpa Months",
    keelakaDesc: "According to the unanimous resolution of the <strong>'Telangana Vidwatsabha' Conference</strong> of 23 eminent Siddhantis and Vedic Scholars (Aug 30, 2026): In Sri Keelaka Samvatsara, Kartika is established as <strong>Samsarpa Kartika (Adhika)</strong>, followed by the combined Margashira-Pushya <strong>Amhaspati Masa (Kshaya Masa)</strong>.",
    intercalaryTableTitle: "📅 10-Year Adhika & Kshaya Masas Schedule (2026–2036)",
    intercalaryTableSubtitle: "Amanta lunar month calculations computed under the selected siddhanta system",
    thInterYr: "Year",
    thInterSamvat: "Samvatsara Name",
    thInterMasa: "Month Name",
    thInterType: "Type / Status",
    thInterSankranti: "Ingresses",
    thInterSpan: "Span (Start – End)",
    thInterRule: "Shastric Rule",
    toDateSpan: "to",
    kdHeroBadge: "📊 Annual Kandadayam Computation",
    kdMainHeading: "Kandadayam Results & Income-Expenditure",
    kdMainSubtitle: "Canonical results for 12 Rashis (Income, Expense, Honor, Disgrace) and 27 Nakshatras across 3 Trimesters (Prathama, Dvitiya, Tritiya Kandayams).",
    kdCreatorBadge: "✍️ Created by: Ramachandra Sastry Munimadugu",
    jumpToRashiKdBtn: "💰 Rashi Kandadayam",
    jumpToNakshatraKdBtn: "⭐ Nakshatra Trimesters",
    jumpToShastraKdBtn: "📜 Shastric Computation Rules",
    kdQuickT1Title: "🌱 First Trimester (Prathama)",
    kdQuickT1Span: "Months 1–4",
    kdQuickT1Months: "Chaitra, Vaishakha, Jyeshtha, Ashadha",
    kdQuickT1Max: "Max Limit: 8 Units (Remainder 0–7)",
    kdQuickT2Title: "🌧️ Second Trimester (Dvitiya)",
    kdQuickT2Span: "Months 5–8",
    kdQuickT2Months: "Shravana, Bhadrapada, Ashwayuja, Kartika",
    kdQuickT2Max: "Max Limit: 3 Units (Remainder 0–2)",
    kdQuickT3Title: "❄️ Third Trimester (Tritiya)",
    kdQuickT3Span: "Months 9–12",
    kdQuickT3Months: "Margashira, Pushya, Magha, Phalguna",
    kdQuickT3Max: "Max Limit: 5 Units (Remainder 0–4)",
    rashiKdSectionTitle: "💰 12 Rashi Kandadayam (Income, Expense, Honor, Disgrace)",
    rashiKdSectionSubtitle: "Comprehensive financial and social status evaluation of all 12 Rashis",
    rashiKdViewCardsBtn: "Cards",
    rashiKdViewTableBtn: "Table",
    thKdRashi: "Rashi",
    thKdLord: "Lord",
    thKdAdayam: "Income (Adayam)",
    thKdVyayam: "Expense (Vyayam)",
    thKdRajapujyam: "Honor (Rajapujyam)",
    thKdAvamanam: "Disgrace (Avamanam)",
    thKdFinStatus: "Financial Status",
    thKdSocStatus: "Social Honor",
    thKdVerdict: "Verdict",
    nakshatraSectionTitle: "⭐ 27 Nakshatra Kandayam Results (Trimester Breakdown)",
    nakshatraSectionSubtitle: "Discover your birth star results across the 3 trimester periods of the year",
    nakshatraSelectLabel: "Nakshatra:",
    nakshatraMasterTableTitle: "📋 Master Table: 27 Nakshatras Trimester Kandayam",
    nakshatraTableSearchInput: "Search by star name...",
    thNId: "S.No",
    thNName: "Nakshatra",
    thNRashis: "Rashis",
    thNT1: "First (Months 1–4)",
    thNT2: "Second (Months 5–8)",
    thNT3: "Third (Months 9–12)",
    thNOverall: "Annual Rating",
    shastraKdTitle: "📜 Shastric Rules & Trimester Science of Kandadayam",
    shastraKdT1Title: "📅 Year Division (3 Trimesters / Kandayams)",
    shastraKdT2Title: "⚖️ 12 Rashi Kandadayam Mathematical Principles",
    nakshatraWord: "Nakshatra",
    spreadRashisPadasLabel: "Spread Rashis / Padas:",
    annualCompositeStatusLabel: "Annual Composite Status",
    trimester1Title: "First Trimester",
    trimester1Months: "Chaitra – Ashadha (Months 1–4)",
    trimester1MaxLimit: "Max limit: 8 units",
    trimester2Title: "Second Trimester",
    trimester2Months: "Shravana – Kartika (Months 5–8)",
    trimester2MaxLimit: "Max limit: 3 units",
    trimester3Title: "Third Trimester",
    trimester3Months: "Margashira – Phalguna (Months 9–12)",
    trimester3MaxLimit: "Max limit: 5 units",
    annualSummaryAdviceLabel: "Annual Summary & Guidance:",
    noNakshatraFound: "No nakshatra results found",
    rashiHeading: "Rashi Phalalu (Gochara Horoscope)",
    rashiSubtitle: "Authoritative predictions based on celestial transits, Chandrabalam, Tarabalam, and Panchangam Kandadayam principles.",
    rashiGocharaBadge: "♈ 12 Rashis Gochara",
    moonTransitLabel: "Moon Transit",
    solarMonthLabel: "Solar Month",
    kandadayamTableLabel: "Panchangam Kandadayam Table",
    kdAdayam: "Income",
    kdVyayam: "Expense",
    kdRajapujyam: "Honor",
    kdAvamanam: "Disgrace",
    statusAuspicious: "Auspicious",
    statusFavorable: "Favorable",
    statusModerate: "Moderate",
    statusCaution: "Caution",
    footerOrgTitle: "Vedic Samhita • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "System Architect & Creator (Astronomical Siddhanta Computation)",
    footerCreatorName: "Ramachandra Sastry Munimadugu",
    footerCreatorDesc: "These panchangam algorithms, Vedic astronomical models, Dharma Shastra canons, and computational systems are authored and architected by <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "Official Website:",
    footerPoweredBy: "Powered by Swiss Ephemeris astronomical computation engine and Aksharamukha script transliteration.",
    chandrashtamaAlertTitle: "Chandrashtama Warning (Chandrashtama Active)",
    chandrashtamaAlertDesc: "Today the Moon transits the 8th house from your Janma Rashi. Exercise utmost caution in arguments, financial dealings, and launching major new agreements. Worship of Lord Shiva is recommended.",
    moonHouseLabel: "Moon House",
    houseSuffix: "th House",
    tarabalamLabel: "Tarabalam",
    taraGood: "Auspicious Tara ✔️",
    taraCaution: "Caution ⚠️",
    luckyNumberLabel: "Lucky Number",
    luckyColorLabel: "Lucky Color",
    luckyDirectionLabel: "Lucky Direction",
    sunTransitLabel: "Solar Transit",
    placeSuffix: "th House",
    sunFavorable: "Favorable Sun Strength (Upachaya) ☀️",
    sunUnfavorable: "Sun Adversity (Patience required)",
    monthlyHighlightsLabel: "Monthly Highlights",
    guruBalamLabel: "Guru Balam",
    guruBalamYes: "Guru Balam Present ✨",
    guruBalamNo: "Guru Shanti Recommended",
    shaniGocharaLabel: "Saturn Transit",
    rahuKetuTransitLabel: "Rahu-Ketu Transit",
    financialAnalysisLabel: "Financial Status Analysis",
    socialAnalysisLabel: "Social Status Analysis",
    rashiOverviewTitle: "General Overview",
    rashiCareerTitle: "Career & Profession",
    rashiFinanceTitle: "Finance & Wealth",
    rashiHealthTitle: "Health & Well-being",
    rashiFamilyTitle: "Family & Relationships",
    rashiRemediesTitle: "Remedies & Prayers",
    lordLabel: "Lord:",
    elementLabel: "Element:",
    compatibilityScoreLabel: "Compatibility Score",
    chandrashtamaMiniBadge: "Chandrashtama",
    sunShortLabel: "Sun",
    incomeShort: "Inc",
    expenseShort: "Exp",
    gpsNotSupported: "GPS Geolocation is not supported by your browser.",
    gpsSuccess: "Location detected successfully",
    gpsDenied: "Location permission denied"
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
    khandaLabel: "খণ্ড",

    prevDayTitle: "Previous Day",
    nextDayTitle: "Next Day",
    maxWord: "Max",
    bannerPurePeriod: "Pure Period",
    bannerTabooAuspicious: "Auspicious Ceremonies Prohibited",
    bannerTabooConstruction: "Construction / Housewarming Prohibited",
    bannerAnnualScheduleBtn: "Annual Schedule & Shastric Rules",
    modalMoudhyamTitle: "🪔 Annual Moudhyam & Kartari Schedule",
    modalMoudhyamSubtitle: "Nirayana Ephemeris Computation • Muhurtha Dharma Shastra Prohibitions & Allowances",
    timezoneLabel: "Timezone",
    moudhyamTimesSubtitle: "🕒 Timings: Your Local Time & (IST Indian Standard Time)",
    thPhase: "Phase",
    thTransit: "Solar Transit",
    thTiming: "Exact Timing",
    thSignificance: "Significance",
    moudhyamSectionTitle: "Moudhyam Periods (Combustion of Jupiter & Venus)",
    moudhyamSectionSubtitle: "Inauspicious periods when Jupiter or Venus are in deep celestial conjunction with the Sun.",
    durationLabel: "Duration",
    daysLabel: "days",
    moudhyamStartLabel: "Start (Combustion / Set):",
    moudhyamEndLabel: "End (Helical Rise):",
    vardhakyaLabel: "Vardhakya Dosha:",
    balyaLabel: "Balya Dosha:",
    prohibitionLabel: "Prohibition:",
    shastraDecisionsTitle: "Dharma Shastra Muhurtha Rules (Permitted vs Prohibited)",
    moudhyamTaboosTitle: "Taboos in Moudhyam:",
    kartariTaboosTitle: "Taboos in Kartari:",
    permittedKarmasTitle: "Permitted Karmas:",
    moudhyamLoading: "Loading Moudhyam & Kartari schedule...",
    moudhyamError: "Error loading schedule. Please try again.",
    adhikaMasaBadge: "Adhika Masa",
    nijaMasaBadge: "Nija Masa",
    kshayaMasaBadge: "Kshaya Masa",
    sankrantiWord: "Sankrantis",
    shuklaPaksha: "Shukla Paksha",
    krishnaPaksha: "Krishna Paksha",
    solarDaySuffix: "day",
    intercalaryHeroBadge: "🏛️ Dharma Shastra & Astronomy • Kalamadhaviyam",
    intercalaryHeroTitle: "Adhika & Kshaya Masas: Astronomy & Dharma Shastra Computation",
    intercalaryHeroSubtitle: "Comprehensive calculation of Adhika, Kshaya, Samsarpa, and Amhaspati months according to Surya Siddhanta and Kalamadhaviya shastric canons.",
    systemSuryaBtn: "📜 Surya Siddhanta (Shastra)",
    systemDrikBtn: "🔭 Drik Siddhanta (Swiss Ephemeris)",
    suryaSystemBadge: "Surya Siddhanta / Dharma Shastra Method",
    drikSystemBadge: "Drik Siddhanta Method (Swiss Ephemeris)",
    kalamadhavaHeader: "Kalamadhava Canonical Verse (Kalamadhaviyam)",
    kalamadhavaRuleDesc: "<strong>Dharma Shastra Rule:</strong> When two asankranta (no solar ingress) months occur in a single solar year, the first is <strong>Samsarpa</strong>. The intermediate month with two ingresses is the <strong>Kshaya Masa (Amhaspati)</strong>. The subsequent asankranta month is the <strong>Adhika Masa</strong>. Routine (Nitya/Naimittika) rites are permitted in Samsarpa; auspicious events like weddings are strictly taboo in Amhaspati (Kshaya).",
    adhikaCardTitle: "Adhika Masa (Asankranta)",
    adhikaCardBadge: "0 Ingresses",
    adhikaCardFormula: "Ingresses = 0 (Asankranta)",
    adhikaCardDesc: "When the Sun does not transit into any new zodiac sign between two successive Amavasyas (New Moons), it is an Adhika Masa. Occurs every ~32.5 lunar months.",
    nijaCardTitle: "Nija Masa (Normal Lunar Month)",
    nijaCardBadge: "1 Ingress",
    nijaCardFormula: "Ingresses = 1 (Sankranta)",
    nijaCardDesc: "A standard lunar month containing exactly one solar ingress. Propitious for all auspicious events and Vedic sacraments.",
    kshayaCardTitle: "Kshaya Masa (Dvi-Sankranta)",
    kshayaCardBadge: "2 Ingresses",
    kshayaCardFormula: "Ingresses = 2 (Dvi-Sankranta)",
    kshayaCardDesc: "When two solar ingresses occur within a single lunar month, it is an expunged or Kshaya month (Amhaspati), fusing two months into one.",
    driftTitle: "📐 Solar-Lunar Calendar Principles (Calendar Drift)",
    driftSolarYr: "Solar Year:",
    driftLunarYr: "Lunar Year (12 × 29.5):",
    driftAnnual: "Annual Drift:",
    drift3Yr: "Drift accumulated in 3 years:",
    driftLagadhaRule: "✨ <strong>Vedanga Jyotisha Canon (Sage Lagadha):</strong> In a 5-year Yuga cycle, 60 Solar months equal 62 Lunar months. Exactly 2 Adhika Masas occur every 5 years.",
    kaliyugaTitle: "🪐 Kaliyuga Cosmic Balance & Kshaya Recurrence Cycle",
    perihelionRule: "💡 <strong>Astronomical Perihelion Rule:</strong> Two solar ingresses within one lunar month can only occur when Earth is near perihelion and the Sun transits rapidly through Sagittarius, Capricorn, or Aquarius.",
    keelakaBadge: "Special Case Study",
    keelakaTitle: "Sri Keelaka Samvatsara (2028–2029) • Kshaya & Samsarpa Months",
    keelakaDesc: "According to the unanimous resolution of the <strong>'Telangana Vidwatsabha' Conference</strong> of 23 eminent Siddhantis and Vedic Scholars (Aug 30, 2026): In Sri Keelaka Samvatsara, Kartika is established as <strong>Samsarpa Kartika (Adhika)</strong>, followed by the combined Margashira-Pushya <strong>Amhaspati Masa (Kshaya Masa)</strong>.",
    intercalaryTableTitle: "📅 10-Year Adhika & Kshaya Masas Schedule (2026–2036)",
    intercalaryTableSubtitle: "Amanta lunar month calculations computed under the selected siddhanta system",
    thInterYr: "Year",
    thInterSamvat: "Samvatsara Name",
    thInterMasa: "Month Name",
    thInterType: "Type / Status",
    thInterSankranti: "Ingresses",
    thInterSpan: "Span (Start – End)",
    thInterRule: "Shastric Rule",
    toDateSpan: "to",
    kdHeroBadge: "📊 Annual Kandadayam Computation",
    kdMainHeading: "Kandadayam Results & Income-Expenditure",
    kdMainSubtitle: "Canonical results for 12 Rashis (Income, Expense, Honor, Disgrace) and 27 Nakshatras across 3 Trimesters (Prathama, Dvitiya, Tritiya Kandayams).",
    kdCreatorBadge: "✍️ Created by: Ramachandra Sastry Munimadugu",
    jumpToRashiKdBtn: "💰 Rashi Kandadayam",
    jumpToNakshatraKdBtn: "⭐ Nakshatra Trimesters",
    jumpToShastraKdBtn: "📜 Shastric Computation Rules",
    kdQuickT1Title: "🌱 First Trimester (Prathama)",
    kdQuickT1Span: "Months 1–4",
    kdQuickT1Months: "Chaitra, Vaishakha, Jyeshtha, Ashadha",
    kdQuickT1Max: "Max Limit: 8 Units (Remainder 0–7)",
    kdQuickT2Title: "🌧️ Second Trimester (Dvitiya)",
    kdQuickT2Span: "Months 5–8",
    kdQuickT2Months: "Shravana, Bhadrapada, Ashwayuja, Kartika",
    kdQuickT2Max: "Max Limit: 3 Units (Remainder 0–2)",
    kdQuickT3Title: "❄️ Third Trimester (Tritiya)",
    kdQuickT3Span: "Months 9–12",
    kdQuickT3Months: "Margashira, Pushya, Magha, Phalguna",
    kdQuickT3Max: "Max Limit: 5 Units (Remainder 0–4)",
    rashiKdSectionTitle: "💰 12 Rashi Kandadayam (Income, Expense, Honor, Disgrace)",
    rashiKdSectionSubtitle: "Comprehensive financial and social status evaluation of all 12 Rashis",
    rashiKdViewCardsBtn: "Cards",
    rashiKdViewTableBtn: "Table",
    thKdRashi: "Rashi",
    thKdLord: "Lord",
    thKdAdayam: "Income (Adayam)",
    thKdVyayam: "Expense (Vyayam)",
    thKdRajapujyam: "Honor (Rajapujyam)",
    thKdAvamanam: "Disgrace (Avamanam)",
    thKdFinStatus: "Financial Status",
    thKdSocStatus: "Social Honor",
    thKdVerdict: "Verdict",
    nakshatraSectionTitle: "⭐ 27 Nakshatra Kandayam Results (Trimester Breakdown)",
    nakshatraSectionSubtitle: "Discover your birth star results across the 3 trimester periods of the year",
    nakshatraSelectLabel: "Nakshatra:",
    nakshatraMasterTableTitle: "📋 Master Table: 27 Nakshatras Trimester Kandayam",
    nakshatraTableSearchInput: "Search by star name...",
    thNId: "S.No",
    thNName: "Nakshatra",
    thNRashis: "Rashis",
    thNT1: "First (Months 1–4)",
    thNT2: "Second (Months 5–8)",
    thNT3: "Third (Months 9–12)",
    thNOverall: "Annual Rating",
    shastraKdTitle: "📜 Shastric Rules & Trimester Science of Kandadayam",
    shastraKdT1Title: "📅 Year Division (3 Trimesters / Kandayams)",
    shastraKdT2Title: "⚖️ 12 Rashi Kandadayam Mathematical Principles",
    nakshatraWord: "Nakshatra",
    spreadRashisPadasLabel: "Spread Rashis / Padas:",
    annualCompositeStatusLabel: "Annual Composite Status",
    trimester1Title: "First Trimester",
    trimester1Months: "Chaitra – Ashadha (Months 1–4)",
    trimester1MaxLimit: "Max limit: 8 units",
    trimester2Title: "Second Trimester",
    trimester2Months: "Shravana – Kartika (Months 5–8)",
    trimester2MaxLimit: "Max limit: 3 units",
    trimester3Title: "Third Trimester",
    trimester3Months: "Margashira – Phalguna (Months 9–12)",
    trimester3MaxLimit: "Max limit: 5 units",
    annualSummaryAdviceLabel: "Annual Summary & Guidance:",
    noNakshatraFound: "No nakshatra results found",
    rashiHeading: "Rashi Phalalu (Gochara Horoscope)",
    rashiSubtitle: "Authoritative predictions based on celestial transits, Chandrabalam, Tarabalam, and Panchangam Kandadayam principles.",
    rashiGocharaBadge: "♈ 12 Rashis Gochara",
    moonTransitLabel: "Moon Transit",
    solarMonthLabel: "Solar Month",
    kandadayamTableLabel: "Panchangam Kandadayam Table",
    kdAdayam: "Income",
    kdVyayam: "Expense",
    kdRajapujyam: "Honor",
    kdAvamanam: "Disgrace",
    statusAuspicious: "Auspicious",
    statusFavorable: "Favorable",
    statusModerate: "Moderate",
    statusCaution: "Caution",
    footerOrgTitle: "Vedic Samhita • Vedic Samhita",
    footerOrgSubtitle: "Vedic Astronomy & Dharma Shastra Computation System",
    footerCreatorRole: "System Architect & Creator (Astronomical Siddhanta Computation)",
    footerCreatorName: "Ramachandra Sastry Munimadugu",
    footerCreatorDesc: "These panchangam algorithms, Vedic astronomical models, Dharma Shastra canons, and computational systems are authored and architected by <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>. <br class=\"hidden sm:inline\"/> All credits go to <strong class=\"text-amber-200 font-bold\">RAMACHANDRA SASTRY MUNIMADUGU</strong>.",
    footerOfficialWebsiteLabel: "Official Website:",
    footerPoweredBy: "Powered by Swiss Ephemeris astronomical computation engine and Aksharamukha script transliteration.",
    chandrashtamaAlertTitle: "Chandrashtama Warning (Chandrashtama Active)",
    chandrashtamaAlertDesc: "Today the Moon transits the 8th house from your Janma Rashi. Exercise utmost caution in arguments, financial dealings, and launching major new agreements. Worship of Lord Shiva is recommended.",
    moonHouseLabel: "Moon House",
    houseSuffix: "th House",
    tarabalamLabel: "Tarabalam",
    taraGood: "Auspicious Tara ✔️",
    taraCaution: "Caution ⚠️",
    luckyNumberLabel: "Lucky Number",
    luckyColorLabel: "Lucky Color",
    luckyDirectionLabel: "Lucky Direction",
    sunTransitLabel: "Solar Transit",
    placeSuffix: "th House",
    sunFavorable: "Favorable Sun Strength (Upachaya) ☀️",
    sunUnfavorable: "Sun Adversity (Patience required)",
    monthlyHighlightsLabel: "Monthly Highlights",
    guruBalamLabel: "Guru Balam",
    guruBalamYes: "Guru Balam Present ✨",
    guruBalamNo: "Guru Shanti Recommended",
    shaniGocharaLabel: "Saturn Transit",
    rahuKetuTransitLabel: "Rahu-Ketu Transit",
    financialAnalysisLabel: "Financial Status Analysis",
    socialAnalysisLabel: "Social Status Analysis",
    rashiOverviewTitle: "General Overview",
    rashiCareerTitle: "Career & Profession",
    rashiFinanceTitle: "Finance & Wealth",
    rashiHealthTitle: "Health & Well-being",
    rashiFamilyTitle: "Family & Relationships",
    rashiRemediesTitle: "Remedies & Prayers",
    lordLabel: "Lord:",
    elementLabel: "Element:",
    compatibilityScoreLabel: "Compatibility Score",
    chandrashtamaMiniBadge: "Chandrashtama",
    sunShortLabel: "Sun",
    incomeShort: "Inc",
    expenseShort: "Exp",
    gpsNotSupported: "GPS Geolocation is not supported by your browser.",
    gpsSuccess: "Location detected successfully",
    gpsDenied: "Location permission denied"
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
  setTitle('prevDayBtn', t('prevDayTitle'));
  setTitle('nextDayBtn', t('nextDayTitle'));

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

  // Intercalary Tab
  setTxt('intercalaryHeroBadge', t('intercalaryHeroBadge'));
  setTxt('intercalaryHeroTitle', t('intercalaryHeroTitle'));
  setTxt('intercalaryHeroSubtitle', t('intercalaryHeroSubtitle'));
  setTxt('systemSuryaBtn', t('systemSuryaBtn'));
  setTxt('systemDrikBtn', t('systemDrikBtn'));
  setTxt('kalamadhavaHeader', t('kalamadhavaHeader'));
  setHtml('kalamadhavaRuleDesc', t('kalamadhavaRuleDesc'));
  setTxt('adhikaCardTitle', t('adhikaCardTitle'));
  setTxt('adhikaCardBadge', t('adhikaCardBadge'));
  setTxt('adhikaCardFormula', t('adhikaCardFormula'));
  setTxt('adhikaCardDesc', t('adhikaCardDesc'));
  setTxt('nijaCardTitle', t('nijaCardTitle'));
  setTxt('nijaCardBadge', t('nijaCardBadge'));
  setTxt('nijaCardFormula', t('nijaCardFormula'));
  setTxt('nijaCardDesc', t('nijaCardDesc'));
  setTxt('kshayaCardTitle', t('kshayaCardTitle'));
  setTxt('kshayaCardBadge', t('kshayaCardBadge'));
  setTxt('kshayaCardFormula', t('kshayaCardFormula'));
  setTxt('kshayaCardDesc', t('kshayaCardDesc'));
  setTxt('driftTitle', t('driftTitle'));
  setTxt('driftSolarYr', t('driftSolarYr'));
  setTxt('driftLunarYr', t('driftLunarYr'));
  setTxt('driftAnnual', t('driftAnnual'));
  setTxt('drift3Yr', t('drift3Yr'));
  setHtml('driftLagadhaRule', t('driftLagadhaRule'));
  setTxt('kaliyugaTitle', t('kaliyugaTitle'));
  setHtml('perihelionRule', t('perihelionRule'));
  setTxt('keelakaBadge', t('keelakaBadge'));
  setTxt('keelakaTitle', t('keelakaTitle'));
  setHtml('keelakaDesc', t('keelakaDesc'));
  setTxt('intercalaryTableTitle', t('intercalaryTableTitle'));
  setTxt('intercalaryTableSubtitle', t('intercalaryTableSubtitle'));
  setTxt('thInterYr', t('thInterYr'));
  setTxt('thInterSamvat', t('thInterSamvat'));
  setTxt('thInterMasa', t('thInterMasa'));
  setTxt('thInterType', t('thInterType'));
  setTxt('thInterSankranti', t('thInterSankranti'));
  setTxt('thInterSpan', t('thInterSpan'));
  setTxt('thInterRule', t('thInterRule'));

  // Kandadayam Tab
  setTxt('kdHeroBadge', t('kdHeroBadge'));
  setTxt('kdMainHeading', t('kdMainHeading'));
  setTxt('kdMainSubtitle', t('kdMainSubtitle'));
  setTxt('kdCreatorBadge', t('kdCreatorBadge'));
  setTxt('jumpToRashiKdBtn', t('jumpToRashiKdBtn'));
  setTxt('jumpToNakshatraKdBtn', t('jumpToNakshatraKdBtn'));
  setTxt('jumpToShastraKdBtn', t('jumpToShastraKdBtn'));
  setTxt('kdQuickT1Title', t('kdQuickT1Title'));
  setTxt('kdQuickT1Span', t('kdQuickT1Span'));
  setTxt('kdQuickT1Months', t('kdQuickT1Months'));
  setTxt('kdQuickT1Max', t('kdQuickT1Max'));
  setTxt('kdQuickT2Title', t('kdQuickT2Title'));
  setTxt('kdQuickT2Span', t('kdQuickT2Span'));
  setTxt('kdQuickT2Months', t('kdQuickT2Months'));
  setTxt('kdQuickT2Max', t('kdQuickT2Max'));
  setTxt('kdQuickT3Title', t('kdQuickT3Title'));
  setTxt('kdQuickT3Span', t('kdQuickT3Span'));
  setTxt('kdQuickT3Months', t('kdQuickT3Months'));
  setTxt('kdQuickT3Max', t('kdQuickT3Max'));
  setTxt('rashiKdSectionTitle', t('rashiKdSectionTitle'));
  setTxt('rashiKdSectionSubtitle', t('rashiKdSectionSubtitle'));
  setTxt('rashiKdViewCardsBtn', t('rashiKdViewCardsBtn'));
  setTxt('rashiKdViewTableBtn', t('rashiKdViewTableBtn'));
  setTxt('thKdRashi', t('thKdRashi'));
  setTxt('thKdLord', t('thKdLord'));
  setTxt('thKdAdayam', t('thKdAdayam'));
  setTxt('thKdVyayam', t('thKdVyayam'));
  setTxt('thKdRajapujyam', t('thKdRajapujyam'));
  setTxt('thKdAvamanam', t('thKdAvamanam'));
  setTxt('thKdFinStatus', t('thKdFinStatus'));
  setTxt('thKdSocStatus', t('thKdSocStatus'));
  setTxt('thKdVerdict', t('thKdVerdict'));
  setTxt('nakshatraSectionTitle', t('nakshatraSectionTitle'));
  setTxt('nakshatraSectionSubtitle', t('nakshatraSectionSubtitle'));
  setTxt('nakshatraSelectLabel', t('nakshatraSelectLabel'));
  setTxt('nakshatraMasterTableTitle', t('nakshatraMasterTableTitle'));
  setPh('nakshatraTableSearchInput', t('nakshatraTableSearchInput'));
  setTxt('thNId', t('thNId'));
  setTxt('thNName', t('thNName'));
  setTxt('thNRashis', t('thNRashis'));
  setTxt('thNT1', t('thNT1'));
  setTxt('thNT2', t('thNT2'));
  setTxt('thNT3', t('thNT3'));
  setTxt('thNOverall', t('thNOverall'));
  setTxt('shastraKdTitle', t('shastraKdTitle'));
  setTxt('shastraKdT1Title', t('shastraKdT1Title'));
  setTxt('shastraKdT2Title', t('shastraKdT2Title'));

  // Rashi Tab
  setTxt('rashiHeading', t('rashiHeading'));
  setTxt('rashiSubtitle', t('rashiSubtitle'));
  setTxt('rashiGocharaBadge', t('rashiGocharaBadge'));

  // Modal
  setTxt('modalMoudhyamTitle', t('modalMoudhyamTitle'));
  setTxt('modalMoudhyamSubtitle', t('modalMoudhyamSubtitle'));

  // Footer
  setTxt('footerOrgTitle', t('footerOrgTitle'));
  setTxt('footerOrgSubtitle', t('footerOrgSubtitle'));
  setTxt('footerCreatorRole', t('footerCreatorRole'));
  setTxt('footerCreatorName', t('footerCreatorName'));
  setHtml('footerCreatorDesc', t('footerCreatorDesc'));
  setTxt('footerOfficialWebsiteLabel', t('footerOfficialWebsiteLabel'));
  setTxt('footerPoweredBy', t('footerPoweredBy'));

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

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const firstCity = searchResults.querySelector('.city-search-item');
      if (firstCity) {
        firstCity.click();
      }
    }
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

  // Moudhyam & Kartari Modal Close
  const closeMdBtn = document.getElementById('closeMoudhyamModalBtn');
  const mdModal = document.getElementById('annualMoudhyamModal');
  if (closeMdBtn && mdModal) {
    closeMdBtn.addEventListener('click', () => mdModal.classList.add('hidden'));
    mdModal.addEventListener('click', (e) => {
      if (e.target === mdModal) mdModal.classList.add('hidden');
    });
  }
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
  if (pakshaRaw === 'Shukla' || pakshaRaw === 'శుక్ల' || (typeof pakshaRaw === 'string' && pakshaRaw.toLowerCase().includes('shukla'))) {
    pakshaDisplay = t('shuklaPaksha');
  } else if (pakshaRaw === 'Krishna' || pakshaRaw === 'కృష్ణ' || (typeof pakshaRaw === 'string' && pakshaRaw.toLowerCase().includes('krishna'))) {
    pakshaDisplay = t('krishnaPaksha');
  }
  document.getElementById('cmPaksha').innerText = pakshaDisplay || '---';

  const cmBadge = document.getElementById('cmMasaBadge');
  const cmStatus = document.getElementById('cmMasaStatus');
  if (cmBadge) {
    const classification = cm.amanta_masa.masa_classification || (cm.amanta_masa.is_adhika ? 'ADHIKA' : 'NIJA');
    const badgeText = cm.amanta_masa.badge_label || (classification === 'ADHIKA' ? t('adhikaMasaBadge') : (classification === 'KSHAYA' ? t('kshayaMasaBadge') : t('nijaMasaBadge')));
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
    const typeLabel = cm.amanta_masa.badge_label || (sc === 0 ? t('adhikaMasaBadge') : (sc === 2 ? t('kshayaMasaBadge') : t('nijaMasaBadge')));
    cmStatus.innerText = `${typeLabel} (${sc} ${t('sankrantiWord')})`;
  }

  // Sauramana
  const regSolar = sm.regional_solar_calendars || {};
  const smSolar = sm.solar_month || {};
  let smSolarText = smSolar.name;
  if (!smSolarText) {
    const rName = smSolar.rashi_name || '';
    const dayVal = smSolar.day ? (STATE.lang === 'english' ? `Day ${smSolar.day}` : `${smSolar.day} ${t('solarDaySuffix')}`) : '';
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

  // 8. Moudhyam & Kartari Assessment Banner
  renderMoudhyamKartariBanner(data.moudhyam_kartari);
}

// ==========================================
// MOUDYAM & KARTARI LIVE & ANNUAL LOGIC
// ==========================================

function renderMoudhyamKartariBanner(mk) {
  const container = document.getElementById('moudhyamKartariBanner');
  if (!container) return;

  if (!mk) {
    container.classList.add('hidden');
    return;
  }
  container.classList.remove('hidden');

  const isMoudhyam = mk.is_moudhyam;
  const isKartari = mk.is_kartari;

  let bgClasses = "bg-gradient-to-r from-emerald-50/90 to-amber-50/60 border-emerald-300 text-emerald-950";
  let iconHtml = "✨";
  let iconBg = "bg-emerald-100 border-emerald-300 text-emerald-700";
  let pillHtml = `<span class="text-[11px] px-2.5 py-0.5 rounded-full font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">✨ ${t('bannerPurePeriod')}</span>`;
  let btnClasses = "bg-emerald-700 hover:bg-emerald-800 text-white";

  if (isMoudhyam) {
    bgClasses = "bg-gradient-to-r from-rose-50/95 via-rose-100/40 to-orange-50/60 border-rose-300 text-rose-950 shadow-xs";
    iconHtml = "⚠️";
    iconBg = "bg-rose-100 border-rose-300 text-rose-700";
    pillHtml = `<span class="text-[11px] px-2.5 py-0.5 rounded-full font-bold bg-rose-100 text-rose-900 border border-rose-300 animate-pulse">⚠️ ${t('bannerTabooAuspicious')}</span>`;
    btnClasses = "bg-rose-700 hover:bg-rose-800 text-white";
  } else if (isKartari) {
    bgClasses = "bg-gradient-to-r from-amber-50/95 via-orange-50/50 to-amber-100/40 border-amber-300 text-amber-950 shadow-xs";
    iconHtml = "🔥";
    iconBg = "bg-amber-100 border-amber-300 text-amber-800";
    pillHtml = `<span class="text-[11px] px-2.5 py-0.5 rounded-full font-bold bg-amber-100 text-amber-900 border border-amber-300">🔥 ${t('bannerTabooConstruction')}</span>`;
    btnClasses = "bg-amber-700 hover:bg-amber-800 text-white";
  }

  container.className = `vedic-card p-4 transition-all border rounded-2xl ${bgClasses}`;

  container.innerHTML = `
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
      <div class="flex items-start sm:items-center gap-3">
        <div class="w-10 h-10 rounded-full ${iconBg} border flex items-center justify-center text-xl font-bold shrink-0 shadow-2xs">
          ${iconHtml}
        </div>
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <h4 class="text-base font-extrabold font-serif-te tracking-wide">${mk.status_title}</h4>
            ${pillHtml}
          </div>
          <p class="text-xs opacity-90 mt-0.5 leading-relaxed">${mk.status_description}</p>
        </div>
      </div>
      <button 
        id="openMoudhyamModalBtn" 
        class="shrink-0 px-4 py-2 rounded-xl text-xs font-bold ${btnClasses} shadow-md transition-all active:scale-95 flex items-center gap-1.5 cursor-pointer"
      >
        <span>📅</span> <span>${t('bannerAnnualScheduleBtn')}</span>
      </button>
    </div>
  `;

  const btn = document.getElementById('openMoudhyamModalBtn');
  if (btn) {
    btn.addEventListener('click', () => openAnnualMoudhyamModal());
  }
}

async function openAnnualMoudhyamModal() {
  const modal = document.getElementById('annualMoudhyamModal');
  const body = document.getElementById('modalMoudhyamBody');
  if (!modal || !body) return;

  modal.classList.remove('hidden');

  if (STATE.annualMoudhyamData && STATE.annualMoudhyamData.year === STATE.year && STATE.annualMoudhyamData.timezone === STATE.tz) {
    renderAnnualMoudhyamModalBody(STATE.annualMoudhyamData);
    return;
  }

  body.innerHTML = `
    <div class="flex flex-col items-center justify-center py-10">
      <div class="w-8 h-8 border-4 border-amber-600 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-xs text-amber-900 mt-2 font-medium">${t('moudhyamLoading')}</p>
    </div>
  `;

  try {
    const res = await fetch(`/api/v1/panchangam/moudhyam-kartari?year=${STATE.year}&language=${STATE.lang}&tz=${encodeURIComponent(STATE.tz)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    STATE.annualMoudhyamData = data;
    renderAnnualMoudhyamModalBody(data);
  } catch (err) {
    console.error('Error fetching annual moudhyam data:', err);
    body.innerHTML = `<div class="text-rose-700 p-4 text-center">${t('moudhyamError')}</div>`;
  }
}

function renderAnnualMoudhyamModalBody(data) {
  const body = document.getElementById('modalMoudhyamBody');
  if (!body) return;

  const ks = data.kartari_schedule;
  const ml = data.moudhyam_schedule;
  const taboos = data.shastric_taboos;
  const tz = data.timezone || STATE.tz || 'Asia/Kolkata';

  const locationBanner = `
    <div class="bg-gradient-to-r from-amber-50 to-orange-50/60 border border-amber-200/90 rounded-xl p-3 flex flex-wrap items-center justify-between gap-2 shadow-2xs">
      <div class="flex items-center gap-2">
        <span class="text-lg">📍</span>
        <div>
          <span class="font-bold text-amber-950 text-sm font-serif-te">${STATE.city}, ${STATE.country}</span>
          <span class="text-[11px] text-stone-600 font-mono ml-2 bg-white/80 px-2 py-0.5 rounded border border-amber-200">${t('timezoneLabel')}: ${tz}</span>
        </div>
      </div>
      <div class="text-[11px] text-amber-900 bg-amber-100/70 border border-amber-300/80 px-2.5 py-1 rounded-lg font-medium">
        ${t('moudhyamTimesSubtitle')}
      </div>
    </div>
  `;

  // 1. Kartari Milestones Table
  const kartariRows = ks.milestones.map(m => `
    <tr class="border-b border-amber-100 hover:bg-amber-50/50 transition">
      <td class="p-2.5 font-bold text-amber-950 font-serif-te whitespace-nowrap">${m.phase}</td>
      <td class="p-2.5 text-xs text-stone-700">${m.transit}</td>
      <td class="p-2.5 text-xs font-mono font-bold text-amber-900 whitespace-nowrap">${m.timing}</td>
      <td class="p-2.5 text-xs text-stone-600">${m.importance}</td>
    </tr>
  `).join('');

  // 2. Moudhyam Cards
  const moudhyamCards = ml.map(m => `
    <div class="p-4 bg-gradient-to-br from-rose-50/70 to-amber-50/40 rounded-xl border border-rose-200 space-y-2">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-1">
        <h5 class="font-extrabold text-rose-950 text-sm sm:text-base font-serif-te flex items-center gap-1.5">
          <span>⚠️</span> <span>${m.type}</span>
        </h5>
        <span class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-rose-100 text-rose-900 border border-rose-300">
          ${t('durationLabel')}: ~${m.duration_days} ${t('daysLabel')}
        </span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
        <div class="p-2.5 bg-white rounded-lg border border-rose-200/80 shadow-2xs">
          <span class="text-stone-500 block text-[11px] font-medium">${t('moudhyamStartLabel')}</span>
          <span class="font-mono font-bold text-rose-900 text-xs sm:text-sm">${m.start}</span>
        </div>
        <div class="p-2.5 bg-white rounded-lg border border-emerald-200/80 shadow-2xs">
          <span class="text-stone-500 block text-[11px] font-medium">${t('moudhyamEndLabel')}</span>
          <span class="font-mono font-bold text-emerald-900 text-xs sm:text-sm">${m.end}</span>
        </div>
      </div>
      <div class="text-xs text-stone-700 bg-white/70 p-2.5 rounded-lg border border-rose-100 flex flex-col sm:flex-row justify-between gap-1">
        <span><strong>${t('vardhakyaLabel')}</strong> ${m.vardhakya_start}</span>
        <span><strong>${t('balyaLabel')}</strong> ${m.balya_end}</span>
      </div>
      <p class="text-xs text-rose-800 font-semibold pt-1">
        <strong>${t('prohibitionLabel')}</strong> ${m.prohibition}
      </p>
    </div>
  `).join('');

  // 3. Taboos List
  const taboosMoudhyamList = (taboos.moudhyam_taboos || []).map(t => `<li class="flex items-center gap-1.5"><span class="text-rose-600 font-bold">✕</span> <span>${t}</span></li>`).join('');
  const taboosKartariList = (taboos.kartari_taboos || []).map(t => `<li class="flex items-center gap-1.5"><span class="text-amber-700 font-bold">✕</span> <span>${t}</span></li>`).join('');
  const permittedList = (taboos.permitted_karmas || []).map(p => `<li class="flex items-center gap-1.5"><span class="text-emerald-600 font-bold">✓</span> <span>${p}</span></li>`).join('');

  body.innerHTML = `
    ${locationBanner}

    <!-- Section A: Kartari (Agni Kartari) -->
    <div class="space-y-3">
      <div class="flex items-center gap-2 border-b border-amber-200 pb-2">
        <span class="text-2xl">🔥</span>
        <div>
          <h4 class="font-bold text-amber-950 text-base font-serif-te">${ks.title}</h4>
          <p class="text-xs text-stone-600">${ks.description}</p>
        </div>
      </div>
      <div class="overflow-x-auto rounded-xl border border-amber-200 bg-white shadow-xs">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="bg-amber-100/80 text-amber-950 font-bold border-b border-amber-200">
              <th class="p-2.5">${t('thPhase')}</th>
              <th class="p-2.5">${t('thTransit')}</th>
              <th class="p-2.5">${t('thTiming')}</th>
              <th class="p-2.5">${t('thSignificance')}</th>
            </tr>
          </thead>
          <tbody>
            ${kartariRows}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Section B: Moudhyam Periods -->
    <div class="space-y-3 pt-2">
      <div class="flex items-center gap-2 border-b border-rose-200 pb-2">
        <span class="text-2xl">🪐</span>
        <div>
          <h4 class="font-bold text-rose-950 text-base font-serif-te">${t('moudhyamSectionTitle')}</h4>
          <p class="text-xs text-stone-600">${t('moudhyamSectionSubtitle')}</p>
        </div>
      </div>
      <div class="space-y-3">
        ${moudhyamCards}
      </div>
    </div>

    <!-- Section C: Dharmashastric Guidelines -->
    <div class="pt-2">
      <h4 class="font-bold text-stone-900 text-sm font-serif-te mb-2.5 flex items-center gap-1.5">
        <span>📜</span> <span>${t('shastraDecisionsTitle')}</span>
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
        <div class="p-3 bg-rose-50/70 border border-rose-200 rounded-xl space-y-1.5">
          <span class="font-bold text-rose-900 block border-b border-rose-200 pb-1">${t('moudhyamTaboosTitle')}</span>
          <ul class="space-y-1 text-stone-700">${taboosMoudhyamList}</ul>
        </div>
        <div class="p-3 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1.5">
          <span class="font-bold text-amber-900 block border-b border-amber-200 pb-1">${t('kartariTaboosTitle')}</span>
          <ul class="space-y-1 text-stone-700">${taboosKartariList}</ul>
        </div>
        <div class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5">
          <span class="font-bold text-emerald-900 block border-b border-emerald-200 pb-1">${t('permittedKarmasTitle')}</span>
          <ul class="space-y-1 text-stone-700">${permittedList}</ul>
        </div>
      </div>
    </div>
  `;
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
        item.className = "city-search-item px-4 py-2.5 hover:bg-amber-50 cursor-pointer border-b border-stone-100 last:border-0 flex justify-between items-center text-sm";
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
  STATE.dailyData = null;
  STATE.monthlyData = null;
  STATE.sankalpaData = null;
  STATE.annualMoudhyamData = null; // Invalidate cache so all tabs re-fetch for new city
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
    alert(t('gpsNotSupported'));
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
        selectCity({
          name: nearestCity.name,
          country: nearestCity.country,
          lat: lat,
          lon: lon,
          tz: nearestCity.tz
        });
        alert(`${t('gpsSuccess')}: ${nearestCity.name}, ${nearestCity.country} (${lat.toFixed(4)}°, ${lon.toFixed(4)}°)`);
      }
    } catch (err) {
      console.error(err);
    } finally {
      btn.classList.remove('opacity-50');
    }
  }, (err) => {
    btn.classList.remove('opacity-50');
    alert(`${t('gpsDenied')}: ` + err.message);
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
      if (activePlanet) activePlanet.innerText = `🌙 ${t('moonTransitLabel')}: ${data.moon_rashi}`;
    } else if (curPeriod === 'monthly') {
      infoBadge.innerText = `🗓️ ${data.year} / ${String(data.month).padStart(2, '0')} (${data.solar_month})`;
      if (activePlanet) activePlanet.innerText = `☀️ ${t('solarMonthLabel')}: ${data.solar_month}`;
    } else {
      infoBadge.innerText = `🪐 ${data.samvatsara} (${data.year})`;
      if (activePlanet) activePlanet.innerText = `✨ ${t('kandadayamTableLabel')}`;
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
        miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 border border-rose-300">⚠️ ${t('chandrashtamaMiniBadge')}</span>`;
      } else {
        const bgCls = score >= 75 ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : 'bg-amber-100 text-amber-800 border-amber-300';
        miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded ${bgCls}">${score}%</span>`;
      }
    } else if (STATE.activeRashiPeriod === 'monthly') {
      miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300">${score}%</span>`;
    } else {
      // Yearly: show aadhayam / vyayam
      const kd = item.kandadayam;
      miniBadge = `<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300 font-mono">${t('incomeShort')}:${kd.aadhayam} ${t('expenseShort')}:${kd.vyayam}</span>`;
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
            <div class="font-bold text-sm text-rose-900 uppercase tracking-wide">${t('chandrashtamaAlertTitle')}</div>
            <div class="text-xs text-rose-800 mt-0.5 leading-relaxed">
              ${t('chandrashtamaAlertDesc')}
            </div>
          </div>
        </div>
      `;
    }

    // Daily Status Badges & Lucky info
    transitAlertHtml += `
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5">
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">${t('moonHouseLabel')}</div>
          <div class="text-xs font-extrabold text-amber-950 mt-0.5">${item.moon_house} ${t('houseSuffix')}</div>
          <div class="text-[10px] text-amber-700 mt-0.5">${item.chandra_bala_status.split('(')[0]}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">${t('tarabalamLabel')}</div>
          <div class="text-xs font-extrabold text-amber-950 mt-0.5">${item.tara_bala_name.split('(')[0]}</div>
          <div class="text-[10px] ${item.is_tara_bala_good ? 'text-emerald-600' : 'text-rose-600'} font-bold mt-0.5">${item.is_tara_bala_good ? t('taraGood') : t('taraCaution')}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">${t('luckyNumberLabel')}</div>
          <div class="text-lg font-extrabold text-amber-800 leading-tight mt-0.5 font-mono">${item.lucky_number}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase">${t('luckyColorLabel')}</div>
          <div class="text-xs font-bold text-stone-800 mt-1">${item.lucky_color}</div>
        </div>
        <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs text-center col-span-2 sm:col-span-1">
          <div class="text-[10px] text-stone-500 font-bold uppercase">${t('luckyDirectionLabel')}</div>
          <div class="text-xs font-bold text-stone-800 mt-1">${item.lucky_direction}</div>
        </div>
      </div>
    `;
  } else if (curPeriod === 'monthly') {
    // Monthly Transit Info
    transitAlertHtml = `
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="p-3.5 bg-white rounded-xl border border-amber-200 shadow-xs">
          <div class="text-[10px] text-stone-500 font-bold uppercase">${t('sunTransitLabel')}</div>
          <div class="text-sm font-extrabold text-amber-950 mt-1">${item.sun_house} ${t('placeSuffix')}</div>
          <div class="text-xs text-amber-800 mt-0.5">${item.is_sun_favorable ? t('sunFavorable') : t('sunUnfavorable')}</div>
        </div>
        <div class="p-3.5 bg-white rounded-xl border border-amber-200 shadow-xs sm:col-span-2">
          <div class="text-[10px] text-stone-500 font-bold uppercase mb-1">${t('monthlyHighlightsLabel')}</div>
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
            <div class="text-[11px] font-bold text-emerald-800 uppercase tracking-wide">💰 ${t('kdAdayam')} (Income)</div>
            <div class="text-3xl font-extrabold text-emerald-950 font-mono mt-1">${kd.aadhayam}</div>
            <div class="text-[10px] text-emerald-700 mt-1">${t('maxWord')}: 14</div>
          </div>
          <div class="p-4 rounded-2xl bg-gradient-to-br from-amber-50 to-orange-100/60 border border-amber-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-amber-800 uppercase tracking-wide">💸 ${t('kdVyayam')} (Expenditure)</div>
            <div class="text-3xl font-extrabold text-amber-950 font-mono mt-1">${kd.vyayam}</div>
            <div class="text-[10px] text-amber-700 mt-1">${t('maxWord')}: 14</div>
          </div>
          <div class="p-4 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-100/60 border border-blue-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-blue-800 uppercase tracking-wide">👑 ${t('kdRajapujyam')} (Honor)</div>
            <div class="text-3xl font-extrabold text-blue-950 font-mono mt-1">${kd.rajapujyam}</div>
            <div class="text-[10px] text-blue-700 mt-1">${t('maxWord')}: 8</div>
          </div>
          <div class="p-4 rounded-2xl bg-gradient-to-br from-rose-50 to-rose-100/60 border border-rose-300 shadow-xs text-center">
            <div class="text-[11px] font-bold text-rose-800 uppercase tracking-wide">🛡️ ${t('kdAvamanam')} (Disgrace)</div>
            <div class="text-3xl font-extrabold text-rose-950 font-mono mt-1">${kd.avamanam}</div>
            <div class="text-[10px] text-rose-700 mt-1">${t('maxWord')}: 8</div>
          </div>
        </div>

        <!-- Kandadayam Insight Pill Bar -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs flex items-center gap-2.5">
            <span class="text-xl">📊</span>
            <div>
              <div class="text-[10px] text-stone-500 font-bold uppercase">${t('financialAnalysisLabel')}</div>
              <div class="text-xs font-extrabold text-amber-900">${kd.finance_status}</div>
            </div>
          </div>
          <div class="p-3 bg-white rounded-xl border border-amber-200 shadow-xs flex items-center gap-2.5">
            <span class="text-xl">🎖️</span>
            <div>
              <div class="text-[10px] text-stone-500 font-bold uppercase">${t('socialAnalysisLabel')}</div>
              <div class="text-xs font-extrabold text-amber-900">${kd.social_status}</div>
            </div>
          </div>
        </div>

        <!-- Planetary Positions -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200 text-center">
            <div class="text-[10px] text-stone-500 font-bold uppercase">${t('guruBalamLabel')} (${item.jupiter_house} ${t('placeSuffix')})</div>
            <div class="text-xs font-bold text-amber-950 mt-0.5">${item.has_guru_balam ? t('guruBalamYes') : t('guruBalamNo')}</div>
          </div>
          <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200 text-center">
            <div class="text-[10px] text-stone-500 font-bold uppercase">${t('shaniGocharaLabel')} (${item.saturn_house} ${t('placeSuffix')})</div>
            <div class="text-xs font-bold text-amber-950 mt-0.5">${item.sade_sati_status}</div>
          </div>
          <div class="p-3 bg-amber-50/80 rounded-xl border border-amber-200 text-center">
            <div class="text-[10px] text-stone-500 font-bold uppercase">${t('rahuKetuTransitLabel')}</div>
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
          <h4>${t('rashiOverviewTitle')}</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.general}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">💼</span>
          <h4>${t('rashiCareerTitle')}</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.career}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">💰</span>
          <h4>${t('rashiFinanceTitle')}</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.finance}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">🩺</span>
          <h4>${t('rashiHealthTitle')}</h4>
        </div>
        <p class="text-xs text-stone-700 leading-relaxed font-normal">${preds.health}</p>
      </div>

      <div class="vedic-card p-4.5 bg-white border border-amber-200/90 shadow-xs md:col-span-2">
        <div class="flex items-center gap-2 text-amber-900 font-bold text-sm mb-2">
          <span class="text-xl">👨‍👩‍👧</span>
          <h4>${t('rashiFamilyTitle')}</h4>
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
        <h4 class="font-extrabold text-sm text-amber-200 uppercase tracking-wide">${t('rashiRemediesTitle')}</h4>
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
              <span>${t('lordLabel')} <strong class="text-amber-900">${rashi.lord}</strong></span>
              <span>•</span>
              <span>${t('elementLabel')} <strong class="text-amber-900">${rashi.element}</strong></span>
            </div>
          </div>
        </div>

        <!-- Score Meter -->
        <div class="flex flex-col items-end sm:items-center">
          <div class="text-[10px] text-stone-500 font-bold uppercase tracking-wider mb-1">${t('compatibilityScoreLabel')}</div>
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
      badge.innerText = t('suryaSystemBadge');
      badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300";
    }
    if (keelakaCallout) keelakaCallout.classList.remove('hidden');
  } else {
    if (btnDrik) btnDrik.className = "px-4 py-2 rounded-xl text-xs font-bold text-white bg-amber-600 shadow transition-all";
    if (btnSurya) btnSurya.className = "px-4 py-2 rounded-xl text-xs font-bold text-amber-200 hover:text-white transition-all";
    if (badge) {
      badge.innerText = t('drikSystemBadge');
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
        <td class="p-3 font-semibold text-amber-950 whitespace-nowrap font-serif-te">${m.samvatsara_name || m.samvatsara_name_telugu}</td>
        <td class="p-3 font-bold text-amber-900">${m.full_display_name}</td>
        <td class="p-3 text-center whitespace-nowrap">${typeBadge}</td>
        <td class="p-3 text-center font-mono font-bold text-stone-800">${m.sankranti_count}</td>
        <td class="p-3 font-mono text-stone-700 whitespace-nowrap">${m.start_date} ${t('toDateSpan')} ${m.end_date}</td>
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
                  <span class="text-emerald-800">${t('kdAdayam')}: <span class="font-mono text-sm">${item.aadhayam}</span>/14</span>
                  <span class="text-rose-800">${t('kdVyayam')}: <span class="font-mono text-sm">${item.vyayam}</span>/14</span>
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
                  <span class="text-purple-800">${t('kdRajapujyam')}: <span class="font-mono text-sm">${item.rajapujyam}</span>/8</span>
                  <span class="text-orange-800">${t('kdAvamanam')}: <span class="font-mono text-sm">${item.avamanam}</span>/8</span>
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
    if (!status) return '';
    const s = status.toLowerCase();
    if (s.includes("ఉత్తమం") || s.includes("ಉತ್ತಮ") || s.includes("உத்தமம்") || s.includes("उत्तम") || s.includes("excellent") || s.includes("auspicious")) {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-emerald-100 text-emerald-900 border border-emerald-300">${status}</span>`;
    } else if (s.includes("అనుకూలం") || s.includes("ಅನುಕೂಲ") || s.includes("அனுகூலம்") || s.includes("अनुकूल") || s.includes("good") || s.includes("favorable")) {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-sky-100 text-sky-900 border border-sky-300">${status}</span>`;
    } else if (s.includes("మధ్యమం") || s.includes("ಮಧ್ಯಮ") || s.includes("மத்திமம்") || s.includes("मध्यम") || s.includes("moderate")) {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-amber-100 text-amber-900 border border-amber-300">${status}</span>`;
    } else {
      return `<span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-rose-100 text-rose-900 border border-rose-300">${status}</span>`;
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
            ${item.name} ${t('nakshatraWord')}
          </h3>
        </div>
        <p class="text-xs font-semibold text-stone-600 mt-1 flex items-center gap-1">
          <span>${t('spreadRashisPadasLabel')}</span>
          <span class="font-bold text-amber-900">${item.rashi_names.join(', ')}</span>
        </p>
      </div>

      <!-- Composite Annual Status -->
      <div class="bg-white px-4 py-2.5 rounded-xl border border-amber-200 shadow-sm text-left md:text-right">
        <div class="text-[10px] text-stone-500 font-bold uppercase tracking-wider">${t('annualCompositeStatusLabel')}</div>
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
              <h4 class="font-extrabold text-amber-950 text-sm">${t('trimester1Title')}</h4>
              <p class="text-[11px] font-semibold text-stone-500">${t('trimester1Months')}</p>
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
          ${t('trimester1MaxLimit')}
        </div>
      </div>

      <!-- Trimester 2 -->
      <div class="vedic-card p-5 bg-white border-2 border-orange-300 flex flex-col justify-between shadow-sm hover:shadow-md transition">
        <div>
          <div class="flex items-center justify-between border-b border-orange-100 pb-2 mb-3">
            <div>
              <h4 class="font-extrabold text-amber-950 text-sm">${t('trimester2Title')}</h4>
              <p class="text-[11px] font-semibold text-stone-500">${t('trimester2Months')}</p>
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
          ${t('trimester2MaxLimit')}
        </div>
      </div>

      <!-- Trimester 3 -->
      <div class="vedic-card p-5 bg-white border-2 border-emerald-300 flex flex-col justify-between shadow-sm hover:shadow-md transition">
        <div>
          <div class="flex items-center justify-between border-b border-emerald-100 pb-2 mb-3">
            <div>
              <h4 class="font-extrabold text-amber-950 text-sm">${t('trimester3Title')}</h4>
              <p class="text-[11px] font-semibold text-stone-500">${t('trimester3Months')}</p>
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
          ${t('trimester3MaxLimit')}
        </div>
      </div>
    </div>

    <!-- Overall Summary Callout -->
    <div class="p-4 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-950 font-medium leading-relaxed flex items-start gap-2.5">
      <span class="text-xl">💡</span>
      <div>
        <strong class="font-bold">${t('annualSummaryAdviceLabel')}</strong> ${item.overall_status}
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
    tbody.innerHTML = `<tr><td colspan="7" class="p-6 text-center text-stone-400 italic">${t('noNakshatraFound')}</td></tr>`;
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
