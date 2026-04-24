# Connect4AI
Connect4AI is a Python desktop Connect 4 game where a human player competes against a machine-learned AI opponent.

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

## Training

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