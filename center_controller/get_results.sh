#!/bin/bash

scp -r pi@10.100.188.118:~/ACK_reliability_test/20240109_NodeA1/processed_stats.txt ./results/20240109/20240109_NodeA1/processed_stats_2.txt
scp -r pi@10.100.190.34:~/ACK_reliability_test/20240109_NodeA2/processed_stats.txt ./results/20240109/20240109_NodeA2/processed_stats_2.txt
scp -r pi@10.100.178.31:~/ACK_reliability_test/20240109_NodeC2/processed_stats.txt  ./results/20240109/20240109_NodeC2/processed_stats_2.txt
scp -r pi@10.100.190.25:~/ACK_reliability_test/20240109_NodeC3/processed_stats.txt ./results/20240109/20240109_NodeC3/processed_stats_2.txt
scp -r pi@10.100.177.14:~/ACK_reliability_test/20240109_NodeC1/processed_stats.txt ./results/20240109/20240109_NodeC1/processed_stats_2.txt

