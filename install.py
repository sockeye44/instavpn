__version__ = "0.1.1"

import log, util, logging

log.setup_logging()

logger = logging.getLogger(__name__)

def main():
    logger.info("Checking your OS version...")
    if util.check_os():
        logger.info("OK")
    else:
        logger.critical("You must use Ubuntu 14.04")

    if util.not_sudo():
        logger.critical("Restart script as root")

    logger.info("Installing packages...")
    if util.install_packages():
        logger.info("OK")
    else:
        logger.critical("Failed to install packages")

    logger.info("Applying sysctl parameters...")
    if util.setup_sysctl():
        logger.info("OK")
    else:
        logger.critical("Failed to apply sysctl parameters")

    logger.info("Creating random passwords...")
    if util.setup_passwords():
        logger.info("OK")
    else:
        logger.critical("Failed to create random passwords")

    logger.info("Other config files...")
    if util.cp_configs():
        logger.info("OK")
    else:
        logger.critical("Fail")

    logger.info("Adding script to rc.local...")
    if util.setup_vpn():
        logger.info("OK")
    else:
        logger.critical("Failed adding script to rc.local")

    logger.info("Installing web UI...")
    if util.webui():
        logger.info("OK")
    else:
        logger.critical("Failed installing web UI")

    util.info()

main()
