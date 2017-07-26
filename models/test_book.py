from models.book import Book


def test_add_title():
    Book.add_title('油层物理')
    Book.add_title('渗流力学', 'shit')


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


def test():
    # test_add_title()
    # test_inc_one()
    # test_dec_one()
    # all_books()
    test_inc()
    test_dec()


if __name__ == '__main__':
    test()
