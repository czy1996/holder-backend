import hashlib

from . import Mongua


class User(Mongua):
    # 子类必须实现 _fields 类方法来定义字段
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
            ('phone', int, -1),
            ('password', str, ''),
            ('salt', str, 'asdjf203'),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form, **kwargs):
        """
        new 是给外部使用的函数
        这是继承覆盖父类的方法, 因为要重写 password
        """
        m = super().new(form)
        m.password = m.salted_password(form.get('password', ''))
        m.save()
        return m

    def blacklist(self):
        b = [
            '_id',
            'password',
            'salt',
        ]
        return b

    def salted_password(self, password):
        salt = self.salt
        hash1 = hashlib.md5(password.encode('ascii')).hexdigest()
        hash2 = hashlib.md5((hash1 + salt).encode('ascii')).hexdigest()
        return hash2

    def update_password(self, password):
        self.password = self.salted_password(password)
        self.save()

    def validate_auth(self, form):
        username = form.get('name', '')
        password = form.get('password', '')
        username_equals = self.name == username
        password_equals = self.password == self.salted_password(password)
        return username_equals and password_equals
