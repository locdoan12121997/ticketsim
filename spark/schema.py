from pyspark.sql.types import (IntegerType,
                               StringType,
                               DoubleType,
                               StructField,
                               StructType,
                               LongType,
                               BooleanType)

schema = {
    'wait_in_scanner_line': StructType([
        StructField("person", LongType(), True),
        StructField("scannerLine", IntegerType(), True),
        StructField("time", DoubleType(), True),
        StructField("duration", DoubleType(), True)
    ]),
    'wait_in_seller_line': StructType([
        StructField("person", LongType(), True),
        StructField("sellerLine", IntegerType(), True),
        StructField("time", DoubleType(), True),
        StructField("duration", DoubleType(), True)
    ])
}