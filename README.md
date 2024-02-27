# LoRaWAN-Automatic_Exp_Testbed
 
This repository constructs a LoRaWAN testbed for easy experimenting and post traffic analysis. The code is in compatible with Chirpstack implementation of LoRaWAN network server. 

It allows for automatic parameters iteration, which contains:
1) MAC layer configuration: ALOHA or [CSMA](https://resources.lora-alliance.org/technical-recommendations/tr013-1-0-0-csma)
2) Re-transmission configuration: NRT of 0/3/6
3) Thousands-device emulation

During experimentation, each node collects network traffic that is triggered by its uplink transmission. The traffic data includes:
1) Serial data: obtained directly from end-node serial print, indicating the successful/failure of each uplink transmission and downlink reception.
2) MQTT data: obtained by subscribing to the Chirpstack MQTT broker, which logs detailed backhaul info, e.g., gateway forwarding, successful network server receiving, network server downlink commanding, gateway downlink sending, etc.

With the traffic data, end-to-end analysis can be carried out in depth. E.g.,
1) UL/DL PRR calculation
2) ALOHA/CSMA performance comparison
3) Re-transmission effectiveness test

The picture below shows the running flow and control logic of the code in this repository:

![alt text](https://github.com/yanbozhang003/LoRaWAN-Automatic_Exp_Testbed/blob/main/Picture1.png)
