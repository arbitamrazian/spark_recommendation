import os
from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS

conf = SparkConf().setAppName("CollaborativeFilteringSpark")
sc = SparkContext(conf=conf, pyFiles=['CollaborativeFilteringSpark.py'])

class CollaborativeFiltering():
    def __init__(self,data_path):
        if data_path:
            self.data = self.__get_data_from_file(data_path)
        self.model = None

    def add_data(self,user_id,data):
        new_ratings = sc.parallelize(ratings)
        self.data = self.data.union(new_ratings)

    def __get_data_from_file(self,data_path):
        raw_movies = sc.textFile(data_path)
        header = raw_movies.first()
        raw_ratings = raw_movies.filter(lambda line: line != header).map(lambda line: line.split(","))
        data = raw_ratings.map(lambda array: (int(array[0]),int(array[1]),float(array[2]))).cache()
        return data

    def train_model(self,rank,seed,iterations):
        if self.data.count()==0:
            raise Exception('No data has been stored')

        self.model = ALS.train(self.data, rank, seed=seed, iterations=iterations)
        return self.model

    def predict(self,unrated_user_RDD):
        #predict ratings for a given user
        if not self.model:
            raise Exception('No model has been trained.  Please run train_model or load_model')
        return model.predictAll(unrated_user_RDD)

    def save_model(self,save_path):
        self.model.save(sc, save_path)
    def load_model(self,save_path):
        self.model = MatrixFactorizationModel.load(sc, save_path)

if __name__ == "__main__":
    collab_filtering = CollaborativeFiltering('hdfs:///user/hadoop/ratings.csv')
    model = collab_filtering.train_model(8,5L,10)
