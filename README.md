# Onion Service De-anonymization Tool

**Educational and Research Purposes Only**

A proof-of-concept tool for demonstrating techniques that could potentially de-anonymize Tor hidden services. This project explores and simulates various methods that security researchers might use to identify the real IP addresses and infrastructure behind onion services.

## Disclaimer

This tool is provided for **educational and authorized security research purposes only**. It is designed to demonstrate techniques as a proof of concept to raise awareness about potential vulnerabilities in anonymous services. Using this tool to de-anonymize actual onion services without explicit permission is illegal and unethical.

## Features

This tool demonstrates several de-anonymization techniques:

1. **Circuit Fingerprinting** - Analyzing Tor circuit patterns to identify patterns and anomalies using statistical methods
2. **Traffic Correlation** - Simulating traffic timing correlation to potentially identify the origin server through pattern matching
3. **Hosting Detection** - Identifying hosting provider signatures, virtualization environments, and server fingerprinting
4. **Service Exploitation** - Demonstrating how service-level vulnerabilities and misconfigurations could lead to information disclosure
5. **Historical Data Analysis** - Correlating historical information, clearnet associations, and archived data
6. **Deceptive Payload Generation** - Creating social engineering payloads that could potentially bypass Tor protections
7. **Browser Exploitation** - Detecting WebRTC leaks, DNS leaks, canvas fingerprinting, and other browser-based vulnerabilities

## Security Implications

Understanding these techniques is crucial for:

- **Tor Hidden Service Operators**: To better protect their anonymous services
- **Security Researchers**: To develop more robust anonymity systems
- **Privacy Advocates**: To understand the limitations of current anonymity networks

This project demonstrates why proper server configuration, careful web browsing habits, and understanding of anonymity technologies are critical for maintaining privacy online.

## Components

The toolkit consists of several modular components:

1. **Main Script (`main.py`)** - Core implementation of de-anonymization techniques including:
   - Circuit analysis algorithms
   - Service fingerprinting
   - Historical data correlation
   - Report generation

2. **Traffic Correlation (`traffic_correlation.py`)** - Analyzes network traffic patterns with:
   - Pattern generation algorithms
   - Statistical correlation techniques
   - Traffic visualization tools
   - Timing attack simulations

3. **Browser Exploitation (`browser_exploit.py`)** - Client-side techniques including:
   - WebRTC leak demonstration
   - Canvas fingerprinting methods
   - DNS leak simulation
   - Browser timing analysis

4. **Web Analyzer (`web_analyzer.py`)** - Web interface with:
   - Interactive visualization dashboard
   - Payload testing environment
   - Analysis result displays
   - Confidence scoring system

5. **Runner Script (`run.py`)** - Unified coordination with:
   - Command-line interface
   - Technique orchestration
   - Output management
   - Configurable parameters

## Installation

```bash
# Clone the repository
git clone https://github.com/dev-ansh-r/onion_de-anonymization
cd onion_de-anonymization

# Install required dependencies
pip install -r requirements.txt

# Optional: Set up a virtual environment first
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Dependencies

This project requires the following Python packages:
- requests >= 2.28.0 - For making HTTP requests
- jinja2 >= 3.0.0 - For templating
- flask >= 2.0.0 - For the web interface
- stem >= 1.8.0 - For Tor control protocol interactions
- matplotlib >= 3.5.0 - For data visualization
- pandas >= 1.4.0 - For data analysis
- scikit-learn >= 1.0.0 - For statistical analysis
- numpy >= 1.23.0 - For numerical operations
- scipy >= 1.8.0 - For scientific computing

## Usage

The tool can be used in several modes:

```bash
# Basic usage with default target
python main.py --report

# Specify a different target onion service
python main.py --target abc123def456.onion --report

# Generate only a specific type of payload
python main.py --payload-type javascript

# Run a specific de-anonymization technique
python main.py --technique traffic

# Simulate payload deployment
python main.py --simulate-deploy

# Full analysis with report generation
python main.py --technique all --report --simulate-deploy

# Run all components using the unified runner
python run.py --target [onion_address] --technique all
```

## Web Interface

The toolkit includes a web-based analysis interface for visualizing results:

```bash
# Start the web analyzer interface
python web_analyzer.py
```

The web interface provides:
- A comprehensive dashboard of analysis runs with timestamps and targets
- Detailed view of identified IP addresses with confidence scores
- Interactive visualization of correlation data and confidence metrics
- Access to generated reports, payloads, and traffic analyses
- Sandbox environment for safely testing browser exploits
- Visual representation of circuit fingerprinting results
- Form-based payload generator

## Output

The tool generates several types of output:

- **Payloads** - In the `output/payloads` directory (HTML/JS files)
  - Social engineering templates
  - WebRTC leak demonstrations
  - Canvas fingerprinting tests
  
- **Analysis Results** - In the `output/results` directory (JSON files)
  - Raw correlation data
  - Circuit fingerprinting analysis
  - Server identification results
  
- **Comprehensive Reports** - In the `output/reports` directory (JSON files)
  - Integrated findings across all techniques
  - Confidence scoring
  - Recommended further investigation steps
  
- **Traffic Analysis** - In the `output/traffic` directory (JSON and PNG files)
  - Traffic pattern recordings
  - Correlation visualizations
  - Timing analysis metrics
  
- **Browser Exploits** - In the `output/browser` directory (HTML files)
  - WebRTC leak demonstrations
  - Canvas fingerprinting examples
  - DNS leak simulations
  
- **Logs** - In the `deanon.log` file in the current directory
  - Detailed operation logs
  - Error tracking
  - Performance metrics

## Demo Target

For demonstration purposes, the tool is configured to target a demo onion service running in a local VM:
- Onion Address: `34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion`
- Known VM IP: `192.168.86.131`

This configuration ensures all testing is done in a controlled environment without targeting actual Tor services.

## Technical Overview

### De-anonymization Techniques

1. **Browser-based Exploits**
   - WebRTC leaks: Exploiting WebRTC to bypass Tor and reveal real IP addresses
   - DNS leaks: Detecting when DNS requests bypass the Tor network
   - Browser fingerprinting: Creating unique identifiers based on browser characteristics
   - Timing attacks: Measuring response times to identify patterns

2. **Network Analysis**
   - Traffic correlation: Matching traffic patterns between Tor entry and exit points
   - Timing analysis: Statistical analysis of packet timing
   - Circuit fingerprinting: Identifying patterns in Tor circuit creation
   - Network monitoring simulation: Demonstrating how privileged network positions can be leveraged

3. **Server Identification**
   - Service fingerprinting: Identifying server software versions and configurations
   - Hosting provider identification: Recognizing signatures of hosting companies
   - Error message analysis: Extracting information from error responses
   - Configuration weakness detection: Identifying common security misconfigurations

### Payload Delivery Approaches

The tool simulates several methods for payload delivery:
- Cross-site scripting (XSS): Injecting malicious scripts into trusted websites
- Social engineering: Creating convincing fake pages to trick users
- Iframe injection: Loading malicious content within legitimate pages
- Resource inclusion: Adding remote resources that can leak information

## Visualization and Analysis

The web interface provides advanced visualization features:
- Interactive bar charts for confidence scores of identified IPs
- Time-series plots of traffic correlation data
- Heat maps of circuit fingerprinting results
- Real-time payload testing with sandbox protection
- Confidence scoring system with color-coded indicators
- Drill-down analysis of individual technique results

## Limitations

This proof-of-concept has several limitations:

1. It does not perform actual de-anonymization but simulates the techniques for educational purposes
2. Real-world implementation would require sophisticated network monitoring capabilities
3. Many techniques would require privileged network positions or zero-day vulnerabilities
4. The success rate would vary significantly based on target configuration and Tor network conditions
5. The toolkit doesn't implement advanced attacks that require specialized hardware or state-level resources
6. All techniques are simulated in ways that prevent actual harm to real Tor services

## Defensive Measures

To protect against these types of attacks, Tor hidden service operators should:

1. Ensure complete isolation between clearnet and Tor services
2. Configure servers to prevent information leakage
3. Use up-to-date Tor software and security patches
4. Implement proper firewall rules and network segregation
5. Be aware of browser-based vulnerabilities when accessing admin interfaces

## Future Improvements

Potential improvements for this educational tool:
- Advanced network traffic visualization tools
- Machine learning algorithms for pattern recognition
- More sophisticated browser fingerprinting techniques
- Simulated guard node analysis systems
- Enhanced reporting with remediation recommendations
- Integrated defensive testing capabilities
- Real-time attack detection demonstrations
- Correlation algorithms with higher statistical confidence
