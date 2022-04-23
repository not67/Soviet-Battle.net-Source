from config import INI_CONFIG
import datetime


def pretty_print_timestamp():
    """
    Returns a pretty formatted timestamp
    """
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


with open(
    INI_CONFIG['LOG_FILE'], 'w+'
) as f:
    pass


class logger:

    @staticmethod
    def log(message):
        with open(
            INI_CONFIG['LOG_FILE'], 'a'
        ) as f:
            f.write('[%s] ' % (pretty_print_timestamp()) + message+'\n')
