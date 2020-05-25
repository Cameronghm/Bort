from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sq

app = Flask(__name__)

class data():
    def __init__(self, savingsperyear, retirementlength, savinglength, incomegrowth,
                 retirementcosts, investmentgrowth, currentsavings, statepension, male):
        self.savingsperyear = savingsperyear
        self.retirementlength = retirementlength
        self.savinglength = savinglength
        self.incomegrowth = incomegrowth
        self.retirementcosts = retirementcosts
        self.investmentgrowth = investmentgrowth
        self.currentsavings = currentsavings
        self.statepension = statepension
        self.male = male

@app.route('/datainput', methods=['POST', 'GET'])
def datainput():
    if request.method == 'POST':
        f = request.form
        savingsperyear = f['savingsperyear']
        retirementlength = f['retirementlength']
        savinglength = f['savinglength']
        incomegrowth = f['incomegrowth']
        retirementcosts = f['retirementcosts']
        investmentgrowth = f['investmentgrowth']
        currentsavings = f['currentsavings']
        statepension = f['statepension']
        male = f['gender']
        print(statepension)
        if statepension=='yes':
            statepension = True
        else:
            statepension = False
        if male=='male':
            male = True
        else:
            male = False
        userinput = data(savingsperyear, retirementlength, savinglength, incomegrowth, retirementcosts, investmentgrowth,
             currentsavings, statepension, male)
        return render_template("datainput.html")

    else:
        return render_template("datainput.html")

if __name__ == '__main__':
    app.run(debug=True)
