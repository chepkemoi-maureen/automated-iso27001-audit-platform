
# ISO 27001 Linux Compliance Audit Platform

## Overview

The **ISO 27001 Linux Compliance Audit Platform** is a cybersecurity automation tool developed to support security compliance assessment by identifying configuration weaknesses in Linux systems and mapping technical findings against **ISO/IEC 27001:2022 security controls**.

The platform reduces the time and effort required for manual compliance audits by automating evidence collection, security checks, compliance evaluation, and reporting.

This project was developed as part of an MSc Cybersecurity research project focused on improving the effectiveness of information security compliance assessments through automation.

---

## Problem Statement

Traditional ISO 27001 compliance audits often rely heavily on manual evidence collection and configuration reviews. This process can be:

- Time-consuming
- Difficult to scale across multiple systems
- Dependent on auditor experience
- Prone to inconsistent assessment results

This platform explores how automated security assessment can improve the efficiency, consistency, and reliability of compliance auditing.

---

## Objectives

The main objectives of this project are:

- Automate Linux security configuration assessments
- Collect technical evidence from target systems
- Map security findings to ISO/IEC 27001:2022 controls
- Identify compliance gaps and misconfigurations
- Generate structured audit reports
- Support faster and more repeatable security assessments

---

## Key Features

### Automated Linux Auditing
- Remote assessment of Linux systems through secure connections
- Automated checks for security configurations
- Identification of potential compliance weaknesses

### ISO 27001:2022 Control Mapping
The platform maps technical findings to relevant ISO 27001 controls, including:

- A.8.5 Secure Authentication
- A.8.9 Configuration Management
- A.8.15 Logging
- A.8.16 Monitoring Activities

### Evidence Collection

The system collects technical evidence required during security audits, including:

- System configurations
- Authentication settings
- Security parameters
- Logging configurations

### Compliance Assessment

The platform evaluates system configurations and highlights:

- Compliant controls
- Non-compliant controls
- Security gaps
- Recommended improvements

### Reporting

Generates structured compliance reports containing:

- Audit findings
- Evidence collected
- Risk observations
- Control mapping results

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Operating System | Linux (Ubuntu) |
| Security Testing | Linux configuration auditing |
| Communication | SSH |
| Compliance Framework | ISO/IEC 27001:2022 |
| Data Processing | Python libraries |
| Reporting | Automated report generation |

---

## System Architecture

```
                 User
                  |
                  |
            Flask Web Interface
                  |
                  |
          Audit & Compliance Engine
                  |
        ------------------------
        |                      |
   Evidence Collector     Risk Analysis
        |
        |
    SSH Connection
        |
        |
 Target Linux Systems
```

---

## Project Structure

```
ISO27001-Audit-Platform/

├── app.py
├── requirements.txt
├── README.md

├── modules/
│   ├── audit_engine.py
│   ├── evidence_collector.py
│   ├── compliance_mapping.py
│   └── risk_engine.py

├── templates/
├── static/

├── reports/
└── screenshots/
```

---

## Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ISO27001-Audit-Platform.git
```

### 2. Navigate to Project Folder

```bash
cd ISO27001-Audit-Platform
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

Activate environment:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Application

```bash
python app.py
```

Access the application:

```
http://127.0.0.1:5000
```

---

## Testing Environment

The platform was tested using virtualized Linux environments:

- Ubuntu Linux audit server
- Target Linux machines with different security configurations
- VirtualBox-based testing environment

Testing involved comparing:

- Securely configured systems
- Default/misconfigured systems

to evaluate detection accuracy and compliance assessment capability.

---

## Research Contribution

This project investigates how automated compliance assessment can improve traditional ISO 27001 audit processes.

The research explores:

- Reduction of manual audit effort
- Faster evidence collection
- Automated control assessment
- Improved consistency in compliance evaluation

---

## Future Improvements

Potential future enhancements include:

- Machine learning-based prediction of compliance failures
- Integration with security monitoring platforms
- Support for additional compliance frameworks
- Real-time security posture monitoring
- Larger-scale multi-system assessments

---

## Author

**Maureen Chepkemoi**

MSc Cybersecurity and Emerging Threats  
Middlesex University Dubai

---

## Disclaimer

This project is developed for academic research and security assessment purposes only. Always obtain appropriate authorization before auditing any system.
