from . import Mongua
from datetime import datetime


class Session(Mongua):
    # 子类必须实现 _fields 类方法来定义字段
    # TODO expire
    @classmethod
    def _fields(cls):
        fields = [
            ('session_id', str, ''),
            ('openid', str, ''),
            ('session_key', str, ''),
            ('utcNow', datetime.utcnow, datetime.utcnow())
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def openid_from_sessionid(cls, session_id):
        s = cls.find_one(session_id=session_id)
        return s.json().get('openid')
