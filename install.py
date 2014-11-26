__version__ = "0.1"

import log, util

def main():
    log.log_info("Checking your OS version...")
    if util.check_os(log):
        log.log_info("OK")
    else:
        log.log_error("You must use Ubuntu 14.04")

    if util.not_sudo():
        log.log_error("Restart script as root")

    log.log_info("Installing packages...")
    if util.install_packages(log):
        log.log_info("OK")
    else:
        log.log_error("Fail")

    log.log_info("Applying sysctl parameters...")
    if util.setup_sysctl(log):
        log.log_info("OK")
    else:
        log.log_error("Fail")

    log.log_info("Creating random passwords...")
    if util.setup_passwords(log):
        log.log_info("OK")
    else:
        log.log_error("Fail")

    log.log_info("Other config files...")
    if util.cp_configs(log):
        log.log_info("OK")
    else:
        log.log_error("Fail")

    log.log_info("Adding script to rc.local...")
    if util.setup_vpn(log):
        log.log_info("OK")
    else:
        log.log_error("Fail")

    log.log_info("")
    log.log_info("Completed. Run 'instavpn -h' for help")


main()