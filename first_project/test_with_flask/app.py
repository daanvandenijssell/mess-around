from flask import Flask, request, url_for, render_template

app = Flask(__name__)


@app.route('/index/<string:name>')
def index(name):
    return render_template('index.html', name=name)


@app.route('/<string:name>')
def return_name(name):
    # name = request.args.get('name')
    return f'Hello {name}!'


if __name__ == '__main__':
    app.run(debug=True)