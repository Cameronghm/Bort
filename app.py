from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3 as sq
import json

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
    def getResults(self):
        spy = int(self.savingsperyear)
        sl = int(self.retirementage) - int(self.age)
        ig = int(self.investmentgrowth)
        cs = int(self.currentsavings)
        swr = int(self.swr)
        
        #finalpot = money in pension bot at beginning of retirment
        final = ((spy)*(1-(((1+(ig/100))**sl)))/(1-(1+(ig/100)))) + (cs*((1+(ig/100))**sl))
        #deathpot = money in pension bot at end of retirment (death)
        deathpot = (final) * (((100-swr)/100)**sl) * (((100+ig)/100)**sl) 
        #initdraw = first year drawdown/ first year income from pulling money from pot
        initdraw = final * ((100-swr)/100)
        #finaldraw = final year drawdown/ final year's income from pot
        finaldraw = ((final) * (((100-swr)/100)**(sl-1)) * (((100+ig)/100)**(sl-1))) * ((100-swr)/100)
        
        return final, deathpot, initdraw, finaldraw

@app.route('/datainput', methods=['POST', 'GET'])
def datainput():
    if request.method == 'POST':
        f = request.form
        temp = {}
        temp['income'] = f['income']
        temp['savingsperyear'] = f['savingsperyear']
        temp['retirementlength'] = f['retirementlength']
        temp['age'] = f['age']
        temp['retirementage'] = f['retirementage']
        temp['incomegrowth'] = f['incomegrowth']
        temp['retirementcosts'] = f['expectedincomeinretirement']
        temp['investmentgrowth'] = f['investmentgrowth']
        temp['currentsavings'] = f['currentsavings']
        statepension = f['statepensioneligibility']
        temp['swr'] = f['safewithdrawalrate']
        male = f['gender']
        if statepension=='yes':
            temp['statepension'] = True
        else:
            temp['statepension'] = False
        if male=='male':
            temp['male'] = True
        else:
            temp['male'] = False
        #userinput = data(income, savingsperyear, retirementlength, age, retirementage, incomegrowth, retirementcosts, investmentgrowth,
        #     currentsavings, statepension, male, swr)
        session['temporary'] = temp
        # Figure out how to get this fucking shit to fucking work
        #session['userinput'] = jsonify(json.dumps(request))
        return redirect(url_for('results'))

    else:
        return render_template("datainput.html")

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.route('/')
def index():
    return redirect(url_for('datainput'))

@app.route('/results', methods=['GET'])
def results():
    f = session['temporary']

    income = f['income']
    savingsperyear = f['savingsperyear']
    retirementlength = f['retirementlength']
    age = f['age']
    retirementage = f['retirementage']
    incomegrowth = f['incomegrowth']
    retirementcosts = f['retirementcosts']
    investmentgrowth = f['investmentgrowth']
    currentsavings = f['currentsavings']
    statepension = f['statepension']
    swr = f['swr']
    male = f['male']
    userinput = data(income, savingsperyear, retirementlength, age, retirementage, incomegrowth, retirementcosts, investmentgrowth,
                     currentsavings, statepension, male, swr)

    finalpot, deathpot, initdraw, finaldraw = userinput.getResults()


    return render_template('dataoutput.html', retirementage = retirementage, finalpot = round(finalpot,2), initdraw = round(initdraw, 2), finaldraw = round(finaldraw, 2), deathpot = round(deathpot,2))

if __name__ == '__main__':
    app.run(debug=True)
