from flask import Flask, request, render_template, redirect, url_for
import cohere
import fitz  # PyMuPDF
import os

app = Flask(__name__)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Function to ask a question using Cohere API
def ask_question(question, context):
    cohere_api_key = 'zboQMKIETkINYPB0Pr1rjqCd1etSu4ntOJIkskYv'
    co = cohere.Client(cohere_api_key)
    
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=f"Context: {context}\n\nQuestion: {question}\nAnswer:",
        max_tokens=50,
        temperature=0.5,
        k=0,
        stop_sequences=["\n"]
    )
    return response.generations[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Specify the path to your PDF file
    pdf_path = 'bot.pdf'
    context = extract_text_from_pdf(pdf_path)
    chat_history = []

    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            answer = ask_question(question, context)
            chat_history.append((question, answer))
            return render_template('index.html', context=context, chat_history=chat_history)

    return render_template('index.html', context=context, chat_history=chat_history)

@app.route('/landing')
def landing():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(debug=True)
