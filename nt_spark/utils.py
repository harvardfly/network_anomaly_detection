import os
import sys
pre_current_dir = os.path.dirname(os.getcwd())
sys.path.append(pre_current_dir)


from nt_spark.spark_sql_base import SparkSql
from pyspark.mllib.clustering import (
    KMeans, KMeansModel
)
from numpy import array
from math import sqrt


class SparkAnomaly(object):
    def __init__(self):
        self.spark_sql = SparkSql()
        self.cat_res = self.spark_sql.load_table_dataframe('cat_resource')

    def get_kmeans_model(self, appid=None):
        """
        读取表的dataframe
        :param appid:
        :return:
        """
        filter_str = "appid = {0}".format(
            appid
        )
        df = self.cat_res.filter(filter_str).map(lambda x:x[0])
        print(df.collect())
        # parsed_data_rdd = df
        #
        # # 建立聚类模型
        # clusters = KMeans.train(parsed_data_rdd, 2, maxIterations=10, initializationMode="random")
        #
        # # Evaluate clustering by computing Within Set Sum of Squared Errors
        # def error(point):
        #     center = clusters.centers[clusters.predict(point)]
        #     return sqrt(sum([x ** 2 for x in (point - center)]))
        #
        # WSSSE = parsed_data_rdd.map(lambda point: error(point)).reduce(lambda x, y: x + y)
        # print("Within Set Sum of Squared Error = " + str(WSSSE))
        #
        # # 保存 训练好的模型
        # # model_path = "{}/kmeans_model".format(current_dir)
        # # if not os.path.exists(model_path):
        # #     clusters.save(sc, model_path)
        # #
        # # trained_model = KMeansModel.load(
        # #     sc, "{}/kmeans_model".format(current_dir)
        # # )
        # # return trained_model

    def get_random_forest_model(self, appid=None):
        """
        读取表的dataframe
        :param appid:
        :return:
        """
        filter_str = "appid = {0}".format(
            appid
        )
        df = self.cat_res.filter(filter_str)

        # 统计排序
        res_df = df.groupBy(
            "cognition_map_num"
        ).count().sort('count', ascending=False)

        return res_df


test = SparkAnomaly()
test.get_kmeans_model(110312)