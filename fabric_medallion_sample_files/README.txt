Fabric Medallion sample data

Bronze: raw data including duplicate order 102 and invalid amounts -500 and 0.
Silver: positive amounts, deduplicated by order_id.
Gold: daily order counts and total revenue from Silver.

Upload bronze_sales.csv into your Fabric Lakehouse Files section, then run this in a Fabric notebook attached to the Lakehouse:

from pyspark.sql import functions as F
bronze = spark.read.option("header", True).option("inferSchema", True).csv("Files/bronze_sales.csv")
bronze.write.format("delta").mode("overwrite").saveAsTable("bronze_sales")
silver = bronze.filter(F.col("amount") > 0).dropDuplicates(["order_id"])
silver.write.format("delta").mode("overwrite").saveAsTable("silver_sales")
gold = silver.groupBy("order_date").agg(F.count("*").alias("total_orders"), F.sum("amount").alias("total_sales"))
gold.write.format("delta").mode("overwrite").saveAsTable("gold_daily_sales")
display(gold.orderBy("order_date"))
