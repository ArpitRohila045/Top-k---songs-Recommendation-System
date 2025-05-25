import pandas as pd
import numpy as np
import logging
from typing import List, Tuple

from abc import ABC, abstractmethod

class DataTranfromer(ABC):

    @abstractmethod
    def transform(self, df : pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to transform the DataFrame.
        """
        pass

class DataFrameToList(DataTranfromer):
    """
    Concrete implementation of DataTranfromer to convert DataFrame to list.
    """
    
    def transform(self, df: pd.DataFrame) -> List[Tuple]:
        """
        Convert the DataFrame to a list of lists.
        """
        logging.info("Transforming DataFrame to list")
        numerical_cols = df.select_dtypes(include=np.number).columns
        categoraical_cols = df.select_dtypes(include='object').columns

        list_data = []

        # Convert categorical columns to string
        for _, row in df.iterrows():
            list_data.append((row[categoraical_cols].tolist(), row[numerical_cols].tolist()))

        logging.info("DataFrame transformed to list")

        return list_data

if __name__ == "__main__":
    # df = pd.read_csv("C:\\Users\\hp\\Downloads\\archive (1)\\song_data.csv.csv" , delimiter=';')
    # transformer = DataFrameToList()
    # transformed_data = transformer.transform(df)
    # print(transformed_data)
    pass
