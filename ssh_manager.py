
import paramiko


class SSHManager:
    def __init__(self, ip, username, key_path, timeout=10):
        self.ip = ip
        self.username = username
        self.key_path = key_path
        self.timeout = timeout
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.ip,
            username=self.username,
            key_filename=self.key_path,
            timeout=self.timeout,
        )

    def run_command(self, command):
    
        if self.client is None:
            raise RuntimeError("Not connected — call connect() first")

        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return output, error

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

   
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
   
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--command", default="hostname && uptime")
    args = parser.parse_args()

    with SSHManager(args.ip, args.user, args.key) as ssh:
        out, err = ssh.run_command(args.command)
        print("STDOUT:\n", out)
        if err:
            print("STDERR:\n", err)