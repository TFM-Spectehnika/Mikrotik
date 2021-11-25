from datetime import datetime
import os
import paramiko
import time
import ftplib


date = datetime.today().strftime("%Y%d%m")
routers = ['10.10.1.1', '10.10.2.1', '10.10.3.1', '10.10.4.1', '10.10.7.1', '10.10.8.1', '10.10.9.1', '10.10.10.1', '10.10.11.1', '10.10.14.1', '10.10.15.1', '192.168.2.200']
user = 'admin'
secret = 'tchibo9536'
port = 22

for router in routers:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=router, username=user, password=secret, port=port)
        name_file = f"{date}_{router}"
        command_backup = f"system backup save name={name_file}"
        command_rsc = f"export file={name_file}.rsc"
        comand_del = ""
        rsccom = client.exec_command(command_backup)
        backupcom = client.exec_command(command_rsc)
        time.sleep(5)
        ftp = ftplib.FTP(router, user, secret)
        ftp.encoding = "utf-8"
        down_rsc = f"{name_file}.rsc"
        down_backup = f"{name_file}.backup"
        if not os.path.exists(f'\\\\srv-file\IT$\Mikrot\\{router}'):
            os.mkdir(f'\\\\srv-file\IT$\Mikrot\\{router}')
        if not os.path.exists(f'\\\\srv-file\IT$\Mikrot\\{router}\\{date}'):
            os.mkdir(f'\\\\srv-file\IT$\Mikrot\\{router}\\{date}')
        out_rsc = f'\\\\srv-file\IT$\Mikrot\\{router}\\{date}\\{down_rsc}'
        out_backup = f'\\\\srv-file\IT$\Mikrot\\{router}\\{date}\\{down_backup}'
        with open(out_rsc, 'wb') as f:
            ftp.retrbinary('RETR ' + down_rsc, f.write)
            with open(out_backup, 'wb') as f:
                ftp.retrbinary('RETR ' + down_backup, f.write)
        ftp.quit()
        client.exec_command("file remove [find type=script]")
        client.exec_command("file remove [find type=backup]")
        client.close()
    except Exception:
        pass


