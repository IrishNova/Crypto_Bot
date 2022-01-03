import pandas as pd
from pymongo import MongoClient
import certifi
from calculator import calculator_main
from matrix_maker import matrix_starter


class Daryl:
    def __init__(self, coin):
        self.coin = coin
        self.raw_data = None
        self.worked_data = None
        self.matrix = None
        self.data_retriever()
        self.data_calc()

    def mongo_cluster(self):
        """
        Connects to MongoDB Atlas Cloud
        cluster = connection to cluster on cloud
        db = specific database within cluster, titled "crypto", though it contains all data for this project.
        :return: variable db which is set up for entry of specific item selected by input
        """
        cluster = MongoClient(
            "mongodb+srv://admin:pword123@beta.jpgpc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        db = cluster["coin_data"]
        return db

    def data_retriever(self):
        """
        Uses connection set up in mongo_cluster() function to access specific item's data, retrieves it and packages that
        data as a DataFrame.
        :param one: User input
        :return: DataFrame of desired item
        """
        col = self.mongo_cluster()["{0}".format(self.coin)]
        temp = []
        for doc in col.find():
            temp.append(doc)
        export = pd.DataFrame(temp, columns=["Date", "Price", 'Market Cap', 'Volume', 'market cap dominance'])
        export = export.set_index("Date")
        self.raw_data = export
        return

    def data_calc(self):
        temp = self.raw_data.copy()
        self.worked_data = calculator_main(temp)
        self.matrix = matrix_starter(self.worked_data)