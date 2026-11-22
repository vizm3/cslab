# Working principle - The program works in five steps:

# Packet Capture: Scapy captures network packets from the selected interface.
# Packet Counting: Each captured packet increments the packet counter.
# Time Monitoring: Packets are counted during a specified time interval.
# Threshold Detection: The program compares the packet count against the configured threshold.
# Alert Generation: If the count exceeds the threshold, a warning is displayed.

#sudo python3 packets_monitoring.py

from scapy.all import sniff
import time
import argparse

# Default configuration
PACKET_THRESHOLD = 100
TIME_INTERVAL = 10

packet_count = 0


# Function to count captured packets
def packet_callback(packet):
    global packet_count
    packet_count += 1


# Function to monitor network traffic
def monitor_network(threshold, interval, interface):

    global packet_count

    print("--------------------------------------")
    print("     NETWORK TRAFFIC MONITOR")
    print("--------------------------------------")

    print(f"Packet Threshold : {threshold}")
    print(f"Time Interval    : {interval} seconds")
    print(f"Interface        : {interface or 'Default'}")
    print("--------------------------------------")

    try:
        while True:

            packet_count = 0

            # Capture packets for the specified interval
            sniff(
                iface=interface,
                prn=packet_callback,
                store=False,
                timeout=interval
            )

            print(f"\nPackets captured: {packet_count}")

            # Check packet threshold
            if packet_count > threshold:

                print("\n[!!!] NETWORK TRAFFIC ALERT [!!!]")
                print("WARNING: Packet threshold exceeded!")
                print(f"Packets detected: {packet_count}")
                print(f"Allowed threshold: {threshold}")

            else:
                print("[OK] Network traffic is normal.")

            print("--------------------------------------")

    except KeyboardInterrupt:
        print("\nNetwork monitoring stopped.")


# Main program
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Network Traffic Monitoring System"
    )

    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=PACKET_THRESHOLD,
        help="Maximum packet threshold"
    )

    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=TIME_INTERVAL,
        help="Monitoring interval in seconds"
    )

    parser.add_argument(
        "-n", "--interface",
        type=str,
        default=None,
        help="Network interface to monitor"
    )

    args = parser.parse_args()

    if args.threshold < 0 or args.interval <= 0:
        parser.error("Threshold must be non-negative and interval must be positive.")

    monitor_network(
        args.threshold,
        args.interval,
        args.interface
    )
