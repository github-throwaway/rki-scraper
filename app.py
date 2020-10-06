import flask
from flask import request, url_for, render_template, redirect
from script import scrape

app = flask.Flask(__name__)

@app.route('/',methods=['GET','POST'])
def my_maps():
    countries=scrape()
    mapbox_access_token = 'pk.eyJ1Ijoia2lhb3JhIiwiYSI6ImNrZnUwNmgwbzBtYnYzM3Q4bzNwZWZhejQifQ.JUoC9n6NAqDkgYutOOSDjw'

    return render_template('index.html', mapbox_access_token=mapbox_access_token
    ,countries=countries
    )

if __name__ == '__main__':
    app.run(debug=True)