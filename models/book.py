from . import Mongua
from utils import log


class Book(Mongua):
    @classmethod
    def _fields(cls):
        fields = [
            ('title', str, ''),
            ('description', str, ''),
            ('publisher', str, ''),
            ('douban_url', str, ''),
            ('inventory', int, 0),
            ('isbn', str, ''),
            ('thumb', str, ''),
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
