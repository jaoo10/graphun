import unittest
from unittest import TestCase
from graphcheck import *

class GraphTest(TestCase):
    def setUp(self):
        self.gu = Graph([1, 2, 3], [(1, 2, 10), (3, 2, 20)], directed=False)
        self.gd = Graph([1, 2, 3], [(1, 2, 10), (3, 2, 20)])
    
    def test_cost(self):
        g = self.gu
        self.assertEqual(10, g.cost(1, 2))
        self.assertEqual(10, g.cost(2, 1))
        self.assertEqual(20, g.cost(2, 3))
        self.assertEqual(20, g.cost(3, 2))
        g = self.gd
        self.assertEqual(10, g.cost(1, 2))
        self.assertEqual(20, g.cost(3, 2))

    def test_is_adj(self):
        g = self.gu
        self.assertFalse(g.is_adj(1, 1))
        self.assertTrue (g.is_adj(1, 2))
        self.assertFalse(g.is_adj(1, 3))
        self.assertTrue (g.is_adj(2, 1))
        self.assertFalse(g.is_adj(2, 2))
        self.assertTrue (g.is_adj(2, 3))
        self.assertFalse(g.is_adj(3, 1))
        self.assertTrue (g.is_adj(3, 2))
        self.assertFalse(g.is_adj(3, 3))
        g = self.gd
        self.assertFalse(g.is_adj(1, 1))
        self.assertTrue (g.is_adj(1, 2))
        self.assertFalse(g.is_adj(1, 3))
        self.assertFalse(g.is_adj(2, 1))
        self.assertFalse(g.is_adj(2, 2))
        self.assertFalse(g.is_adj(2, 3))
        self.assertFalse(g.is_adj(3, 1))
        self.assertTrue (g.is_adj(3, 2))
        self.assertFalse(g.is_adj(3, 3))

    def test_adj(self):
        g = self.gu
        self.assertEqual([2], list(g.adj(1)))
        self.assertEqual([1, 3], list(g.adj(2)))
        self.assertEqual([2], list(g.adj(3)))
        g = self.gd
        self.assertEqual([2], list(g.adj(1)))
        self.assertEqual([], list(g.adj(2)))
        self.assertEqual([2], list(g.adj(3)))


class ParseTgfTest(TestCase):
    def setUp(self):
        self.tgf = ['1',
                    '2',
                    '3',
                    '#',
                    '1 2 10',
                    '3 2']

    def test_parse_pgf(self):
        g = parse_tgf(self.tgf)
        self.assertTrue(g.directed)
        self.assertEqual(['1', '2', '3'], g.V)
        self.assertEqual(set([('1', '2', 10), ('3', '2', None)]), g.E)

    def test_parse_pgf_undirect(self):
        g = parse_tgf_undirected(self.tgf)
        self.assertFalse(g.directed)
        self.assertEqual(['1', '2', '3'], g.V)
        self.assertEqual(set([('1', '2', 10), ('3', '2', None)]), g.E)


class FakeTestResult(object):
    def __init__(self):
        self.errors = []

    def add_error(self, msg, expected=None, actual=None):
        self.errors.append((msg, expected, actual))

    def success(self):
        return not self.errors

class BfsTest(TestCase):
    def test_bfs_parse_valid(self):
        actual = bfs_parse(['1 2 3', '4 5 6'])
        expected = {('1', '2') : '3',
                    ('4', '5') : '6'}
        self.assertEqual(expected, actual)

    def test_bfs_parse_invalid(self):
        # less values
        self.assertRaises(ParseError, bfs_parse, ['1 2'])
        # more values
        self.assertRaises(ParseError, bfs_parse, ['1 2 3 4'])
        # duplicated edge
        self.assertRaises(ParseError, bfs_parse, ['1 2 3', '1 2 4'])

    def test_bfs_check_success(self):
        e = {('1', '3') : '1',
             ('1', '2') : '2'}

        test_result = FakeTestResult()
        bfs_check(test_result, e, dict(e))
        self.assertTrue(test_result.success())

    def test_bfs_check_fail(self):
        e = {('1', '3') : '1',
             ('1', '2') : '2'}
        test_result = FakeTestResult()
        bfs_check(test_result, e, {('1', '3') : '2',
                                   ('1', '2') : '1'})
        self.assertEqual(len(test_result.errors), 1)
        # check error message
        _, expected, actual = test_result.errors[0]
        self.assertEqual(expected, ['1 2 2', '1 3 1'])
        self.assertEqual(actual, ['1 2 1', '1 3 2'])


class TsTest(TestCase):
    def setUp(self):
        self.g = Graph([1, 2, 3], [(1, 2, None), (2, 3, None)])

    def test_ts_check_success(self):
        test_result = FakeTestResult()
        ts_check(test_result, self.g, [1, 2, 3])
        self.assertTrue(test_result.success())
        
    def test_ts_check_invalid_vertex(self):
        test_result = FakeTestResult()
        ts_check(test_result, self.g, [1, 2, 30])
        self.assertFalse(test_result.success())

    def test_ts_check_duplicated_vertex(self):
        test_result = FakeTestResult()
        ts_check(test_result, self.g, [1, 2, 2, 3])
        self.assertFalse(test_result.success())

    def test_ts_check_bad_edge(self):
        # bad = right -> left edge
        test_result = FakeTestResult()
        ts_check(test_result, self.g, [1, 3, 2])
        self.assertFalse(test_result.success())

class SccTest(TestCase):
    def setUp(self):
        self.sccs = [['1', '2', '3'], ['4'], ['5']]
    
    def test_scc_check_success(self):
        test_result = FakeTestResult()
        scc_check(test_result, self.sccs, [['5'], ['2', '3', '1'], ['4']])
        self.assertTrue(test_result.success())
                               
        # different order
        test_result = FakeTestResult()
        scc_check(test_result, self.sccs, [['5'], ['2', '3', '1'], ['4']])
        self.assertTrue(test_result.success())

    def test_scc_check_duplicated_vertex(self):
        test_result = FakeTestResult()
        scc_check(test_result, self.sccs, [['5', '5'], ['2', '3', '1'], ['4']])
        self.assertFalse(test_result.success())

    def test_scc_check_wrong_scc(self):
        test_result = FakeTestResult()
        scc_check(test_result, self.sccs, [['2'], ['5', '3', '1'], ['4']])
        self.assertFalse(test_result.success())
        _, e, a = test_result.errors[0]
        self.assertEqual(['1 2 3', '4', '5'], e)
        self.assertEqual(['1 3 5', '2', '4'], a)


class SpTest(TestCase):
    def setUp(self):
        self.g = Graph(['a', 'b', 'c', 'd', 'e'],
                       [('a', 'b', 3), ('a', 'c', 1), ('a', 'd', 5),
                        ('b', 'd', 3), ('c', 'd', 3), ('e', 'a', 2)])
        self.path = {
            ('a', 'a') : (['a'], 0),
            ('a', 'b') : (['a', 'b'], 3),
            ('a', 'c') : (['a', 'c'], 1),
            ('a', 'd') : (['a', 'c', 'd'], 4),
        }

    def test_sp_parse(self):
        r = sp_parse(['a b c 2', 'c 4'])
        self.assertEqual({('a', 'c') : (['a', 'b', 'c'], 2),
                          ('c', 'c') : (['c'], 4)},
                         r)
        # less values
        self.assertRaises(ParseError, sp_parse, ['a'])
        # repeated
        self.assertRaises(ParseError, sp_parse, ['a b c d 4', 'a d 2'])

    def test_is_path(self):
        self.assertTrue(is_path(self.g, ['a']))
        self.assertTrue(is_path(self.g, ['a', 'b']))
        self.assertTrue(is_path(self.g, ['a', 'b', 'd']))
        self.assertFalse(is_path(self.g, ['a', 'c', 'd', 'b']))

    def test_path_cost(self):
        self.assertEqual(0, path_cost(self.g, ['a']))
        self.assertEqual(3, path_cost(self.g, ['a', 'b']))
        self.assertEqual(6, path_cost(self.g, ['a', 'b', 'd']))
        self.assertEqual(4, path_cost(self.g, ['a', 'c', 'd']))

    def test_sp_check_ok(self):
        p = dict(self.path)
        test_result = FakeTestResult()
        sp_check(test_result, self.g, self.path, p)
        self.assertTrue(test_result.success())

    def test_sp_check_missing(self):
        p = dict(self.path)
        del p[('a', 'a')]
        test_result = FakeTestResult()
        sp_check(test_result, self.g, self.path, p)
        self.assertFalse(test_result.success())

    def test_sp_check_extra(self):
        p = dict(self.path)
        p[('a', 'e')] = (['a', 'e'], 2)
        test_result = FakeTestResult()
        sp_check(test_result, self.g, self.path, p)
        self.assertFalse(test_result.success())

    def test_sp_check_not_path(self):
        p = dict(self.path)
        p[('a', 'b')] = (['a', 'c', 'b'], 3)
        test_result = FakeTestResult()
        sp_check(test_result, self.g, self.path, p)
        self.assertFalse(test_result.success())

    def test_sp_check_wrong_cost(self):
        p = dict(self.path)
        p[('a', 'd')] = (['a', 'c', 'd'], 5)
        test_result = FakeTestResult()
        sp_check(test_result, self.g, self.path, p)
        self.assertFalse(test_result.success())

    def test_sp_check_not_shortest(self):
        p = dict(self.path)
        p[('a', 'd')] = (['a', 'd'], 5)
        test_result = FakeTestResult()
        sp_check(test_result, self.g, self.path, p)
        self.assertFalse(test_result.success())


class MstTest(TestCase):
    def setUp(self):
        self.g = Graph(['a', 'b', 'c', 'd'],
                       [('a', 'b', 3), ('a', 'c', 1), ('a', 'd', 2),
                        ('b', 'd', 3), ('c', 'd', 3)],
                       directed=False)
        # edges in tree (a, b), (a, c) e (a, d)
        self.weight = 6

    def test_mst_parse_result(self):
        self.assertEqual([('a', 'b'), ('a', 'c'), ('c', 'd')],
                         mst_parse_result(['a b', 'a c', 'c d']))

        self.assertRaises(ParseError, mst_parse_result, ['a'])
        self.assertRaises(ParseError, mst_parse_result, ['a', 'b', 'c'])

    def test_mst_check_success(self):
        test_result = FakeTestResult()
        mst_check(test_result, self.g, self.weight, [('a', 'b'), ('d', 'a'), ('c', 'a')])
        self.assertTrue(test_result.success())

    def test_mst_check_invalid_edge(self):
        test_result = FakeTestResult()
        mst_check(test_result, self.g, 6, [('b', 'c'), ('d', 'a'), ('c', 'a')])
        self.assertFalse(test_result.success())

    def test_mst_check_not_a_tree(self):
        # same weight, not a tree (|edges| < |V| - 1)
        test_result = FakeTestResult()
        mst_check(test_result, self.g, self.weight, [('b', 'd'), ('d', 'c')])
        self.assertFalse(test_result.success())

        # same weight, |edges| = |V| - 1, not a tree (more than one component)
        test_result = FakeTestResult()
        mst_check(test_result, self.g, self.weight, [('a', 'c'), ('a', 'd'), ('d', 'c')])
        self.assertFalse(test_result.success())

    def test_mst_check_wrong_weight(self):
        test_result = FakeTestResult()
        mst_check(test_result, self.g, self.weight, [('b', 'd'), ('d', 'c'), ('d', 'a')])
        self.assertFalse(test_result.success())


if __name__ == '__main__':
    unittest.main()
