# Hangman App

This repository contains a Flask-based web application that lets users play a word guessing game. The app generates random words and allows users to select different difficulty levels. Players can make attempts and receive feedback on their guesses until they complete the word.

## Features

- **Adjustable Difficulty**: Users can choose different difficulty levels, adjusting the number of allowed attempts.
- **Random Words**: Uses the `random-word` library to generate random English words.
- **Game Statistics**: Displays player performance statistics at the end of the game.

## Requirements

Ensure that Docker is installed on your machine.

### Python Dependencies
The Python dependencies are listed in `requirements.txt` and include:
- Flask
- random-word

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/paujorques02/hangman_app.git
   cd hangman_app
   ```

## Running with Docker

1. **Build the Docker image**:
    ```bash
    docker build -t hangman_app .
    ```

2. **Bun the container**:
    ```bash 
    docker run -p 5000:5000 hangman_app
    ```

3. **Open your browser**:
    Go to `http://localhost:5000`.

## License

This project is licensed under the MIT License.