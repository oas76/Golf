from flask import Flask, render_template, json, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from GolfSetup import GolfSetup
from GolfSetup import Config
from GolfSetup import Players
from forms import forms
import traceback
import pymongo
import os


app=Flask(__name__)
app.config.update(dict(
    SECRET_KEY="H0le1n0ne",
    WTF_CSRF_SECRET_KEY="H0le1n0ne"
))

@app.route("/",methods=['GET'])
def main():
    return render_template('index.html')

@app.route("/randomize", methods=['POST'])
def randomize():
    try:
        teamsize = int(request.form['teamsize'])
        if 0 < teamsize <= len(Players.getPlayers()):
            res = GolfSetup.createPairing(size=teamsize)
            return jsonify(tournament = res)

        return jsonify(tournament = None)

    except Exception, err:
        traceback.print_exc()


@app.route("/players",methods=['GET'])
def players():
    try:
        players = Players.getPlayers()
        if len(players):
            return render_template('players.html', players=players)
        else:
            return render_template('players.html', players={})

    except Exception, err:
        traceback.print_exc()

#@app.route("/players",methods=['GET'])
#def addPlayer():
#    try:


@app.route("/player/<uuid>",methods=['GET','POST'])
def updateplayer(uuid):
    try:
        form = forms.NameHandicapForm()
        vals = None
        if request.method=='POST' and form.validate_on_submit():
            attempt_name = request.form['playername']
            attempt_hc = request.form['handicap']
            attempt_hcdec = request.form['handicapdec']
            if attempt_hc and attempt_hcdec and attempt_name:
                newhc = (int(attempt_hc)*10 + int(attempt_hcdec))/float(10)
                if not uuid == '0' :
                    Players.updatePlayer(uuid,attempt_name,newhc)
                else:
                    Players.addPlayer(attempt_name,newhc)
                return redirect(url_for('players'))
        elif request.method=='GET' and uuid:
            Player = Players.getPlayerByIndex(uuid)
            if Player:
                vals = {}
                vals['Name'] = Player['Name']
                vals['hc'] = int(Player['hc'])
                vals['hcdec'] = int(float(Player['hc'])*10)%10
        return render_template('editplayer.html', form=form, player=vals)
    except Exception, err:
        traceback.print_exc()


@app.route("/deleteplayer/<uuid>",methods=['GET'])
def deleteplayer(uuid):
    try:
        delete_uuid = uuid
        Players.deletePlayer(delete_uuid)
        return redirect(url_for('players'))
    except Exception, err:
        traceback.print_exc()


if __name__ == "__main__":
    app.debug = True
    app.run()