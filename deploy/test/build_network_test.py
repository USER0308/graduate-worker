# encoding: utf-8
import unittest


class BuildNetworkTest(unittest.TestCase):
    def tearDown(self):
        # 每个测试用例之后执行的操作
        pass

    def setUp(self):
        # 每个测试用例之前执行的操作
        pass

    @classmethod
    def tearDownClass(self):
        # 所有测试运行完后执行一次
        pass

    @classmethod
    def setUpClass(self):
        # 所有测试运行前执行一次
        pass

    def test_a_run(self):
        pass

    def test_b_run(self):
        pass

if __name__ == '__main__':
    unittest.main()