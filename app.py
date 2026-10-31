from flask import Flask, render_template, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Загрузка базы героев
with open('heroes.json', 'r', encoding='utf-8') as f:
    HEROES = json.load(f)

# Загрузка инцидентов
with open('incidents.json', 'r', encoding='utf-8') as f:
    INCIDENTS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', 
                           total=len(HEROES),
                           active=sum(1 for h in HEROES if h['status'] == 'ACTIVE'),
                           incidents=INCIDENTS[:3])

@app.route('/roster')
def roster():
    return render_template('roster.html', heroes=HEROES)

@app.route('/dossier/<agent_id>')
def dossier(agent_id):
    hero = next((h for h in HEROES if h['id'] == agent_id), None)
    if not hero:
        return "Агент не найден", 404
    return render_template('dossier.html', hero=hero)

@app.route('/full-dossier/<agent_id>')
def full_dossier(agent_id):
    # Проверяем, существует ли файл досье
    dossier_path = os.path.join('dossiers', f'{agent_id}.html')
    if not os.path.exists(dossier_path):
        return "Досье не найдено", 404
    return send_from_directory('dossiers', f'{agent_id}.html')

@app.route('/incidents')
def incidents():
    return render_template('incidents.html', incidents=INCIDENTS)

@app.route('/incident/<incident_id>')
def incident_detail(incident_id):
    incident = next((i for i in INCIDENTS if i['id'] == incident_id), None)
    if not incident:
        return "Инцидент не найден", 404
    return render_template('incident_detail.html', incident=incident)

@app.route('/api/heroes')
def api_heroes():
    return jsonify(HEROES)

@app.route('/api/incidents')
def api_incidents():
    return jsonify(INCIDENTS)

if __name__ == '__main__':
    # В продакшене используем порт из переменной окружения
    port = int(os.environ.get('PORT', 5000))
    # debug=False обязателен для production
    app.run(host='0.0.0.0', port=port, debug=False)