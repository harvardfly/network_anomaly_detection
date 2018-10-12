import os
import sys

pre_current_dir = os.path.dirname(os.getcwd())
sys.path.append(pre_current_dir)

from nt_spark.spark_sql_base import SparkSql
from pyspark.mllib.clustering import (
    KMeans, KMeansModel
)
from pyspark.mllib.tree import (
    RandomForest, RandomForestModel
)
from numpy import array
from math import sqrt


class SparkAnomaly(object):
    def __init__(self, appid, start_time, end_time):
        self.appid = appid
        self.start_time = start_time
        self.end_time = end_time
        self.spark_sql = SparkSql()
        self.cat_res = self.spark_sql.load_table_dataframe('cat_resource')
        self.filter_str = "appid = {0} " \
                          "and create_time >= {1} " \
                          "and update_time <= {2}".format(
            self.appid, self.start_time, self.end_time,
        )

    def get_kmeans_model(self):
        """
        读取表的dataframe
        :return:
        """
        df = self.cat_res.filter(self.filter_str)
        parsed_data_rdd = df.rdd.map(lambda x: array([x[4], x[5], x[6]]))

        # 建立聚类模型
        clusters = KMeans.train(
            parsed_data_rdd, 2,
            maxIterations=10,
            initializationMode="random"
        )

        # Evaluate clustering by computing Within Set Sum of Squared Errors
        def error(point):
            center = clusters.centers[clusters.predict(point)]
            return sqrt(sum([x ** 2 for x in (point - center)]))

        WSSSE = parsed_data_rdd.map(lambda point: error(point)).reduce(lambda x, y: x + y)
        print("Within Set Sum of Squared Error = " + str(WSSSE))

        # # 保存 训练好的模型
        # # model_path = "{}/kmeans_model".format(current_dir)
        # # if not os.path.exists(model_path):
        # #     clusters.save(sc, model_path)
        # #
        # # trained_model = KMeansModel.load(
        # #     sc, "{}/kmeans_model".format(current_dir)
        # # )
        # # return trained_model

    def get_random_forest_model(self):
        """
        读取表的dataframe
        :return:
        """
        df = self.cat_res.filter(self.filter_str)

        pass


test = SparkAnomaly(110312, 1539331733000, 1539334343000)
test.get_kmeans_model()
