efrom flask import Flask, render_template, json, request, jsonify, redirect, url_for
from GolfSetup import GolfSetup
from GolfSetup import Config
from GolfSetup import Players

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def main():
    return render_template('index.html')

@app.route("/randomize", methods=['POST'])
def randomize():
    teamsize = int(request.form['teamsize'])
    if 0 < teamsize <= len(Config.players):
        res = GolfSetup.createPairing(size=teamsize)
        return jsonify(tournament = res)
    else:
        return jsonify(tournament = None)

@app.route("/players",methods=['GET'])
def players():
    return render_template('players.html', players=(Players.getPlayers('./data/Players.json')['Players']))

@app.route("/editplayer",methods=['GET','POST'])
def editplayers():
    return render_template('editplayer.html')

@app.route("/deleteplayer",methods=['GET','POST'])
def deleteplayers():
    pid = request.args['pid']
    if pid:
        Players.deletePlayer('./data/Players.json',int(pid))
    return redirect(url_for('players'))

@app.route("/saveplayer",methods=['POST'])
def saveplayers():

    if request.method == 'POST':
        name = request.form['newname']
        hc = int(request.form['newhandicap'])
        dec = int(request.form['newhandicapdec'])
        print "%s %d %d" % (name,hc,dec)
        if name and hc and dec:
            hc = (hc*100 + dec)/100.0
            Players.addPlayer('./data/Players.json', name, hc)
            return redirect(url_for('players'))

    return redirect(url_for('editplayer'))


if __name__ == "__main__":
    app.run()