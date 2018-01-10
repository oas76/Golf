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

@app.route("/randomize", methods=['POST','GET'])
def randomize():
    try:
        # validate the received values
        if request.method == 'POST':
            # read input fields
            _nrOfteams = int(request.form['numberOfTeams'])
            if _nrOfteams:
                _res = GolfSetup.main(size=_nrOfteams)
                return render_template('result.html', result = _res)

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(debug = True)