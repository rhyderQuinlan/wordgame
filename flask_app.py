from flask import Flask, render_template, request, session
import generate
import validity
import collections
import time


app = Flask(__name__)
app.secret_key="Blu3r3dy3ll0wgr33n"

def validate_words(wordstring, sourceword):
    errors = []
    wordlist = wordstring.split()
    sourcewordlist = collections.Counter(list(sourceword.lower()))
    session['correct'] = 0
    if len(wordlist) != 7:
        errors.append("You may only enter 7 words.")
    else:
        for x in range(7):
            if validity.checkword(wordlist[x], sourcewordlist, sourceword, errors) == True:
                session['correct'] += 1

    session['errors'] = errors
    if session['correct'] == 7:
        return True
    else:
        return False

def on_leaderboard(leaderboardlist, time):
    if leaderboardlist[20].value > time:
        return True
    else:
        return False

@app.route('/')
def display_home():
    return render_template("index.html", title="Wordgame Wonders")

@app.route('/startgame')
def startgame():
    session['sourceword'] = generate.sourceword()
    session['time'] = time.time()
    return render_template("game.html", title='Wordgame Wonders', sourceword=session.get('sourceword'))

@app.route('/validate', methods=['POST'])
def validate():
    if request.method=='POST':
        session['wordstring'] = request.form['wordstring']
        if validate_words(session.get('wordstring'), session.get('sourceword')):
            session['stoptime'] = round(time.time() - session.get('time'), 2)
            session['leaderboardlist'] = generate.leaderboard(session.get('stoptime'))
            on_leaderboard = on_leaderboard(session.get('leaderboardlist'), session.get('stoptime'))
            if on_leaderboard == True:
                return render_template('on_leaderboard.html', title="Top 20!", time=session.get('stoptime'))
            else:
                return render_template('leaderboard.html', leaderboard=leaderboardlist)
        else:
            return render_template('fail.html', title="Almost", time=session.get('stoptime'), errors=session.get('errors'))

@app.route('/leaderboard', methods=['POST'])
def add_to_leaderboard():
    if request.method=='POST':
        session['name'] = request.form['name']
        for x in range(20):
            if leaderboardlist[x].value() > session.get('time'):
                for y = x in len:
                    leaderboardlist[y + 1] = leaderboardlist[y]




if __name__ == '__main__':
    app.run(debug=True)
