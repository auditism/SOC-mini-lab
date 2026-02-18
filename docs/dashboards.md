
# Splunk Dashboards & Searches

Below are the SPL queries used to build dashboards.

---

## 1. Total Firewall Events
```spl
index=main sourcetype=pfsense filterlog | stats count
```
### 2. Blocked Traffic
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<action>pass|block),"
| search action=block
| stats count
```
### 3. Unique Source IPs
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<src_ip>[^,]+),(?<dest_ip>[^,]+)"
| stats dc(src_ip) as unique_ips
```
### 4. Top Source IPs
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw "(?<src_ip>[\d\.]+)"
| stats count by src_ip
| sort - count
| head 10
```
### 5. Top Destination IPs
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<src_ip>[^,]+),(?<dest_ip>[^,]+)"
| stats count by dest_ip
| sort - count
| head 10
```
### 6. Protocol Breakdown
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<proto>tcp|udp|icmp|ICMPv6|TCP|UDP),"
| stats count by proto
```
### 7. Block vs Pass Percentage
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<action>pass|block),"
| stats count by action
| eventstats sum(count) as total
| eval percentage = round((count / total) * 100, 2)
```
### 8. Top Ports & Services
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw ",(?<proto>tcp|udp),[^,]*,(?<src_ip>[\d\.]+),(?<dest_ip>[\d\.]+),(?<src_port>\d+),(?<dest_port>\d+)"
| stats count by dest_port, proto
| sort - count
| head 15
```
### 9. Connection Flows
```spl
index=main sourcetype=pfsense filterlog
| rex field=_raw "(?<src_ip>[\d\.]+),(?<dest_ip>[\d\.]+)"
| eval Connection = src_ip." → ".dest_ip
| table _time, Connection
| head 25
```
## Suricata IDS searches

### Suspicious HTTP User-Agents (Attack Tools)
```
index=suricata event_type=http http.http_user_agent=*
| regex http.http_user_agent="(?i)(curl|wget|python|nmap|nikto|sqlmap|metasploit|masscan|zgrab|scrapy|go-http|ruby)"
| stats count, values(http.url) as urls, values(http.hostname) as hostnames by src_ip, dest_ip, http.http_user_agent
| sort - count
| rename http.http_user_agent as "User-Agent", src_ip as "Source", dest_ip as "Destination", urls as "URLs", hostnames as "Hosts"
```
### .exe file downloads (for windows hosts)
```
index=suricata event_type=alert alert.severity IN (1,2,3)
| stats count, latest(_time) as last_seen, values(src_ip) as sources, values(dest_ip) as destinations by alert.signature, alert.category, alert.severity
| sort - alert.severity, - count
| head 20
| rename alert.signature as "Alert Signature", alert.category as "Category", alert.severity as "Severity", sources as "Source IPs", destinations as "Dest IPs"
```
### emerging threats detection 
```
index=suricata event_type=alert alert.severity IN (1,2,3)
| stats count, latest(_time) as last_seen, values(src_ip) as sources, values(dest_ip) as destinations by alert.signature, alert.category, alert.severity
| sort - alert.severity, - count
| head 20
| rename alert.signature as "Alert Signature", alert.category as "Category", alert.severity as "Severity", sources as "Source IPs", destinations as "Dest IPs"
```
