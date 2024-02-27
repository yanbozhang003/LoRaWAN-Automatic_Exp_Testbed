import base64
import json
import sys
import datetime

def decode_base64(data):
    """Decode base64 encoded data to string."""
    return base64.b64decode(data).decode('utf-8')

def process_log_file(file_content):
    """Process the log file content based on the provided step-by-step guidance."""
    transmission_results = {}

    lines = file_content.split('\n')

    # Find the last occurrence of the specified string
    search_string = "[LoRaWAN] Sending uplink packet || Hello World! #0"
    last_occurrence = -1
    for i in range(len(lines) - 1, -1, -1):
        if search_string in lines[i]:
            last_occurrence = i
            break

    # Check if the string was found; if not, process the file normally
    start_line = last_occurrence if last_occurrence != -1 else 0


    for i in range(start_line, len(lines)):
        if "[LoRaWAN] Sending uplink packet" in lines[i]:
            # Extract the sent message
            sent_message = lines[i].split("||")[1].strip()

            # Initialize list for this message if not already present
            if sent_message not in transmission_results:
                transmission_results[sent_message] = []

            success = 0  # Default to failure
            for j in range(i + 1, len(lines)):
                if "[LoRaWAN] Waiting for downlink" in lines[j]:
                    # Search for success confirmation between the two lines
                    for k in range(i + 1, j):
                        if "TOPIC: application/46f95f5e-fb72-4178-9652-e5976b974ea2/device/70b3d57ed005e1a2/event/up" in lines[k]:
                            try:
                                received_data_part = lines[k].split('"data":"')[1]
                                received_data = received_data_part.split('"')[0]
                                received_message = decode_base64(received_data)
                                if received_message == sent_message:
                                    success = 1  # Successful transmission
                            except IndexError:
                                # In case the data extraction fails
                                continue
                    break

            # Add the success/failure indicator to the list for this message
            transmission_results[sent_message].append(success)

    return transmission_results

def interpret_mac_scheme(mac_num):
    mac_schemes = {0: "ALOHA", 1: "CSMA", 2: "XCSMA2"}
    return mac_schemes.get(mac_num, "Unknown")

RT_num = sys.argv[1]
DN = sys.argv[2]
MAC_num = int(sys.argv[3])
Trace_num = sys.argv[4]

# Interpret the MAC scheme
mac_scheme = interpret_mac_scheme(MAC_num)

# log_file = f'./20240104_allNodes/ALOHA/MAX_RT_{RT_num}/DN_{DN}_tr{Trace_num}.txt'

# Read the file content from the uploaded file
log_filename = f'/home/pi/ACK_reliability_test/20240131_NodeA2/{mac_scheme}/MAX_RT_{RT_num}/DN_{DN}_tr{Trace_num}.txt'
with open(log_filename, "r") as file:
    file_content = file.read()

# Process the log file and get the results
results = process_log_file(file_content)

# Save the results to a JSON file
json_filename = f'/home/pi/ACK_reliability_test/20240131_NodeA2/{mac_scheme}/MAX_RT_{RT_num}/DN_{DN}_tr{Trace_num}.json'
with open(json_filename, 'w') as json_file:
    json.dump(results, json_file, indent=4)


# process json
with open(json_filename, 'r') as file:
    data = json.load(file)

# Initialize counters
tx_frame_count = 0
rx_frame_count = 0
tx_event_count = 0
utx_event_count = 0

# Process data to calculate the required metrics
for key, value in data.items():
    tx_frame_count += 1
    tx_event_count += len(value)
    if 1 in value:
        rx_frame_count += 1
        first_one_index = value.index(1)
        utx_event_count += len(value) - first_one_index - 1
        # if len(value) - first_one_index - 1 > 0:
        #     print(utx_event_count)

# Calculating the metrics
frame_loss_rate = 1 - (rx_frame_count / tx_frame_count) if tx_frame_count > 0 else 0
avg_retransmission = (tx_event_count / tx_frame_count - 1) if tx_frame_count > 0 else 0
unnecessary_retransmission_rate = (utx_event_count / tx_frame_count) if tx_frame_count > 0 else 0

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create the message string
message = f"{current_time} DN: {DN} NRT: {RT_num} MAC: {mac_scheme} Tr: {Trace_num} | Frame loss rate: {frame_loss_rate} Averaged re-transmission: {avg_retransmission} unnecessary re-transmission: {unnecessary_retransmission_rate}"

# Define the path to your log file
stats_file = "/home/pi/ACK_reliability_test/20240131_NodeA2/processed_stats.txt"

# Write the message to a new line in the text file
with open(stats_file, 'a') as file:
    file.write(message + "\n")  # '\n' creates a new line in the file after the message

print("Node A2 completed processing")

# print(f"{current_time} Frame loss rate: {frame_loss_rate} | Averaged re-transmission: {avg_retransmission} | unnecessary re-transmission: {unnecessary_retransmission_rate}")
# print("Frame loss rate: ", frame_loss_rate, " | Averaged re-transmission: ", avg_retransmission, " | unnecessary re-transmission: ", unnecessary_retransmission_rate)


