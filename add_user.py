from werkzeug.security import generate_password_hash

from main import User, app, db

# Cria o banco de dados e as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()  # Cria as tabelas do banco de dados

    # Dados do novo usuário
    username = "admin"  # Substitua pelo nome de usuário desejado
    password = "123456"  # Substitua pela senha desejada
    hashed_password = generate_password_hash(
        password, method='pbkdf2:sha256')  # Alteração aqui

    # Adiciona o novo usuário ao banco de dados
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    print("Usuário criado com sucesso!")
