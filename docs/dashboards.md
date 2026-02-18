
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
