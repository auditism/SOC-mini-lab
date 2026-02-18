In order to receive logs, we also need to setup splunk on the ubuntu machine, here's an example of the configuration files

## inputs.conf


```ini
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
