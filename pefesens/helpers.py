import paramiko
import logging

logging.getLogger("paramiko").setLevel(logging.ERROR)


def exec_command_ssh(host, usr, cmd):
    client = None
    try:
        logging.debug(f"[helpers] ssh {usr}@{host} running : {cmd}")
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=usr)
        _, stdout, stderr = client.exec_command(cmd)
        r_out, r_err = stdout.readlines(), stderr.readlines()
    finally:
        if client:
            client.close()
    return r_out, r_err
