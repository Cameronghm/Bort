from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sq

app = Flask(__name__)

@app.route('/datainput', methods=['POST', 'GET'])
def datainput():
    if request.method == 'POST':
        pass

    else:
        return 'Hiya'

if __name__ == '__main__':
    app.run(debug=True)
