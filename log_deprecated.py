import logging
import multiprocessing
import os.path
import sys

from os_ import is_my_pc
from file import FileUtil
from mpfhandler import MultProcTimedRotatingFileHandler

lock = multiprocessing.Lock()


class LogUtil(object):
    inited = False
    __default_logger_name = 'root'
    __log = None
    source_filepath = ''

    # ====================================================
    # default logging config
    # ====================================================
    # level = logging.NOTSET, logging.DEBUG, logging.INFO,
    # logging.WARNING, logging.ERROR, logging.CRITICAL
    filename = ''
    datefmt = '%Y-%m-%d %H:%M:%S'
    # '[%(asctime)s] %(message)s'
    format = '[%(asctime)s][%(levelname)5s] %(message)s'

    @classmethod
    def get_logger(cls,
                   source_filepath=None,
                   level=logging.DEBUG,
                   format=format,
                   datefmt=datefmt,
                   console_mode=False):
        """
        get global logging object with multiprocessing-safe.
        :param source_filepath:
        :param console_mode: default: False
        :param datefmt:
        :param format:
        :param level: logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL(logging.FATAL
        :return: logging object
        """
        with lock:
            if cls.__log and cls.__log.hasHandlers() and cls.__log.level >= level:
                sys.stderr.write('reuse old logger (id:%s, log_path:%s), level:%s\n' %
                                 (id(cls.__log), cls.source_filepath, cls.__log.level))
                return cls.__log

            cls.source_filepath = source_filepath
            if not console_mode and is_my_pc():
                console_mode = True

            if source_filepath is None:
                console_mode = True
                log_path = None
            else:
                log_path = cls.__log_path_from_path(source_filepath)

            error_log_path = None
            if log_path:
                error_log_path = log_path.replace('.log', '.error.log')

                # create log dir
                if log_path and \
                        not os.path.exists(os.path.dirname(log_path)):
                    os.makedirs(os.path.dirname(log_path))

                if error_log_path and \
                        not os.path.exists(os.path.dirname(error_log_path)):
                    os.makedirs(os.path.dirname(error_log_path))

            cls.__log = LogUtil.__create_logger(log_path,
                                                error_log_path,
                                                level,
                                                console_mode,
                                                format,
                                                datefmt)
            cls.__log.setLevel(level)

            # LogUtil.basigConfig(level, format=format, datefmt=datefmt)
            # logging.getLogger("multiprocessing").setLevel(logging.CRITICAL)
            # logging.getLogger("urllib3").setLevel(logging.CRITICAL)
            # logging.getLogger("requests").setLevel(logging.CRITICAL)
            # logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)
            # logging.getLogger('elasticsearch.trace').setLevel(logging.CRITICAL)
            # logging.getLogger("py2neo").setLevel(logging.CRITICAL)
            # logging.getLogger("py2neo.batch").setLevel(logging.CRITICAL)
            # logging.getLogger("py2neo.cypher").setLevel(logging.CRITICAL)
            # logging.getLogger("httpstream").setLevel(logging.CRITICAL)
        return cls.__log

    @staticmethod
    def basigConfig(level=logging.NOTSET, format=format, datefmt=datefmt):
        logging.basicConfig(
            level=level,
            format=format,
            datefmt=datefmt
        )

    @staticmethod
    def __log_path_from_path(source_file, sub_log_dir='logs'):
        """
        :param sub_log_dir:
        :param source_file:
        :e.g. ::LogUtil.get_logger(__file__) ./a.py -> ./logs/a.log
        :e.g. ::LogUtil.get_logger(__file__, sub_log_dir='xx') ./a.py -> ./xx/a.log
        """
        _dir = os.path.join(os.path.dirname(source_file), sub_log_dir)
        _basename = os.path.basename(source_file)
        if len(sys.argv) > 1:
            _basename = '%s.%s' % (_basename, FileUtil.to_filename('.'.join(sys.argv[1:])))
        log_path = os.path.join(_dir, _basename) + '.log'
        return log_path

    @staticmethod
    def __create_logger(log_path,
                        error_log_path=None,
                        level=logging.NOTSET,
                        console_mode=False,
                        format=format,
                        datefmt=datefmt):
        if not LogUtil.inited:
            LogUtil.inited = True
            sys.stderr.write('console_mode: %s\n' % console_mode)
            sys.stderr.write('level: %s\n' % logging.getLevelName(level))
            if log_path is not None:
                sys.stderr.write('log_path: %s\n' % log_path)
            if error_log_path is not None:
                sys.stderr.write('error_log_path: %s\n' % error_log_path)

        # for single process
        # but MultProcTimedRotatingFileHandler support multiprocessing
        log = logging.getLogger(log_path)

        formatter = logging.Formatter(fmt=format, datefmt=datefmt)

        # ===================
        # logging handlers
        # ===================
        log.propagate = False
        log.handlers = []

        if console_mode:
            # console logger
            _consoleHandler = logging.StreamHandler(stream=sys.stdout)
            _consoleHandler.setLevel(level)
            _consoleHandler.setFormatter(
                logging.Formatter(fmt='%(message)s', datefmt=datefmt))
            log.addHandler(_consoleHandler)

            # console error logger
            _console_errorHandler = logging.StreamHandler(stream=sys.stderr)
            _console_errorHandler.setLevel(logging.ERROR)
            _console_errorHandler.setFormatter(
                logging.Formatter(fmt='%(message)s', datefmt=datefmt))
            log.addHandler(_console_errorHandler)

        if log_path:
            _fileHandler = MultProcTimedRotatingFileHandler(
                filename=log_path, when='midnight', interval=1, backupCount=0)
            _fileHandler.setLevel(level)
            _fileHandler.setFormatter(formatter)
            log.addHandler(_fileHandler)

            if error_log_path:
                _file_errorHandler = MultProcTimedRotatingFileHandler(
                    filename=error_log_path, when='midnight', interval=1, backupCount=0)
                _file_errorHandler.setLevel(logging.ERROR)
                _file_errorHandler.setFormatter(formatter)
                log.addHandler(_file_errorHandler)
        return log

    @classmethod
    def add_to_app_logger(cls, app):
        for h in cls.__log.handlers:
            app.logger.addHandler(h)
        return app.logger
