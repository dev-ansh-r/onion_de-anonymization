#!/usr/bin/env python3
# Onion Service De-anonymization Toolkit Runner
# For educational and research purposes only

import os
import sys
import time
import argparse
import logging
import subprocess
import datetime
import json

# Import our modules
try:
    from main import OnionDeanonymizer, DeceptivePayloadGenerator, DeploymentTools
    from traffic_correlation import TrafficCorrelator
    from browser_exploit import BrowserExploitGenerator
    MODULES_IMPORTED = True
except ImportError:
    MODULES_IMPORTED = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("deanon_toolkit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("deanon_toolkit")

# Default target information
DEFAULT_TARGET = "34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion"
DEFAULT_VM_IP = None  # Changed from a hardcoded IP to None to make it optional

class DeAnonymizationToolkit:
    """
    Unified toolkit for demonstrating Tor hidden service de-anonymization techniques.
    This is for educational and research purposes only.
    """
    def __init__(self, target_onion=DEFAULT_TARGET, base_output_dir="output", target_ip=DEFAULT_VM_IP):
        self.target_onion = target_onion
        self.target_ip = target_ip
        self.base_output_dir = base_output_dir
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(base_output_dir, f"run_{self.timestamp}")
        
        # Create output directories
        self.dirs = {
            "base": self.output_dir,
            "payloads": os.path.join(self.output_dir, "payloads"),
            "browser": os.path.join(self.output_dir, "browser"),
            "traffic": os.path.join(self.output_dir, "traffic"),
            "reports": os.path.join(self.output_dir, "reports")
        }
        
        for dir_path in self.dirs.values():
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        logger.info(f"Initialized de-anonymization toolkit for {target_onion}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def run_full_analysis(self):
        """
        Run a complete de-anonymization analysis using all available techniques
        """
        logger.info("Starting full de-anonymization analysis")
        
        results = {
            "target": self.target_onion,
            "timestamp": datetime.datetime.now().isoformat(),
            "techniques": {},
            "identified_ips": [],
            "overall_confidence": 0
        }
        
        # Run traffic correlation
        if self._check_module_available("traffic_correlation"):
            logger.info("Running traffic correlation analysis")
            traffic_results = self.run_traffic_correlation()
            results["techniques"]["traffic_correlation"] = traffic_results
            
            # Extract any identified IPs
            if "best_match" in traffic_results:
                results["identified_ips"].append({
                    "ip": traffic_results["best_match"],
                    "confidence": traffic_results["highest_correlation"],
                    "source": "traffic_correlation"
                })
        
        # Run browser exploit generation
        if self._check_module_available("browser_exploit"):
            logger.info("Generating browser exploitation payloads")
            browser_results = self.generate_browser_exploits()
            results["techniques"]["browser_exploit"] = browser_results
            
            # Extract any identified IPs from simulated data
            if "identified_ips" in browser_results:
                for ip in browser_results["identified_ips"]:
                    results["identified_ips"].append({
                        "ip": ip,
                        "confidence": 0.8,  # Simulated confidence
                        "source": "browser_exploit"
                    })
        
        # Run core de-anonymization techniques
        if self._check_module_available("main"):
            logger.info("Running core de-anonymization techniques")
            core_results = self.run_core_techniques()
            results["techniques"]["core"] = core_results
            
            # Extract any identified IPs
            if "potential_identifiers" in core_results and "ip_addresses" in core_results["potential_identifiers"]:
                for ip in core_results["potential_identifiers"]["ip_addresses"]:
                    results["identified_ips"].append({
                        "ip": ip,
                        "confidence": core_results.get("overall_confidence", 0.7),
                        "source": "core_techniques"
                    })
        
        # Calculate overall confidence based on all techniques
        if results["identified_ips"]:
            results["overall_confidence"] = sum(ip_data["confidence"] for ip_data in results["identified_ips"]) / len(results["identified_ips"])
        
        # Generate the final comprehensive report
        report_file = os.path.join(self.dirs["reports"], f"comprehensive_report_{self.timestamp}.json")
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Comprehensive analysis completed. Report saved to: {report_file}")
        
        # Print a summary
        self._print_summary(results)
        
        return results
    
    def run_traffic_correlation(self):
        """
        Run traffic correlation analysis
        """
        try:
            # Create traffic correlator
            correlator = TrafficCorrelator(
                self.target_onion,
                output_dir=self.dirs["traffic"]
            )
            
            # Generate a distinctive traffic pattern
            correlator.generate_traffic_pattern("burst", 100)
            
            # Simulate sending the traffic
            correlator.simulate_traffic_sending(30)
            
            # Simulate traffic monitoring - use a dynamic list of IPs for monitoring
            # If a target IP is provided, include it first in the list
            target_ips = []
            if self.target_ip:
                target_ips.append(self.target_ip)
            
            # Add some common local network IPs for demonstration purposes
            target_ips.extend(["192.168.1.1", "10.0.0.1", "172.16.0.1"])
            
            correlator.simulate_traffic_monitoring(target_ips, 30)
            
            # Analyze the correlation
            summary = correlator.analyze_traffic_correlation()
            
            # Generate visualization
            correlator.visualize_correlation()
            
            logger.info("Traffic correlation analysis completed")
            return summary
            
        except Exception as e:
            logger.error(f"Error running traffic correlation: {str(e)}")
            return {"error": str(e)}
    
    def generate_browser_exploits(self):
        """
        Generate browser exploitation payloads
        """
        try:
            # Create browser exploit generator
            generator = BrowserExploitGenerator(output_dir=self.dirs["browser"])
            
            # Generate different variants
            variants = generator.generate_target_variants(3)
            
            # Simulate a server receiving exploitation data
            server_result = generator.simulate_exploitation_server()
            
            logger.info(f"Generated {len(variants)} browser exploit variants")
            
            return {
                "variants": [variant["type"] for variant in variants],
                "exploit_files": [variant["files"]["exploit"] for variant in variants],
                "data_file": server_result["data_file"],
                "summary_file": server_result["summary_file"],
                "identified_ips": server_result["identified_ips"]
            }
            
        except Exception as e:
            logger.error(f"Error generating browser exploits: {str(e)}")
            return {"error": str(e)}
    
    def run_core_techniques(self):
        """
        Run core de-anonymization techniques
        """
        try:
            # Create payload generator
            generator = DeceptivePayloadGenerator(
                payload_type="html",
                output_dir=self.dirs["payloads"],
                target_onion=self.target_onion
            )
            
            # Generate payload
            payload_file = generator.generate_payload()
            generator.generate_tracking_metadata()
            
            # Run de-anonymization techniques
            deanonymizer = OnionDeanonymizer(self.target_onion, output_dir=self.dirs["reports"])
            results = deanonymizer.run_all_techniques()
            
            # Generate report
            report = deanonymizer.generate_report(results)
            
            # Simulate payload deployment
            deployer = DeploymentTools(self.target_onion)
            deploy_result = deployer.deploy_payload(payload_file)
            
            logger.info("Core de-anonymization techniques completed")
            
            return report
            
        except Exception as e:
            logger.error(f"Error running core techniques: {str(e)}")
            return {"error": str(e)}
    
    def run_single_technique(self, technique):
        """
        Run a single specific de-anonymization technique
        """
        logger.info(f"Running single technique: {technique}")
        
        if technique == "traffic":
            return self.run_traffic_correlation()
        elif technique == "browser":
            return self.generate_browser_exploits()
        elif technique == "circuit" or technique == "hosting" or technique == "service" or technique == "historical":
            # Map to specific core technique
            try:
                deanonymizer = OnionDeanonymizer(self.target_onion, output_dir=self.dirs["reports"])
                
                # Map technique name to method
                technique_map = {
                    "circuit": "circuit_fingerprinting",
                    "hosting": "hosting_detection",
                    "service": "service_exploitation",
                    "historical": "historical_data"
                }
                
                method = technique_map.get(technique)
                if method:
                    method_func = getattr(deanonymizer, f"technique_{method}", None)
                    if method_func:
                        result = method_func()
                        logger.info(f"Completed {technique} technique")
                        return result
            
            except Exception as e:
                logger.error(f"Error running {technique} technique: {str(e)}")
                return {"error": str(e)}
        
        logger.error(f"Unknown technique: {technique}")
        return {"error": f"Unknown technique: {technique}"}
    
    def _check_module_available(self, module_name):
        """Check if a module is available"""
        if not MODULES_IMPORTED:
            # Try to run as subprocess
            return True
        
        if module_name == "traffic_correlation":
            return 'TrafficCorrelator' in globals()
        elif module_name == "browser_exploit":
            return 'BrowserExploitGenerator' in globals()
        elif module_name == "main":
            return 'OnionDeanonymizer' in globals()
        
        return False
    
    def _print_summary(self, results):
        """Print a human-readable summary of results"""
        print("\n" + "="*60)
        print(f" DE-ANONYMIZATION SUMMARY FOR {self.target_onion}")
        print("="*60)
        
        print(f"\nAnalysis completed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Techniques applied: {', '.join(results['techniques'].keys())}")
        
        if results["identified_ips"]:
            print("\nPOTENTIAL IDENTIFIED IPs:")
            for ip_data in results["identified_ips"]:
                print(f"  • {ip_data['ip']} (confidence: {ip_data['confidence']:.2f}, source: {ip_data['source']})")
            print(f"\nOverall confidence: {results['overall_confidence']:.2f}")
        else:
            print("\nNo IPs identified with sufficient confidence.")
        
        print(f"\nFull report saved to: {self.dirs['reports']}")
        print("="*60)
        print("\nDISCLAIMER: This is a simulation for educational purposes only.")
        print("No actual de-anonymization has occurred.")
        print("="*60 + "\n")

def run_as_subprocess(script, args):
    """Run a script as a subprocess"""
    cmd = [sys.executable, script] + args
    logger.info(f"Running as subprocess: {' '.join(cmd)}")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        logger.error(f"Subprocess failed with error code {process.returncode}")
        logger.error(stderr)
        return {"error": stderr}
    
    logger.info("Subprocess completed successfully")
    
    # Try to parse the output as JSON
    try:
        if stdout.strip().startswith("{") and stdout.strip().endswith("}"):
            return json.loads(stdout)
    except:
        pass
    
    return {"output": stdout}

def main():
    """
    Main function to parse arguments and run the toolkit
    """
    parser = argparse.ArgumentParser(description='Onion Service De-anonymization Toolkit (For Educational Purposes Only)')
    parser.add_argument('--target', type=str, default=DEFAULT_TARGET, help='Target .onion address')
    parser.add_argument('--ip', type=str, default=DEFAULT_VM_IP, help='Optional known IP address of the target (for testing/simulation)')
    parser.add_argument('--technique', type=str, default='all', help='Technique to run (all, traffic, browser, circuit, hosting, service, historical)')
    parser.add_argument('--report', action='store_true', help='Generate a comprehensive report')
    parser.add_argument('--simulate-deploy', action='store_true', help='Simulate payload deployment')
    parser.add_argument('--payload-type', type=str, default='html', help='Type of payload to generate (html, js)')
    parser.add_argument('--output-dir', type=str, default='output', help='Base output directory')
    
    args = parser.parse_args()
    
    # Display disclaimer
    print("\n" + "="*80)
    print("  DISCLAIMER: FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY")
    print("  This toolkit demonstrates techniques as a proof of concept.")
    print("  Using this on actual Tor hidden services without permission is illegal.")
    print("="*80 + "\n")
    
    # Run the toolkit
    toolkit = DeAnonymizationToolkit(
        target_onion=args.target,
        base_output_dir=args.output_dir,
        target_ip=args.ip
    )
    
    # Run the selected technique
    if args.technique == 'all':
        results = toolkit.run_full_analysis()
    else:
        results = toolkit.run_single_technique(args.technique)
    
    if args.report:
        print("\nReport generated in:", toolkit.dirs["reports"])
    
    if args.simulate_deploy:
        if MODULES_IMPORTED:
            deployer = DeploymentTools(args.target)
            print("\nSimulating payload deployment...")
            deploy_result = deployer.deploy_payload(None, simulation=True)
            print("Simulation completed:", deploy_result.get("status", "unknown"))
        else:
            print("\nCannot simulate deployment: modules not imported")
    
    return 0

if __name__ == "__main__":
    main() 