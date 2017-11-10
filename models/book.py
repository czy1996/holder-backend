from . import Mongua
from utils import log, douban_isbn


class Book(Mongua):
    @classmethod
    def _fields(cls):
        fields = [
            ('title', str, ''),
            ('description', str, '暂无'),
            ('publisher', str, ''),
            ('douban_url', str, ''),
            ('inventory', int, 0),
            ('isbn', str, ''),
            ('thumb', str, ''),
            ('first_price', int, 0),
            ('second_price', int, 0),
            ('author', list, ''),
            ('category', str, 'other'),
            ('filled', bool, False)
        ]
        fields.extend(super()._fields())
        return fields

    def increase_one(self):
        self.update({
            'inventory': self.inventory + 1,
        })

    def decrease_one(self):
        self.update({
            'inventory': self.inventory - 1,
        })

    def increase(self, num):
        self.update({
            'inventory': self.inventory + num,
        })

    def decrease(self, num):
        self.update({
            'inventory': self.inventory - num,
        })

    @classmethod
    def find_by_title(cls, title=''):
        # print('*** title', title)
        return cls.find_one(title=title)

    @classmethod
    def add_title(cls, title='', description='暂无简介', publisher='', douban_url='', inventory=0, **kwargs):
        data = {
            'title': title,
            'description': description,
            'publisher': publisher,
            'douban_url': douban_url,
            'inventory': inventory,
        }
        data.update(kwargs)
        b = cls.new(data)
        return b

    def fill_douban(self):
        log('***debug filldouban', self.isbn)
        if self.isbn is not None:
            log('no previous isbn')
            douban = douban_isbn(self.isbn)
            log(douban)
            try:
                data = {
                    'title': douban['title'],
                    'publisher': douban['publisher'],
                    'douban_url': douban['url'],
                    'author': douban['author'],
                    'thumb': douban['image'],
                    'description': douban['summary'],
                    'first_price': douban['price'],
                    'filled': True
                }
            except KeyError:
                data = {
                    'filled': False,
                }
            self.update(data)

    @classmethod
    def isbn(cls, code):
        if cls.has(isbn=code):
            return cls.find_one(isbn=code)
        else:
            b = cls.new({
                'isbn': code
            })
            b.fill_douban()
            return b

    @classmethod
    def dec(cls, cart):
        for k, v in cart.items():
            b = cls.get(int(k))
            b.decrease(v)
