import paramiko

ip_offset = 111
server_prefix = "[RESEARCH_NETWORK_PREFIX]."
server_suffix = [str(a) for a in range(0 + ip_offset, 42 + ip_offset)]
username = "[ROOT_USERNAME]"
password = "[SERVER_PASSWORD]"

interface_l = [('eth0', ["[RESEARCH_NETWORK_PREFIX]."]), ('eth2', ["[INTERNAL_NETWORK_PREFIX].20."]), ("eth3", ["[INTERNAL_NETWORK_PREFIX].50."])]

for interface in interface_l:
    for suffix in server_suffix:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_prefix + suffix, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(
            "ifconfig " + interface[0] + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'")
        for l in stdout.readlines():
            for prefix in interface[1]:
                print l[:-1], prefix + suffix
