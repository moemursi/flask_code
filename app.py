from flask import Flask,jsonify,request,url_for, redirect ,session

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'verysecretkey'


@app.route('/')
def index():
    session.pop('name', None)
    return '<h1> Hello buddy  </h1>'

@app.route('/home', methods=['POST','GET'], defaults={'name': 'Default'})
@app.route('/home/<string:name>',methods=['POST','GET'])
def home(name):
    session['name'] = name
    return "hello {}".format(name)

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

        return '''<form method="POST" action="/theform">
                    <input type="text" name="name">
                    <input type="text" name="location">
                    <input type="submit" value="Submit">
                </form>'''
    else:
        name = request.form['name']
        # location = request.form['location']
        # return ' Hello {} . You are from {} , submitted successfully'.format(name,location)
        return redirect(url_for('home',name=name))


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


if __name__ == "__main__":
    app.run()





















