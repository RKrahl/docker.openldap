#! /usr/bin/python3

import os
import os.path
from pathlib import Path
import shutil
import subprocess

slapadd = '/usr/sbin/slapadd'
slapd = '/usr/sbin/slapd'

etc_dir = Path('/etc/openldap')
tls_dir = etc_dir / 'tls'
conf_dir = etc_dir / 'slapd.d'
pid_dir = Path('/run/slapd')

if tls_dir.is_dir():
    uris = "ldap:/// ldaps:/// ldapi:///"
else:
    uris = "ldap:/// ldapi:///"

def init_openldap():
    init_config = etc_dir / 'slapd.ldif'
    init_cmd = [slapadd, '-n', '0',
                '-F', str(conf_dir), '-l', str(init_config)]
    subprocess.run(init_cmd, check=True)

def fix_directories():
    pid_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
    shutil.chown(pid_dir, user='ldap', group='ldap')
    for dirpath, dirnames, filenames in os.walk(conf_dir):
        shutil.chown(dirpath, user='ldap', group='ldap')
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            shutil.chown(filepath, user='ldap', group='ldap')

if not (conf_dir / 'cn=config').is_dir():
    init_openldap()

fix_directories()

slapd_cmd = [slapd, '-h', uris, '-F', str(conf_dir),
             '-u', 'ldap', '-g', 'ldap', '-o', 'slp=off']
subprocess.Popen(slapd_cmd)
