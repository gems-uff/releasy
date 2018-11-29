import pygit2
import datetime
import os

def create_test_data():
    path = 'tests/data/'
    repo = pygit2.init_repository(path, False)

    developer = pygit2.Signature('commiter', 'commiter@git')
    tree = repo.TreeBuilder().write()
    c1 = repo.create_commit('refs/heads/master',developer, developer,'c1',tree,[])
    c2 = repo.create_commit('refs/heads/master', developer, developer, 'c2', tree, [c1])
    c3 = repo.create_commit('refs/heads/master', developer, developer, 'c3', tree, [c2])
    c4 = repo.create_commit('refs/heads/master', developer, developer, 'c4', tree, [c3])
    b1 = repo.create_branch('b1', repo.head.get_object())
    c5 = repo.create_commit('refs/heads/b1', developer, developer, 'c5', tree, [c4])
    c6 = repo.create_commit('refs/heads/master', developer, developer, 'c6', tree, [c4])
    c7 = repo.create_commit('refs/heads/master', developer, developer, 'c7', tree, [c4,c5])


def touch():
    with open('tests/data/log', 'a') as f:
        f.write(datetime.datetime.now().strftime('%H:%M:%S.%f'))

create_test_data()