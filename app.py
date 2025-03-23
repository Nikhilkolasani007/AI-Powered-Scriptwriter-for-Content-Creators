from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
import sqlite3
import google.generativeai as genai  # Import Gemini API

app = Flask(__name__)
app.secret_key = "AIzaSyCIju1JtzOTb4UP8t8shQ3OzeLyxAPFaXM"  # Used for session management

# Configure Google Gemini API
genai.configure(api_key="AIzaSyCIju1JtzOTb4UP8t8shQ3OzeLyxAPFaXM")  # Replace with your actual API key

# Function to get available models dynamically
def get_available_model():
    try:
        models = genai.list_models()
        for model in models:
            if "gemini-1.5" in model.name and "generateContent" in model.supported_generation_methods:
                return model.name  # Use the latest Gemini 1.5 models
        return "gemini-1.5-flash"  # Fallback to Gemini 1.5 Flash if available
    except Exception as e:
        print(f"Error fetching models: {e}")
        return None


# Database Connection Function
def connect_db():
    return sqlite3.connect('database.db')

# Home Page
@app.route('/')
def home():
    return render_template('register.html')
# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        cur = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except:
            return "Username already exists. Try another."

    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # user[2] = stored hashed password
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials. Try again."

    return render_template('login.html')

# User Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])

# AI Chat Route (Added Below Dashboard)
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect('/login')

    response = None
    response = None
    selected_model = get_available_model()  # Dynamically fetch the best model
    if not selected_model:
        return "No available AI models at the moment. Try again later."

    if request.method == 'POST':
        user_input = request.form['user_input']
        try:
            model = genai.GenerativeModel(selected_model)
            response = model.generate_content(user_input).text
        except Exception as e:
            response = f"Error generating response: {e}"
    return render_template('chat.html', response=response)


# User Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
