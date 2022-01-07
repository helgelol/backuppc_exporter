# BackupPC Exporter

Prometheus Exporter for BackupPC

# Features
- Parses through the files of your backups and exports the information of the last backup job of each host.
- Has support to ignore hosts that you're no longer actively backing up.

# Installation

```
git clone https://github.com/helgelol/backuppc_exporter.git
mv backuppc_exporter/backuppc_exporter.service /etc/systemd/system/backuppc_exporter.service
mkdir /etc/backuppc_exporter && mv backuppc_exporter/backuppc_exporter.py && cd /etc/backuppc_exporter
python3 -m pip install prometheus_client
systemctl daemon-reload && systemctl enable backuppc_exporter && systemctl start backuppc_exporter
```

- Service should now be running on port `localhost:9999`
- It  autostarts after reboot as defined in the `.service` file

### Happy scraping!
