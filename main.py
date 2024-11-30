import json
import time

import pyautogui
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from calculo import calcular_numeros_sugeridos
from interface import atualizar_tabuleiro, criar_tabuleiro

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Coordenadas dos números na roleta
coordenadas_numeros = {
    0: (739, 596),
    1: (758, 619),
    2: (759, 597),
    3: (759, 575),
    4: (782, 621),
    5: (780, 598),
    6: (782, 574),
    7: (803, 618),
    8: (802, 596),
    9: (802, 574),
    10: (827, 620),
    11: (825, 598),
    12: (825, 573),
    13: (849, 620),
    14: (848, 597),
    15: (848, 572),
    16: (872, 621),
    17: (869, 597),
    18: (870, 575),
    19: (893, 620),
    20: (893, 597),
    21: (891, 575),
    22: (916, 620),
    23: (916, 597),
    24: (917, 574),
    25: (938, 618),
    26: (937, 598),
    27: (937, 573),
    28: (961, 619),
    29: (959, 597),
    30: (959, 574),
    31: (982, 619),
    32: (982, 597),
    33: (983, 574),
    34: (1005, 621),
    35: (1006, 596),
    36: (1004, 575),
}


def clicar_numeros(numeros):
    """
    Clica automaticamente nos números sugeridos, movimentando o mouse para as coordenadas.
    """
    for numero in numeros:
        if numero in coordenadas_numeros:
            x, y = coordenadas_numeros[numero]
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.click()
            time.sleep(0.005)
        else:
            print(f"Coordenada para o número {numero} não encontrada.")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)


def create_tables():
    db.create_all()


# Chamada manual para inicializar o banco de dados
with app.app_context():
    create_tables()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        user_ip = request.remote_addr
        if user.ip_address is None:
            user.ip_address = user_ip
            db.session.commit()
        elif user.ip_address != user_ip:
            return "Access denied: IP mismatch.", 403
        session['user_id'] = user.id
        return redirect('/dashboard')
    return "Invalid username or password.", 401


@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    if 'user_id' not in session:
        return "Unauthorized", 401

    try:
        data = json.loads(request.data)
        historico = data.get('historico', [])
        if len(historico) != 25:
            return jsonify({"error": "Please provide exactly 25 numbers."}), 400
        sugestoes = calcular_numeros_sugeridos(historico, quantidade=20)
        return jsonify({"sugestoes": sugestoes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/click', methods=['POST'])
def click():
    if 'user_id' not in session:
        return "Unauthorized", 401

    try:
        data = json.loads(request.data)
        numeros = data.get('numeros', [])
        clicar_numeros(numeros)  # Chama a função de clique automática
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        create_tables()  # Inicializa o banco de dados
    app.run(debug=True)
