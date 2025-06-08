import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print('Testing something')
        self.assertEqual(True, False)  # add assertion here
        print('End of Test')



if __name__ == '__main__':
    unittest.main()