const socket = new WebSocket("ws://localhost:6789");

socket.onopen = () => {
  console.log("Connected to server");
};

socket.onmessage = (event) => {
  const gameState = JSON.parse(event.data);
  updateBoard(gameState.board);
  updateTurn(gameState.current_turn);
};

function sendMove(player, piece, move) {
  const message = JSON.stringify({
    player: player,
    piece: piece,
    move: move,
  });
  socket.send(message);
}
function updateBoard(board) {
  const boardElement = document.getElementById("board");
  boardElement.innerHTML = ""; // Clear the current board

  for (let row = 0; row < board.length; row++) {
    for (let col = 0; col < board[row].length; col++) {
      const cell = document.createElement("div");
      const piece = board[row][col];

      if (piece) {
        cell.innerText = piece; // Display the piece identifier
        cell.classList.add("piece");
        cell.dataset.piece = piece;
        cell.dataset.row = row;
        cell.dataset.col = col;

        // Highlight the piece if it's clicked
        cell.addEventListener("click", () => {
          const selectedPieceElement =
            document.getElementById("selected-piece");
          selectedPieceElement.innerText = `${piece} (Row: ${row + 1}, Col: ${
            col + 1
          })`;
          selectedPieceElement.dataset.row = row;
          selectedPieceElement.dataset.col = col;
          selectedPieceElement.dataset.piece = piece;
        });
      }

      boardElement.appendChild(cell);
    }
  }
}
function updateTurn(turn) {
  document.getElementById(
    "current-player"
  ).innerText = `Current Player: ${turn}`;
}
