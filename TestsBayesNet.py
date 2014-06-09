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

    def test_querygiven_alarm(self):
        cases = [
            (('B', {'B': False}), .999),
            (('B', {'B': True}), .001),
            (('A', {'A': True, 'B': True, 'E': False}), .94),
            (('A', {'A': False, 'B': False, 'E': True}), .71),
            (('A', {'A': False, 'B': False, 'E': False}), .999),
            (('M', {'M': False, 'A': False}), .99)
        ]
        for i, o in cases:
            self.assertAlmostEqual(self.net_alarm.querygiven(*i), o)

    def test_querygiven_ex2(self):
        cases = [
            (('A', {'A': False}), 0.7),
            (('B', {'B': True}), 0.6),
            (('E', {'C': True, 'E': False}), 0.3),
            (('D', {'B': False, 'A': True, 'D': False}), 0.2),
            (('D', {'B': False, 'A': True, 'D': True}), 0.8),
            (('C', {'C': True, 'A': True}), 0.8),
            (('C', {'C': False, 'A': False}), 0.6)
        ]
        for i, o in cases:
            self.assertAlmostEqual(self.net_ex2.querygiven(*i), o)

    def test_genpermutations(self):
        cases = [0, 1, 2, 5]
        for c in cases:
            res = self.net_alarm.genpermutations(c)
            for r in res:
                self.assertEqual(len(r), c)
            self.assertEqual(len(set(res)), len(res))

    def test_makefactor0(self):
        i = ('D', {'D': ['D', 'A']}, {'B': True})
        o = (['A', 'D'], {(True, True): 0.7, (True, False): 0.30000000000000004, 
            (False, True): 0.1, (False, False): 0.9})
        self.assertEqual(self.net_ex2.makefactor(*i), o)

    def test_pointwise0(self):
        i1 = (['C', 'E'], {(False, False): 0.8, (False, True): 0.2, (True, True): 0.7, (True, False): 0.3})
        i2 = (['A', 'C'], {(True, True): 0.8, (True, False): 0.2, (False, True): 0.4, (False, False): 0.6})
        o = (['A', 'C', 'E'], {(False, True, True): 0.27999999999999997, 
            (False, False, False): 0.48, (True, True, False): 0.24, 
            (True, False, False): 0.16000000000000003, (False, True, False): 0.12, 
            (False, False, True): 0.12, (True, True, True): 0.5599999999999999, 
            (True, False, True): 0.04000000000000001})
        self.assertEqual(self.net_ex2.pointwise('C', i1, i2), o)

    def test_sumout0(self):
        self.assertEqual(self.net_ex2.sumout('D', [(['A', 'D'], {(True, True): 0.7, 
            (True, False): 0.3, (False, True): 0.1, (False, False): 0.9})]),
        [(['A'], {(False,): 1.0, (True,): 1.0})])

if __name__ == '__main__':
    unittest.main()

'''
Net
    __init__
    _parse
    makefactor
    pointwise
    sumout
    enum_ask
    enum_all
    elim_ask
query
main
'''