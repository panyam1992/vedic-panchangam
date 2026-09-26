/**
 * 'సిద్ధాంత కర్త / జ్యోతిష్య బ్రహ్మ' (Siddhanta Karta / Jyotishya Brahma) Chat Controller.
 */

let chatMessagesHistory = [];

function initChat(kundaliData) {
  const chatBody = document.getElementById("chatBody");
  const quickChips = document.getElementById("quickChips");
  
  if (!chatBody) return;

  chatBody.innerHTML = "";
  chatMessagesHistory = [];

  const name = kundaliData.input.name || "జాతుకుడు";
  const gender = (kundaliData.input.gender || "male").toLowerCase();
  const isFemale = (gender === "female");

  // Welcome message from Siddhanta Karta
  const welcomeText = `నమస్కారం **${isFemale ? 'శ్రీమతి/కుమారి ' : 'శ్రీ '}${name}** గారూ! 🙏
నేను మీ **సిద్ధాంత కర్త / జ్యోతిష్య బ్రహ్మ**ను. 

మీ జన్మ లగ్నమైన **${kundaliData.lagna.rashi_name_te}** మరియు జన్మ నక్షత్రమైన **${kundaliData.panchangam.nakshatra}** ఆధారంగా మీ జాతక చక్రం మరియు ప్రస్తుత గ్రహ సంచారం (గోచారం) పరిశీలించాను. 

మీ జీవితం, వివాహం, ఉద్యోగం, ఆరోగ్యం లేదా శని గోచార పరిహారాలకు సంబంధించి ఏవైనా సందేహాలు ఉంటే నన్ను అడగవచ్చు. శాస్త్ర ప్రమాణాలతో మీకు మార్గదర్శనం చేస్తాను.`;

  appendChatMessage("assistant", welcomeText, [
    "బృహత్ పరాశర హోరా శాస్త్రం",
    "ఉత్తర కాలామృతం",
    "జాతక చంద్రిక"
  ]);

  // Render Context-aware Quick Chips based on Gender
  if (quickChips) {
    quickChips.innerHTML = "";
    const chips = isFemale ? [
      "నా వివాహ యోగం & మాంగల్య బలం ఎలా ఉంది?",
      "నా ఉద్యోగం / కెరీర్ లో ఎదుగుదల ఎప్పుడు ఉంటుంది?",
      "నాకు శని గోచార ప్రభావం ఎలా ఉంది? పరిహారాలు ఏమిటి?",
      "సంతాన యోగం & కుటుంబ సౌఖ్యం ఎలా ఉన్నాయి?",
      "నా ఆరోగ్యం, మనఃప్రశాంతత కోసం ఏ పరిహారం చేయాలి?"
    ] : [
      "నా ఉద్యోగం / వ్యాపారంలో పురోగతి ఎప్పుడు?",
      "సంతాన యోగం & ప్రాప్తి ఎప్పుడు? పరిహారాలు ఏమిటి?",
      "వివాహం ఎప్పుడు జరిగే అవకాశం ఉంది? అనుకూల సమయం?",
      "ఏలినాటి శని / అష్టమ శని ప్రభావం ఎలా ఉంది?",
      "నా జాతకంలో ప్రధాన రాజయోగాలు ఏమిటి?",
      "ఆర్థిక స్థిరత్వం కోసం ఏ దైవారాధన చేయాలి?"
    ];

    chips.forEach(text => {
      const chip = document.createElement("button");
      chip.className = "quick-chip";
      chip.textContent = text;
      chip.onclick = () => {
        document.getElementById("chatInput").value = text;
        sendMessage();
      };
      quickChips.appendChild(chip);
    });
  }
}

function appendChatMessage(role, text, citations = [], remedies = []) {
  const chatBody = document.getElementById("chatBody");
  if (!chatBody) return;

  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-msg ${role}`;

  // Format basic markdown (bold, list)
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "<br><br>")
    .replace(/\n/g, "<br>");

  let html = `<div>${formatted}</div>`;

  // Citations
  if (citations && citations.length > 0) {
    html += `<div style="margin-top: 10px; border-top: 1px dashed #E5DEC9; padding-top: 6px;">`;
    html += `<small style="color: #6C5D53; font-weight: 600; display: block; margin-bottom: 4px;">📜 గ్రంథ ప్రమాణాలు:</small>`;
    citations.forEach(c => {
      html += `<span class="citation-badge">${c}</span>`;
    });
    html += `</div>`;
  }

  // Remedies Box
  if (remedies && remedies.length > 0) {
    html += `<div class="remedy-box">`;
    html += `<strong>🌿 శాస్త్రోక్త వైదిక పరిహారాలు:</strong><ul style="margin-left: 18px; margin-top: 4px;">`;
    remedies.forEach(r => {
      html += `<li>${r}</li>`;
    });
    html += `</ul></div>`;
  }

  msgDiv.innerHTML = html;
  chatBody.appendChild(msgDiv);
  chatBody.scrollTop = chatBody.scrollHeight;

  chatMessagesHistory.push({ role, content: text });
}

async function sendMessage() {
  const input = document.getElementById("chatInput");
  const sendBtn = document.getElementById("btnSend");
  if (!input) return;

  const question = input.value.trim();
  if (!question) return;

  // Append user message
  appendChatMessage("user", question);
  input.value = "";
  input.focus();

  // Show loading indicator
  const chatBody = document.getElementById("chatBody");
  const loadingDiv = document.createElement("div");
  loadingDiv.id = "chatLoadingIndicator";
  loadingDiv.className = "chat-msg assistant";
  loadingDiv.innerHTML = `<em>జ్యోతిష్య బ్రహ్మ మీ కుండలిని మరియు శాస్త్ర గ్రంథాలను శోధిస్తున్నారు...</em> <span class="spinner" style="margin-left: 8px; vertical-align: middle;"></span>`;
  chatBody.appendChild(loadingDiv);
  chatBody.scrollTop = chatBody.scrollHeight;

  if (sendBtn) sendBtn.disabled = true;

  try {
    const resp = await fetch("/api/v1/chat/consult", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        kundali_data: window.currentKundaliData || {},
        chat_history: chatMessagesHistory.slice(-6),
        language: "telugu"
      })
    });

    let data;
    try {
      data = await resp.json();
    } catch (parseErr) {
      const errText = await resp.text();
      console.error("Non-JSON error from server:", errText);
      throw new Error(`సర్వర్ లోపం (${resp.status}): ${errText.slice(0, 100)}`);
    }

    loadingDiv.remove();

    if (resp.ok) {
      appendChatMessage("assistant", data.answer, data.shastra_citations, data.remedies);
    } else {
      appendChatMessage("assistant", `క్షమించండి, సమాధానం పొందడంలో సమస్య ఏర్పడింది: ${data.detail || "Error"}`);
    }
  } catch (err) {
    console.error("Chat consult error:", err);
    if (document.getElementById("chatLoadingIndicator")) {
      document.getElementById("chatLoadingIndicator").remove();
    }
    appendChatMessage("assistant", `సమస్య ఏర్పడింది (${err.message || 'నెట్‌వర్క్ సమస్య'}). దయచేసి మళ్ళీ ప్రయత్నించండి.`);
  } finally {
    if (sendBtn) sendBtn.disabled = false;
  }
}

