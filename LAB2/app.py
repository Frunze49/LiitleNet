import argparse
import subprocess
import ipaddress
import validators
import sys


def check_validity(host):
    if not validators.domain(host):
        try:
            ipaddress.ip_address(host)
        except Exception:
            print('Can not resolve this host', file=sys.stderr)
            return False

    process = subprocess.run(
        ['cat', '/proc/sys/net/ipv4/icmp_echo_ignore_all'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if process.stdout == 1:
        print('ICMP blocked', file=sys.stderr)
        return False

    process = subprocess.run(
        ["ping", host, '-M', 'do', '-s', str(0), '-c', '1'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if process.returncode != 0:
        print('HOST did not give response', file=sys.stderr)
        return False
    
    return True


def mtu_get(host):
    left = 0
    right = 8973

    while left != right and left < right - 1:
        middle_value = (left + right) // 2
        process = subprocess.run(
            ["ping", host, '-M', 'do', '-s', str(middle_value), '-c', '5'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if process.returncode == 0:
            left = middle_value
        elif process.returncode == 1:
            right = middle_value
        else:
            print('Ping returns trash', file=sys.stderr)
            exit(1)
    return left


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='Host of the server')
    args = parser.parse_args()
    host = args.host

    if (check_validity(host)):
        print("Take a seat and wait.")
        print('MTU for {} is {}'.format(host, mtu_get(host) + 28))
    else:
        exit(1)

if __name__ == '__main__':
    main()