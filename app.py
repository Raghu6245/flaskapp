from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import pyperclip
import threading
import time

app = Flask(__name__)

# Set your OpenAI API key
api_key = "sk-ze3k1lRD1qZUqM_aqR4_BI_vcnwqsOsFfXvRewjsXRT3BlbkFJMVCtf1xRytzXHPRX_rlgs9pbqMNWfcBUtRhn363DUA"
client = OpenAI(api_key=api_key)

latest_question = ""
latest_answer = ""

# Function to get answers from GPT-3.5-turbo
def get_answer(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Provide at least three points for the given content: {text}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_answer', methods=['GET'])
def get_answer_route():
    global latest_answer
    return jsonify({'answer': latest_answer})

def clipboard_monitor():
    global latest_question, latest_answer
    last_paste = pyperclip.paste()
    while True:
        current_paste = pyperclip.paste()
        if current_paste != last_paste:
            last_paste = current_paste
            latest_question = current_paste
            print(f"New clipboard content detected: {current_paste}")
            # Fetch the answer based on the clipboard content
            latest_answer = get_answer(current_paste)
        time.sleep(1)  # Check every 1 second

if __name__ == '__main__':
    # Start the clipboard monitor in a separate thread
    threading.Thread(target=clipboard_monitor, daemon=True).start()
    app.run(debug=True)
