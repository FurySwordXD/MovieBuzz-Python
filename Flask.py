from flask import Flask, render_template, request, session, jsonify
import pymysql.cursors
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    connection = pymysql.connect(host='localhost',user='root', password='', db='moviebuzz')
    cursor = connection.cursor()

    sql = 'SELECT * FROM movies'
    rows = cursor.execute(sql)

    result = cursor.fetchall()
    
    data = []
    for i in result:
        data.append({
            "name": i[0], "genre": i[1], "language": i[2], "img_src": i[3], "duration": i[5]
        })
    print(data)
    
    return render_template("Home.html",movieData=data,moviesCount=len(data))

@app.route("/movie/<movieName>")
def movie(movieName):
    connection = pymysql.connect(host='localhost',user='root', password='', db='moviebuzz')
    cursor = connection.cursor()

    sql = 'SELECT * FROM movies WHERE name = %s'
    data = (movieName)
    cursor.execute(sql, data)

    result = cursor.fetchone()
    
    data = { "name": result[0], "genre": result[1], "language": result[2], "img_src": result[3], "duration": result[5], "big_img_src": result[4] }
    print(data)
    
    return render_template("Movie.html",data=data)

#AJAX
@app.route("/login", methods=['POST'])
def login():
    connection = pymysql.connect(host='localhost',user='root', password='', db='moviebuzz')
    cursor = connection.cursor()
    
    email = request.form['Email']
    pwd = request.form['Password']

    sql = 'SELECT * FROM users WHERE email = %s AND password = %s'
    data = (email, pwd)
    rows = cursor.execute(sql, data)
    result = cursor.fetchone()

    connection.close()

    if rows == 1:
        return jsonify({
            "flag": 1,
            "message": "Logged in Successfully!",
            "email": result[0],
            "name": result[2],
            "age": result[3]
        })
    else:
        return jsonify({
                "flag": 0,
                "message": "Login unsuccessful..."
            })

@app.route("/register", methods=['POST'])
def register():
    connection = pymysql.connect(host='localhost',user='root', password='', db='moviebuzz')
    cursor = connection.cursor()

    email = request.form['Email']
    pwd = request.form['Password']
    age = request.form['Age']
    name = request.form['Name']

    sql = "INSERT INTO users(email, password, name, age) VALUES(%s, %s, %s, %s)"
    data = (email, pwd, name, age)
    result = cursor.execute(sql, data)

    connection.commit()

    if result == 1:
        return jsonify({
            "flag": 1,
            "message": "Registered successfully!",
            "email": email,
            "name": name,
            "age": age
        })
    else:
        return jsonify({
            "flag": 0,
            "message": "Registration unsuccessful!"
        })

@app.route("/edit", methods=['POST'])
def edit():
    connection = pymysql.connect(host='localhost',user='root', password='', db='moviebuzz')
    cursor = connection.cursor()

    email = request.form['Email']
    pwd = request.form['Password']
    age = request.form['Age']
    name = request.form['Name']

    if pwd == "":
        sql = "UPDATE users SET Name = %s, Age = %s WHERE Email = %s"
        data = (name, age, email)
    else:
        sql = "UPDATE users SET Name = %s, Age = %s, Password = %s WHERE Email = %s"
        data = (name, age, pwd, email)
    result = cursor.execute(sql, data)

    connection.commit()

    if result == 1:
        return jsonify({
            "flag": 1,
            "message": "Edit successfully!",
            "email": email,
            "name": name,
            "age": age
        })
    else:
        return jsonify({
            "flag": 0,
            "message": "Edit unsuccessful!"
        })

@app.route("/logout", methods=['GET'])
def logout():
    return jsonify({
            "flag": 1,
            "message": "Logged out!",
            "email": "",
            "name": "",
            "age": ""
        })

if __name__ == "__main__":
    app.run(debug=True)