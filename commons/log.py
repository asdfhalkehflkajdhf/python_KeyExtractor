import logging
import g_config

def get_logger(logger_name):
    # 文件日志

    # 为logger添加的日志处理器
    logger = logging.getLogger(logger_name)
    logger.addHandler(g_config.file_handler)
    logger.addHandler(g_config.console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)
    return logger

if __name__ == "__main__":
    # 试下是否可以输出 （“aaa”, b）的形式,

    logger = get_logger("test")

    b ="====="
    logger.info("asdf")
    logger.info("asdf"+b)
    logger.info("asdf %s"%( b))


    '''这种方式是不可以的'''
    logger.info("asdf",b)