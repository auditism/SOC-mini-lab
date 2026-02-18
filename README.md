# SOC-mini-lab
This document complements my soc mini lab walkthrough
Overview

This page documents the full setup, configuration, troubleshooting steps, and Splunk dashboards used in a multi‑VM cybersecurity lab environment. It is designed to be published as a GitHub Pages article or used as a YouTube video script.

1. Lab Environment Structure

Machine

Role

Operating System

IP Address

pfSense

Firewall

FreeBSD-based OS

Internal + External

Kali

Attacker

Linux (Debian-based)

192.168.2.101

Windows

Host on Network

Windows

192.168.2.11

Ubuntu

Splunk + User Host

Linux (Ubuntu)

192.168.2.10

Role Descriptions

pfSense: Controls all network traffic and provides firewall, VPN, and routing.

Kali: Used to simulate attacker behavior (port scans, enumeration, etc.).

Windows: Endpoint monitored via Splunk Universal Forwarder and Sysmon.

Ubuntu: Hosts Splunk Enterprise and a custom Python login server for log simulation.

Features Implemented

Real‑time firewall log analysis

Port scan detection

Failed authentication monitoring

Suspicious command execution alerts

Network traffic visualization

Suricata IDS logs (planned integration)

2. Kali Attacker Activity

Network Discovery

sudo nmap -sn 192.168.2.0/24

Port Scan

sudo nmap -sS -p 1-1000 --reason 192.168.2.10 -v

3. Windows → Splunk Integration

Key Steps

Install Splunk Universal Forwarder

Install Sysmon + Sysmon config

Configure inputs.conf and props.conf

Verify connectivity to Splunk server

Useful Commands

Check forwarder service:

sc query SplunkForwarder

List forward servers:

"C:\Program Files\SplunkUniversalForwarder\bin"\splunk list forward-server

Check forwarder logs:

cd "C:\Program Files\SplunkUniversalForwarder\var\log\splunk"
type splunkd.log | findstr ERROR

Trigger Sysmon event:

calc.exe

View Sysmon logs:

wevtutil qe "Microsoft-Windows-Sysmon/Operational" /c:5 /rd:true /f:text

Restart forwarder:

net stop SplunkForwarder64
net start SplunkForwarder64

4. Ubuntu → Splunk Configuration

inputs.conf

[udp://5514]
connection_host = ip
sourcetype = pfsense:filterlog
index = main

[monitor:///var/log/auth.log]
index = main
sourcetype = linux:auth

[monitor:///var/log/syslog]
index = main
sourcetype = linux:syslog

[monitor:///var/log/ufw.log]
index = main
sourcetype = linux:ufw

Adding Custom Log File (Python Login Server)

sudo /opt/splunk/bin/splunk add monitor /home/giorgio/simulated_logs/login_events.log -index main -sourcetype custom:login_events

5. pfSense → Splunk Integration

Splunk Listener

[udp://514]
connection_host = ip
host = pfsense
index = main
sourcetype = pfsense
no_appending_timestamp = true

Steps

Configure pfSense to send logs via Syslog to Splunk server.

Create a new inputs.conf entry on Splunk.

Restart pfSense.

Events appear under sourcetype="pfsense:firewall".

6. OpenVPN Setup on pfSense

Steps

Register a stable hostname via DuckDNS

Configure OpenVPN using pfSense wizard

Add full‑tunnel routing:

redirect-gateway def1

Test connection from mobile device

Troubleshooting

Check firewall rules

Verify OpenVPN server configuration

Ensure DuckDNS IP is updating correctly

7. VirtualBox Guest Additions

Manual Installation Steps

Download ISO manually

Attach ISO to VM storage

Install packages from mounted device (usually /dev/sr0)

8. Splunk Searches and Dashboards

1. Total Firewall Events

index=main sourcetype=pfsense filterlog | stats count

2. Blocked Traffic Only

index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<action>pass|block),"
| search action=block
| stats count

3. Unique Source IPs

index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<src_ip>+),(?<dest_ip>+)"
| stats dc(src_ip) as unique_ips

4. Top Source IPs

index=main sourcetype=pfsense filterlog
| rex field=_raw "(?<src_ip>[\d\.]+)"
| stats count by src_ip
| sort - count
| head 10

5. Top Destination IPs

index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<src_ip>+),(?<dest_ip>+)"
| stats count by dest_ip
| sort - count
| head 10

6. By Protocol

index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<proto>tcp|udp|icmp|ICMPv6|TCP|UDP),"
| stats count by proto

7. Block vs Pass Percentage

index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<action>pass|block),"
| stats count by action
| eventstats sum(count) as total
| eval percentage = round((count / total) * 100, 2)

8. Top Ports and Services

index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<proto>tcp|udp),*,(?<src_ip>[\d\.]+),(?<dest_ip>[\d\.]+),(?<src_port>\d+),(?<dest_port>\d+)"
| stats count by dest_port, proto
| sort - count
| head 15
| eval service=case(
    dest_port==80, "HTTP",
    dest_port==443, "HTTPS",
    dest_port==53, "DNS",
    dest_port==22, "SSH",
    dest_port==3389, "RDP",
    dest_port==445, "SMB",
    dest_port==139, "NetBIOS",
    dest_port==8000, "Splunk Web",
    dest_port==8089, "Splunk Mgmt",
    dest_port==123, "NTP",
    dest_port==67, "DHCP",
    1=1, "Other"
  )
| table dest_port, service, proto, count

9. Connection Flows

index=main sourcetype=pfsense filterlog
| rex field=_raw "(?<src_ip>[\d\.]+),(?<dest_ip>[\d\.]+)"
| eval Connection = src_ip." → ".dest_ip
| table _time, Connection
| head 25

9. Troubleshooting Summary

Verify Splunk Forwarder service

Check connectivity to Splunk server

Inspect splunkd.log for errors

Restart Splunk services when needed

Validate pfSense syslog settings

10. Additional Components

Python Login Server (for simulated logs)

A simple Python script was used to generate login attempts and feed them into Splunk.

Windows HTTP Page

A small local webpage was created to generate HTTP requests for logging and monitoring.

Conclusion

This lab provides a complete, realistic environment for practicing SOC analysis, log ingestion, detection engineering, and attacker simulation. It can be expanded with Suricata, Zeek, ELK, or cloud integrations in future iterations.
