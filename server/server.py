import asyncio
import websockets
import json

# Game state initialization
game_state = {
    "A": ["A-P1", "A-P2", "A-H1", "A-H2", "A-P3"],
    "B": ["B-P1", "B-P2", "B-H1", "B-H2", "B-P3"],
    "board": [
        ["A-P1", "A-P2", "A-H1", "A-H2", "A-P3"],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["B-P1", "B-P2", "B-H1", "B-H2", "B-P3"]
    ],
    "current_player": "A",
    "move_history": []
}

# Move validation logic
def is_valid_move(player, character, move):
    board = game_state["board"]
    
    # Locate the character's current position
    current_position = None
    for i in range(5):
        for j in range(5):
            if board[i][j] == character:
                current_position = (i, j)
                break
        if current_position:
            break
    
    if not current_position:
        return False  # The character is not on the board

    # Extract target position from the move
    target_position = move

    # Ensure the move is within bounds
    if not (0 <= target_position[0] < 5 and 0 <= target_position[1] < 5):
        return False  # Move is out of bounds

    # Example movement rule: characters can move one square horizontally or vertically
    row_diff = abs(target_position[0] - current_position[0])
    col_diff = abs(target_position[1] - current_position[1])
    if (row_diff + col_diff) != 1:
        return False  # Invalid move; should move only one square horizontally or vertically

    # Ensure target position is not occupied by a player's own piece
    target_piece = board[target_position[0]][target_position[1]]
    if target_piece and target_piece[0] == player:
        return False  # Invalid move; cannot move to a square occupied by own piece

    return True  # Move is valid

# Update the game board based on a move
def update_board(player, character, move):
    board = game_state["board"]
    
    # Locate the character's current position
    current_position = None
    for i in range(5):
        for j in range(5):
            if board[i][j] == character:
                current_position = (i, j)
                break
        if current_position:
            break
    
    if current_position:
        # Clear the character's current position
        board[current_position[0]][current_position[1]] = ""
        
        # Move the character to the new position
        board[move[0]][move[1]] = character

# WebSocket server handler
async def handle_move(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        player = data["player"]
        character = data["character"]
        move = data["move"]

        if player != game_state["current_player"]:
            response = {"status": "error", "message": "Not your turn."}
        elif is_valid_move(player, character, move):
            update_board(player, character, move)
            game_state["current_player"] = "B" if player == "A" else "A"
            game_state["move_history"].append(f"{player}-{character}:{move}")
            response = {"status": "success", "game_state": game_state}
        else:
            response = {"status": "invalid_move", "message": "Invalid move. Please try again."}

        await websocket.send(json.dumps(response))

# Main function to run the server
async def main():
    start_server = await websockets.serve(handle_move, "localhost", 6789)
    await start_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
