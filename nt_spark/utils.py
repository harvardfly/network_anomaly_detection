import os
import sys

pre_current_dir = os.path.dirname(os.getcwd())
sys.path.append(pre_current_dir)

from nt_spark.spark_sql_base import SparkSql
from pyspark.mllib.clustering import (
    KMeans
)
from numpy import array
from nt_spark.models import CatResultData
from nt_spark.serializers import CatResultDataSerializer


class SparkAnomaly(object):
    def __init__(self, appid, start_time, end_time):
        self.appid = appid
        self.start_time = start_time
        self.end_time = end_time
        self.spark_sql = SparkSql()
        self.cat_res = self.spark_sql.load_table_dataframe('cat_resource')
        self.cat_normal_res = self.spark_sql.load_table_dataframe(
            'cat_normal_resource'
        )
        self.filter_str = "appid = {0} " \
                          "and create_time >= {1} " \
                          "and update_time <= {2}".format(
            self.appid, self.start_time, self.end_time,
        )
        self.model_filter_str = "appid = {0}".format(self.appid)

    def get_kmeans_model(self):
        """
        得到kmeans聚类模型
        :return:
        """
        df = self.cat_normal_res.filter(self.model_filter_str)
        parsed_data_rdd = df.rdd.map(lambda x: array([x[4], x[5], x[6]]))

        # 建立聚类模型
        clusters = KMeans.train(
            parsed_data_rdd, 3,
            maxIterations=10,
            initializationMode="random"
        )

        return clusters

    def get_kmeans_predict(self):
        """
        获取appid指定时间段的预测结果
        :return:
        """
        df = self.cat_res.filter(self.filter_str)
        parsed_data_rdd = df.rdd.map(lambda x: array([x[4], x[5], x[6]]))
        clusters = self.get_kmeans_model()
        predict_result = clusters.predict(parsed_data_rdd)
        return predict_result.collect()

    def get_random_forest_model(self):
        """
        读取表的dataframe
        :return:
        """
        df = self.cat_res.filter(self.filter_str)

        pass


def get_kmeans_result(appid, start_time, end_time):
    """
    获取appid指定时间段的cat数据
    :param appid:
    :param start_time:
    :param end_time:
    :return:
    """
    cat_result_obj = CatResultData.objects.filter(
        appid=appid,
        start_time=start_time,
        end_time=end_time,
        algorithm_name="kmeans"
    ).first()
    if not cat_result_obj:
        arg_result = SparkAnomaly(appid, start_time, end_time)
        content = arg_result.get_kmeans_predict()
        cat_result_obj = CatResultData.objects.create(
            appid=appid,
            start_time=start_time,
            end_time=end_time,
            algorithm_name="kmeans",
            result_data=content
        )
    ser_data = CatResultDataSerializer(cat_result_obj).data
    return ser_data
