from __future__ import print_function, unicode_literals

import unittest
from builtins import zip
from builtins import object

from parserator.training import readTrainingData

from usaddress import parse, GROUP_LABEL


class TestPerformance(object):  # for test generators, must inherit from object
    # these are simple address patterns
    def test_simple_addresses(self):
        test_file = 'measure_performance/test_data/simple_address_patterns.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data:
            address_text, components = labeled_address
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            yield equals, address_text, labels_pred, labels_true

    # for making sure that performance isn't degrading
    # from now on, labeled examples of new address formats
    # should go both in training data & test data
    def test_all(self):
        test_file = 'measure_performance/test_data/labeled.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data:
            address_text, components = labeled_address
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            yield equals, address_text, labels_pred, labels_true


class TestPerformanceOld(object):  # some old tests for usaddress
    def test_synthetic_addresses(self):
        test_file = 'measure_performance/test_data/synthetic_osm_data.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data:
            address_text, components = labeled_address
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            yield equals, address_text, labels_pred, labels_true

    def test_us50(self):
        test_file = 'measure_performance/test_data/us50_test_tagged.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data:
            address_text, components = labeled_address
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            yield fuzzy_equals, address_text, labels_pred, labels_true


def equals(addr, labels_pred, labels_true):
    pretty_print(addr, labels_pred, labels_true)
    assert labels_pred == labels_true


def fuzzy_equals(addr, labels_pred, labels_true):
    labels = []
    fuzzy_labels = []
    for label in labels_pred:
        if label.startswith('StreetName'):
            fuzzy_labels.append('StreetName')
        elif label.startswith('AddressNumber'):
            fuzzy_labels.append('AddressNumber')
        elif label == 'Null':
            fuzzy_labels.append('NotAddress')
        else:
            fuzzy_labels.append(label)
    for label in labels_true:
        labels.append(label)
    pretty_print(addr, fuzzy_labels, labels)

    assert fuzzy_labels == labels


def pretty_print(addr, predicted, true):
    print('ADDRESS: ', addr)
    print('pred: ', predicted)
    print('true: ', true)


if __name__ == '__main__':
    unittest.main()
