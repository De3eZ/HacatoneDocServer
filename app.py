from flask import Flask, request, jsonify
from flask import SQLAclchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hacatone.db'
db = SQLAclchemy(app)

@app.route('/api/mobile/registration', methods=['POST'])
def registration():
    data = request.get_json()

    name = data['name']
    surname = data['surname']
    patronymic = data['patronymic']
    login = data['login']
    password = data['password']

    #todo добавить получение токена из бд
    token=''
    refreshToken=''

    return jsonify({'token': token, 'refreshToken' : refreshToken})

@app.route('/api/mobile/auth/', methods=['POST'])
def auth():
    data = request.get_json()

    login = data['login']
    password = data['password']

    #todo Логика следующая: проверяет корректность данных по таблице 1.2, если всё верно возвращает  объект Если введен неправильный пароль кидает ошибку

    result = True

    return result

@app.route('/api/mobile/refresh', methods=['GET','POST'])
def refresh():
    data = request.get_json()

    refreshToken = data['refreshToken']

    #todo Ищет этот токен в таблице 1.3, если находит выполняется следующая логика:
    #     Запись в таблице с этим refreshToken модифицируется и token обновляется на новый сгенерируемый и возвращается объект с новыми данными

    # todo добавить получение токена из бд
    token = ''
    refreshToken = ''

    return jsonify({'token': token, 'refreshToken' : refreshToken})

if __name__ == "__main__":
    app.run(debug=True, port=8000)