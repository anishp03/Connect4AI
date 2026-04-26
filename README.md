# Connect4AI
Connect4AI is a Python desktop Connect 4 game where a human player competes against a machine-learned AI opponent.

## Documents

All project documents, including the final report and the Individual Contribution Report are located in the `documents/` folder at the root of this project.

## GUI (Anish Patel)

The GUI is implemented in `connect4/gui/app.py` using Pygame. It is responsible for creating the game window, drawing the Connect 4 board, handling mouse input, showing turn and result text, and displaying the scoreboard.

### GUI Responsibilities

- render the board and pieces

- convert mouse clicks into board column selections

- display Human / AI turn text

- display win / draw messages

- load and display persistent scores from `connect4/scores.json`

### GUI Process Flow

1. Launch the game window from `main.py`.

2. Load the saved scoreboard from `scores.json`.

3. Wait for the user to press **Start Game**.

4. Draw the empty board and show the current turn.

5. When the player clicks a column, convert the click position into a board column index.

6. Pass that column into the game logic layer.

7. Redraw the board after the move is applied.

8. Update the result text and scoreboard if the round ends.

---

## Game Logic

The game rules are implemented in `connect4/logic/logic.py`. This file acts as the rule engine for Connect 4 and keeps the GUI separated from the actual board logic.

### Game Logic Responsibilities

- create a new empty 6x7 board

- determine whether a move is legal

- place a piece in the lowest open row of a selected column

- return all currently available columns

- detect whether the board is full

- check horizontal, vertical, and diagonal wins

- return the current game status

### Core Functions

- `empty_board()` creates a fresh board

- `valid_move(board, column)` checks whether a move is legal

- `place_piece(board, column, player)` applies a move to the board

- `available_moves(board)` returns all valid columns

- `board_full(board)` checks if no more moves are possible

- `check_win(board, piece)` checks for a four-in-a-row

- `game_status(board)` returns whether the game should continue or end

### Game Logic Process Flow

1. The GUI sends the selected column to the logic layer.

2. The logic checks whether the move is valid.

3. If valid, the piece is placed in the correct row.

4. The board is checked for:

   - a Player 1 / Human win

   - a Player 2 / AI win

   - a draw

   - or continuation

5. The result is returned to the GUI so the interface can update the board, score, and round state.

---

## Machine Learning AI (Nathan Daigle)

The AI is trained from a Connect 4 CSV dataset. Each board state is converted into 42 numeric features, one for each slot on the board, and the model learns to predict which column the AI should play next.

The ML code lives in `connect4/ai/ml.py`. The game calls `predictColumn(board)`, so the GUI does not need to know how the model works.

The predictor uses a hybrid strategy:

1. Play an immediate winning move for the AI.
2. Block an immediate human winning move.
3. Use the trained dataset-backed model from `connect4/ai/model.joblib`.
4. Fall back to center-first legal moves when no model is available.

## Dataset

The model is trained from a Connect 4 game database CSV. Place the dataset in a local `data/` folder, for example:

```bash
data/connect4.csv
```

The training pipeline expects at least 42 board-state columns. If the CSV includes a move label column named `best_column`, `column`, `move`, `target`, or `label`, it trains against that label. If the dataset only has board states, the pipeline generates move labels using Connect 4 tactics: immediate wins, blocking human wins, then center-weighted legal moves.

Board values are normalized as:

- `0`, `empty`, `b`, or `blank` for an empty slot.
- `1`, `human`, `player1`, or `o` for the human player.
- `2`, `ai`, `player2`, or `x` for the AI player.

## How to Train and Run

Enter the Root Directory of this Project "/Project4":

```bash
cd /Project4
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python train_model.py data/connect4.csv
```

The script prints accuracy and a classification report, then saves the model to:

```bash
connect4/ai/model.joblib
```

After training, start the game with:

```bash
python main.py
```

During gameplay, the AI evaluates the current board, uses the trained model to score possible columns, and makes its move automatically after the human player clicks a valid column.