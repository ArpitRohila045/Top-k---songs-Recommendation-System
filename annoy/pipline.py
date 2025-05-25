from annoy.data_ingestion import ZipDataIngestor
from annoy.data_transformation import DataFrameToList, DataTranfromer
from annoy.model_traning import AnnoyModel
from annoy.model_query import QueryModel
from annoy.model import Node


import numpy as np

class pipline:
     
    def __init__(self):
        #loading the data
        file_path = "C:\\Users\\hp\\Downloads\\archive (1)\\song_data.csv.csv"
        sep = ";"
        data = ZipDataIngestor()
        df = data.ingest(file_path, sep)

        transformer = DataFrameToList()
        transformed_data = transformer.transform(df)


        # Training the model
        model = AnnoyModel(K=10, imb=0.5)
        root = Node(None , transformed_data)
        model.train(root)

        # Querying the model
        self.query = QueryModel(root)


