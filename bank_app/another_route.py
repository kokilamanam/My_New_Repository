import  flask
app=flask.Flask(__name__)

@app.route('/')
def hello():
    return 'hello_world!'

@app.route('/koki/<username>')
def hai(username):
    return 'hai everyone welcome %s' %username


if __name__=='__main__':
    app.run(debug=True)
print("------------------------")


