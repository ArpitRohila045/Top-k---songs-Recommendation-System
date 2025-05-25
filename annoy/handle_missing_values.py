import logging
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MissingValueHandler(ABC):

    @abstractmethod
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to handle missing values in a DataFrame.
        """
        pass

# Concrete implementation of MissingValueHandler for mean imputation

class MeanImputer(MissingValueHandler):


    def handle(self, df : pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values by replacing them with the mean of the column.
        """
        logging.info("Missing values hadling by imputing with mean")
        numerical_cols = df.select_dtypes(include=np.number).columns

        for col in numerical_cols:
            if df[col].isnull().any():
                mean_value = df[col].mean()
                df[col].fillna(mean_value, inplace=True)
        
        logging.info("Missing values handled by imputing with mean")

        return df

class DropMissing(MissingValueHandler):

    def __init__(self, threshold : int, axes : int = 0) -> pd.DataFrame:
        """
        Initialize the DropMissing handler with a threshold for dropping rows/columns.
        """
        self.threshold = threshold
        self.axes = axes

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:

        logging.info(f"Missing values handling by dropping {self.axes} with {self.threshold}")
        df.dropna(thresh=self.threshold, axis=self.axes, inplace=True)
        logging.info(f"Missing values handled by dropping {self.axes} with threshold {self.threshold}")
        return df

class MissingValueHandlerFactory:

    def __init__(self, startegy : MissingValueHandler):
        self.strategy = startegy

    def set_strategy(self, strategy: MissingValueHandler) -> None:
        """
        Set the strategy for handling missing values.
        """
        self.strategy = strategy

    def handle_missing_values(self, df : pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame using the selected strategy.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")
        
        return self.strategy.handle(df)

if __name__ == "__main__":
    # Example usage
    data = {
        'A': [1, 2, None, 4],
        'B': [None, 5, 6, 7],
        'C': [8, 9, 10, None]
    }
    df = pd.DataFrame(data)

    # Using MeanImputer
    mean_imputer = MeanImputer()
    handler = MissingValueHandlerFactory(mean_imputer)
    df = handler.handle_missing_values(df)
    print("DataFrame after mean imputation:")
    print(df)
