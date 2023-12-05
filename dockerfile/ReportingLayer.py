import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: structured_network_wordcount.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    checkpointDir=sys.argv[3]
    partitionPath=sys.argv[4]

spark = SparkSession\
.builder\
.appName("Reportingtable")\
.getOrCreate()

    # Create DataFrame representing the stream of input lines from connection to host:port
# table = spark.readStream.format('socket').option('host', host).option('port', port).load()

# table = spark.readStream.format("delta").load("file:///home/munais2")
lines = spark.readStream.format("delta").load("file:///home/munais2")
table=lines.select("EPP_IP","EPP_IP2","EPP_IP3","Log_ID","Client_Computer","IP_Address","MAC_Address","Serial_Number","OS","Client_User","Content_Policy","Content_Policy_Type","Destination_Type","Destination","Device_VID","Device_PID","Device_Serial","EPP_Client_Version","File_Name","File_Hash","File_Size","Matched_Item","Item_Details","Date_Time_Server","Date_Time_Client","Date_Time_Server_UTC","Date_Time_Client_UTC","date","client_date")


    
DeltaPath="/home/restore2"
checkpoint_path="/home/restore/checkpoint"  
query=table.writeStream \
.partitionBy("Date","EPP_IP2","Content_Policy","client_date",'Client_User',"Destination","Destination_Type","Matched_Item","Item_Details") \
.format("delta") \
.outputMode("append") \
.option("mergeSchema", "true") \
.option("checkpointLocation", checkpoint_path) \
.trigger(processingTime='10 seconds') \
.start(DeltaPath)
query.awaitTermination()


    
   

 