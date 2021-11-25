import paramiko
import time
from datetime import datetime
from shutil import copyfile

date = datetime.today().strftime("%Y%d%m")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='172.16.10.22', username='ubnt', password='27122017', port='22')

stdin, stdout, stderr = client.exec_command('ls -S /data/autobackup | head -n1')
outlines = stdout.readlines()
resp = ''.join(outlines)
fl = resp
resp = '/data/autobackup/'+f'{resp}'
resp = resp.rstrip()
print(resp)
fl = fl.rstrip()
ftp_client=client.open_sftp()
ftp_client.get(f'{resp}', f'{fl}')
ftp_client.close()
time.sleep(2)
client.close()
copyfile(f'{fl}', '\\\\srv-file\IT$\Mikrot\\' + f'{fl}')

