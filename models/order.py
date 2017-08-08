from . import Mongua


class Order(Mongua):
    # 子类必须实现 _fields 类方法来定义字段
    @classmethod
    def _fields(cls):
        fields = [
            ('items', dict, {}),
            ('user', int, -1),
            ('status', str, 'open')
        ]
        fields.extend(super()._fields())
        return fields
