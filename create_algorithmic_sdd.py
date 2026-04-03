import os
import datetime
from fpdf import FPDF

class ProjectPDF(FPDF):
    def header(self):
        self.set_draw_color(225, 235, 245)
        self.set_line_width(0.2)
        for i in range(0, 215, 8):
            self.line(i, 0, i, 297)
        for i in range(0, 300, 8):
            self.line(0, i, 210, i)
            
        self.set_draw_color(190, 210, 225)
        self.set_line_width(1.5)
        for offset in range(0, 60, 12):
            self.line(150 + offset, 297, 210 + offset, 250)
            
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(15, 35, 75)
            self.cell(0, 10, 'Explainable Clickbait Detection System - Algorithmic SDD', 0, 0, 'R')
            self.ln(12)

    def footer(self):
        self.set_y(-25)
        logo_path = r'c:\GUIDO\Crowd detection\GUIDO logo.png'
        if os.path.exists(logo_path):
            self.image(logo_path, x=(210 - 20) / 2, y=self.get_y(), w=20)
            
        self.set_y(-15)
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(15, 35, 75)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

    def cover_page(self):
        self.add_page()
        logo_path = r'c:\GUIDO\Crowd detection\GUIDO logo.png'
        if os.path.exists(logo_path):
            self.image(logo_path, x=25, y=40, w=160)
        else:
            self.set_font('Helvetica', 'B', 50)
            self.set_y(60)
            self.set_text_color(10, 30, 80)
            self.cell(0, 20, 'GUIDO', 0, 1, 'C')

        self.set_y(120)
        self.set_fill_color(30, 50, 90)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 16)
        
        text = 'Guides your way to a perfect project'
        width = self.get_string_width(text) + 20
        self.set_x((210 - width) / 2)
        self.cell(width, 14, text, 0, 1, 'C', fill=True)

        self.ln(30)
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(15, 35, 75)
        self.multi_cell(0, 12, 'Algorithmic Software Design Document (SDD)', 0, 'C')

        self.ln(5)
        self.set_font('Helvetica', '', 16)
        self.set_text_color(60, 80, 100)
        self.cell(0, 10, 'Explainable Clickbait Detection System', 0, 1, 'C')

        self.ln(30)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(15, 35, 75)
        self.cell(0, 10, 'Data Flow & Core Logic Specification', 0, 1, 'C')
        self.set_font('Helvetica', '', 11)
        self.cell(0, 10, f'Generated on: {datetime.date.today().strftime("%B %d, %Y")}', 0, 1, 'C')

    def h1(self, title):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(15, 35, 75)
        self.ln(10)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(30, 50, 90)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def h2(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(25, 65, 125)
        self.ln(6)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(1)
        
    def h3(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(25, 65, 125)
        self.ln(4)
        self.cell(0, 10, title, 0, 1, 'L')

    def p(self, text):
        self.set_font('Helvetica', '', 12)
        self.set_text_color(15, 20, 35)
        self.multi_cell(0, 7, text)
        self.ln(3)

    def li(self, text):
        self.set_font('Helvetica', '', 12)
        self.set_text_color(15, 20, 35)
        self.set_x(15)
        self.cell(5, 7, chr(149), 0, 0)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def code_block(self, lines):
        self.set_font('Courier', '', 10)
        self.set_fill_color(240, 245, 250)
        self.set_text_color(0, 0, 0)
        self.ln(2)
        for line in lines:
            self.cell(0, 6, line, border=0, ln=1, fill=True)
        self.ln(4)

pdf = ProjectPDF()
pdf.set_auto_page_break(auto=True, margin=30)
pdf.cover_page()
pdf.add_page()

content = [
    {"type": "h1", "text": "1. System Overview"},
    {"type": "p", "text": "The Explainable Clickbait Detection System operates as a high-performance distributed pipeline across the browser extension client and the Python FastAPI inference server. This Algorithmic Software Design Document (SDD) outlines the sequential execution pathways, algorithmic logic, and data structures enabling real-time detection and explainable artificial intelligence (XAI)."},

    {"type": "h1", "text": "2. Algorithm: Client-Side DOM Scraping & Batching"},
    {"type": "h2", "text": "2.1 Objective"},
    {"type": "p", "text": "Extract logical headlines from raw HTML pages efficiently without overwhelming browser memory or triggering infinite loops on dynamic infinite-scroll sites."},
    {"type": "h2", "text": "2.2 Pseudocode"},
    {"type": "code_block", "lines": [
        "function scanHeadlines():",
        "  headings = querySelectorAll('h1, h2, h3, h4, [role=\"heading\"] a')",
        "  batch = []",
        "  elements = []",
        "  ",
        "  for heading in headings:",
        "    text = trim(heading.innerText)",
        "    if words(text) > 3 AND NOT heading.attribute.processed:",
        "      batch.push(text)",
        "      elements.push(heading)",
        "      heading.attribute.processed = True",
        "",
        "  if batch is empty: return",
        "  ",
        "  for chunk in chunk_array(batch, size=20):",
        "    sendMessageToBackground(action=\"PREDICT\", data=chunk)"
    ]},
    {"type": "p", "text": "The 20-text batching metric guarantees massive arrays of DOM headings from dense sites (e.g., Reddit, Twitter) process efficiently without destroying CPU/thread allocation."},

    {"type": "h1", "text": "3. Algorithm: Message Passing & CSP Proxy Bypass"},
    {"type": "h2", "text": "3.1 Objective"},
    {"type": "p", "text": "Bypass rigid Content Security Policies (CSPs) embedded in target websites preventing raw JavaScript from communicating directly with the localhost server."},
    {"type": "h2", "text": "3.2 Pseudocode"},
    {"type": "code_block", "lines": [
        "// In background.js (Service Worker)",
        "listenForMessage(request, sender, sendResponse):",
        "  if request.type == \"PREDICT\":",
        "    try:",
        "      response = fetch(\"http://localhost:8000/predict\", ",
        "                       body=request.headlines, ",
        "                       method=\"POST\")",
        "      sendResponse(success=True, data=response.json())",
        "    except Error:",
        "      sendResponse(success=False)"
    ]},

    {"type": "h1", "text": "4. Algorithm: DistilBERT Model Inference Pipeline"},
    {"type": "h2", "text": "4.1 Objective"},
    {"type": "p", "text": "Parse incoming string payloads through the Transformer model, yielding probability outputs determining clickbait classification. Handled natively within FastAPI."},
    {"type": "h2", "text": "4.2 Pseudocode"},
    {"type": "code_block", "lines": [
        "function predict_batch(headlines_list):",
        "  results = []",
        "  for text in headlines_list:",
        "    // 1. Subword Tokenization mapping text to integers",
        "    tokens = tokenizer(text, truncation=True, padding=True)",
        "    ",
        "    // 2. Transformer Forward Pass (No Gradient Calc for Speed)",
        "    with torch.no_grad():",
        "      logits = DistilBertModel(tokens)",
        "    ",
        "    // 3. Normalizing output tensor values to probabilities",
        "    probabilities = softmax(logits, dimension=1)",
        "    class_prob_0 = probabilities[0] // Non-Clickbait",
        "    class_prob_1 = probabilities[1] // Clickbait",
        "    ",
        "    // 4. Binary Classification Threshold",
        "    isClickbait = (class_prob_1 > class_prob_0)",
        "    confidence = max(class_prob_0, class_prob_1)",
        "    ",
        "    results.append({",
        "      headline: text,",
        "      isClickbait: isClickbait,",
        "      confidence: confidence",
        "    })",
        "  return results"
    ]},

    {"type": "h1", "text": "5. Algorithm: LIME Explainability Generation (XAI)"},
    {"type": "h2", "text": "5.1 Objective"},
    {"type": "p", "text": "Isolate the contribution of specific grammatical tokens within a text string to the ultimate model categorization (Clickbait vs Non-Clickbait)."},
    {"type": "h2", "text": "5.2 Pseudocode"},
    {"type": "code_block", "lines": [
        "function generate_lime_explanation(headline):",
        "  // 1. Initialize Explainer instance targeting text classification",
        "  explainer = LimeTextExplainer(classes=[\"Safe\", \"Clickbait\"])",
        "  ",
        "  // 2. Perturb input and query the DistilBERT inference loop 100 times",
        "  //    by systematically blanking out random words and measuring ",
        "  //    probabilistic drop-off variance.",
        "  explanation = explainer.explain_instance(",
        "     text_instance=headline,",
        "     classifier_fn=predict_probabilities,",
        "     num_features=6, // Max core words to analyze",
        "     num_samples=100 // Iterations",
        "  )",
        "  ",
        "  // 3. Return a correlated array of Tuples [(\"word\", weight_float)]",
        "  return explanation.as_list()"
    ]},

    {"type": "h1", "text": "6. Algorithm: Dynamic DOM Rendering & Data Visualization"},
    {"type": "h2", "text": "6.1 Objective"},
    {"type": "p", "text": "Map the LIME XAI array physically into the browser standard HTML tooltip structure, matching numeric intensity to RGBA background color gradients alongside rendering the advanced glass tooltip."},
    {"type": "h2", "text": "6.2 Pseudocode"},
    {"type": "code_block", "lines": [
        "function render_XAI_Hover(explanation_array, headline_string):",
        "  scores_map = convert_array_to_map(explanation_array)",
        "  html_output = \"<div>\"",
        "  ",
        "  for word in split_string(headline_string):",
        "    score = scores_map[word] DEFAULT 0.0",
        "    alpha = MIN( ABS(score) * 15.0, 1.0 )",
        "    ",
        "    if score > 0:",
        "      // Correlates to Clickbait Prediction (Red color scale)",
        "      color = rgba(220, 38, 38, alpha)",
        "    else if score < 0:",
        "      // Correlates to Safe Prediction (Green color scale)",
        "      color = rgba(22, 163, 74, alpha)",
        "    else:",
        "      color = transparent",
        "",
        "    html_output += \"<span style='background: {color}'>\" + word + \"</span>\"",
        "    ",
        "  html_output += \"</div>\"",
        "  tooltipDOM.innerHTML = html_output"
    ]},

    {"type": "h1", "text": "7. Algorithm: Storage Mapping & Digital Wellbeing Pipeline"},
    {"type": "h2", "text": "7.1 Objective"},
    {"type": "p", "text": "Maintain cross-session historical domain tracking to populate the Chart.js 'Wall of Shame' and instantly render CSS blur filters across matched DOM headline elements."},
    {"type": "h2", "text": "7.2 Pseudocode"},
    {"type": "code_block", "lines": [
        "// Executed per batch processing loop (post-inference)",
        "function handle_analytics_and_blur(predictions):",
        "  domain = window.location.hostname",
        "  stats = chrome.storage.local.get(\"DomainStats\")",
        "  ",
        "  for prediction in predictions:",
        "    stats[domain].total_count += 1",
        "    if prediction.isClickbait:",
        "      stats[domain].clickbait_count += 1",
        "      ",
        "      // Apply Wellbeing Blur if activated in Settings",
        "      if USER_SETTINGS.blur_enabled:",
        "        prediction.DOM_Element.classList.add(\"blur-filter-heavy\")",
        "        ",
        "  chrome.storage.local.set({\"DomainStats\": stats})"
    ]}
]

for item in content:
    if item['type'] == 'h1':
        pdf.h1(item['text'])
    elif item['type'] == 'h2':
        pdf.h2(item['text'])
    elif item['type'] == 'h3':
        pdf.h3(item['text'])
    elif item['type'] == 'p':
        pdf.p(item['text'])
    elif item['type'] == 'li':
        pdf.li(item['text'])
    elif item['type'] == 'code_block':
        pdf.code_block(item['lines'])

pdf.output('Algorithmic_SDD_GUIDO_Theme.pdf')
print("Successfully generated Algorithmic SDD PDF.")
