# GitHub Copilot prompt sequence

## 01 Project blueprint

Inspect @workspace and data/sales_orders.csv. Design a Fabric sales medallion lab with one Lakehouse lh_sales_medallion, a Copy Data pipeline from Files/incoming/sales_orders.csv to Files/bronze/sales_orders.csv, three Fabric Spark notebooks 01_bronze, 02_silver, 03_gold, and a Power BI star schema. Give precise file names, dependencies, validations, and which steps require Fabric web UI. Do not create resources or claim deployment.

## 02 Bronze code

Read data/sales_orders.csv and .github/copilot-instructions.md. Write a Fabric PySpark notebook that reads Files/bronze/sales_orders.csv as strings, stamps ingested_at and source_file, saves bronze_sales as Delta overwrite, validates 10 rows and displays sample. Do not use pandas for Fabric cloud processing.

## 03 Silver code

Read 01_bronze.py and the CSV. Generate Fabric PySpark transformations for integer order_id, date order_date, decimal price and quantity, trimmed names, reject rows with invalid mandatory fields, deduplicate by order_id using deterministic ordering, derive sales_amount, save silver_sales and silver_rejected_sales as Delta. Add assertions for row count and sum 182250.00.

## 04 Gold code

Read 02_silver.py. Generate PySpark to create dim_customer, dim_product, dim_date and fact_sales from silver_sales; make stable customer_key and product_key; date_key yyyyMMdd; preserve order grain and test dimension key uniqueness, foreign key matches, fact count 10, sum 182250.00. Discuss why customer region might be order-specific instead of a customer attribute.

## 05 Pipeline plan

Explain Fabric UI configuration for pl_sales_medallion: Copy activity reading lh_sales_medallion Files/incoming/sales_orders.csv (Binary) writing Files/bronze/sales_orders.csv, followed by Notebook activities 01_bronze, 02_silver, 03_gold connected on Success. Describe default Lakehouse attachment, save, run, monitor and retry. Do not invent automated VS Code pipeline deployment.

## 06 Review and test

Review all three notebook sources for PySpark correctness, missing imports, accidental local paths, idempotence and data quality. Produce runnable validation code for the Fabric notebook and a failure checklist. Do not report that anything actually ran.

## 07 Power BI build

Using fact_sales, dim_customer, dim_product and dim_date, give steps to create a NEW Power BI semantic model in Fabric, relationships (one dimension to many fact) and DAX Sales Amount = SUM(fact_sales[sales_amount]), Orders = DISTINCTCOUNT(fact_sales[order_id]), Units = SUM(fact_sales[quantity]). Explain report visuals and validation totals.