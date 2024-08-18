# imports
from score import read_current_score
from flask import Flask

# ################# Main Score Flask ##################


app = Flask(__name__)


# Route to serve the score with HTML
@app.route('/')
def score_server():
    score = read_current_score()
    if score >= 0:
        html = f"""
            <html>
            <head><title>Scores Game</title></head>
            <body>
                <h1>The Score is:</h1>
                <div id="score">{score}</div>
            </body>
            </html>
            """
        return html
    else:
        error = score
        html = f"""
                    <html>
                    <head><title>Scores Game</title></head>
                    <body>
                        <h1>ERROR:</h1>
                        <div id ="score" style="color:red">{error}</div>
                    </body>
                    </html>
                    """
        return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)