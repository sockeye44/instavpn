import subprocess
import select
import logging

logger = logging.getLogger(__name__)

def call(popenargs,
        stdout_log_level=logging.DEBUG,
        stderr_log_level=logging.ERROR, **kwargs):
    child = subprocess.Popen(popenargs, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwargs)

    log_level = {child.stdout: stdout_log_level,
                 child.stderr: stderr_log_level}

    def check_io():
        ready_to_read = select.select([child.stdout, child.stderr], [], [], 1000)[0]
        for io in ready_to_read:
            line = io.readline()
            logger.log(log_level[io], line[:-1])

    while child.poll() is None:
        check_io()

    check_io()

    return child.wait()
