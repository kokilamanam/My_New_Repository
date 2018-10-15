import  flask
app=flask.Flask(__name__)

@app.route('/')
def hello():
    return 'hello_world!'

@app.route('/koki/<username>')
def hai(username):
    return 'hai everyone welcome %s' %username

# @app.route('/')
# def hello_world():
#    return ‘hello world’
# app.add_url_rule(‘/’, ‘hello’, hello_world)


if __name__=='__main__':
    app.run(debug=True)
print("------------------------")


