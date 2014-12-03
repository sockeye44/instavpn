import platform, os, logging_subprocess, random, string, logging, sys, json, urllib2


def check_os(logger):
    if platform.linux_distribution() != ('Ubuntu', '14.04', 'trusty'):
        logger.log_debug('OS: ' + ' '.join(platform.linux_distribution()))
        return False
    return True


def not_sudo():
    return os.getuid() != 0


def install_packages(logger):
    logger.log_debug('Update package lists')
    if logging_subprocess.call("apt-get update", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Update packages')
    if logging_subprocess.call("apt-get -y upgrade", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Install node.js')
    if logging_subprocess.call("apt-get install -y nodejs-legacy npm build-essential libssl-dev", logger.logger,
                               stdout_log_level=logging.DEBUG, stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Install vnstat')
    if logging_subprocess.call("apt-get install -y vnstat vnstati", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Install VPN server packages')
    if logging_subprocess.call("DEBIAN_FRONTEND=noninteractive apt-get install -q -y openswan xl2tpd ppp lsof",
                               logger.logger,
                               stdout_log_level=logging.DEBUG, stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    return True


def setup_sysctl(logger):
    if logging_subprocess.call("sh files/sysctl.sh", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False
    return True


def setup_passwords(logger):
    try:
        char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits
        f = open('/etc/ppp/chap-secrets', 'w')
        f.write("username1 l2tpd password1 *\nusername2 l2tpd password2 *".replace("password1", ''.join(
            random.sample(char_set * 12, 12))).replace("password2", ''.join(random.sample(char_set * 12, 12))))
        f.close()
        f = open('/etc/ipsec.secrets', 'w')
        f.write('1.2.3.4 %any: PSK "' + ''.join(random.sample(char_set * 16, 16)) + '"')
        f.close()
    except:
        logger.logger.error(sys.exc_info()[0])
        return False

    return True


def cp_configs(logger):
    logger.log_debug('xl2tpd.conf')
    if logging_subprocess.call("cp files/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('options.xl2tpd')
    if logging_subprocess.call("cp files/options.xl2tpd /etc/ppp/options.xl2tpd", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('ipsec.conf.template')
    if logging_subprocess.call("cp files/ipsec.conf.template /etc/ipsec.conf.template", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    return True


def setup_vpn(logger):
    logger.log_debug('Write setup-vpn.sh to /etc')
    if logging_subprocess.call("cp files/setup-vpn.sh /etc/setup-vpn.sh", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Add to rc.local')
    try:
        f = open('/etc/rc.local', 'w')
        f.write('bash /etc/setup-vpn.sh\nexit 0')
        f.close()
    except:
        logger.logger.error(sys.exc_info()[0])
        return False

    logger.log_debug('Execute setup-vpn.sh')
    if logging_subprocess.call("bash /etc/setup-vpn.sh", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Ufw default forward policy')
    for line in fileinput.input("/etc/default/ufw", inplace=True):
        print line.replace('DEFAULT_FORWARD_POLICY="DROP"', 'DEFAULT_FORWARD_POLICY="ACCEPT"'),
    
    if logging_subprocess.call("service ufw restart", logger.logger, stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False
    
    logger.log_debug('Copy CLI')
    if logging_subprocess.call("chmod +x files/instavpn && cp files/instavpn /usr/bin/instavpn", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    return True

def webui(logger):

    logger.log_debug('Generate random password')
    char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits
    with open('web/server/credentials.json', 'r+') as f:
        json_data = json.loads(f.read())
        json_data['admin']['password'] = ''.join(random.sample(char_set * 16, 16))
        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()

    logger.log_debug('Copy web UI directory')
    if logging_subprocess.call("cp -rf web/ /opt/instavpn", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Install node_modules')
    if logging_subprocess.call("cd /opt/instavpn && npm install", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Copy upstart script')
    if logging_subprocess.call("cp files/instavpn.conf /etc/init", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Add vnstati to cron')
    if logging_subprocess.call('crontab -l | { cat; echo "* * * * * vnstati -s -i eth0 -o /opt/instavpn/public/images/vnstat.png"; } | crontab -', logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    logger.log_debug('Start service')
    if logging_subprocess.call("start instavpn", logger.logger,
                               stdout_log_level=logging.DEBUG,
                               stderr_log_level=logging.DEBUG, shell=True) != 0:
        return False

    return True


def info(logger):
    
    logger.log_info('')
    
    with open('/opt/instavpn/server/credentials.json') as f:
        json_data = json.loads(f.read())
        logger.log_info('Browse web UI at http://' + urllib2.urlopen("http://myip.dnsdynamic.org/").read() + ':8080/')
        logger.log_info('Username: ' + json_data['admin']['login'] + ', password: ' + json_data['admin']['password'])
    
    logger.log_info('')

    logger.log_info("Completed. Run 'instavpn -h' for help")
