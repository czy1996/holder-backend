from . import Mongua


class Topic(Mongua):
    # 子类必须实现 _fields 类方法来定义字段
    @classmethod
    def _fields(cls):
        fields = [
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, -1),
        ]
        fields.extend(super()._fields())
        return fields
