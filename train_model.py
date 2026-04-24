import argparse

from connect4.ai import trainFromDataset


def main():
    argumentParser = argparse.ArgumentParser(description="Train the Connect4 AI model.")
    argumentParser.add_argument("csvPath", help="Path to the Connect4 training CSV.")
    argumentParser.add_argument(
        "--model-path",
        dest="modelPath",
        default="connect4/ai/model.joblib",
        help="Where to save the trained model.",
    )
    parsedArgs = argumentParser.parse_args()

    metrics = trainFromDataset(parsedArgs.csvPath, parsedArgs.modelPath)

    print(f"Training rows: {metrics['training_rows']}")
    print(f"Test rows: {metrics['test_rows']}")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(metrics["classification_report"])


if __name__ == "__main__":
    main()
