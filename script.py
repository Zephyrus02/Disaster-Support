import mysql.connector
import geocoder
from flask import Flask, request, render_template
app = Flask(__name__)


# home function to call homepage for user
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/involve")
def involve():
    return render_template('involve.html')

@app.route("/donate")
def donate():
    return render_template('involve.html')


# guide function to call guidelines page for user
@app.route("/guide", methods=['GET', 'POST'])
def guide():
    calamity = request.form['disaster']
    fw = request.form['FW']
    med = request.form['Med']
    note = request.form['note']

    g = geocoder.ip("me")
    my_add = g.address
    ADD = my_add

    conn = mysql.connector.connect(host="localhost", user="root", password="root", port='3306', database="provider")
    cursor = conn.cursor()

    # Preparing SQL query to INSERT a record into the database.
    insert_stmt = (
    "INSERT INTO alert(Address, Calamity, FW, Med, Note)"
    "VALUES (%s, %s, %s, %s, %s)"
    )
    data = (ADD, calamity, fw, med, note)

    try:
    # Executing the SQL command
        cursor.execute(insert_stmt, data)
        
        # Commit your changes in the database
        conn.commit()

    except:
    # Rolling back in case of error
        conn.rollback()

    print("Data inserted")

    # Closing the connection
    conn.close()

    return render_template('guide.html', Calamity=calamity, FW=fw, Med=med, Note=note)


# display function to call the display page for the responsible authorities
@app.route("/display", methods=['GET', 'POST'])
def display():

    db = mysql.connector.connect(host="localhost", user="root", password="root", port='3306', database="provider")
    my_cursor = db.cursor()

    my_cursor.execute("Select * from alert")
    reqres = my_cursor.fetchall()

    my_cursor.execute("SELECT * FROM resources")
    totres = my_cursor.fetchall()

    avlres = 0
    for i in totres:
        if i[0] == reqres[0][0]:
          avlres = i  

    return render_template('display.html', Res = reqres, Avl = avlres)

app.run(debug=True)
