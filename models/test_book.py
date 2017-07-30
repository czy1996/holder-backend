from models.book import Book


def test_add_title():
    Book.add_title('油层物理学', thumb='https://img3.doubanio.com/lpic/s7628151.jpg')
    Book.add_title('渗流力学基础', 'shit')
    Book.add_title('算法设计与分析')


def test_inc_one():
    b = Book.find_by_title('油层物理')
    b.increase_one()


def test_dec_one():
    b = Book.find_by_title('油层物理')
    b.decrease_one()


def test_inc():
    b = Book.find_by_title('渗流力学')
    b.increase(10)


def test_dec():
    b = Book.find_by_title('油层物理')
    b.decrease(1)


def all_books():
    bs = Book.all()
    print('all books', bs)


def refill():
    bs = Book.all()
    for b in bs:
        b.fill_douban()


def test():
    # test_add_title()
    # test_inc_one()
    # test_dec_one()
    # all_books()
    # test_add_title()
    refill()


if __name__ == '__main__':
    test()
