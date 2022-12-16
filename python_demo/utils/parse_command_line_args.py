from argparse import ArgumentParser


def parse_command_line_producer_args():
    arg_parser = ArgumentParser()
    
    arg_parser.add_argument("--topic", required=True, help="Topic name")
    arg_parser.add_argument("--bootstrap-servers", required=False, default="localhost:9092", help="Bootstrap server address")
    arg_parser.add_argument("--schema-file", required=True, help="File name of Avro schema to use")
    
    return arg_parser.parse_args()

def parse_command_line_consumer_args():
    arg_parser = ArgumentParser()
    
    arg_parser.add_argument("--topic", required=True, help="Topic name")
    arg_parser.add_argument("--bootstrap-servers", required=False, default="localhost:9092", help="Bootstrap server address")
    arg_parser.add_argument("--group-id", required=True, help="Group id to which consumer belongs")
    arg_parser.add_argument("--schema-file", required=True, help="File name of Avro schema to use")
    
    return arg_parser.parse_args()
