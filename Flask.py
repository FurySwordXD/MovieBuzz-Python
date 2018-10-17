from flask import Flask, render_template, request, session, jsonify
import pymysql.cursors
app = Flask(__name__)

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
            "name": i[0], "genre": i[1], "language": i[2], "img_src": i[3], "duration": i[4]
        })
    print(data)
    
    return render_template("Home.html",movieData=data,moviesCount=len(data))

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

if __name__ == "__main__":
    app.run(debug=True)