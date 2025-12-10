from flask import Flask, request, jsonify, session, send_file
import requests
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

API_KEY = "sk-or-v1-krmhebba"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def demander_a_l_ia(conversation_historique):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5000',
        'X-Title': 'AWB chatbot'
    }
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": conversation_historique,
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code != 200:
            print(f"Erreur API: {response.status_code}")
            print(f"Message: {response.text}")
            return "Une erreur technique est survenue."

        return response.json()['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Erreur Python: {e}")
        return "Erreur de connexion."

@app.route('/')
def index():
    session.clear()
    session['historique'] = [
        {
            "role": "system", 
            "content": "Tu es l'assistant virtuel officiel d'Attijariwafa Bank. Tu es professionnel, courtois et expert en services bancaires. Tu aides les clients sur les sujets suivants : comptes bancaires, application mobile Attijari Mobile, crédits et cartes. Si une question est hors du domaine bancaire, refuse poliment de répondre."
        }
    ]
    try:
        with open('AWB_chatbot.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Fichier HTML introuvable"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    historique = session.get('historique', [])
    historique.append({"role": "user", "content": user_message})
    
    reponse_ia = demander_a_l_ia(historique)
    
    historique.append({"role": "assistant", "content": reponse_ia})
    session['historique'] = historique
    return jsonify({'reponse': reponse_ia})

@app.route('/AWB_chatbot.css')
def css():
    try:
        with open('AWB_chatbot.css', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/css'}
    except: return "", 404

@app.route('/AWB_chatbot.js')
def js():
    try:
        with open('AWB_chatbot.js', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'application/javascript'}
    except: return "", 404

@app.route('/logo.webp')
def logo():
    try:
        return send_file('logo.webp', mimetype='image/webp')
    except: return "", 404

if __name__ == '__main__':
    app.run(debug=True)