import prometheus_client
import os
import time
import datetime

dataDir = '/var/lib/backuppc/pc/'

def backup_info_last(filepath):
    valuemap = [ 'num', 'type', 'startTime', 'endTime', 'nFiles', 'size', 'nFilesExists', 'sizeExists' ]
    ret = {}
    line = ''
    with open(filepath) as f:
        while True:
            last = line
            line = f.readline()
            if line == '':
                break
        data = last.split("\t")
        for k in valuemap:
            ret[k] = data[valuemap.index(k)]
    return ret

IGNORED_HOSTS = ['']
BACKUPTYPEMAP = ['full', 'incr']
UPDATE_PERIOD = 300

BACKUPPC_BACKUP_NUM = prometheus_client.Gauge('backuppc_backup_num', 'Backup job num', ['host'])
BACKUPPC_BACKUP_TYPE = prometheus_client.Gauge('backuppc_backup_type', 'Type of backup job', ['host'])
BACKUPPC_BACKUP_STARTTIME = prometheus_client.Gauge('backuppc_backup_starttime', 'Start time of backup job', ['host'])
BACKUPPC_BACKUP_ENDTIME = prometheus_client.Gauge('backuppc_backup_endtime', 'End time of backup job', ['host'])
BACKUPPC_BACKUP_NFILES = prometheus_client.Gauge('backuppc_backup_nfiles', 'Number of files in backup job', ['host'])
BACKUPPC_BACKUP_SIZE = prometheus_client.Gauge('backuppc_backup_size', 'Size of backup job', ['host'])
BACKUPPC_BACKUP_NFILESEXISTS = prometheus_client.Gauge('backuppc_backup_nfilesexists', 'Number of files exists', ['host'])
BACKUPPC_BACKUP_SIZEEXISTS = prometheus_client.Gauge('backuppc_backup_sizeexists', 'Size that exists', ['host'])
BACKUPPC_BACKUP_STARTTIME_AGE_SECONDS = prometheus_client.Gauge('backuppc_backup_starttime_age_seconds', 'Seconds since start of backup', ['host'])
BACKUPPC_BACKUP_ENDTIME_AGE_SECONDS = prometheus_client.Gauge('backuppc_backup_endtime_age_seconds', 'Seconds since end of backup', ['host'])
BACKUPPC_BACKUP_DURATION_SECONDS = prometheus_client.Gauge('backuppc_backup_duration_seconds', 'Duration of backup job in seconds', ['host'])

if __name__ == '__main__':
  prometheus_client.start_http_server(9999)
  
while True:
  print("Updating exported values")
  hostnames = next(os.walk(dataDir))[1]
  now = int(datetime.datetime.now().timestamp())
  for host in hostnames:
    if host in IGNORED_HOSTS:
      continue
    
    backupFilepath = dataDir + host + "/backups"
    try:
      info = backup_info_last(backupFilepath)
      BACKUPPC_BACKUP_NUM.labels(host).set(info['num'])
      BACKUPPC_BACKUP_TYPE.labels(host).set(BACKUPTYPEMAP.index(info['type']))
      BACKUPPC_BACKUP_STARTTIME.labels(host).set(info['startTime'])
      BACKUPPC_BACKUP_ENDTIME.labels(host).set(info['endTime'])
      BACKUPPC_BACKUP_NFILES.labels(host).set(info['nFiles'])
      BACKUPPC_BACKUP_SIZE.labels(host).set(info['size'])
      BACKUPPC_BACKUP_NFILESEXISTS.labels(host).set(info['nFilesExists'])
      BACKUPPC_BACKUP_SIZEEXISTS.labels(host).set(info['sizeExists'])
      BACKUPPC_BACKUP_STARTTIME_AGE_SECONDS.labels(host).set(now - int(info['startTime']))
      BACKUPPC_BACKUP_ENDTIME_AGE_SECONDS.labels(host).set(now - int(info['endTime']))
      BACKUPPC_BACKUP_DURATION_SECONDS.labels(host).set(int(info['endTime'] )- int(info['startTime']))
    except FileNotFoundError:
      continue
    
  time.sleep(UPDATE_PERIOD)
 
