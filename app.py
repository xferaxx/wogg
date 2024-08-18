import os
import secrets
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from guess_game import generate_number, compare_results
from currency_roulette_game import compare_resultss, get_money_interval
from memory_game import generate_sequence, is_list_equal
from score import ScoreDatabase
import random
import pygame

app = Flask(__name__)
secret_key = secrets.token_hex(32)
app.secret_key = os.getenv('SECRET_KEY', secret_key)


@app.route('/')
def home():
    if 'user_id' in session:
        db = ScoreDatabase()
        user_id = session['user_id']
        username = session.get('username', 'User')
        current_score = db.get_current_score(user_id)
        print(f"Rendering index.html with username: {username} and score: {current_score}")  # Debugging print
        return render_template('index.html', score=current_score, username=username)
    return redirect(url_for('login'))


@app.route('/score')
def score():
    if 'user_id' in session:
        db = ScoreDatabase()
        user_id = session['user_id']
        current_score = db.get_current_score(user_id)
        return render_template('score.html', score=current_score)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = ScoreDatabase()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Attempting login with username: {username} and password: {password}")  # Debugging print
        user_id = db.authenticate_user(username, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            print(f"Login successful for user_id: {user_id}")  # Debugging print
            return redirect(url_for('home'))
        else:
            print("Login failed")  # Debugging print
            return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = ScoreDatabase()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            db.create_user(username, password)
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print(f"Error creating user: {err}")  # Debugging print
            return render_template('register.html', error="Username already exists. Please choose another one.")
    return render_template('register.html')


@app.route('/memory-game', methods=['GET', 'POST'])
def memory_game():
    db = ScoreDatabase()
    user_id = session.get('user_id')
    username = session.get('username')
    current_score = db.get_current_score(user_id) if user_id else 0
    if request.method == 'POST':
        print("Memory game form data received:", request.form)  # Debugging print
        if 'level' in request.form:
            # Stage 1: Generate the sequence based on the selected level
            level = int(request.form['level'])
            session['level'] = level
            session['username'] = username
            pc_list = generate_sequence(level)
            pc_list_str = ','.join(map(str, pc_list))  # Prepare the list as a comma-separated string
            return render_template('memory_game.html', show_sequence=True, pc_list=pc_list_str, score=current_score,
                                   username=username)
        elif 'user_list' in request.form:
            # Stage 2: Compare user input with the generated sequence
            pc_list = list(map(int, request.form['pc_list'].split(',')))
            user_list = list(map(int, request.form['user_list'].split(',')))
            if is_list_equal(user_list, pc_list):
                level = session.get('level')
                points_of_winning = (level * 3) + 5

                try:
                    db.add_score(session['user_id'],
                                 points_of_winning)  # Update score only if the player wins
                    print("Score updated successfully.")  # Debugging print
                except Exception as e:
                    print(f"Error updating score: {e}")  # Debugging print
                result_message = "Congratulations! You won!"
            else:
                result_message = f"Sorry, you lost. The correct sequence was: {', '.join(map(str, pc_list))}"
            return render_template('memory_game.html', result_message=result_message, score=current_score,
                                   username=username)
    return render_template('memory_game.html', show_sequence=False, score=current_score, username=username)


@app.route('/guess-game', methods=['GET', 'POST'])
def guess_game():
    db = ScoreDatabase()
    user_id = session.get('user_id')
    username = session.get('username')
    current_score = db.get_current_score(user_id) if user_id else 0
    if request.method == 'POST':
        if 'level' in request.form:
            level = int(request.form['level'])
            session['level'] = level
            session['username'] = username
            generated_number = generate_number(level)
            return render_template('guess_game.html', show_guess=True, generated_number=generated_number, level=level,
                                   score=current_score, username=username)
        elif 'user_guess' in request.form:
            generated_number = int(request.form['generated_number'])
            user_guess = int(request.form['user_guess'])
            if compare_results(generated_number, user_guess):
                level = session.get('level')
                points_of_winning = (level * 3) + 5
                db.add_score(session['user_id'], points_of_winning)
                print("Score updated successfully.")
                result_message = "Congratulations! You guessed the correct number!"
            else:
                result_message = f"Sorry, you guessed wrong. The correct number was: {generated_number}"
            return render_template('guess_game.html', result_message=result_message, score=current_score,
                                   username=username)
    return render_template('guess_game.html', show_guess=False, score=current_score, username=username)


@app.route('/currency-roulette', methods=['GET', 'POST'])
def currency_roulette():
    db = ScoreDatabase()
    user_id = session.get('user_id')
    username = session.get('username')
    current_score = db.get_current_score(user_id) if user_id else 0
    if request.method == 'POST':
        if 'level' in request.form:
            level = int(request.form['level'])
            session['level'] = level
            session['username'] = username
            usd, usd_ils = get_money_interval(level)
            if usd is None or usd_ils is None:
                return render_template('currency_roulette.html',
                                       result_message="An error occurred while retrieving currency data. Please try "
                                                      "again.",
                                       score=current_score)
            return render_template('currency_roulette.html', show_guess=True, usd=usd, usd_ils=usd_ils, level=level,
                                   score=current_score, username=username)

        elif 'user_guess' in request.form:
            user_guess = float(request.form['user_guess'])
            usd_ils = float(request.form['usd_ils'])
            result, correct_value = compare_resultss(user_guess, usd_ils, session.get('level', 1))
            if result:
                level = session.get('level')
                points_of_winning = (level * 3) + 5
                db.add_score(session['user_id'], points_of_winning)
                print("Score updated successfully.")
                result_message = f"Congratulations! Your guess was correct! The value was {correct_value:.2f} ILS."
            else:
                result_message = f"Sorry, your guess was incorrect. The correct value was: {correct_value:.2f} ILS."
            return render_template('currency_roulette.html', result_message=result_message, score=current_score,
                                   username=username)
    return render_template('currency_roulette.html', show_guess=False, score=current_score, username=username)


@app.route('/rock-paper-scissors', methods=['GET', 'POST'])
def rock_paper_scissors():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = ScoreDatabase()
    user_id = session['user_id']
    current_score = db.get_current_score(user_id)

    # Add the Rock, Paper, Scissors game
    choices = ['rock', 'paper', 'scissors']
    rules = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }

    if request.method == 'POST':
        if 'level' in request.form:
            # Handle level selection
            level = int(request.form['level'])
            session['level'] = level
            return render_template('rock_paper_scissors.html', show_choices=True, score=current_score,
                                   username=session.get('username'))

        elif 'choice' in request.form:
            # Handle player's choice
            player_choice = request.form['choice']
            computer_choice = random.choice(['rock', 'paper', 'scissors'])
            result_message = ""

            # Determine the result
            if player_choice == computer_choice:
                result_message = f"It's a tie! Both chose {player_choice.capitalize()}."
            elif (player_choice == 'rock' and computer_choice == 'scissors') or \
                    (player_choice == 'paper' and computer_choice == 'rock') or \
                    (player_choice == 'scissors' and computer_choice == 'paper'):
                result_message = f"You win! {player_choice.capitalize()} beats {computer_choice.capitalize()}."
                level = session.get('level', 1)
                points_of_winning = (level * 3) + 5
                db.add_score(user_id, points_of_winning)
            else:
                result_message = f"You lose! {computer_choice.capitalize()} beats {player_choice.capitalize()}."

            return render_template('rock_paper_scissors.html', result_message=result_message, score=current_score,
                                   username=session.get('username'))

    return render_template('rock_paper_scissors.html', show_choices=False, score=current_score,
                           username=session.get('username'))


@app.route('/tic-tac-toe', methods=['GET', 'POST'])
def tic_tac_toe():
    db = ScoreDatabase()
    user_id = session.get('user_id')
    username = session.get('username')
    current_score = db.get_current_score(user_id) if user_id else 0

    if request.method == 'POST':
        if 'level' in request.form:
            # Stage 1: Select level
            level = int(request.form['level'])
            session['level'] = level
            session['username'] = username
            return render_template('tic_tac_toe.html', show_board=True, level=level, score=current_score,
                                   username=username)

        elif 'result' in request.form:
            # Stage 2: Game result
            result = request.form['result']
            level = session.get('level', 1)
            if result == 'win':
                points_of_winning = (level * 3) + 5
                db.add_score(session['user_id'], points_of_winning)
                print("Score updated successfully.")
                result_message = "Congratulations! You won!"
            elif result == 'loss':
                points_of_losing = -8  # Deduct 8 points
                db.add_score(session['user_id'], points_of_losing)
                print("Score deducted for loss.")
                result_message = "Sorry, you lost. 8 points have been deducted from your score."
            else:
                result_message = "It's a tie! No points were lost or gained."

            return render_template('tic_tac_toe.html', result_message=result_message, score=current_score,
                                   username=username)

    return render_template('tic_tac_toe.html', show_board=False, score=current_score, username=username)


@app.route('/snake', methods=['GET', 'POST'])
def snake():
    db = ScoreDatabase()
    user_id = session.get('user_id', 'guest')  # For demonstration purposes, using 'guest' as default
    username = session.get('username', 'Player')
    current_score = db.get_current_score(user_id)

    if request.method == 'POST':
        if 'level' in request.form:
            # Handle level selection
            level = int(request.form['level'])
            session['level'] = level
            return render_template('snake.html', show_board=True, level=level, score=current_score, username=username)

        elif 'result' in request.form:
            # Handle the result after the game ends
            result = request.form['result']
            level = session.get('level', 1)
            if result == 'win':
                points_of_winning = (level * 3) + 5
                db.add_score(user_id, points_of_winning)
                result_message = "Congratulations! You won!"
            elif result == 'loss':
                points_of_losing = -0  # Deduct 8 points
                db.add_score(user_id, points_of_losing)
                result_message = "Sorry, you lost. 8 points have been deducted from your score."
            else:
                result_message = "It's a tie! No points were lost or gained."

            return render_template('snake.html', result_message=result_message, score=current_score, username=username)

    return render_template('snake.html', show_board=False, score=current_score, username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
