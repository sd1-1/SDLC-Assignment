from flask import Flask, render_template

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



if __name__ == "__main__":
    app.run(debug=True)