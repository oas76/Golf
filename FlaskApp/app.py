from flask import Flask, render_template, json, request
from GolfSetup import GolfSetup
from GolfSetup import Config

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

@app.route("/teamsetup")
def showRandomize():
    return render_template('randomize.html', players = Config.players)

@app.route("/randomize", methods=['POST'])
def randomize():
    try:
         # read input fields
        _nrOfteams = int(request.form['numberOfTeams'])

        # validate the received values
        if _nrOfteams:
            _res = GolfSetup.main(size=_nrOfteams)
            return render_template('result.html',result = _res)
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(debug = True)