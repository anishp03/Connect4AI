# Connect4AI
This is a AI vs Human Connect4 Application

## Machine Learning AI

The AI code lives in `connect4/ai/ml.py`. The game calls `predictColumn(board)`, so the GUI does not need to know how the model works.

The predictor uses a hybrid strategy:

1. Play an immediate winning move for the AI.
2. Block an immediate human winning move.
3. Use a trained model from `connect4/ai/model.joblib` when one exists.
4. Fall back to center-first legal moves when no model is available.

## Dataset

Place the Connect4 CSV dataset in a local `data/` folder, for example:

```bash
data/connect4.csv
```

The raw dataset is ignored by git because Kaggle/UCI datasets can be large. The training pipeline expects at least 42 board-state columns. If the CSV includes a move label column named `best_column`, `column`, `move`, `target`, or `label`, it trains against that label. If the dataset only has board states, the pipeline generates labels using the same tactical rules as the game AI.

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