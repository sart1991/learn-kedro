import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px  # noqa:  F401
import plotly.graph_objs as go
import seaborn as sn
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import SparkSession


# This function uses plotly.express
def compare_passenger_capacity_exp(preprocessed_shuttles: SparkDataFrame):
    spark = SparkSession.builder.appName("PassengerCapacityComparison").getOrCreate()

    # Register the DataFrame as a temporary table
    preprocessed_shuttles.createOrReplaceTempView("shuttles")

    # Perform the grouping and aggregation using SQL
    query = """
            SELECT shuttle_type, AVG(passenger_capacity) as passenger_capacity
            FROM shuttles
            GROUP BY shuttle_type
        """
    grouped_data = spark.sql(query)
    # Convert Spark DataFrame to Pandas for visualization
    pandas_grouped_data = grouped_data.toPandas()
    return pandas_grouped_data


def compare_passenger_capacity_go(preprocessed_shuttles: SparkDataFrame):
    spark = SparkSession.builder.appName("PassengerCapacityComparison").getOrCreate()

    # Register the DataFrame as a temporary table
    preprocessed_shuttles.createOrReplaceTempView("shuttles")

    # Perform the grouping and aggregation using SQL
    query = """
        SELECT shuttle_type, AVG(passenger_capacity) as avg_passenger_capacity
        FROM shuttles
        GROUP BY shuttle_type
    """
    grouped_data = spark.sql(query)

    # Convert Spark DataFrame to Pandas for visualization
    pandas_grouped_data = grouped_data.toPandas()

    # Create the Plotly figure
    fig = go.Figure(
        [
            go.Bar(
                x=pandas_grouped_data["shuttle_type"],
                y=pandas_grouped_data["avg_passenger_capacity"],
            )
        ]
    )

    return fig


def create_confusion_matrix(
    y_test: pd.Series, y_pred: pd.Series
):
    """Plots the evaluation results.

    Args:
        y_test: Testing data for price.
        y_pred: Predicted price.
    """

    data = {"y_Actual": y_test, "y_Predicted": y_pred}
    df = pd.DataFrame(data, columns=["y_Actual", "y_Predicted"])
    confusion_matrix = pd.crosstab(
        df["y_Actual"], df["y_Predicted"], rownames=["Actual"], colnames=["Predicted"]
    )
    sn.heatmap(confusion_matrix, annot=True)
    return plt
