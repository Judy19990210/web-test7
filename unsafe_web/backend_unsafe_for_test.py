from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='ST19950412',
        database='security_group_10',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"  #unsafe way
            #email insert: user@example.com' OR '1'='1' -- 
            cursor.execute(query)

            print(query)

            user = cursor.fetchone()
            print(user)

            if user:  #unsafe way
                return jsonify(success=True)
            else:
                return jsonify(success=False)
    finally:
        connection.close()

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    print(f"Email: {email}, Username: {username}, Password: {password}")

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            query1 = f"SELECT * FROM users WHERE email = '{email}'" #unsafe way
            cursor.execute(query1)

            user = cursor.fetchone()

            if user:
                return jsonify(success=False)

            unsafe_query = f"INSERT INTO users (email, username, password) VALUES ('{email}', '{username}', '{password}')"   #unsafe
            cursor.execute(unsafe_query)
            
            connection.commit()

            return jsonify(success=True)
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)







