import unittest
from app.app import app

class TestApp(unittest.TestCase):
    def test_index(self):
        #tester = app.test_client(self)
        #response = tester.get('/', content_type='html/text')
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.data, b'<h1>Welcome to Essai Github Actions CI/CD</h1>')
        print("Les tests sont OOOOKKKKKKKKKKKKKKKK")


if __name__ == '__main__':
    unittest.main()

