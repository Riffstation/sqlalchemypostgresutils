# Alex Martelli's 'Borg'
class DBBorg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class DBConf(DBBorg):
    pass

conf = DBConf()


def get_db_conf():
    return conf
