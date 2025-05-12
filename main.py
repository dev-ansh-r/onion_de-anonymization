#!/usr/bin/env python3
# Onion Service De-anonymization Tool
# For authorized security research and educational purposes only

import argparse
import os
import json
import random
import string
import ipaddress
import subprocess
import requests
import socket
import time
import re
import logging
from datetime import datetime
from jinja2 import Template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("deanon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("onion_deanon")

# Target information (for demo only)
TARGET_ONION = "34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion"
KNOWN_VM_IP = None  # Set to None to make it optional, previously hardcoded as "192.168.86.131"

# Templates for different payload types
TEMPLATES = {
    "html": """
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        /* Additional styles would be here */
    </style>
    <script>
        // Deceptive telemetry script for demonstration purposes
        function reportTelemetry() {
            try {
                // Exploit WebRTC to bypass Tor and reveal real IP (demonstration)
                function attemptWebRTCLeak() {
                    // This would contain actual WebRTC leak code in a real exploit
                    console.log("WebRTC leak technique initiated");
                    
                    // In a real attack, this would use the WebRTC API to establish 
                    // peer connections that might bypass Tor
                }
                
                // DNS leak technique (demonstration)
                function attemptDNSLeak() {
                    // This would contain actual DNS leak code in a real exploit
                    console.log("DNS leak technique initiated");
                    
                    // In a real attack, this might force DNS lookups outside Tor
                }
                
                // Browser fingerprinting technique
                function collectBrowserFingerprint() {
                    const fingerprint = {
                        userAgent: navigator.userAgent,
                        language: navigator.language,
                        platform: navigator.platform,
                        screenDimensions: window.screen.width + "x" + window.screen.height,
                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                        timestamp: new Date().toISOString()
                    };
                    
                    // In a real attack, this would be sent to a collection server
                    console.log("Collected fingerprint:", fingerprint);
                    return fingerprint;
                }
                
                // Timing correlation technique
                function performTimingCorrelation() {
                    // Generate unique pattern of timed requests that could be
                    // correlated with traffic monitoring
                    console.log("Timing correlation initiated");
                    
                    // In a real attack, this would make specific patterns of requests
                    // that could be identified in network traffic
                }
                
                // Execute techniques
                attemptWebRTCLeak();
                attemptDNSLeak();
                const fingerprint = collectBrowserFingerprint();
                performTimingCorrelation();
                
                // Simulate data exfiltration
                const trackingData = {
                    trackingId: "{{ tracking_id }}",
                    timestamp: new Date().toISOString(),
                    fingerprint: fingerprint
                };
                
                // In a real attack, this would use various exfiltration techniques
                // to send data outside of Tor
                console.log("Exfiltration payload:", trackingData);
            } catch (e) {
                console.error("Error in telemetry reporting:", e);
            }
        }
        
        // Execute when page loads
        window.onload = function() {
            // Small delay to ensure page is loaded
            setTimeout(reportTelemetry, 1000);
        };
    </script>
</head>
<body>
    <div class="container">
        <h1>{{ header_text }}</h1>
        <p>{{ main_content }}</p>
        
        <!-- Hidden container for data collection -->
        <div style="display:none;" id="debug-info">
            Server ID: {{ server_id }}
            Debug Mode: {{ debug_mode }}
            Time: <span id="server-time">{{ server_time }}</span>
        </div>
    </div>
</body>
</html>
    """,
    
    "javascript": """
/* 
 * {{ script_name }} - {{ script_description }}
 * Generated on: {{ generation_date }}
 * Version: {{ version }}
 */

// Configuration object
const config = {
    debugMode: {{ debug_mode | lower }},
    serverId: "{{ server_id }}",
    timestamp: {{ timestamp }},
    trackingId: "{{ tracking_id }}",
    features: {{ features | tojson }}
};

// De-anonymization techniques wrapped in deceptive code
function initSystem() {
    if (config.debugMode) {
        console.log("Initializing with server ID: " + config.serverId);
    }
    
    // Main payload execution
    executePayload();
    
    // Process data (cover functionality)
    processData({
        id: "{{ data_id }}",
        source: "{{ data_source }}"
    });
}

// Main payload function containing de-anonymization techniques
function executePayload() {
    // In a real attack, this would contain actual code for:
    // 1. WebRTC leak attempts
    // 2. Browser fingerprinting
    // 3. Timing correlation techniques
    // 4. DNS leak attempts
    // 5. Advanced browser exploitation techniques
    
    // Actual implementation would vary based on target and approach
    
    // Example telemetry data that would be exfiltrated
    const telemetryData = {
        trackingId: config.trackingId,
        timestamp: new Date().toISOString(),
        browser: navigator.userAgent,
        platform: navigator.platform,
        screenSize: window.screen.width + "x" + window.screen.height,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        languages: navigator.languages.join(",")
    };
    
    // In a real attack, this would use sophisticated exfiltration techniques
    console.log("Telemetry data:", telemetryData);
}

// Process data function (cover functionality)
function processData(data) {
    console.log("Processing data: " + data.id);
    // Processing logic would be here
}

// Initialize when loaded
initSystem();
    """
}

class DeceptivePayloadGenerator:
    def __init__(self, payload_type="html", output_dir="payloads", target_onion=TARGET_ONION):
        self.payload_type = payload_type
        self.output_dir = output_dir
        self.tracking_id = self._generate_tracking_id()
        self.target_onion = target_onion
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def _generate_tracking_id(self):
        """Generate a unique tracking ID for the payload"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    def _generate_template_data(self):
        """Generate template data for the payload"""
        return {
            # HTML template variables
            "page_title": "Security Update Required",
            "header_text": "Security Alert",
            "main_content": "Our systems have detected unusual activity on your account. Please verify your identity to continue.",
            "server_id": f"SRV-{self._generate_tracking_id()}",
            "debug_mode": "disabled",
            "server_time": datetime.now().isoformat(),
            "tracking_id": self.tracking_id,
            
            # JavaScript template variables
            "script_name": "SecurityUtil",
            "script_description": "Security verification module",
            "generation_date": datetime.now().strftime("%Y-%m-%d"),
            "debug_mode": "false",
            "timestamp": int(datetime.now().timestamp()),
            "features": {
                "analytics": True,
                "verification": True,
                "protection": True
            },
            "data_id": f"REQ-{self._generate_tracking_id()}",
            "data_source": "security_system",
            "version": "1.0.3"
        }
    
    def generate_payload(self):
        """Generate the deceptive payload based on the selected type"""
        if self.payload_type not in TEMPLATES:
            raise ValueError(f"Unknown payload type: {self.payload_type}")
        
        template_str = TEMPLATES[self.payload_type]
        template = Template(template_str)
        
        # Generate data for the template
        template_data = self._generate_template_data()
        
        # Render the template
        rendered_payload = template.render(**template_data)
        
        # Save the payload to a file
        file_extension = self.payload_type
        if file_extension == "javascript":
            file_extension = "js"
            
        output_filename = os.path.join(self.output_dir, f"payload_{self.tracking_id}.{file_extension}")
        
        with open(output_filename, 'w') as f:
            f.write(rendered_payload)
        
        logger.info(f"Generated payload: {output_filename}")
        return output_filename
    
    def generate_tracking_metadata(self):
        """Generate tracking metadata for the correlation server"""
        tracking_data = {
            "tracking_id": self.tracking_id,
            "creation_time": datetime.now().isoformat(),
            "payload_type": self.payload_type,
            "target_onion": self.target_onion
        }
        
        tracking_file = os.path.join(self.output_dir, f"tracking_{self.tracking_id}.json")
        
        with open(tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=2)
        
        logger.info(f"Generated tracking file: {tracking_file}")
        return tracking_file

class OnionDeanonymizer:
    """
    Class for demonstrating Tor hidden service de-anonymization techniques.
    For educational and research purposes only.
    """
    def __init__(self, target_onion, output_dir="results", target_ip=None):
        self.target_onion = target_onion
        self.output_dir = output_dir
        self.target_ip = target_ip  # Optional known IP for testing/simulation
        self.methods = [
            "circuit_fingerprinting",
            "traffic_correlation",
            "hosting_detection",
            "service_exploitation",
            "historical_data"
        ]
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        logger.info(f"Initialized de-anonymizer for {target_onion}")
    
    def run_all_techniques(self):
        """Run all available de-anonymization techniques"""
        results = {}
        
        for method in self.methods:
            logger.info(f"Running technique: {method}")
            method_func = getattr(self, f"technique_{method}", None)
            if method_func:
                results[method] = method_func()
            else:
                results[method] = {"status": "error", "message": "Method not implemented"}
        
        # Save combined results
        results_file = os.path.join(self.output_dir, f"deanon_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"All techniques completed. Results saved to: {results_file}")
        return results
    
    def technique_circuit_fingerprinting(self):
        """
        Simulate circuit fingerprinting technique
        In a real implementation, this would analyze Tor circuit patterns
        """
        logger.info("Simulating circuit fingerprinting technique")
        
        # This is a simulation - in a real implementation this would:
        # 1. Make requests to the onion service
        # 2. Analyze circuit establishment patterns
        # 3. Look for timing correlations
        
        results = {
            "technique": "circuit_fingerprinting",
            "timestamp": datetime.now().isoformat(),
            "findings": {
                "circuit_pattern_identified": True,
                "estimated_geographic_region": random.choice(["North America", "Europe", "Asia"]),
                "confidence_level": random.uniform(0.6, 0.9)
            }
        }
        
        return results
    
    def technique_traffic_correlation(self):
        """
        Simulate traffic correlation analysis
        In a real implementation, this would correlate traffic patterns
        """
        logger.info("Simulating traffic correlation technique")
        
        # This is a simulation - in a real implementation this would:
        # 1. Generate specific traffic patterns to the onion service
        # 2. Monitor for correlating patterns at network vantage points
        # 3. Apply statistical analysis to identify correlations
        
        results = {
            "technique": "traffic_correlation",
            "timestamp": datetime.now().isoformat(),
            "findings": {
                "correlation_detected": True,
                "potential_ip_ranges": [
                    "192.168.0.0/16",  # Target is in a local VM for demo
                    "10.0.0.0/8"
                ],
                "confidence_level": random.uniform(0.7, 0.95),
                "known_vm_ip": self.target_ip  # For demonstration
            }
        }
        
        return results
    
    def technique_hosting_detection(self):
        """
        Simulate hosting provider detection technique
        In a real implementation, this would analyze for hosting signatures
        """
        logger.info("Simulating hosting detection technique")
        
        # This is a simulation - in a real implementation this would:
        # 1. Analyze server fingerprints
        # 2. Compare against known hosting provider signatures
        # 3. Check for VPS/dedicated hosting indicators
        
        results = {
            "technique": "hosting_detection",
            "timestamp": datetime.now().isoformat(),
            "findings": {
                "hosting_type": "virtualized_environment",
                "potential_providers": [
                    "VirtualBox",  # For demo purposes - actual VM being used
                    "VMware",
                    "Local VM"
                ],
                "confidence_level": 0.85
            }
        }
        
        return results
    
    def technique_service_exploitation(self):
        """
        Simulate service-level exploitation technique
        In a real implementation, this would attempt to identify vulnerabilities
        """
        logger.info("Simulating service exploitation technique")
        
        # This is a simulation - in a real implementation this would:
        # 1. Scan for vulnerabilities in the onion service
        # 2. Attempt controlled exploitation to bypass Tor protections
        # 3. Extract server information that might reveal location
        
        results = {
            "technique": "service_exploitation",
            "timestamp": datetime.now().isoformat(),
            "findings": {
                "vulnerabilities_found": 2,
                "server_info": {
                    "server_type": "Apache",
                    "php_version": "7.4.3",
                    "operating_system": "Ubuntu 20.04"
                },
                "potential_identifiers": {
                    "local_username": "linux",  # Demo value
                    "hostname": "vm-ubuntu",
                    "timezone": "UTC+05:30"
                }
            }
        }
        
        return results
    
    def technique_historical_data(self):
        """
        Simulate historical data analysis
        In a real implementation, this would analyze historical data
        """
        logger.info("Simulating historical data analysis")
        
        # This is a simulation - in a real implementation this would:
        # 1. Search for historical information about the onion service
        # 2. Look for correlations with clearnet services
        # 3. Analyze domain registration, SSL certificates, etc.
        
        results = {
            "technique": "historical_data",
            "timestamp": datetime.now().isoformat(),
            "findings": {
                "service_first_seen": "2023-06-15",
                "related_clearnet_domains": [
                    "example.com",
                    "test-site.net"
                ],
                "registration_details": {
                    "registrar": "NameCheap",
                    "email_pattern": "user***@gmail.com"
                }
            }
        }
        
        return results
    
    def generate_report(self, results):
        """Generate a comprehensive report from all technique results"""
        logger.info("Generating comprehensive de-anonymization report")
        
        # Combine all findings
        combined_findings = {}
        for method, result in results.items():
            if "findings" in result:
                combined_findings[method] = result["findings"]
        
        # Analyze combined findings for convergence
        potential_ips = []
        if "traffic_correlation" in combined_findings:
            if "known_vm_ip" in combined_findings["traffic_correlation"]:
                potential_ips.append(combined_findings["traffic_correlation"]["known_vm_ip"])
        
        # Generate confidence scores
        confidence_scores = {}
        for method, findings in combined_findings.items():
            if "confidence_level" in findings:
                confidence_scores[method] = findings["confidence_level"]
        
        # Create overall report
        report = {
            "target_onion": self.target_onion,
            "analysis_time": datetime.now().isoformat(),
            "techniques_applied": list(results.keys()),
            "potential_identifiers": {
                "ip_addresses": potential_ips,
                "hosting_environments": combined_findings.get("hosting_detection", {}).get("potential_providers", []),
                "server_information": combined_findings.get("service_exploitation", {}).get("server_info", {})
            },
            "confidence_scores": confidence_scores,
            "overall_confidence": sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0,
            "recommendations": [
                "Perform additional targeted scans on identified IP ranges",
                "Monitor identified hosting providers for correlations",
                "Investigate historical domain relationships"
            ]
        }
        
        # Save the report
        report_file = os.path.join(self.output_dir, f"deanon_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"Comprehensive report generated: {report_file}")
        return report

class DeploymentTools:
    """
    Tools for deploying de-anonymization payloads to target onion services
    """
    def __init__(self, target_onion):
        self.target_onion = target_onion
        logger.info(f"Initialized deployment tools for {target_onion}")
    
    def deploy_payload(self, payload_file, method="iframe_injection"):
        """
        Simulate deployment of a payload to the target onion service
        This is a simulation - in a real scenario this would be a social engineering
        or vulnerability exploitation approach
        """
        logger.info(f"Simulating payload deployment via {method}")
        
        deployment_result = {
            "status": "simulated",
            "target": self.target_onion,
            "payload": os.path.basename(payload_file),
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "notes": "This is a simulation for educational purposes"
        }
        
        logger.info(f"Payload deployment simulated: {method}")
        return deployment_result
    
    def analyze_deployment_vectors(self):
        """
        Analyze potential deployment vectors for the target
        """
        logger.info("Analyzing potential deployment vectors")
        
        # In a real scenario, this would scan for vulnerabilities,
        # input vectors, or other ways to deliver payloads
        
        vectors = [
            {
                "type": "xss",
                "location": "search parameter",
                "difficulty": "medium",
                "notes": "Requires user interaction"
            },
            {
                "type": "social_engineering",
                "location": "messaging system",
                "difficulty": "easy",
                "notes": "Requires crafting convincing message"
            },
            {
                "type": "iframe_injection",
                "location": "profile page",
                "difficulty": "hard",
                "notes": "Requires authentication"
            }
        ]
        
        logger.info(f"Identified {len(vectors)} potential deployment vectors")
        return vectors

def main():
    parser = argparse.ArgumentParser(description="Onion De-anonymization Toolkit (Educational Purposes Only)")
    parser.add_argument("--target", default=TARGET_ONION, help="Target .onion address")
    parser.add_argument("--ip", default=KNOWN_VM_IP, help="Optional IP address of target (for testing/simulation)")
    parser.add_argument("--output", default="output", help="Output directory for results")
    parser.add_argument("--technique", choices=["all", "circuit", "traffic", "hosting", "service", "historical"], 
                      default="all", help="De-anonymization technique to run")
    parser.add_argument("--payload-type", choices=["html", "javascript"], default="html", 
                      help="Type of payload to generate")
    parser.add_argument("--simulate-deploy", action="store_true",
                      help="Simulate payload deployment (educational demonstration only)")
    parser.add_argument("--report", action="store_true",
                      help="Generate comprehensive report")
    
    args = parser.parse_args()
    
    # Create output directories
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    payloads_dir = os.path.join(args.output, "payloads")
    results_dir = os.path.join(args.output, "results")
    
    for directory in [args.output, payloads_dir, results_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Generate payload
    logger.info(f"Generating {args.payload_type} payload for {args.target}")
    generator = DeceptivePayloadGenerator(
        payload_type=args.payload_type,
        output_dir=payloads_dir,
        target_onion=args.target
    )
    
    payload_file = generator.generate_payload()
    generator.generate_tracking_metadata()
    
    # Run de-anonymization techniques
    deanonymizer = OnionDeanonymizer(args.target, output_dir=results_dir, target_ip=args.ip)
    
    if args.technique == "all":
        results = deanonymizer.run_all_techniques()
    else:
        # Run specific technique
        technique_method = getattr(deanonymizer, f"technique_{args.technique}")
        results = {args.technique: technique_method()}
    
    # Simulate payload deployment if requested
    if args.simulate_deploy:
        deployer = DeploymentTools(args.target)
        deploy_result = deployer.deploy_payload(payload_file)
        logger.info(f"Deployment simulation completed with status: {deploy_result.get('status', 'unknown')}")
    
    # Generate comprehensive report if requested
    if args.report:
        report = deanonymizer.generate_report(results)
        logger.info(f"Report generated with overall confidence: {report['overall_confidence']:.2f}")
    
    return 0

if __name__ == "__main__":
    main()