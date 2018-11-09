from flask import Flask, render_template, request, session
import generate
import validite
import collections
import time


app = Flask(__name__)
app.secret_key="Blu3r3dy3ll0wgr33n"

def validate_words():
    session['tempwords'] = []
    session['errors'] = []
    session['wordlist'] = session.get('wordstring').split()
    session['sourcewordlist'] = collections.Counter(list(session.get('sourceword')))
    session['correct'] = 0
    if len(session.get('wordlist')) != 7:
        session['errors'].append("You may only enter 7 words.")
    else:
        for x in range(7):
            if validite.checkword(session.get('wordlist')[x].lower(), session.get('sourcewordlist'), session.get('sourceword'), session.get('errors'), session.get('tempwords')) == True:
                session['correct'] += 1

    if session['correct'] == 7:
        return True
    else:
        return False

def check_leaderboard(leaderboardlist, time):
    session['empty'] = False
    if len(leaderboardlist) == 0:
        session['empty'] = True
        return True
    elif len(leaderboardlist) < 20:
        return True
    elif leaderboardlist[20][1] > time:
        return True
    else:
        return False

@app.route('/')
def display_home():
    return render_template("index.html", title="Wordgame Wonders")

@app.route('/startgame')
def startgame():
    session['sourceword'] = generate.sourceword()
    session['leaderboardlist'] = generate.leaderboard()
    session['time'] = time.time()
    return render_template("game.html", title='Wordgame Wonders', sourceword=session.get('sourceword'))

@app.route('/validate', methods=['POST'])
def validate():
    if request.method=='POST':
        session['wordstring'] = request.form['wordstring']
        session['stoptime'] = round(time.time() - session.get('time'), 2)
        if validate_words():
            session['on_leaderboard'] = check_leaderboard(session.get('leaderboardlist'), session.get('stoptime'))
            if session.get('on_leaderboard') == True:
                return render_template('on_leaderboard.html', title="Top 20!", time=session.get('stoptime'))
            else:
                return render_template('leaderboard.html', leaderboard=session.get('leaderboardlist'))
        else:
            return render_template('incorrect.html', title=(str(session.get('correct')) + " out of 7!"), time=session.get('stoptime'), errors=session.get('errors'), correct=session.get('correct'))

@app.route('/leaderboard', methods=['POST'])
def add_to_leaderboard():
    if request.method=='POST':
        session['name'] = request.form['name']
        session['player_score'] = [session.get('name'),float(session.get('stoptime'))]

        leaderboard = session.get('leaderboardlist')

        if session.get('empty'):
            leaderboard.append(session.get('player_score'))
        elif float(session.get('stoptime') > float(leaderboard[len(leaderboard) - 1][1])):
            leaderboard.append(session.get('player_score'))
        else:
            for i in range(0, len(leaderboard)):
                if float(session.get('stoptime') < float(leaderboard[i][1])):
                    leaderboard.insert(i, session.get('player_score'))
                    break

        open('leaderboard.txt', 'w').close()
        for line in leaderboard:
            with open('leaderboard.txt', 'a') as file:
                string = line[0]+","+str(line[1])
                file.write(string + '\n')

    return render_template('leaderboard.html', leaderboard = leaderboard)

@app.route('/showleaderboard')
def show_leaderboard():
        return render_template('leaderboard.html', leaderboard=session.get('leaderboardlist'), length=len(session.get('leaderboardlist')))


if __name__ == '__main__':
    app.run(debug=True)


#errors:
    #space in name causes error
