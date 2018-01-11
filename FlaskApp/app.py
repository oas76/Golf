from flask import Flask, render_template, json, request, jsonify
from GolfSetup import GolfSetup
from GolfSetup import Config

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html', players=Config.players)

@app.route("/randomize", methods=['POST'])
def randomize():
    teamsize = int(request.form['teamsize'])
    if 0 < teamsize <= len(Config.players):
        res = GolfSetup.createPairing(size=teamsize)
        return jsonify(tournament = list(res))
    else:
        return jsonify(tournament = None)

if __name__ == "__main__":
    app.run(debug=True)