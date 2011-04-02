import os, unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase

class Users(FunkLoadTestCase):
    def load(self, datasets):
        for dataset in datasets:
            path = os.path.join(os.path.dirname(__file__), 'datasets/%s.csv')
            with open(path) as f:
                pass

    def setUp(self):
        self.base = 'http://localhost:8004'
        print vars(self)
        self.load(self.get_confList('main', 'datasets'))

    def test_table(self):
        self.get(self.base + '/users', description='users')
        self.assert_('<h1>Users</h1>' in self.getBody(), 'Expected Users in body')

if __name__ in ('main', '__main__'):
    unittest.main()
