from pathlib import Path

from connect4.logic.logic import (
    COLUMNS,
    PLAYER1,
    PLAYER2,
    ROWS,
    available_moves,
    check_win,
    place_piece,
)


modelPath = Path(__file__).with_name("model.joblib")
centerFirstColumns = [3, 2, 4, 1, 5, 0, 6]
labelColumns = ("best_column", "column", "move", "target", "label")


def boardToFeatures(board, aiPiece=PLAYER2, humanPiece=PLAYER1):
    values = []
    for row in board:
        for cell in row:
            if cell == aiPiece:
                values.append(2)
            elif cell == humanPiece:
                values.append(1)
            else:
                values.append(0)
    return values


def scoreColumns(board, modelPath=modelPath):
    predictor = Connect4HybridPredictor(modelPath)
    return predictor.scoreColumns(board)


def predictColumn(board, modelPath=modelPath):
    predictor = Connect4HybridPredictor(modelPath)
    return predictor.predict(board)


def trainFromDataset(csvPath, modelPath=modelPath):
    pd = importPandas()
    joblib = importJoblib()
    trainTestSplit, RandomForestClassifier, classificationReport, accuracyScore = (
        importSklearn()
    )

    data = pd.read_csv(csvPath)
    features, labels = prepareTrainingData(data)
    featureValues = features.to_numpy()
    labelValues = labels.to_numpy()

    xTrain, xTest, yTrain, yTest = trainTestSplit(
        featureValues,
        labelValues,
        test_size=0.2,
        random_state=42,
        stratify=labels if labels.nunique() > 1 else None,
    )

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(xTrain, yTrain)

    predictions = model.predict(xTest)
    metrics = {
        "accuracy": accuracyScore(yTest, predictions),
        "classification_report": classificationReport(
            yTest,
            predictions,
            zero_division=0,
        ),
        "training_rows": len(features),
        "test_rows": len(xTest),
    }

    modelPath = Path(modelPath)
    modelPath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, modelPath)
    return metrics


def prepareTrainingData(data):
    pd = importPandas()

    labelColumn = findLabelColumn(data.columns)
    boardColumns = findBoardColumns(data.columns, labelColumn)

    features = data.loc[:, boardColumns].map(normalizeCell)

    if labelColumn:
        labels = data[labelColumn].map(normalizeLabel)

    if not labelColumn or labels.isna().all():
        labels = features.apply(
            lambda row: labelFromFeatures(row.tolist()),
            axis=1,
        )

    trainingData = pd.concat(
        [features, labels.rename("label")],
        axis=1,
    ).dropna()

    return trainingData.loc[:, boardColumns], trainingData["label"].astype(int)


class Connect4HybridPredictor:
    def __init__(self, modelPath=modelPath):
        self.modelPath = Path(modelPath)
        self.model = None
        self.modelLoaded = False

    def predict(self, board):
        rankedColumns = self.scoreColumns(board)
        if rankedColumns:
            return rankedColumns[0][0]
        return None

    def scoreColumns(self, board):
        legalColumns = available_moves(board)
        scores = []

        for column in legalColumns:
            score = self.scoreColumn(board, column)
            scores.append((column, score))

        return sorted(scores, key=lambda item: item[1], reverse=True)

    def scoreColumn(self, board, column):
        if moveWins(board, column, PLAYER2):
            return 1000

        if moveWins(board, column, PLAYER1):
            return 900

        modelScore = self.modelScore(board, column)
        fallbackScore = 10 - centerFirstColumns.index(column)
        return modelScore + fallbackScore

    def modelScore(self, board, column):
        model = self.loadModel()

        if model is None:
            return 0

        features = modelFeatures(model, board)

        if hasattr(model, "predict_proba"):
            classes = list(model.classes_)
            probabilities = model.predict_proba(features)[0]
            if column in classes:
                return float(probabilities[classes.index(column)] * 100)

        predictedColumn = int(model.predict(features)[0])
        if predictedColumn == column:
            return 100
        return 0

    def loadModel(self):
        if not self.modelLoaded:
            self.modelLoaded = True
            if self.modelPath.exists():
                joblib = importJoblib()
                self.model = joblib.load(self.modelPath)

        return self.model


def copyBoard(board):
    return [row[:] for row in board]


def moveWins(board, column, piece):
    testBoard = copyBoard(board)
    placed = place_piece(testBoard, column, piece)
    return placed and check_win(testBoard, piece)


def modelFeatures(model, board):
    features = [boardToFeatures(board)]
    if hasattr(model, "feature_names_in_"):
        pd = importPandas()
        return pd.DataFrame(features, columns=model.feature_names_in_)
    return features


def findLabelColumn(columns):
    for column in columns:
        if str(column).lower() in labelColumns:
            return column
    return None


def findBoardColumns(columns, labelColumn):
    boardColumns = [column for column in columns if column != labelColumn]
    if len(boardColumns) >= ROWS * COLUMNS:
        return boardColumns[: ROWS * COLUMNS]
    raise ValueError("Dataset must contain at least 42 board-state columns.")


def normalizeCell(value):
    valueText = str(value).strip().lower()
    mapping = {
        "0": 0,
        "empty": 0,
        "b": 0,
        "blank": 0,
        "1": 1,
        "human": 1,
        "player1": 1,
        "o": 1,
        "2": 2,
        "ai": 2,
        "player2": 2,
        "x": 2,
    }
    return mapping.get(valueText, 0)


def normalizeLabel(value):
    valueText = str(value).strip().lower()
    labelMap = {
        "left": 0,
        "center-left": 2,
        "center": 3,
        "center-right": 4,
        "right": 6,
    }

    if valueText in labelMap:
        return labelMap[valueText]

    try:
        label = int(float(value))
        if 1 <= label <= COLUMNS:
            return label - 1
        return label
    except ValueError:
        return None


def labelFromFeatures(features):
    board = [
        features[row * COLUMNS : (row + 1) * COLUMNS]
        for row in range(ROWS)
    ]
    legalColumns = available_moves(board)

    for column in legalColumns:
        if moveWins(board, column, PLAYER2):
            return column

    for column in legalColumns:
        if moveWins(board, column, PLAYER1):
            return column

    for column in centerFirstColumns:
        if column in legalColumns:
            return column

    return None


def importPandas():
    import pandas as pd

    return pd


def importJoblib():
    import joblib

    return joblib


def importSklearn():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score as accuracyScore
    from sklearn.metrics import classification_report as classificationReport
    from sklearn.model_selection import train_test_split as trainTestSplit

    return trainTestSplit, RandomForestClassifier, classificationReport, accuracyScore
