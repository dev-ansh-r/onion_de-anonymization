#!/usr/bin/env python3
# Traffic Correlation Analysis Module
# For educational and research purposes only

import os
import json
import random
import time
import logging
import socket
import datetime
import ipaddress
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("traffic_correlation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("traffic_correlation")

class TrafficCorrelator:
    """
    Advanced traffic correlation analysis module.
    This simulates techniques that could potentially correlate traffic patterns
    between a Tor hidden service and its origin server.
    """
    def __init__(self, target_onion, output_dir="output/traffic"):
        self.target_onion = target_onion
        self.output_dir = output_dir
        self.known_guard_nodes = []
        self.traffic_samples = []
        self.correlation_results = {}
        self.confidence_threshold = 0.7
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        logger.info(f"Initialized traffic correlator for {target_onion}")
    
    def generate_traffic_pattern(self, pattern_type="random", sample_count=100):
        """
        Generate a distinctive traffic pattern to send to the target
        to later correlate with monitored traffic
        """
        logger.info(f"Generating {pattern_type} traffic pattern with {sample_count} samples")
        
        pattern = []
        
        if pattern_type == "random":
            # Random pattern of requests
            for _ in range(sample_count):
                delay = random.uniform(0.1, 2.0)
                pattern.append({
                    "delay": delay,
                    "size": random.randint(200, 2000)
                })
                
        elif pattern_type == "burst":
            # Bursts of requests followed by pauses
            burst_length = random.randint(5, 15)
            pause_length = random.randint(5, 15)
            
            current_mode = "burst"
            count = 0
            
            for _ in range(sample_count):
                if current_mode == "burst":
                    delay = random.uniform(0.1, 0.3)
                    size = random.randint(800, 1500)
                    count += 1
                    if count >= burst_length:
                        current_mode = "pause"
                        count = 0
                else:
                    delay = random.uniform(1.5, 3.0)
                    size = random.randint(100, 300)
                    count += 1
                    if count >= pause_length:
                        current_mode = "burst"
                        count = 0
                
                pattern.append({
                    "delay": delay,
                    "size": size
                })
                
        elif pattern_type == "sequence":
            # Specific sequence pattern that's highly distinctive
            sequence = [0.1, 0.2, 0.5, 1.0, 0.1, 0.1, 2.0]
            for i in range(sample_count):
                seq_index = i % len(sequence)
                pattern.append({
                    "delay": sequence[seq_index],
                    "size": random.randint(200, 2000)
                })
        
        self.traffic_pattern = pattern
        
        # Save the pattern
        pattern_file = os.path.join(self.output_dir, f"pattern_{pattern_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(pattern_file, 'w') as f:
            json.dump(pattern, f, indent=2)
            
        logger.info(f"Traffic pattern generated and saved to: {pattern_file}")
        return pattern
    
    def simulate_traffic_sending(self, monitor_duration=30):
        """
        Simulate sending the traffic pattern to the target
        For educational purposes only - no actual traffic is sent
        """
        logger.info(f"Simulating sending traffic pattern to {self.target_onion}")
        
        if not hasattr(self, 'traffic_pattern'):
            self.generate_traffic_pattern()
        
        # In a real implementation, this would:
        # 1. Connect to the Tor network
        # 2. Send the pattern of requests to the target onion service
        # 3. Log timing and response information
        
        sending_log = {
            "target": self.target_onion,
            "timestamp_start": datetime.datetime.now().isoformat(),
            "pattern_length": len(self.traffic_pattern),
            "expected_duration": sum(p["delay"] for p in self.traffic_pattern),
            "notes": "This is a simulation - no actual traffic sent"
        }
        
        logger.info(f"Pattern would take approximately {sending_log['expected_duration']:.2f} seconds to send")
        logger.info(f"In a real implementation, would now monitor traffic for {monitor_duration} seconds")
        
        # Save the sending log
        log_file = os.path.join(self.output_dir, f"sending_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, 'w') as f:
            json.dump(sending_log, f, indent=2)
        
        return sending_log
    
    def simulate_traffic_monitoring(self, target_ips=None, duration=30):
        """
        Simulate monitoring traffic for the target IP addresses
        """
        logger.info(f"Simulating traffic monitoring for {duration} seconds")
        
        # For demonstration, generate some simulated traffic captures
        captures = []
        
        # Use provided IPs or generate some samples
        if not target_ips:
            target_ips = [
                "192.168.1.1",  # Common router IP
                "10.0.0.1",
                "172.16.0.1"
            ]
        
        # Generate traffic samples for each IP
        for ip in target_ips:
            # We'll set the actual target based on traffic pattern correlation
            # rather than a hardcoded IP address
            is_actual_target = False  # This will be determined by analysis
            
            # For demo purposes, we'll make a random IP show stronger pattern correlations
            # In a real scenario, the actual target would naturally exhibit pattern correlation
            include_pattern = random.random() < 0.3  # 30% chance any IP could have matching pattern
            
            # If we're the first IP in a provided list, give it a higher chance to be the target
            if target_ips and ip == target_ips[0]:
                include_pattern = random.random() < 0.9  # 90% chance the first IP has our pattern
            
            traffic_data = []
            
            if include_pattern and hasattr(self, 'traffic_pattern'):
                # This IP either is our target or we'll make it look similar by chance
                base_time = time.time()
                current_time = base_time
                
                # Add some random traffic before our pattern
                for _ in range(random.randint(5, 20)):
                    current_time += random.uniform(0.1, 1.0)
                    traffic_data.append({
                        "timestamp": current_time,
                        "size": random.randint(100, 2000),
                        "direction": random.choice(["in", "out"])
                    })
                
                # Add our pattern with some noise
                for pattern_item in self.traffic_pattern:
                    current_time += pattern_item["delay"] * random.uniform(0.9, 1.1)  # Add some jitter
                    traffic_data.append({
                        "timestamp": current_time,
                        "size": pattern_item["size"] + random.randint(-100, 100),  # Add some noise
                        "direction": "out" if random.random() < 0.8 else "in"  # Mostly outgoing for pattern
                    })
                
                # Add some random traffic after our pattern
                for _ in range(random.randint(5, 20)):
                    current_time += random.uniform(0.1, 1.0)
                    traffic_data.append({
                        "timestamp": current_time,
                        "size": random.randint(100, 2000),
                        "direction": random.choice(["in", "out"])
                    })
            else:
                # This is not our target, generate random traffic
                base_time = time.time()
                current_time = base_time
                
                for _ in range(random.randint(50, 150)):
                    current_time += random.uniform(0.1, 1.0)
                    traffic_data.append({
                        "timestamp": current_time,
                        "size": random.randint(100, 2000),
                        "direction": random.choice(["in", "out"])
                    })
            
            # Sort by timestamp
            traffic_data.sort(key=lambda x: x["timestamp"])
            
            capture = {
                "ip": ip,
                "is_actual_target": is_actual_target,  # For evaluation only
                "capture_start": base_time,
                "capture_end": traffic_data[-1]["timestamp"],
                "packet_count": len(traffic_data),
                "traffic_data": traffic_data
            }
            
            captures.append(capture)
        
        self.traffic_samples = captures
        
        # Save the captures
        for i, capture in enumerate(captures):
            capture_file = os.path.join(self.output_dir, f"capture_{capture['ip'].replace('.', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            # Remove the traffic_data from the saved file to keep it smaller
            capture_save = capture.copy()
            capture_save["traffic_data_sample"] = capture_save["traffic_data"][:10]  # Just save a sample
            del capture_save["traffic_data"]
            
            with open(capture_file, 'w') as f:
                json.dump(capture_save, f, indent=2)
        
        logger.info(f"Generated {len(captures)} simulated traffic captures")
        return captures
    
    def analyze_traffic_correlation(self):
        """
        Analyze the traffic samples to find correlations with our traffic pattern
        """
        logger.info("Analyzing traffic correlation")
        
        if not hasattr(self, 'traffic_pattern') or not self.traffic_samples:
            logger.error("No traffic pattern or samples available for analysis")
            return None
        
        results = {}
        
        # For each traffic sample
        for sample in self.traffic_samples:
            ip = sample["ip"]
            traffic_data = sample["traffic_data"]
            
            # Extract the time deltas between packets
            time_deltas = []
            for i in range(1, len(traffic_data)):
                time_deltas.append(traffic_data[i]["timestamp"] - traffic_data[i-1]["timestamp"])
            
            # Extract the pattern time deltas
            pattern_deltas = [item["delay"] for item in self.traffic_pattern]
            
            # Find potential matches for our pattern in the time deltas
            matches = self._find_pattern_matches(time_deltas, pattern_deltas)
            
            # Calculate correlation score
            if matches:
                best_match = max(matches, key=lambda m: m["correlation"])
                correlation = best_match["correlation"]
            else:
                best_match = None
                correlation = 0.0
            
            # For demo purposes, we know the actual target
            is_actual_target = sample.get("is_actual_target", False)
            
            results[ip] = {
                "correlation_score": correlation,
                "match_count": len(matches),
                "best_match": best_match,
                "is_actual_target": is_actual_target,  # For evaluation only
                "conclusion": correlation > self.confidence_threshold
            }
        
        self.correlation_results = results
        
        # Save the results
        results_file = os.path.join(self.output_dir, f"correlation_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Generate a summary report
        summary = {
            "target_onion": self.target_onion,
            "analysis_time": datetime.datetime.now().isoformat(),
            "pattern_type": getattr(self, 'pattern_type', "unknown"),
            "ips_analyzed": len(results),
            "potential_matches": [ip for ip, data in results.items() if data["conclusion"]],
            "best_match": max(results.items(), key=lambda x: x[1]["correlation_score"])[0],
            "highest_correlation": max(data["correlation_score"] for data in results.values())
        }
        
        logger.info(f"Traffic correlation analysis complete")
        logger.info(f"Best match: {summary['best_match']} with correlation {summary['highest_correlation']:.4f}")
        
        # Save the summary
        summary_file = os.path.join(self.output_dir, f"correlation_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def _find_pattern_matches(self, time_series, pattern, window_size=None):
        """
        Find potential matches of our pattern in the time series
        using a sliding window approach
        """
        if not pattern or not time_series:
            return []
        
        if window_size is None:
            window_size = len(pattern)
        
        matches = []
        
        # Slide a window through the time series
        for i in range(len(time_series) - window_size + 1):
            window = time_series[i:i+window_size]
            
            # Calculate correlation coefficient between window and pattern
            try:
                correlation, p_value = stats.pearsonr(window, pattern[:window_size])
                
                # If NaN (can happen with constant values), use a different metric
                if np.isnan(correlation):
                    # Calculate normalized Euclidean distance as an alternative
                    distance = np.linalg.norm(np.array(window) - np.array(pattern[:window_size]))
                    max_distance = np.linalg.norm(np.zeros(window_size) - np.array(pattern[:window_size]))
                    if max_distance > 0:
                        correlation = 1 - (distance / max_distance)
                    else:
                        correlation = 0
            except:
                correlation = 0
            
            if correlation > 0.5:  # Only record significant correlations
                matches.append({
                    "start_index": i,
                    "window": window,
                    "correlation": correlation
                })
        
        return matches
    
    def visualize_correlation(self, output_file=None):
        """
        Generate a visualization of the traffic correlation results
        """
        if not self.correlation_results:
            logger.error("No correlation results available to visualize")
            return
        
        # Prepare data for plotting
        ips = list(self.correlation_results.keys())
        correlations = [data["correlation_score"] for data in self.correlation_results.values()]
        is_target = [data["is_actual_target"] for data in self.correlation_results.values()]
        
        # Create a bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(ips, correlations, color=['green' if t else 'blue' for t in is_target])
        
        # Add a horizontal line for the threshold
        ax.axhline(y=self.confidence_threshold, color='r', linestyle='-', label='Threshold')
        
        # Add labels and title
        ax.set_xlabel('IP Address')
        ax.set_ylabel('Correlation Score')
        ax.set_title('Traffic Correlation Analysis Results')
        ax.set_ylim(0, 1)
        
        # Add a legend
        ax.legend(['Confidence Threshold', 'Target IP' if any(is_target) else 'Highest Correlation'])
        
        # Rotate IP labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the visualization
        if output_file is None:
            output_file = os.path.join(self.output_dir, f"correlation_plot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        plt.savefig(output_file)
        logger.info(f"Correlation visualization saved to: {output_file}")
        
        return output_file

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Traffic Correlation Analysis Tool (For Educational Purposes Only)")
    parser.add_argument("--target", required=True, help="Target onion service address")
    parser.add_argument("--output", default="output/traffic", help="Output directory for results")
    parser.add_argument("--pattern-type", choices=["random", "burst", "sequence"], default="burst",
                        help="Type of traffic pattern to generate")
    parser.add_argument("--sample-count", type=int, default=100, help="Number of samples in the traffic pattern")
    parser.add_argument("--monitor-duration", type=int, default=30, help="Duration to monitor traffic (simulated)")
    parser.add_argument("--visualize", action="store_true", help="Generate visualization of results")
    
    args = parser.parse_args()
    
    # Create the correlator
    correlator = TrafficCorrelator(args.target, args.output)
    
    # Generate the traffic pattern
    correlator.generate_traffic_pattern(args.pattern_type, args.sample_count)
    
    # Simulate sending the traffic
    correlator.simulate_traffic_sending(args.monitor_duration)
    
    # Simulate monitoring traffic
    correlator.simulate_traffic_monitoring(duration=args.monitor_duration)
    
    # Analyze the correlation
    summary = correlator.analyze_traffic_correlation()
    
    # Visualize the results if requested
    if args.visualize:
        correlator.visualize_correlation()
    
    # Print a summary
    print("\n=== Traffic Correlation Summary ===")
    print(f"Target: {args.target}")
    print(f"Analysis completed at: {summary['analysis_time']}")
    print(f"Pattern type: {summary['pattern_type']}")
    print(f"IPs analyzed: {summary['ips_analyzed']}")
    print(f"Potential matches: {', '.join(summary['potential_matches']) if summary['potential_matches'] else 'None'}")
    print(f"Best match: {summary['best_match']} (correlation: {summary['highest_correlation']:.4f})")
    print(f"Results saved to: {args.output}")

if __name__ == "__main__":
    main() 