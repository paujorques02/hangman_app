# main_app.py
from flask import Flask, render_template, request, redirect, url_for, session
from random_word import RandomWords

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

def is_valid_letter(letter):
    """Validates if the input is a single alphabetical letter."""
    return letter.isalpha() and len(letter) == 1

# Routes of the application
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['attempts'] = choose_difficulty(request.form['difficulty'])
        session['remaining_attempts'] = session['attempts']  # Track remaining attempts
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
        session['machine_optimal_attempts'] = 0  # Initialize optimal attempts counter
        session['machine_attempts_for_current_word'] = len(set(session['current_word']))
        return redirect(url_for('play'))

    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        if 'finalize' in request.form:
            return redirect(url_for('stats'))

        letter = request.form['letter'].upper()

        # Validate the letter input
        if not is_valid_letter(letter):
            guessed_word = ' '.join([letter if letter in session['guessed_letters'] else '_' for letter in session['current_word']])
            return render_template('play.html', word=guessed_word, attempts=session['remaining_attempts'], error="Please enter a single alphabetical letter.")

        # Increment total attempts regardless of correct or incorrect guess
        session['player_info']['total_attempts'] += 1
        session['remaining_attempts'] -= 1  # Deduct remaining attempts for each guess

        if letter in session['current_word'] and letter not in session['guessed_letters']:
            session['guessed_letters'].append(letter)
        elif letter not in session['current_word']:
            session['wrong_guesses'] += 1

        # Update attempts used by player
        session['player_info']['attempts_used'] = session['wrong_guesses']
        session.modified = True

        if set(session['current_word']) == set(session['guessed_letters']):
            session['player_info']['words_completed'] += 1

            # Accumulate machine's optimal attempts for completed word
            session['machine_optimal_attempts'] += session['machine_attempts_for_current_word']

            if session['words']:
                session['current_word'] = session['words'].pop()
                session['guessed_letters'] = []
                session['wrong_guesses'] = 0
                session['remaining_attempts'] = session['attempts']  # Reset remaining attempts for new word
                session['machine_attempts_for_current_word'] = len(set(session['current_word']))
            else:
                session['player_info']['won'] = True
                return redirect(url_for('stats'))

        elif session['remaining_attempts'] <= 0:
            # If remaining attempts are exhausted, go to stats
            session['machine_optimal_attempts'] += session['machine_attempts_for_current_word']
            return redirect(url_for('stats'))

    guessed_word = ' '.join([letter if letter in session['guessed_letters'] else '_' for letter in session['current_word']])
    return render_template('play.html', word=guessed_word, attempts=session['remaining_attempts'])

@app.route('/stats')
def stats():
    player_info = session.get('player_info', {})
    machine_optimal_attempts = session.get('machine_optimal_attempts', 0)
    return render_template('stats.html', player_info=player_info, machine_attempts=machine_optimal_attempts)

if __name__ == '__main__':
    app.run(debug=True)

