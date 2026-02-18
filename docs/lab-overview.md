# Lab Overview

## Virtual Machines (As of 31.08.25)

| Machine     | Role               | Operating System     | IP Address              |
| ----------- | ------------------ | -------------------- | ----------------------- |
| **pfSense** | Firewall           | FreeBSD-based OS     | Internal + External     |
| **Kali**    | Attacker           | Linux (Debian-based) | 192.168.2.101           |
| **Windows** | Host on Network    | Windows              | 192.168.2.11            |
| **Ubuntu**  | Splunk + User Host | Linux (Ubuntu)       | 192.168.2.10            |

---

## Role Descriptions

### pfSense
- Firewall, routing, VPN  
- Sends logs to Splunk  
- Used for firewall event analysis  

### Kali Linux
- Attacker machine  
- Used for scanning, enumeration, exploitation  

### Windows Host
- Sysmon installed  
- Splunk Universal Forwarder  
- Generates endpoint logs  

### Ubuntu Server
- Splunk Enterprise  
- Python login server  
- Central analysis machine  

---

## Features Implemented

- Real‑time firewall log analysis  
- Port scan detection  
- Failed authentication monitoring  
- Suspicious command execution alerts  
- Network traffic visualization  
- Suricata integration (planned)
