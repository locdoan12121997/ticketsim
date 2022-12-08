from pyspark.sql.types import (IntegerType,
                               DoubleType,
                               StructField,
                               StructType,
                               LongType)

schema = {
    'wait_in_scanner_line': StructType([
        StructField("person", LongType(), True),
        StructField("scannerLine", IntegerType(), True),
        StructField("time", DoubleType(), True),
        StructField("duration", DoubleType(), True)
    ]),
    'wait_in_seller_line': StructType([
        StructField("firstId", LongType(), True),
        StructField("lastId", LongType(), True),
        StructField("sellerLine", IntegerType(), True),
        StructField("time", DoubleType(), True),
        StructField("duration", DoubleType(), True)
    ])
}