from flask import Flask, render_template, request
app = Flask(__name__)

import obtain_player_stats

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/failed')
# def failed():
#     return render_template('failed.html')

@app.route('/list',methods = ['POST'])
def list():
    msg = "No record of player in database. Pwned."
    if request.method == 'POST':
        nm = request.form['nm']
        player_record = obtain_player_stats.get_player_record(nm);
        if player_record == None:
            return render_template("failed.html",msg = msg)
        else:
            msg = "Successful retrieval"
            return render_template("list.html",msg = msg,rows = player_record)

if __name__ == '__main__':
    app.run(debug = True)
