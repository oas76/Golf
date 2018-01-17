from flask import Flask, render_template, json, request, jsonify
from GolfSetup import GolfSetup
from GolfSetup import Config

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
    return render_template('players.html', players=Config.players)

@app.route("/editplayer",methods=['GET','POST'])
def editplayers():
    #player_index = int(request.form['playerindex'])
    return render_template('editplayer.html')

@app.route("/deleteplayer",methods=['POST'])
def deleteplayers():
    return False

@app.route("/saveplayer",methods=['POST'])
def saveplayers():
    name = request.form['newname']
    hc = float(request.form['newhandicap'])
    if name and hc:
        #save values
        pass
        return jsonify(saved=True)
    else:
        return jsonify(saved=False)

if __name__ == "__main__":
    app.run()