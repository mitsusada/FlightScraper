# -*- encoding: utf-8 -*-
"""Module handling internal and dependency logging."""
import logging
import logzero


def setup_logzero(output_file, log_level):
    log_fmt = '[%(levelname)s %(asctime)s] %(message)s'
    if log_level == 'debug':
        log_level = logging.DEBUG
        log_fmt = (
            '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]'
            '%(end_color)s %(message)s')
    elif log_level == 'info':
        log_level = logging.INFO
    elif log_level == 'warning':
        log_level = logging.WARNING
    elif log_level == 'error':
        log_level = logging.ERROR
    elif log_level == 'critical':
        log_level = logging.CRITICAL

    formatter = logzero.LogFormatter(fmt=log_fmt)
    logzero.setup_default_logger(formatter=formatter)
    logzero.loglevel(log_level)
    logzero.logfile(
        output_file, loglevel=log_level,
        encoding='utf-8', maxBytes=1e9, backupCount=3, formatter=formatter)
