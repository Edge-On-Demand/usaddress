# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from usaddress import token_features


class TestTokenFeatures(unittest.TestCase):
    def test_unicode(self):
        features = token_features('å')
        assert features['endsinpunc'] is False


if __name__ == '__main__':
    unittest.main()
