#! /usr/bin/python3

from pathlib import Path
import subprocess

sed = '/usr/bin/sed'
slapadd = '/usr/sbin/slapadd'

etc_dir = Path('/etc/openldap')
tls_dir = etc_dir / 'tls'
conf_dir = etc_dir / 'slapd.d'

def init_openldap():
    sysconf = {
        'OPENLDAP_CONFIG_BACKEND': 'ldap',
        'OPENLDAP_START_LDAP': 'yes',
        'OPENLDAP_START_LDAPI': 'yes',
    }
    if tls_dir.is_dir():
        sysconf['OPENLDAP_START_LDAPS'] = 'yes'
    sed_cmd = [sed, '-i']
    for k, v in sysconf.items():
        sed_cmd.extend(['-e', 's/%s=".*"/%s="%s"/' % (k, k, v)])
    sed_cmd.append('/etc/sysconfig/openldap')
    subprocess.run(sed_cmd, check=True)
    init_config = etc_dir / 'slapd.ldif'
    init_cmd = [slapadd, '-n', '0',
                '-F', str(conf_dir), '-l', str(init_config)]
    subprocess.run(init_cmd, check=True)

if not (conf_dir / 'cn=config').is_dir():
    init_openldap()

subprocess.Popen('/usr/lib/openldap/start')
