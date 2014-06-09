#!/usr/bin/env python3
import unittest
from BayesNet import Net

'''
Test methods:
    assertEqual
    assertNotEqual
    assertTrue
    assertFalse
    assertIs
    assertIsNot
    assertIsNone
    assertIsNotNone
    assertIn
    assertNotIn
    assertIsInstance
    assertNotIsInstance
'''

class TestBayesNet(unittest.TestCase):
    def setUp(self):
        self.net_alarm = Net('alarm.bn')
        self.net_ex2 = Net('ex2.bn')

    def test_parse(self):
        # func(self)
        # self.assert...(self, value)
        pass

    def test_normalize0(self):
        inputs = [[0.00059224, 0.0014919]]
        outputs = [(0.284165171, 0.715834828)]
        for i1, i2 in enumerate(inputs):
            res = self.net_alarm.normalize(i2)
            self.assertAlmostEqual(res[0], outputs[i1][0])
            self.assertAlmostEqual(res[1], outputs[i1][1])

    def test_toposort0(self):
        res = self.net_alarm.toposort()
        self.assertEqual(res, ['B', 'E', 'A', 'J', 'M'])

    def test_toposort1(self):
        res = self.net_ex2.toposort()
        self.assertEqual(res, ['A', 'B', 'C', 'D', 'E'])

if __name__ == '__main__':
    unittest.main()

'''
Net
    __init__
    _parse
    - normalize
    - toposort
    querygiven
    genpermutations
    makefactor
    pointwise
    sumout
    enum_ask
    enum_all
    elim_ask
query
main
'''