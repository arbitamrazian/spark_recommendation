import os
from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS

conf = SparkConf().setAppName("CollaborativeFilteringSpark")
sc = SparkContext(conf=conf, pyFiles=['CollaborativeFilteringSpark.py'])

class CollaborativeFiltering():
    def __init__(self):
        self.model = None

    def get_data_from_file(self,data_path):
        raw_movies = sc.textFile(data_path)
        header = raw_movies.first()
        raw_ratings = raw_movies.filter(lambda line: line != header).map(lambda line: line.split(","))
        self.base_ratings = raw_ratings.map(lambda array: (int(array[0]),int(array[1]),float(array[2]))).cache()
        return self.base_ratings

    def train_model(self,data,rank,seed,iterations):
        self.model = ALS.train(data, rank, seed=seed, iterations=iterations)
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

collab_filtering = CollaborativeFiltering()
data = collab_filtering.get_data_from_file('hdfs:///user/hadoop/ratings.csv')
model = collab_filtering.train_model(data,8,5L,10)
