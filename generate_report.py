import os
import datetime
from fpdf import FPDF

class ProjectPDF(FPDF):
    def header(self):
        # --- Grid Background Theme ---
        # Very light blue grid lines (softened for better text contrast)
        self.set_draw_color(225, 235, 245)
        self.set_line_width(0.2)
        # Draw vertical lines
        for i in range(0, 215, 8):
            self.line(i, 0, i, 297)
        # Draw horizontal lines
        for i in range(0, 300, 8):
            self.line(0, i, 210, i)
            
        # Draw diagonal styling strokes on bottom right
        self.set_draw_color(190, 210, 225)
        self.set_line_width(1.5)
        for offset in range(0, 60, 12):
            self.line(150 + offset, 297, 210 + offset, 250)
            
        # Standard header for internal pages
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(15, 35, 75)
            self.cell(0, 10, 'Explainable Clickbait Detection System', 0, 0, 'R')
            self.ln(12)

    def footer(self):
        # Small Watermark of the logo on each page
        self.set_y(-25)
        logo_path = r'C:\GUIDO\Explainable Clickbait Detection\GUIDO logo.png'
        if os.path.exists(logo_path):
            # Centered small watermark at the bottom of the page
            self.image(logo_path, x=(210 - 20) / 2, y=self.get_y(), w=20)
            
        self.set_y(-15)
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(15, 35, 75)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

    def cover_page(self):
        self.add_page()
        
        # Add big GUIDO logo in the center top
        logo_path = r'C:\GUIDO\Explainable Clickbait Detection\GUIDO logo.png'
        if os.path.exists(logo_path):
            self.image(logo_path, x=25, y=40, w=160)
        else:
            self.set_font('Helvetica', 'B', 50)
            self.set_y(60)
            self.set_text_color(10, 30, 80)
            self.cell(0, 20, 'GUIDO', 0, 1, 'C')

        # Add the themed dark blue box from the reference
        self.set_y(120)
        self.set_fill_color(30, 50, 90) # Dark Navy Blue
        self.set_text_color(255, 255, 255) # White Text
        self.set_font('Helvetica', 'B', 16)
        
        

        self.ln(30)
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(15, 35, 75) # Deep blue
        self.multi_cell(0, 12, 'Explainable Clickbait Detection System', 0, 'C')

        self.ln(5)
        self.set_font('Helvetica', '', 16)
        self.set_text_color(60, 80, 100)
        self.cell(0, 10, 'AI-Powered Detection with LIME Interpretability', 0, 1, 'C')

        self.ln(30)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(15, 35, 75)
        self.cell(0, 10, 'Project Documentation & Setup Guide', 0, 1, 'C')
        self.set_font('Helvetica', '', 11)
        self.cell(0, 10, f'Generated on: {datetime.date.today().strftime("%B %d, %Y")}', 0, 1, 'C')

    def h1(self, title):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(15, 35, 75)
        self.ln(10)
        self.cell(0, 10, title, 0, 1, 'L')
        # Decorative Line
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
        self.set_text_color(15, 20, 35) # Near-black for maximum contrast
        self.multi_cell(0, 7, text)
        self.ln(3)

    def li(self, text):
        self.set_font('Helvetica', '', 12)
        self.set_text_color(15, 20, 35)
        self.set_x(15)
        self.cell(5, 7, chr(149), 0, 0)
        self.multi_cell(0, 7, text)
        self.ln(2)

# Application Logic
pdf = ProjectPDF()
pdf.set_auto_page_break(auto=True, margin=30)
pdf.cover_page()
pdf.add_page()

content = [
    {"type": "h1", "text": "1. Introduction"},
    {"type": "p", "text": "Clickbait headlines are designed to attract attention and encourage visitors to click on a link to a particular web page. While effective for marketing, they often lead to low-quality content, misinformation, and a frustrating user experience. Traditional detection methods rely on manual flagging or simple keyword matching, which are easily bypassed."},
    {"type": "p", "text": "The Explainable Clickbait Detection System is a complete full-stack Artificial Intelligence solution that uses Natural Language Processing (NLP) to detect deceptive headlines automatically in real-time."},
    {"type": "p", "text": "The primary features of this system include:"},
    {"type": "li", "text": "Accurate Local AI Detection utilizing a fine-tuned DistilBERT transformer running entirely on your local machine."},
    {"type": "li", "text": "Explainable AI (XAI) integration using LIME (Local Interpretable Model-Agnostic Explanations) to show exactly which words caused the AI to flag the title."},
    {"type": "li", "text": "Privacy-Focused architecture because all inference runs locally via FastAPI without uploading browsing habits to the cloud."},
    {"type": "li", "text": "A Chrome Extension with a premium Liquid Glass aesthetic designed to scan, highlight, and explain clickbait dynamically on any website."},
    {"type": "li", "text": "A Web Application hosting a manual testing portal featuring real-time Chart.js visual analytics and domain tracking."},
    {"type": "li", "text": "A Wall of Shame Dashboard and Digital Wellbeing blur modes to protect users from deceptive psychological tactics."},

    {"type": "h1", "text": "2. Objectives of the Project"},
    {"type": "p", "text": "The main objectives of this project are:"},
    {"type": "li", "text": "To develop a highly accurate AI model capable of distinguishing clickbait from legitimate news."},
    {"type": "li", "text": "To provide transparency by integrating explainability so users understand why the model made a specific prediction."},
    {"type": "li", "text": "To process everything locally, guaranteeing user privacy while scanning their browsing history."},
    {"type": "li", "text": "To create a seamless browser extension that works directly on standard news portals and search engines."},
    {"type": "li", "text": "To track analytics and present them via simple, intuitive interfaces mapping deceptive behaviors."},

    {"type": "h1", "text": "3. Real-World Applications"},
    {"type": "p", "text": "This framework offers substantial utility beyond generic academic testing. Real-world applications include:"},
    {"type": "li", "text": "News filtering systems eliminating low-effort content from user feeds."},
    {"type": "li", "text": "Social media monitoring for combating click-fraud and sensationalism."},
    {"type": "li", "text": "Digital wellbeing tools mitigating psychological exhaustion caused by manipulative phraseology."},
    {"type": "li", "text": "Journalism credibility analysis, establishing automated trust scores based on semantic integrity."},

    {"type": "h1", "text": "4. Technology Stack"},
    {"type": "h2", "text": "4.1 Python, FastAPI & PyTorch"},
    {"type": "p", "text": "Python is the primary language running the backend intelligence. PyTorch is the machine learning framework running the tensors, and FastAPI acts as the ultra-fast asynchronous REST API interface fielding extension requests."},

    {"type": "h2", "text": "4.2 DistilBERT Transformer"},
    {"type": "p", "text": "A highly refined, smaller version of BERT (Bidirectional Encoder Representations from Transformers). DistilBERT offers up to 60% faster inference while retaining 97% of BERT's natural language understanding. The model is specifically fine-tuned on clickbait datasets."},

    {"type": "h2", "text": "4.3 LIME (Explainable AI)"},
    {"type": "p", "text": "Local Interpretable Model-Agnostic Explanations (LIME) mathematically perturbs the input sentence and evaluates how the DistilBERT probabilities shift. It constructs a visual heatmap highlighting which specific words pushed the prediction towards Clickbait or Safe."},

    {"type": "h2", "text": "4.4 Browser Extension API (Manifest V3)"},
    {"type": "p", "text": "Using raw Javascript, CSS, and HTML under Chrome's Manifest V3 architecture. Background service workers proxy the local API requests to bypass strict site Content Security Policies (CSP), while content scripts dynamically manipulate DOM header elements."},

    {"type": "h2", "text": "4.5 Web UI & Chart.js"},
    {"type": "p", "text": "The standalone testing portal is built with raw stylized CSS glassmorphism, completely devoid of complex frontend frameworks for maximum performance. Chart.js is utilized for compiling raw JSON statistics into beautiful interactive graphs."},

    {"type": "h1", "text": "5. System Architecture"},
    {"type": "p", "text": "The architecture pipelines the NLP task across multiple detached components:"},
    {"type": "li", "text": "Data Initialization Module (Fine-Tuning Script)"},
    {"type": "li", "text": "Inference Endpoint (FastAPI Server)"},
    {"type": "li", "text": "Explainability Engine (LIME Interpreter)"},
    {"type": "li", "text": "Web Client Portal (Input Web App)"},
    {"type": "li", "text": "Browser Injection (Chrome Extension)"},
    {"type": "p", "text": "The system works by extracting headlines dynamically from webpages and sending them to a local FastAPI server, where the fine-tuned DistilBERT model executes classification. The LIME module instantly generates localized explanations based on the tensor probabilities, and the structured verdict is returned asynchronously to the browser extension for real-time DOM visualization."},
    {"type": "p", "text": "This modular pipeline ensures that the machine-learning execution is completely physically isolated from the web-rendering thread, preventing freezing and ensuring optimal multi-core utilization."},

    {"type": "h1", "text": "6. Installation & Prerequisites"},
    {"type": "p", "text": "To initialize the framework, it is required to use a Python version 3.8+ capable environment."},
    {"type": "li", "text": "1. Clone/Download the project framework folder."},
    {"type": "li", "text": "2. Create a virtual environment: python -m venv .venv"},
    {"type": "li", "text": "3. Activate it: .\.venv\Scripts\activate"},
    {"type": "li", "text": "4. Install modules: pip install -r requirements.txt"},
    
    {"type": "h1", "text": "7. Model Training & Backend Execution"},
    {"type": "h2", "text": "7.1 Training the Local DistilBERT Model"},
    {"type": "p", "text": "Prior to execution, the local weights must be trained. Ensure 'clickbait_data.csv' is saved containing standard 'headline' and 'label' columns inside the model directory."},
    {"type": "p", "text": "Execute: python model/train.py"},
    {"type": "p", "text": "The script handles dataset splitting, tokenization, multi-epoch processing via hardware acceleration, performance metric evaluations, and final exporting to the /local_model folder."},
    {"type": "h2", "text": "7.2 Starting the FastAPI Server"},
    {"type": "p", "text": "Once weights generate successfully, launch the REST inference endpoint."},
    {"type": "p", "text": "Execute: uvicorn backend.app:app --host 0.0.0.0 --port 8000"},
    {"type": "p", "text": "The system automatically parses the raw safetensors into memory alongside the LIME explainer setup."},

    {"type": "h1", "text": "8. Advanced Extension Integrations"},
    {"type": "p", "text": "The Chrome extension dynamically parses heading elements (H1, H2, class='title', etc.) currently loaded in the viewport array. It batches queries to the localhost:8000 pipeline in chunks of 20 to prevent pipeline stalling and renders color-coded verdict outlines (Red/Green)."},
    {"type": "h3", "text": "Wall of Shame Dashboard"},
    {"type": "p", "text": "The platform utilizes chrome.storage.local to map statistical domains historically. Tracking which corporate entities output the highest ratio of deceptive titles globally against the baseline testing average, visualized in localized interactive graphs."},
    {"type": "h3", "text": "Digital Wellbeing Mode"},
    {"type": "p", "text": "A CSS blur filter that actively censors identified clickbait terminology until physically hovered. Designed specifically to remove the psychological stress of deceptive FOMO (Fear Of Missing Out) tactics deployed structurally."},

    {"type": "h1", "text": "9. VIVA QUESTIONS AND ANSWERS"},
    
    {"type": "h2", "text": "PART 1: AI MODEL AND ARCHITECTURE"},
    {"type": "h3", "text": "Q1: Why did you choose DistilBERT over standard BERT or basic Logistic Regression?"},
    {"type": "p", "text": "Logistic regression struggles with deep contextual associations in modern deceptive sentences. Standard BERT is highly accurate but computationally massive. DistilBERT presents the perfect middle-ground: shrinking the parameter size by 40% and accelerating inference by 60%, allowing it to execute instantly on local CPUs continuously for browser plugins."},
    
    {"type": "h3", "text": "Q2: How does LIME (Explainable AI) function mathematically in your application?"},
    {"type": "p", "text": "LIME operates by isolating the headline prediction, generating hundreds of perturbed random versions of the text (removing words randomly), and submitting them backward into the DistilBERT inference engine. By correlating which removed words drastically dropped the Clickbait probability, LIME maps out the exact linguistic importance of individual terms."},

    {"type": "h3", "text": "Q3: Why run the model entirely locally? Why not use an external Cloud API?"},
    {"type": "p", "text": "If a browser extension parses and uploads every single headline a user renders across their entire internet browsing history to a central cloud server, it represents a massive invasion of privacy. Running processing locally on port 8000 ensures maximum security, zero ongoing server expenditure, and sub-millisecond network latency."},

    {"type": "h3", "text": "Q4: How does the Chrome extension bypass standard Content Security Policies (CSP)?"},
    {"type": "p", "text": "Modern browsers block injected Content Scripts from making raw fetch requests to arbitrary IP ports (like localhost). To bypass this, the Content Script forwards a messaging payload to the internal Background Service Worker (background.js). The Service Worker acts as an invisible proxy with elevated permissions, executing the API fetch and delivering the transparent output backward to the DOM rendering loop."},

    {"type": "h2", "text": "PART 2: DEVELOPMENT AND ANALYTICS"},
    {"type": "h3", "text": "Q5: How did you mitigate visual clutter if the extension flags multiple headlines?"},
    {"type": "p", "text": "Instead of immediately rendering massive LIME explanation boxes everywhere, the system utilizes 'Hover-to-Explain' delays. It simply outlines the specific item in Green or Red. Full visual context and heatmaps only render following a confirmed 800-millisecond hover interaction."},

    {"type": "h3", "text": "Q6: What is the purpose of the Wall of Shame feature?"},
    {"type": "p", "text": "It serves as a longitudinal data collection mechanic storing specific website domains mapped against the volume of clickbait generated. This provides users numerical leverage dynamically mapping untrustworthy organizations systematically utilizing deception."},

    {"type": "h3", "text": "Q7: What is Digital Wellbeing blur?"},
    {"type": "p", "text": "It actively applies a CSS variable blur to any detected clickbait headline matching the target criteria. The psychological trigger of clickbait works upon peripheral visual engagement. By blurring it out entirely, users are unburdened from the cognitive load of ignoring manipulative phraseology."},

    {"type": "h3", "text": "Q8: What are the primary system limitations?"},
    {"type": "p", "text": "The framework cannot detect image-based clickbait (misleading thumbnails without text). It also holds a limited understanding of extreme sarcasm or modern internet slang not inherently parsed inside the localized datasets. Consequently, performance depends heavily on dataset quality, and edge cases may produce false positives for highly emotional but legitimate headlines."},
    
    {"type": "h3", "text": "Q9: How can this system be structurally improved in future scoped versions?"},
    {"type": "p", "text": "Future development cycles could improve overall dataset sizes to guarantee better generalized accuracy. The model could also be customized specifically for domain-specific news sub-sectors (like finance or gaming). Finally, we could optimize raw inference parsing for extremely low-end systems and refine UI responsiveness and dashboard visualization clarity."},

    {"type": "h3", "text": "Q10: What is Clickbait in NLP terms?"},
    {"type": "p", "text": "Clickbait is a form of misleading textual content that uses exaggerated, emotional, or curiosity-driven language to attract user attention. In NLP, it is treated as a binary text classification problem, where input text is classified as clickbait or non-clickbait based on learned linguistic patterns."},

    {"type": "h3", "text": "Q11: What is Tokenization and why is it important?"},
    {"type": "p", "text": "Tokenization is the process of converting raw text into smaller units (tokens), such as words or subwords. In DistilBERT, subword tokenization is used to handle unknown or rare words efficiently. It is essential because machine learning models require numerical representation and cannot process raw text directly."},

    {"type": "h3", "text": "Q12: What is the role of the attention mechanism in DistilBERT?"},
    {"type": "p", "text": "The attention mechanism helps the model focus on important words in a sentence by assigning specific weights to each token. This allows the model to understand context dynamically and relationships between words, vastly improving global classification accuracy."},

    {"type": "h3", "text": "Q13: What is the exact difference between BERT and DistilBERT?"},
    {"type": "p", "text": "DistilBERT is a mathematically compressed version of BERT via knowledge distillation. It contains fewer parameters, making it significantly faster and lighter while retaining roughly 97% of the original performance. It is extremely suitable for real-time edge applications like browser extensions."},

    {"type": "h3", "text": "Q14: What is overfitting and how did you avoid it?"},
    {"type": "p", "text": "Overfitting occurs when an AI model performs exceptionally well on its specific training data but fails to generalize to unseen real-world data. It was avoided by using techniques like explicit dataset validation splits, hyperparameter tuning, and limiting total training epochs."},

    {"type": "h3", "text": "Q15: Why is FastAPI used instead of Flask?"},
    {"type": "p", "text": "FastAPI is fundamentally faster at runtime execution and inherently supports asynchronous operations. This makes it far more suitable for handling dozens of simultaneous real-time classification requests fired from a busy DOM browser extension without blocking."},

    {"type": "h3", "text": "Q16: What exactly is 'inference' in your system?"},
    {"type": "p", "text": "Inference is the live procedural phase outlining the process of utilizing the mathematically trained model to make immediate predictions on brand-new, unseen input data (headlines) in real-time."},

    {"type": "h3", "text": "Q17: What is the specific role of Chart.js in your project setup?"},
    {"type": "p", "text": "Chart.js is leveraged inside the centralized web dashboard to visualize aggregated JSON analytics - such as clickbait frequency, domain tracking over time, and user interaction patterns - in an interactive, highly visual format."},

    {"type": "h3", "text": "Q18: What is CSP (Content Security Policy) regarding your extension?"},
    {"type": "p", "text": "CSP is an ingrained browser security mechanism that restricts where loaded scripts can fetch arbitrary data. In this project, CSP restrictions directly from websites are bypassed safely by utilizing an invisible background service worker to explicitly handle API fetch operations."},

    {"type": "h3", "text": "Q19: What type of machine learning is used in this model?"},
    {"type": "p", "text": "The system formally relies on Supervised Learning architectures, where the model adjusts parameters based explicitly on pre-labeled target data mapping definitions of clickbait versus entirely non-clickbait features."}
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

pdf.output('Final_Report_GUIDO_Theme.pdf')
print("Extensive themed PDF report 'Final_Report_GUIDO_Theme.pdf' successfully generated.")
