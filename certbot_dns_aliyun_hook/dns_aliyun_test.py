"""Tests for certbot_dns_aliyun.dns_aliyun."""

import unittest

API_KEY = 'foo'
SECRET = 'bar'


class AliyunLexiconClientTest(unittest.TestCase):

    def setUp(self):
        from certbot_dns_aliyun_hook.dns_aliyun import AliyunDNSClient

        self.client = AliyunDNSClient(API_KEY, SECRET, 0)

        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
