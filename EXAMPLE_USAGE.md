# Example Usage: Onion De-anonymization Toolkit

This document provides examples of how to use the toolkit for educational purposes.

## Basic Usage (Onion Address Only)

You can run the toolkit with just an onion address, without specifying an IP:

```bash
python run.py --target yourtarget.onion --technique all --report
```

This will:
1. Target the specified onion address
2. Run all de-anonymization techniques
3. Generate a comprehensive report

## Full Analysis with Visualization

For a complete analysis with visualization:

```bash
python run.py --target yourtarget.onion --technique all --report
python web_analyzer.py
```

Then open your browser to http://localhost:5000 to see the results.

## Using Specific Techniques

You can run specific techniques individually:

```bash
# Run traffic correlation only
python run.py --target yourtarget.onion --technique traffic --report

# Run browser exploitation only
python run.py --target yourtarget.onion --technique browser --report
```

## Testing with Known IP (For VM Testing)

If you're testing in a controlled environment with a VM, you can specify the IP:

```bash
python run.py --target yourtarget.onion --ip 192.168.1.100 --technique all --report
```

This helps in validating the toolkit in a controlled environment where you know the actual IP.

## Payload Generation Only

If you just want to generate payloads without running analysis:

```bash
python main.py --target yourtarget.onion --payload-type html
```

## Web Interface

The web interface provides a user-friendly way to view results:

1. Run an analysis using the command line tools
2. Start the web interface: `python web_analyzer.py`
3. Open your browser to http://localhost:5000
4. View the analysis results, visualizations, and identified IPs

## Important Notes

- This toolkit is for educational purposes only
- All IP identification is simulated in this toolkit
- Using such techniques on actual Tor hidden services without permission is illegal
- For research, always use in controlled environments 