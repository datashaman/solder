import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase

class UserTest(FunkLoadTestCase):
    def setUp(self):
        self.base = 'http://localhost:8004'

    def test_simple(self):
        self.get(self.base + '/users', description='users')
        self.assert_('<h1>Users</h1>' in self.getBody(), 'Expected Users in body')

if __name__ in ('main', '__main__'):
    unittest.main()
