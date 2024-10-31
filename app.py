from flask import Flask, render_template, request, redirect, url_for, session
from random_word import RandomWords
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Game logic
def choose_difficulty(option):
    difficulties = {
        "1": 20,
        "2": 16,
        "3": 12,
        "4": 10
    }
    return difficulties.get(option, 20)  # default value 20 attempts

def get_random_words(n_words):
    r = RandomWords()
    return [r.get_random_word().upper() for _ in range(n_words)]

# Routes of the application
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['attempts'] = choose_difficulty(request.form['difficulty'])
        session['words'] = get_random_words(int(request.form['num_words']))
        session['current_word'] = session['words'].pop()
        session['guessed_letters'] = []
        session['wrong_guesses'] = 0
        session['player_info'] = {
            'attempts_used': 0,
            'won': False,
            'total_attempts': 0,
            'words_completed': 0
        }
        session['machine_attempts'] = len(set(session['current_word']))  # Ideal number of attempts for the machine
        return redirect(url_for('play'))

    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        if 'finalize' in request.form:
            # Redirect to stats page if the player clicks "End Game"
            return redirect(url_for('stats'))

        letter = request.form['letter'].upper()

        # Check if the letter is correct and hasn't been guessed before
        if letter in session['current_word'] and letter not in session['guessed_letters']:
            session['guessed_letters'].append(letter)
        elif letter not in session['current_word']:
            session['wrong_guesses'] += 1

        # Update attempts used by player
        session['player_info']['attempts_used'] = session['wrong_guesses']
        session['player_info']['total_attempts'] += 1
        session.modified = True

        # Check if the player has won the current word
        if set(session['current_word']) == set(session['guessed_letters']):
            session['player_info']['words_completed'] += 1  # Track completed words

            # Check if there are more words to play
            if session['words']:
                # Load the next word
                session['current_word'] = session['words'].pop()
                session['guessed_letters'] = []
                session['wrong_guesses'] = 0
                session['machine_attempts'] = len(set(session['current_word']))
            else:
                # If no more words, redirect to stats
                session['player_info']['won'] = True
                return redirect(url_for('stats'))

        elif session['wrong_guesses'] >= session['attempts']:
            # If the player loses on the current word, go to stats
            return redirect(url_for('stats'))

    # Generate the word with guessed letters format: A _ A _ _
    guessed_word = ' '.join([letter if letter in session['guessed_letters'] else '_' for letter in session['current_word']])
    return render_template('play.html', word=guessed_word, attempts=session['attempts'] - session['wrong_guesses'])

@app.route('/stats')
def stats():
    # Show stats page with player info and comparison with machine
    player_info = session.get('player_info', {})
    machine_attempts = session.get('machine_attempts', 0)
    return render_template('stats.html', player_info=player_info, machine_attempts=machine_attempts)

if __name__ == '__main__':
    app.run(debug=True)
