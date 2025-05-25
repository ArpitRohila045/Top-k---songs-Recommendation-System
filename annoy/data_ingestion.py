import zipfile
import os
from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
import pandas as pd


class DataIngerstor(ABC):
    """
    Abstract base class for data ingestion.
    """
    
    @abstractmethod
    def ingest(self, zip_file_path: str) -> None:
        """
        Unzip the given file to the specified directory.
        """
        pass
    

# Implementing the ZipDataIngestor class 
class ZipDataIngestor(DataIngerstor):
    """
    Concrete implementation of DataIngerstor for zip files.
    """
    
    def ingest(self, file_path: str, seprator : str) -> pd.DataFrame:
        """
        Unzip the given file to the specified directory.
        """
        # with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        #     zip_ref.extractall("extracted_data/")  # Extract to the data directory

        # extracted_files = os.listdir("extracted_data/")
        # csv_files = [f for f in extracted_files if f.endswith('csv')]

        # if not csv_files:
        #     raise ValueError("No CSV files found in the zip archive.")

        # # Assuming we only need the first CSV file for ingestion
        # csv_file_path = os.path.join("extracted_data/", csv_files[0])
        pdf = pd.read_csv(file_path, sep=seprator)

        return pdf
    
# Data Ingestion Factory
class DataIngestorFactory:
    """
    Factory class to create data ingestor instances>
    """

    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngerstor:

        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
# Example usage

if __name__ == "__main__":
    # # session = SparkSession.builder\
    # #     .appName("Dataingestion")\
    # #     .getOrCreate()
    
    # ingestor = ZipDataIngestor()
    # file_path = "C:\\Users\\hp\\Downloads\\archive (1)\\song_data.csv.csv"

    # df = ingestor.ingest(file_path)
    # print(df.head())
    pass
