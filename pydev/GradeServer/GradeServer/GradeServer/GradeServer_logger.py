# -*- coding: utf-8 -*-
"""
    photolog.photolog_logger
    ~~~~~~~~

    photolog 로그 모듈. 
    photolog 어플리케이션에서 사용할 공통 로그 객체를 생성.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import logging
from datetime import datetime
from logging import getLogger, handlers, Formatter

from GradeServer.database import dao
from GradeServer.model.serverLogs import ServerLogs

class Log:
    __log_level_map = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error' : logging.ERROR,
        'critical' : logging.CRITICAL
        }
    
    __my_logger=None
    
    @staticmethod
    def init(logger_name='GradeServer', 
             log_level='debug',
             log_filepath='GradeServer/resource/log/GradeServer.log'):
        Log.__my_logger = getLogger(logger_name);
        Log.__my_logger.setLevel(Log.__log_level_map.get(log_level, 
                                                         'warn'))
        
        formatter = \
            Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        Log.__my_logger.addHandler(console_handler)
            
        file_handler = \
            handlers.TimedRotatingFileHandler(log_filepath, 
                                              when='D', 
                                              interval=1)
        file_handler.setFormatter(formatter)
        Log.__my_logger.addHandler(file_handler)
    
    @staticmethod
    def debug(memberId, msg):
        Log.__my_logger.debug(msg)
        Log.insert_logs(0, memberId, msg)
    
    @staticmethod
    def info(memberId, msg):
        Log.__my_logger.info(msg)
        Log.insert_logs(0, memberId, msg)
    
    @staticmethod
    def warn(memberId, msg):
        Log.__my_logger.warn(msg)
        Log.insert_logs(0, memberId, msg)
    
    @staticmethod
    def error(memberId, msg):
        Log.__my_logger.error(msg)
        Log.insert_logs(0, memberId, msg)
    
    @staticmethod
    def critical(memberId, msg):
        Log.__my_logger.critical(msg)
        Log.insert_logs(0, memberId, msg)
        
    @staticmethod
    def insert_logs(serverStatus, memberId, logContent):
        dao.add(ServerLogs(loggedDate = datetime.now(),
                           serverStatus = serverStatus,
                           memberId = memberId,
                           logContent = logContent))
        dao.commit()