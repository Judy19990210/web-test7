from flask import Flask, request, jsonify, render_template, make_response, session
from flask_cors import CORS
from flask_sslify import SSLify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import pymysql
import bcrypt
import re
import os

app = Flask(__name__)
#sslify = SSLify(app) # 将所有请求重定向到 HTTPS
talisman = Talisman(app)  #启用默认的安全策略，包括强制使用 HTTPS 和 HSTS 策略。 Enable default security policies, including mandatory HTTPS and HSTS policies.
CORS(app) #允许跨域请求 Cross-domain requests are allowed

limiter = Limiter(key_func=get_remote_address, default_limits=["200/day", "50/hour"])
limiter.init_app(app)

app.config['SESSION_COOKIE_SECURE'] = True # 设置安全的会话cookie  Set secure session cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True # 设置HTTP Only会话cookie  Set HTTP Only session cookies
app.config['SECRET_KEY'] = os.urandom(24) # 生成随机的会话密钥  Generate a random session key

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='ST19950412',
        database='security_group_10',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
@limiter.limit("5/minute")  # 限制登录请求为每分钟5次 Limit login requests to five per minute
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))  #参数化查询 Parameterized query
            user = cursor.fetchone()

            if not user:
                return jsonify(success=2, error_message="Invalid email or password")
            
            hashed_password = user['password']
            # Check if the password is already hashed
            if hashed_password.startswith('$2b$'):
                # Compare the hashed password with the plaintext password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    session['user_email'] = user['email']  #记录用户登录状态 Records the user login status
                    return jsonify(success=1) #login success
                else:
                    return jsonify(success=2, error_message="Invalid email or password")
            else:
                # The password is not hashed, return False
                return jsonify(success=3, error_message="Password is not hashed")            

    finally:
        connection.close()


@app.route('/register', methods=['POST'])
@limiter.limit("5/minute")  # 限制注册请求为每分钟5次 Limit registration requests to 5 per minute
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    password_confirm = request.json.get('password_confirm')

    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
        return jsonify(success=1, error_message="The password does not meet the format requirements.")

    if password != password_confirm:
        return jsonify(success=2, error_message="The two passwords are different. Please re-enter them.")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))   #参数化查询 Parameterized query
            user = cursor.fetchone()

            if user:
                return jsonify(success=3, error_message="The email already exists.")
            
            cursor.execute('INSERT INTO users (email, username, password) VALUES (%s, %s, %s)', ( email, username, hashed_password.decode('utf-8') )) #参数化查询 Parameterized query
            connection.commit()
            return jsonify(success=4) #alarm: registion success
        
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, ssl_context='adhoc') # 使用自签名证书启动HTTPS服务器 Start the HTTPS server using the self-signed certificate

