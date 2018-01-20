from flask import Flask, render_template, json, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from GolfSetup import GolfSetup
from GolfSetup import Config
from GolfSetup import Players
from forms import forms

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/",methods=['GET'])
def main():
    return render_template('index.html')

@app.route("/randomize", methods=['POST'])
def randomize():
    try:
        teamsize = int(request.form['teamsize'])
        if 0 < teamsize <= len(Players.getPlayers('./data/Players.json')['Players']):
            res = GolfSetup.createPairing(size=teamsize)
            return jsonify(tournament = res)

        return jsonify(tournament = None)

    except Exception as e:
        print(e.message)


@app.route("/players",methods=['GET'])
def players():
    try:
        return render_template('players.html', players=(Players.getPlayers('./data/Players.json')['Players']))

    except Exception as e:
        print(e.message)

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
                    Players.editPlayer('./data/Players.json',pid,attempt_name,newhc)
                else:
                    Players.addPlayer('./data/Players.json',attempt_name,newhc)
                return redirect(url_for('players'))
        elif request.method=='GET' and pid:
            Player = Players.getPlayerByIndex('./data/Players.json',pid)
            if Player:
                vals = {}
                vals['Name'] = Player['Name']
                vals['hc'] = int(Player['hc'])
                vals['hcdec'] = int(float(Player['hc'])*10)%10
        return render_template('editplayer.html', form=form, player=vals)
    except Exception as e:
        print e.message
        print e.args


@app.route("/deleteplayer/<int:pid>",methods=['GET'])
def deleteplayer(pid):
    try:
        delete_pid = pid
        Players.deletePlayer('./data/Players.json', delete_pid)
        return redirect(url_for('players'))
    except Exception as e:
        print(e.message)


if __name__ == "__main__":
    app.run(DEBUG=True)