from flask import Flask,jsonify,request,url_for, redirect ,session,render_template,g
import sqlite3


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'verysecretkey'


#connect to db
def connect_db():
    sql = sqlite3.connect('/Users/m.e/Desktop/packt/flask_study/data.db')
    sql.row_factory = sqlite3.Row  #return dictionary instead of tuples
    return sql

#call db
def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3_db'):
        g.sqlite3_db.close()




@app.route('/')
def index():
    session.pop('name', None)
    return '<h1> Hello buddy  </h1>'

@app.route('/home', methods=['POST','GET'], defaults={'name': 'Default'})
@app.route('/home/<string:name>',methods=['POST','GET'])
def home(name):
    session['name'] = name
    # return "hello {}".format(name)
    db = get_db()
    cur = db.execute('select id,name,location from users')
    results = cur.fetchall()

    return render_template('home.html',name=name,display=True,results=results)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'Not in session'
    return jsonify({
        'key': 'value',
        'listKey' : [2,3,4,5],
        'name' : name
    })

@app.route('/query')
def query():
    name =  request.args.get('name')
    location = request.args.get('location')
    return 'you are on the query page {} ,{} '.format(name,location)

# @app.route('/theform')
# def theform():
#     return '''<form method="POST" action="/process">
#                 <input type="text" name="name">
#                 <input type="text" name="location">
#                 <input type="submit" value="Submit">
#               </form>'''
@app.route('/theform',methods=['POST','GET'])
def theform():
    if request.method== 'GET':

        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        db = get_db()
        db.execute('insert into users(name,location) values (? ,?)',[name,location])
        db.commit()
        return redirect(url_for('results'))
        # return ' Hello {} . You are from {} , submitted successfully'.format(name,location)
        # return redirect(url_for('home',name=name,location=location))


@app.route('/process',methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return ' Hello {} . You are from {} , submitted successfully'.format(name,location)

@app.route('/processjson',methods=['POST'])
def processjson():
    data = request.get_json()
    print(data)
    name = data["name"]
    location = data["location"]
    email = data["email"]
    hobbies = data["hobbies"]


    return jsonify({
        'result'  : 'success',
        'name' : name,
        'location' : location,
        'email' : email,
        'hobbies' : hobbies,
    })

@app.route('/include')
def include():
    return render_template('include.html')


@app.route('/results')
def results():
    db = get_db()
    cur = db.execute('select id,name,location from users')
    results = cur.fetchall()
    return "<h1> The Id is {}  The name {}  The Lcoation {} </h1>".format(results[0]['id'],results[0]['name'],results[0]['location'])

if __name__ == "__main__":
    app.run(debug=True)





















