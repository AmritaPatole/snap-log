import socket
import io
import random
import avro.schema
from avro.io import DatumWriter
from kafka3 import KafkaProducer
from utils.parse_command_line_args import parse_command_line_producer_args

def CreateKafkaProducer(args):
    bootstrap_servers = [args.bootstrap_servers]
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
    schema_path = "./avro/" + args.schema_file
    schema = avro.schema.parse(open(schema_path).read())
    return producer, schema

def ReadFromSocket():
    server_socket = socket.socket() 
    server_socket.bind(('localhost', 5000))
    server_socket.listen(2)
    print("socket name: "+ str(server_socket.getsockname()))

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    return server_socket, conn, address

def ParseRecord(record):
    record_array = bytearray(record)

    vpc_id = record_array[0:2]
    vpc_id = int.from_bytes(vpc_id, "big")

    vnic_id = record_array[2:4]
    vnic_id = int.from_bytes(vnic_id, "big")

    sip = record_array[4:8]
    sip = int.from_bytes(sip, "big")

    dip = record_array[8:12]
    dip = int.from_bytes(dip, "big")

    proto = record_array[12:13]
    proto = int.from_bytes(proto, "big")

    padding = record_array[13:15]
    padding = int.from_bytes(padding, "big")

    icmp_type = record_array[15:16]
    icmp_type = int.from_bytes(icmp_type, "big")

    icmp_code = record_array[16:17]
    icmp_code = int.from_bytes(icmp_code, "big")

    flow_dir = record_array[17:18]
    flow_dir = int.from_bytes(flow_dir, "big")

    vlan_id = record_array[18:20]
    vlan_id = int.from_bytes(vlan_id, "big")

    pkt_count = record_array[20:28]
    pkt_count = int.from_bytes(pkt_count, "big")
    
    byte_count = record_array[28:36]
    byte_count = int.from_bytes(byte_count, "big")

    pkt_drop_count = record_array[36:44]
    pkt_drop_count = int.from_bytes(pkt_drop_count, "big")
    
    byte_drop_count = record_array[44:52]
    byte_drop_count = int.from_bytes(byte_drop_count, "big")

    pkt_delta_count = record_array[52:60]
    pkt_delta_count = int.from_bytes(pkt_delta_count, "big")
    
    byte_delta_count = record_array[60:68]
    byte_delta_count = int.from_bytes(byte_delta_count, "big")

    pkt_delta_drop_count = record_array[68:76]
    pkt_delta_drop_count = int.from_bytes(pkt_delta_drop_count, "big")
    
    byte_delta_drop_count = record_array[76:84]
    byte_delta_drop_count = int.from_bytes(byte_delta_drop_count, "big")

    flow_start = record_array[84:92]
    flow_start = int.from_bytes(flow_start, "big")

    flow_end = record_array[92:100]
    flow_end = int.from_bytes(flow_end, "big")

    flow_last = record_array[100:108]
    flow_last = int.from_bytes(flow_last, "big")

    flow_id = record_array[108:116]
    flow_id = int.from_bytes(flow_id, "big")

    exp_ip_add = record_array[116:120]
    exp_ip_add = int.from_bytes(exp_ip_add, "big")

    flow_end = record_array[120:121]
    flow_end = int.from_bytes(flow_end, "big")

    pad2 = record_array[121:122]
    pad2 = int.from_bytes(pad2, "big")

    pad3 = record_array[122:123]
    pad3 = int.from_bytes(pad3, "big")
    
    data_record = {"vpcid": vpc_id, "vnicid": vnic_id, "sip": sip, "dip": dip, "protocol": proto, 
            "padding": padding, "icmp_type": icmp_type, "icmp_code": icmp_code, "flow_direction": flow_dir,
            "vlan_id": vlan_id, "pkt_count": pkt_count, "bytes_count": byte_count, "pkt_drop_count": pkt_drop_count, 
            "byte_drop_count": byte_drop_count, "pkt_delta_count": pkt_delta_count, 
            "byte_delta_count": byte_delta_count, "pkt_drop_delta_count": pkt_delta_drop_count, 
            "byte_drop_delta_count": byte_delta_drop_count, "flow_start_time": flow_start,
            "flow_end_time": flow_end, "flow_last_time": flow_last, "flow_id": flow_id, "exporter_ip": exp_ip_add, 
            "flow_end_reason": flow_end, "pad2": pad2, "pad3": pad3}

    return data_record

if __name__ == "__main__":
    args = parse_command_line_producer_args()
    producer, schema = CreateKafkaProducer(args)
    server_socket, conn, address = ReadFromSocket()

    while True:
        record = conn.recv(123)
        if not record:
            continue;
        kafka_message = ParseRecord(record)
        
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(kafka_message, encoder)
        raw_bytes = bytes_writer.getvalue()
        producer.send(args.topic, raw_bytes)
        producer.flush()
