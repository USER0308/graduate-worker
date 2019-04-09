# encoding: utf-8
import unittest
import os
from deploy.utils import template

class TemplateTest(unittest.TestCase):
    def tearDown(self):
        # 每个测试用例之后执行的操作
        pass

    def setUp(self):
        # 每个测试用例之前执行的操作
        pass

    @classmethod
    def tearDownClass(self):
        # 所有测试运行完后执行一次
        print "测试完毕,测试结果如下:"
        ## 检测是否存在 configtx.yaml, crypto-config.yaml, docker-compose.yaml,且目标为文件
        for name in ['configtx.yaml', 'crypto-config.yaml', 'docker-compose.yaml']:
            if os.path.exists(name):
                if os.path.isfile(name):
                    ## 删掉已有的 configtx.yaml, crypto-config.yaml, docker-compose.yaml
                    print "已生成文件{}".format(name)
                else:
                    print "生成{}错误,目标不是文件".format(name)
            else:
                print "未检测到{}存在".format(name)

        print "清理环境..."
        for name in ['configtx.yaml', 'crypto-config.yaml', 'docker-compose.yaml']:
            if os.path.exists(name):
                if os.path.isfile(name):
                    ## 删掉已有的 configtx.yaml, crypto-config.yaml, docker-compose.yaml
                    print "检测到已有{}, 正在删除已有的{}...".format(name, name)
                    os.remove(name)
                else:
                    os.removedirs(name)

        for name in ['configtx.yaml', 'crypto-config.yaml', 'docker-compose.yaml']:
            if not os.path.exists(name):
                print "{}已被删除".format(name)

        print "清理完毕\n"

    @classmethod
    def setUpClass(self):
        # 所有测试运行前执行一次
        print "准备测试环境...\n"
        ## 检测是否存在 configtx.yaml, crypto-config.yaml, docker-compose.yaml
        ## 不管是目录还是文件,都删除
        for name in ['configtx.yaml', 'crypto-config.yaml', 'docker-compose.yaml']:
            if os.path.exists(name):
                if os.path.isfile(name):
                    ## 删掉已有的 configtx.yaml, crypto-config.yaml, docker-compose.yaml
                    print "检测到已有{}, 正在删除已有的{}...".format(name, name)
                    os.remove(name)
                else:
                    os.removedirs(name)

        for name in ['configtx.yaml', 'crypto-config.yaml', 'docker-compose.yaml']:
            if not os.path.exists(name):
                print "{}已被删除".format(name)

        print "准备完毕,开始正式测试\n"

    def test_configtx_gen_run(self):
        # 测试 configtx_gen 函数
        file_in_path = os.path.exists('configtx.yaml')
        self.assertFalse(file_in_path)
        template.configtx_gen(orderer_num=1,org_num=1,peer_num=1,ca_num=0,couchdb_num=0,cli=1)
        file_in_path = os.path.exists('configtx.yaml')
        self.assertTrue(file_in_path)

    def test_crypto_config_gen_run(self):
        # 测试 crypto_config_gen 函数
        file_in_path = os.path.exists('crypto-config.yaml')
        self.assertFalse(file_in_path)
        template.crypto_config_gen(orderer_num=1, org_num=1, peer_num=1, ca_num=0, couchdb_num=0, cli=1)
        file_in_path = os.path.exists('crypto-config.yaml')
        self.assertTrue(file_in_path)

    def test_docker_compose_gen_test(self):
        # 测试 docker_compose_gen 函数
        # 测试 config_gen 函数
        file_in_path = os.path.exists('docker-compose.yaml')
        self.assertFalse(file_in_path)
        template.docker_compose_gen(orderer_num=1,org_num=1,peer_num=1,ca_num=0,couchdb_num=0,cli_num=1)
        file_in_path = os.path.exists('docker-compose.yaml')
        self.assertTrue(file_in_path)

if __name__ == '__main__':
    unittest.main()