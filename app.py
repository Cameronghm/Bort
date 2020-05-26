from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3 as sq

app = Flask(__name__)
app.secret_key = b'\x9d\xb7\x8ftz\x853\xbag\xc5{U-\xba\x8c)'

class data():
    def __init__(self, income, savingsperyear, retirementlength, age, retirementage, incomegrowth,
                 retirementcosts, investmentgrowth, currentsavings, statepension, male, swr):
        self.income = income # Current income, mostly for comparsons sake
        self.savingsperyear = savingsperyear # How much they will save / year before they retire
        self.retirementlength = retirementlength # How long they expect to be in retirement
        self.age = age # Current age
        self.retirementage = retirementage # What age they want to retire
        self.incomegrowth = incomegrowth # How much income expected to grow / year
        self.retirementcosts = retirementcosts # expected income in retirement
        self.investmentgrowth = investmentgrowth # How much investments grow/year
        self.currentsavings = currentsavings # Amount in savings at beginning
        self.statepension = statepension # True = eligible False = not
        self.swr = swr # Safe withdrawal rate
        self.male = male # True = male False = female
    def getFinalSavings(self):
        spy = self.savingsperyear
        sl = self.retirementage - self.age
        ig = self.investmentgrowth
        cs = self.currentsavings
        final = ((spy)*(1-(((1+(ig/100))**sl)))/(1-(1+(ig/100)))) + (cs*((1+(ig/100))**sl))
        return final

@app.route('/datainput', methods=['POST', 'GET'])
def datainput():
    if request.method == 'POST':
        f = request.form
        income = f['income']
        savingsperyear = f['savingsperyear']
        retirementlength = f['retirementlength']
        age = f['age']
        retirementage = f['retirementage']
        incomegrowth = f['incomegrowth']
        retirementcosts = f['expectedincomeinretirement']
        investmentgrowth = f['investmentgrowth']
        currentsavings = f['currentsavings']
        statepension = f['statepensioneligibility']
        swr = f['safewithdrawalrate']
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
        userinput = data(income, savingsperyear, retirementlength, age, retirementage, incomegrowth, retirementcosts, investmentgrowth,
             currentsavings, statepension, male, swr)

        #session['userdata'] = userinput
        return render_template("datainput.html")

    else:
        return render_template("datainput.html")

@app.route('/faq', methods=['POST', 'GET'])
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
