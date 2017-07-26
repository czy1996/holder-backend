from models.user import User


def add_user():
    form = dict(
        name='chen',
        password='123',
    )
    u = User.new(form)
    print('add user', u.id)


def find_user():
    us = User.find(name='chen')
    print('find user chen', us)

    us = User.find(name='gua')
    print('find user gua', us)


def has_user():
    print('has user chen: ', User.has(name='chen'))
    print('has user gua: ', User.has(name='gua'))


def get_user():
    u = User.get(1)
    print('get user id 1', u)


def all_user():
    us = User.all()
    print('all user', us)


def delete_user():
    u = User.find_one(name='ziang')
    u.delete()
    print('user ziang deleted', u)


def test_json():
    u = User.find_one(name='chen')
    print('user json', u.json())


def update_user():
    u = User.get(8)
    u.update({
        'name': 'mia',
    })
    print('user updated', u)


def test():
    # add_user()
    find_user()
    # has_user()
    get_user()
    all_user()
    # delete_user()
    test_json()
    update_user()


if __name__ == '__main__':
    test()
