from flask import Flask, render_template, request
app = Flask(__name__)

import obtain_player_stats

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/singles')
def singles():
    return render_template('singlessearch.html')

@app.route('/htoh')
def htoh():
    return render_template('headtohead.html')

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

@app.route('/listhtoh',methods = ['POST'])
def listhtoh():
    msg = "No record of player in database. Pwned."
    nmone = request.form['nmone']
    nmtwo = request.form['nmtwo']
    match_record = obtain_player_stats.get_headtohead(nmone,nmtwo);
    if match_record == None:
        return render_template("failed.html",msg = msg)
    else:
        msg = "Successful retrieval"
        return render_template("listhtoh.html",msg = msg,rows = match_record)

@app.route('/scouter',methods = ['GET'])
def scouter():
    match_record = obtain_player_stats.get_trueskill();
    _, tourney_list = obtain_player_stats.get_detailed_tournament_info();
    avepower = sum( [float(x[1]) for x in match_record] )/len(match_record)
    avepower = float( "{0:.1f}".format(avepower) )
    return render_template("scouter.php",rows = [match_record, len(match_record), avepower, tourney_list])

if __name__ == '__main__':
    app.run(debug = True)
