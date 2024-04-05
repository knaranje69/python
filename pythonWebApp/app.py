from flask import Flask, render_template, request

app = Flask(__name__)


# Define the routes for your web app and the corresponding functions to handle the
# request. For example, you can create a simple route that displays "Hello World!" 
# when the user visits the root URL(/)

@app.route('/')	
def index():
	return 'Hello World'

if __name__ == '__main__':
	app.run(debug=True)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/greet', method=['GET', 'POST'])
def greet():
	if request.method == 'POST':
		name = request.form['name']
		return f"Hello, {name}!"
	return render_template('greet.html')
