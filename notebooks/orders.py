# Databricks notebook source
from pyspark.sql import functions as F, Window
for key in ('input_path','catalog','schema'):
    dbutils.widgets.text(key,'')
path, catalog, schema=[dbutils.widgets.get(k) for k in ('input_path','catalog','schema')]
assert path and catalog and schema, 'Provide all dev parameters'
for value in (catalog,schema):
    assert value.replace('_','').isalnum(), 'Use simple safe identifier'
prefix=f'{catalog}.{schema}.'
raw=spark.read.option('header',True).csv(path)
raw.write.format('delta').mode('overwrite').saveAsTable(prefix+'demo_orders_bronze')
parsed=raw.select(F.expr('try_cast(order_id as bigint)').alias('order_id'),F.expr('try_cast(customer_id as bigint)').alias('customer_id'),F.expr('try_cast(order_date as date)').alias('order_date'),'status',F.expr('try_cast(amount as decimal(19,2))').alias('amount'),F.expr('try_cast(updated_at as timestamp)').alias('updated_at'))
valid=(F.col('order_id')>0)&(F.col('customer_id')>0)&F.col('order_date').isNotNull()&F.col('status').isin('PAID','CANCELLED')&(F.col('amount')>=0)&F.col('updated_at').isNotNull()
assert parsed.filter(~F.coalesce(valid,F.lit(False))).limit(1).count()==0,'Invalid order input'
w=Window.partitionBy('order_id').orderBy(F.col('updated_at').desc(),F.col('status').desc(),F.col('amount').desc(),F.col('customer_id').desc(),F.col('order_date').desc())
silver=parsed.withColumn('rn',F.row_number().over(w)).filter('rn=1').drop('rn')
silver.write.format('delta').mode('overwrite').saveAsTable(prefix+'demo_orders_silver')
silver.filter("status='PAID'").groupBy('order_date').agg(F.count('*').alias('paid_orders'),F.sum('amount').alias('revenue')).write.format('delta').mode('overwrite').saveAsTable(prefix+'demo_daily_revenue')
