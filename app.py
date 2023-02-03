from flask import Flask, render_template,redirect,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/usermanagement')
def usermanagement():
    return render_template('usermanagement.html')


@app.route('/quizresults')
def quizresults():
    return render_template('quizresults.html')



@app.route('/login', methods=['POST'])
def login():

    email = request.form['useremail']
    print(email)
    return redirect("landing",code=302)



if __name__ == "__main__":
    app.run(debug=True)