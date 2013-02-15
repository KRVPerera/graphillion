# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from graphillion import setset
import tempfile
import unittest


s0 = set()
s1 = set(['1'])
s2 = set(['2'])
s3 = set(['3'])
s4 = set(['4'])
s12 = set(['1', '2'])
s13 = set(['1', '3'])
s14 = set(['1', '4'])
s23 = set(['2', '3'])
s24 = set(['2', '4'])
s34 = set(['3', '4'])
s123 = set(['1', '2', '3'])
s124 = set(['1', '2', '4'])
s134 = set(['1', '3', '4'])
s234 = set(['2', '3', '4'])
s1234 = set(['1', '2', '3', '4'])

s245 = set(['2', '4', '5'])


class TestSetset(unittest.TestCase):

    def setUp(self):
        setset.set_universe(['1', '2', '3', '4'])

    def tearDown(self):
        pass

    def test_init(self):
        setset.set_universe([])

        self.assertEqual(setset._obj2int, {})
        self.assertEqual(setset._int2obj, [None])
        self.assertEqual(setset.get_universe(), [])

        setset.set_universe(['i', 'ii'])
        self.assertEqual(setset._obj2int, {'i': 1, 'ii': 2})
        self.assertEqual(setset._int2obj, [None, 'i', 'ii'])
        self.assertEqual(setset.get_universe(), ['i', 'ii'])

        ss = setset({})
        self.assertEqual(
            ss,
            setset([set(), set(['i']), set(['i','ii']), set(['ii'])]))

        setset.set_universe(['1'])
        self.assertEqual(setset._obj2int, {'1': 1})
        self.assertEqual(setset._int2obj, [None, '1'])
        self.assertEqual(setset.get_universe(), ['1'])

        ss = setset({})
        self.assertEqual(ss, setset([s0, s1]))

    def test_constructors(self):
        ss = setset()
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(repr(ss), 'setset([])')

        ss = setset(s0)
        self.assertEqual(repr(ss), 'setset([set([])])')

        ss = setset(frozenset(['1', '2']))
        self.assertEqual(repr(ss), "setset([set(['1', '2'])])")

        ss = setset([s0, s12, s13])
        self.assertEqual(repr(ss),
                         "setset([set([]), set(['1', '2']), set(['1', '3'])])")

        ss = setset({'include': ['1', '2'], 'exclude': ['4']})
        self.assertEqual(repr(ss),
                         "setset([set(['1', '2']), set(['1', '3', '2'])])")

        # copy constructor
        ss = setset([s0, s12, s13])
        self.assertEqual(repr(ss),
                         "setset([set([]), set(['1', '2']), set(['1', '3'])])")

        ss1 = setset([s0, s12, s13])
        ss2 = ss1.copy()
        self.assertTrue(isinstance(ss2, setset))
        ss1.clear()
        self.assertEqual(repr(ss1), 'setset([])')
        self.assertEqual(repr(ss2),
                         "setset([set([]), set(['1', '2']), set(['1', '3'])])")

        # large set of sets
        ss = setset({})
        self.assertEqual(
            repr(ss),
            "setset([set([]), set(['1']), set(['2']), set(['3']), set(['4']), set(['1', ' ...")

    def test_comparison(self):
        ss = setset(s12)
        self.assertEqual(ss, setset(s12))
        self.assertNotEqual(ss, setset(s13))

        v = [s0, s12, s13]
        ss = setset(v)
        self.assertTrue(ss.isdisjoint(setset([s1, s123])))
        self.assertFalse(ss.isdisjoint(setset([s1, s12])))

        self.assertTrue(ss.issubset(setset(v)))
        self.assertFalse(ss.issubset(setset([s0, s12])))
        self.assertTrue(ss <= setset(v))
        self.assertFalse(ss <= setset([s0, s12]))
        self.assertTrue(ss < setset([s0, s1, s12, s13]))
        self.assertFalse(ss < setset(v))

        self.assertTrue(ss.issuperset(setset(v)))
        self.assertFalse(ss.issuperset(setset([s1, s12])))
        self.assertTrue(ss >= setset(v))
        self.assertFalse(ss >= setset([s1, s12]))
        self.assertTrue(ss > setset([set(), s12]))
        self.assertFalse(ss > setset(v))

    def test_unary_operators(self):
        ss = setset([s0, s1, s12, s123, s1234, s134, s14, s4])

        self.assertTrue(isinstance(~ss, setset))
        self.assertEqual(~ss, setset([s124, s13, s2, s23, s234, s24,s3, s34]))

        self.assertTrue(isinstance(ss.smaller(3), setset))
        self.assertEqual(ss.smaller(3), setset([s0, s1, s12, s14, s4]))
        self.assertTrue(isinstance(ss.larger(3), setset))
        self.assertEqual(ss.larger(3), setset([s1234]))
        self.assertTrue(isinstance(ss.same_size(3), setset))
        self.assertEqual(ss.same_size(3), setset([s123, s134]))

        ss = setset([s12, s14, s23, s34])
        self.assertTrue(isinstance(ss.hitting(), setset))
        self.assertEqual(
            ss.hitting(), setset([s123, s1234, s124, s13, s134, s234, s24]))

        ss = setset([s12, s123, s1234, s245])
        self.assertTrue(isinstance(ss.minimal(), setset))
        self.assertEqual(ss.minimal(), setset([s12, s245]))
        self.assertTrue(isinstance(ss.maximal(), setset))
        self.assertEqual(ss.maximal(), setset([s1234, s245]))

    def test_binary_operators(self):
        u = [s0, s1, s12, s123, s1234, s134, s14, s4]
        v = [s12, s14, s23, s34]
        ss = setset(u) & setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s12, s14]))
        ss = setset(u).intersection(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s12, s14]))

        ss = setset(u)
        ss &= setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s12, s14]))
        ss = setset(u)
        ss.intersection_update(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s12, s14]))

        ss = setset(u) | setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(
            ss, setset([s0, s1, s12, s123, s1234, s134, s14, s23, s34, s4]))
        ss = setset(u).union(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(
            ss, setset([s0, s1, s12, s123, s1234, s134, s14, s23, s34, s4]))

        ss = setset(u)
        ss |= setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(
            ss, setset([s0, s1, s12, s123, s1234, s134, s14, s23, s34, s4]))
        ss = setset(u)
        ss.update(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(
            ss, setset([s0, s1, s12, s123, s1234, s134, s14, s23, s34, s4]))

        ss = setset(u) - setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s4]))
        ss = setset(u).difference(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s4]))

        ss = setset(u)
        ss -= setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s4]))
        ss = setset(u)
        ss.difference_update(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s4]))

        ss = setset(u) ^ setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s23, s34, s4]))
        ss = setset(u).symmetric_difference(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s23, s34, s4]))

        ss = setset(u)
        ss ^= setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s23, s34, s4]))
        ss = setset(u)
        ss.symmetric_difference_update(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s123, s1234, s134, s23, s34, s4]))

        v = [s12]
        ss = setset(u) / setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s3, s34]))
        ss = setset(u).quotient(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s3, s34]))

        ss = setset(u)
        ss /= setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s3, s34]))
        ss = setset(u)
        ss.quotient_update(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s3, s34]))

        ss = setset(u) % setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s134, s14, s4]))
        ss = setset(u).remainder(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s134, s14, s4]))

        ss = setset(u)
        ss %= setset(v)
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s134, s14, s4]))
        ss = setset(u)
        ss.remainder_update(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s134, s14, s4]))

        ss = setset(u).flip('1')
        self.assertEqual(ss, setset([s0, s1, s14, s2, s23, s234, s34, s4]))

        ss = setset(u).flip()
        self.assertEqual(ss, setset([s0, s123, s1234, s2, s23, s234, s34, s4]))

        v = [s12, s14, s23, s34]
        ss = setset(u).join(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(
            ss, setset([s12, s123, s124, s1234, s134, s14, s23, s234, s34]))

        ss = setset(u).meet(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s12, s14, s2, s23, s3, s34, s4]))

        v = [s12, s14, s23, s34]
        ss = setset(u).subsets(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s12, s14, s4]))

        ss = setset(u).supersets(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s12, s123, s1234, s134, s14]))

        ss = setset(u).non_subsets(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s123, s1234, s134]))

        ss = setset(u).non_supersets(setset(v))
        self.assertTrue(isinstance(ss, setset))
        self.assertEqual(ss, setset([s0, s1, s4]))

    def capacity(self):
        ss = setset()
        self.assertFalse(ss)

        ss = setset([s0, s12, s13])
        self.assertTrue(ss)

        self.assertEqual(len(ss), 3)
        self.assertEqual(ss.len(), 3)

    def test_iterators(self):
        ss1 = setset([s0, s12, s13])
        ss2 = setset()
        for s in ss1:
            ss2 = ss2 | setset(s)
        self.assertEqual(ss1, setset([s0, s12, s13]))
        self.assertEqual(ss1, ss2)

        ss2 = setset()
        for s in ss1:
            ss2 = ss2 | setset(s)
        self.assertEqual(ss1, ss2)

        ss1 = setset([s0, s12, s13])
        ss2 = setset()
        for s in ss1.randomize():
            ss2 = ss2 | setset(s)
        self.assertEqual(ss1, ss2)

        gen = ss1.randomize()
        self.assertTrue(isinstance(gen.next(), set))

        ss = setset([s0, s1, s12, s123, s1234, s134, s14, s4])
        r = []
        for s in ss.maximize({'1': .3, '2': -.2, '3': -.2}, default=.4):
            r.append(s)
        self.assertEqual(len(r), 8)
        self.assertEqual(r[0], s14)
        self.assertEqual(r[1], s134)
        self.assertEqual(r[2], s4)

        r = []
        for s in ss.maximize():
            r.append(s)
        self.assertEqual(len(r), 8)
        self.assertEqual(r[0], s1234)
        self.assertEqual(r[-1], set())

        r = []
        for s in ss.minimize({'1': .3, '2': -.2, '3': -.2}, default=.4):
            r.append(s)
        self.assertEqual(len(r), 8)
        self.assertEqual(r[0], s123)
        self.assertEqual(r[1], set())
        self.assertEqual(r[2], s12)

        r = []
        for s in ss.minimize():
            r.append(s)
        self.assertEqual(len(r), 8)
        self.assertEqual(r[0], set())
        self.assertEqual(r[-1], s1234)

    def test_lookup(self):
        ss1 = setset([s0, s12, s13])
        self.assertTrue(s12 in ss1)
        self.assertTrue(s1 not in ss1)

        ss2 = ss1.include('1')
        self.assertTrue(isinstance(ss2, setset))
        self.assertEqual(ss2, setset([s12, s13]))

        ss2 = ss1.exclude('2')
        self.assertTrue(isinstance(ss2, setset))
        self.assertEqual(ss2, setset([s0, s13]))

    def test_modifiers(self):
        v = [s0, s12, s13]
        ss = setset(v)
        ss.add(s1)
        self.assertTrue(s1 in ss)

        ss.remove(s1)
        self.assertTrue(s1 not in ss)
        self.assertRaises(KeyError, ss.remove, s1)

        ss.add(s1)
        ss.discard(s1)
        self.assertTrue(s1 not in ss)
        ss.discard(s1)  # no exception raised

        ss = setset(v)
        ss.add('2')
        self.assertEqual(ss, setset([s12, s123,
                                     s2]))

        ss = setset(v)
        ss.remove('2')
        self.assertEqual(ss, setset([s0, s1, s13]))
        self.assertRaises(KeyError, ss.remove, '4')

        ss = setset(v)
        ss.discard('2')
        self.assertEqual(ss, setset([s0, s1, s13]))
        ss.discard('4')  # no exception raised

        v = [s1, s12, s13]
        ss = setset(v)
        s = ss.pop()
        self.assertTrue(s not in ss)
        self.assertEqual(ss | setset(s), setset(v))

        self.assertTrue(ss)
        ss.clear()
        self.assertFalse(ss)

        self.assertRaises(KeyError, ss.pop)

    def test_io(self):
        ss = setset()
        st = ss.dumps()
        self.assertEqual(st, "B\n.\n")
        ss.loads(st)
        self.assertEqual(ss, setset())

        ss = setset(set())
        st = ss.dumps()
        self.assertEqual(st, "T\n.\n")
        ss.loads(st)
        self.assertEqual(ss, setset(set()))

        v = [s0, s1, s12, s123, s1234, s134, s14, s4]
        ss = setset(v)
        st = ss.dumps()
        ss = setset()
        ss.loads(st)
        self.assertEqual(ss, setset(v))

        # skip this test, becasue string is treated as an element
#        ss = setset(st)
#        self.assertEqual(ss, setset(v))

        f = tempfile.TemporaryFile()
        ss.dump(f)
        ss = setset()
        f.seek(0)
        ss.load(f)
        self.assertEqual(ss, setset(v))

    def test_large(self):
        n = 5000
        setset.set_universe(xrange(n))
        ss = setset({}) - setset([set([1]) - set([1, 2])])
        self.assertTrue(ss)
        self.assertAlmostEqual(ss.len() / (2**n - 2), 1)

        i = 0
        for s in ss:
            if i > 3: break
            i += 1


if __name__ == '__main__':
    unittest.main()