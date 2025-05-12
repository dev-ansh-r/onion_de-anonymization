# Onion Service De-anonymization Toolkit Usage Guide

**IMPORTANT: Educational & Research Purposes Only**

This toolkit demonstrates techniques that could potentially be used to de-anonymize Tor hidden services. It is provided strictly for educational and authorized security research purposes.

## Prerequisites

- Python 3.8 or higher
- Tor Browser (for testing)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/onion_deanon.git
   cd onion_deanon
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Basic Usage

### Running the Full Toolkit

To run all de-anonymization techniques against a target onion service:

```
python run.py --target 34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion
```

This will:
1. Generate deceptive payloads
2. Perform traffic correlation analysis
3. Generate browser-based exploitation code
4. Run circuit fingerprinting
5. Analyze hosting provider indicators
6. Search for service-level vulnerabilities
7. Generate a comprehensive report

### Running Specific Techniques

To run only a specific technique:

```
python run.py --technique traffic
```

Available techniques:
- `traffic` - Traffic correlation analysis
- `browser` - Browser-based exploitation
- `circuit` - Circuit fingerprinting
- `hosting` - Hosting provider detection
- `service` - Service-level exploitation
- `historical` - Historical data analysis

### Output

All results are saved in the `output` directory, organized by run timestamp:

```
output/
  └── run_YYYYMMDD_HHMMSS/
      ├── payloads/        # Generated deceptive payloads
      ├── browser/         # Browser exploitation files
      ├── traffic/         # Traffic correlation analysis
      └── reports/         # Comprehensive reports
```

## Individual Components

You can also run each component separately:

### Traffic Correlation

```
python traffic_correlation.py --target 34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion --visualize
```

This module creates distinctive traffic patterns, sends them to the target (simulated), and then analyzes network traffic to identify correlations.

### Browser Exploitation

```
python browser_exploit.py --variants 3 --simulate-server
```

This generates browser-based exploitation payloads that demonstrate techniques like WebRTC leaks, DNS leaks, canvas fingerprinting, and timing attacks.

### Core De-anonymization

```
python main.py --technique all --report
```

This runs the core de-anonymization techniques and generates a comprehensive report.

## Demo Target

For demonstration purposes, the toolkit is configured to target a demo onion service running in a local VM:
- Onion Address: `34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion`
- Known VM IP: `192.168.86.131`

## Example Workflow

1. Generate browser exploitation payloads:
   ```
   python browser_exploit.py --variants 3
   ```

2. Run traffic correlation analysis:
   ```
   python traffic_correlation.py --target 34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion --pattern-type burst --visualize
   ```

3. Run core de-anonymization techniques:
   ```
   python main.py --target 34iwqw2sficqeksqelyyoo5cnulb622jofbimc5iuq73mjj3abn4vuyd.onion --technique all --report
   ```

4. Or simply run everything at once:
   ```
   python run.py
   ```

## Understanding the Results

The toolkit generates comprehensive reports with:

1. **Potential IP addresses** - Addresses that might be associated with the hidden service
2. **Confidence scores** - How confident the toolkit is in each finding
3. **Traffic pattern correlations** - Visualization of traffic pattern matching
4. **Server fingerprinting** - Details about the server infrastructure
5. **Recommendations** - Next steps for further investigation

## Limitations

This is a proof-of-concept with several limitations:

1. Many techniques are simulated rather than fully implemented
2. Real de-anonymization would require sophisticated network monitoring
3. Tor's security measures are constantly improving
4. Success rates would vary significantly based on target configuration

## Ethical Considerations

Only use this toolkit:
- On systems you own or have explicit permission to test
- For legitimate security research
- In accordance with applicable laws and regulations

## References

For more information on Tor hidden service security:

1. [Tor Project: Hidden Service Protection](https://community.torproject.org/onion-services/advanced/guard-discovery/)
2. [DEFCON: Tor Hidden Service De-anonymization](https://www.defcon.org/html/defcon-25/dc-25-speakers.html)
3. [Academic Research: Circuit Fingerprinting Attacks](https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/kwon) 