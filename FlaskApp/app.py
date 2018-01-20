from flask import Flask, render_template, json, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from GolfSetup import GolfSetup
from GolfSetup import Config
from GolfSetup import Players
from forms import forms
import traceback
import os.path

app = Flask(__name__)
app.secret_key = "super secret key"
this_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(this_path, "/data/Players.json")
os.environ['DATA_PATH'] = data_path


@app.route("/",methods=['GET'])
def main():
    return render_template('index.html')

@app.route("/randomize", methods=['POST'])
def randomize():
    try:
        teamsize = int(request.form['teamsize'])
        if 0 < teamsize <= len(Players.getPlayers(data_path)['Players']):
            res = GolfSetup.createPairing(size=teamsize)
            return jsonify(tournament = res)

        return jsonify(tournament = None)

    except Exception, err:
        traceback.print_exc()


@app.route("/players",methods=['GET'])
def players():
    try:
        return render_template('players.html', players=(Players.getPlayers(data_path)['Players']))

    except Exception, err:
        traceback.print_exc()

@app.route("/editplayer/<int:pid>",methods=['GET','POST'])
def editplayer(pid):
    try:
        form = forms.NameHandicapForm()
        vals = None
        if request.method=='POST' and form.validate_on_submit():
            attempt_name = request.form['playername']
            attempt_hc = request.form['handicap']
            attempt_hcdec = request.form['handicapdec']
            if attempt_hc and attempt_hcdec and attempt_name:
                newhc = (int(attempt_hc)*10 + int(attempt_hcdec))/float(10)
                if pid:
                    Players.editPlayer(data_path,pid,attempt_name,newhc)
                else:
                    Players.addPlayer(data_path,attempt_name,newhc)
                return redirect(url_for('players'))
        elif request.method=='GET' and pid:
            Player = Players.getPlayerByIndex(data_path,pid)
            if Player:
                vals = {}
                vals['Name'] = Player['Name']
                vals['hc'] = int(Player['hc'])
                vals['hcdec'] = int(float(Player['hc'])*10)%10
        return render_template('editplayer.html', form=form, player=vals)
    except Exception, err:
        traceback.print_exc()


@app.route("/deleteplayer/<int:pid>",methods=['GET'])
def deleteplayer(pid):
    try:
        delete_pid = pid
        Players.deletePlayer(data_path, delete_pid)
        return redirect(url_for('players'))
    except Exception, err:
        traceback.print_exc()


if __name__ == "__main__":
    app.debug = True
    app.run()