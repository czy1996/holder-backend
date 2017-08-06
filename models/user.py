import hashlib
from utils import (
    log,
)

from . import Mongua
from flask_wxapp import gen_3rd_session_key
from .session import Session
from flask import (
    request,
)


class User(Mongua):
    # 子类必须实现 _fields 类方法来定义字段
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
            ('phone', int, -1),
            ('password', str, ''),
            ('salt', str, 'asdjf203'),
            ('openid', str, 'shit'),
            ('gender', int, 1),
            ('city', str, ''),
            ('country', str, ''),
            ('avatarUrl', str, ''),
            ('dorm', str, ''),
            ('cart', dict, {}),
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

    @classmethod
    def find_by_openid(cls, openid):
        """
        用 openid 查找，没有就新建一个
        :param openid: 
        :return: 
        """
        u = cls.find_one(openid=openid)
        if u is None:
            u = cls.new({
                "openid": openid,
            })
        # log(u)
        return u

    @classmethod
    def auth(cls, code):
        """
        code 换取登录凭证
        :param code: 
        :return: 
        """
        from app import wxapp
        info = wxapp.jscode2session(code)
        session_id = gen_3rd_session_key()
        log(info, type(info))
        Session.new(session_id=session_id, openid=info['openid'], session_key=info['session_key'])
        return session_id

    @classmethod
    def current_user(cls):
        session_id = request.headers.get('Session_id', None)
        openid = Session.openid_from_sessionid(session_id)
        return cls.find_by_openid(openid)

    def add_cart(self, id, number=1):
        n = self.cart.get(str(id), 0)
        self.cart[str(id)] = n + number
        self.save()
