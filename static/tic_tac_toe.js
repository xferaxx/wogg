let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameActive = true;
let difficultyLevel = 1;

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function startGame(level) {
    difficultyLevel = level;
    document.getElementById('level-selection').style.display = 'none';
    document.getElementById('tic-tac-toe-container').style.display = 'block';
}

function handleResultValidation() {
    let roundWon = false;
    for (let i = 0; i < winningConditions.length; i++) {
        const winCondition = winningConditions[i];
        let a = board[winCondition[0]];
        let b = board[winCondition[1]];
        let c = board[winCondition[2]];
        if (a === '' || b === '' || c === '') {
            continue;
        }
        if (a === b && b === c) {
            roundWon = true;
            break;
        }
    }

    if (roundWon) {
        document.getElementById('game-status').innerText = `Player ${currentPlayer} has won!`;
        gameActive = false;

        // Set the result value and automatically submit the form
        document.getElementById('result-input').value = currentPlayer === "X" ? 'win' : 'loss';

        // Delay the form submission to allow the message to display
        setTimeout(() => {
            document.querySelector('form').submit();  // Auto-submit the form after a short delay
        }, 1000);  // 1 second delay

        return;
    }

    if (!board.includes("")) {
        document.getElementById('game-status').innerText = "It's a tie!";
        gameActive = false;

        // Set the result as a tie and automatically submit the form
        document.getElementById('result-input').value = 'tie';

        // Delay the form submission to allow the message to display
        setTimeout(() => {
            document.querySelector('form').submit();  // Auto-submit the form after a short delay
        }, 1000);  // 1 second delay

        return;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";
    if (currentPlayer === "O" && gameActive) {
        makeComputerMove();
    }
}

function makeMove(index) {
    if (board[index] !== "" || !gameActive) {
        return;
    }
    board[index] = currentPlayer;
    document.getElementById(`cell-${index}`).innerText = currentPlayer;
    handleResultValidation();
}

function makeComputerMove() {
    let availableIndices = [];
    for (let i = 0; i < board.length; i++) {
        if (board[i] === "") {
            availableIndices.push(i);
        }
    }

    if (availableIndices.length > 0) {
        const randomIndex = availableIndices[Math.floor(Math.random() * availableIndices.length)];
        board[randomIndex] = currentPlayer;
        document.getElementById(`cell-${randomIndex}`).innerText = currentPlayer;
        handleResultValidation();
    }
}

function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    currentPlayer = "X";
    gameActive = true;
    document.getElementById('game-status').innerText = "";
    for (let i = 0; i < 9; i++) {
        document.getElementById(`cell-${i}`).innerText = "";
    }
}
