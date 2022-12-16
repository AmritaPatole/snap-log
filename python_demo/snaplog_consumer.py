import io
import avro.schema
import avro.io
import avro.datafile
from utils.parse_command_line_args import parse_command_line_consumer_args
from kafka3 import KafkaConsumer


if __name__ == '__main__':
    args = parse_command_line_consumer_args()

    consumer = KafkaConsumer(args.topic, group_id=args.group_id, bootstrap_servers=[args.bootstrap_servers], 
            auto_offset_reset='earliest', enable_auto_commit=True, auto_commit_interval_ms=1000)
    schema_path = "./avro/" + args.schema_file 
    schema = avro.schema.parse(open(schema_path).read())  

    for msg in consumer:
        #bytes_reader = io.BytesIO(msg.value)
        #reader = avro.datafile.DataFileReader(bytes_reader, avro.io.DatumReader())
        #for rec in reader:
        #    print(rec)

        bytes_reader = io.BytesIO(msg.value)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        rec = reader.read(decoder)
        print(rec)

