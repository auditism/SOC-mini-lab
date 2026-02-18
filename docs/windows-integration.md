# Windows → Splunk Integration

## Steps Performed

1. Installed Splunk Universal Forwarder  
2. Installed Sysmon + Sysmon configuration  
3. Configured `inputs.conf` and `props.conf`  
4. Verified connectivity to Splunk server  

## Configs
Here's what we can expect the config to look like:


inputs.conf
```
# Windows Security Event Log
[WinEventLog://Microsoft-Windows-Sysmon/Operational]
checkpointInterval = 5
current_only = false
disabled = false
evt_resolve_ad_obj = true
index = main
renderXml = false
sourcetype = WinEventLog:Sysmon

[WinEventLog://Security]
checkpointInterval = 5
current_only = false
disabled = false
evt_resolve_ad_obj = true
index = main
sourcetype = WinEventLog:Security
start_from = oldest
```

outputs.conf 
```
[tcpout]
defaultGroup = default-autolb-group

[tcpout:default-autolb-group]
server = 192.168.2.10:9997

[tcpout-server://192.168.2.10:9997]

```
