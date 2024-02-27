#!/bin/bash

# Define the sets of values for each parameter
#RT_nums=(0 3 6)
#DNs=(250 150 80 30)
#Trace_nums=(1 2 3)
#MAC_schemes=(0 1 2)
RT_nums=(0)
DNs=(250)
Trace_nums=(1)
MAC_schemes=(0 9 2)

# Define the IP addresses of the remote devices
remote_ips=("10.100.188.118" "10.100.190.34" "10.100.178.31" "10.100.190.25" "10.100.177.14")
#remote_ips=("10.100.188.118")

# Iterate over each combination of parameters
for Trace_num in "${Trace_nums[@]}"
do
    for MAC_scheme in "${MAC_schemes[@]}"
    do
        for RT_num in "${RT_nums[@]}"
        do
            for DN in "${DNs[@]}"
            do
                # Determine the delay based on the value of DN
                if [ $DN -eq 30 ]; then
                    Delay=1800
                elif [ $DN -eq 80 ]; then
                    Delay=1200
                else
                    Delay=1200
                fi

                # Run the Python script with the current set of parameters
                echo "$(date '+%Y-%m-%d %H:%M:%S') New logging started for RT_num=$RT_num, DN=$DN, MAC_scheme=$MAC_scheme, Trace_num=$Trace_num"
                for ip1 in "${remote_ips[@]}"
                    do
                    ssh pi@$ip1 "python3 ~/ACK_reliability_test/bash_setting_logger3.py $RT_num $DN $MAC_scheme $Trace_num $Delay" &
                done
                # python3 ./bash_setting_logger.py $RT_num $DN $Trace_num $Delay
            
                wait

		echo "$(date '+%Y-%m-%d %H:%M:%S') Record done, No processing required."
#                echo "$(date '+%Y-%m-%d %H:%M:%S') Record done, start processing ..."

                # Run log processing
#                for ip2 in "${remote_ips[@]}"
#                    do
#                    ssh pi@$ip2 "python3 ~/ACK_reliability_test/bash_process_log3.py $RT_num $DN $MAC_scheme $Trace_num"
#                done
                # python3 ./bash_process_log.py $RT_num $DN $Trace_num
                
#                echo "$(date '+%Y-%m-%d %H:%M:%S') Processing completed."
            done
        done
    done
done

