import unittest

from leftist_heap_kit import LeftistHeap


class TestConstruction(unittest.TestCase):
    def test_empty_len_zero(self):
        self.assertEqual(len(LeftistHeap()), 0)

    def test_empty_pop_raises(self):
        with self.assertRaises(IndexError):
            LeftistHeap().pop()

    def test_init_from_iterable(self):
        h = LeftistHeap([5, 3, 8, 1, 9, 2, 7, 0])
        self.assertEqual(len(h), 8)
        self.assertEqual(h.pop(), 0)

    def test_init_from_generator(self):
        h = LeftistHeap(x * x - 10 for x in range(5))
        out = [h.pop() for _ in range(len(h))]
        self.assertEqual(out, [-10, -9, -6, -1, 6])


class TestBasicOps(unittest.TestCase):
    def test_push_peek_order(self):
        h = LeftistHeap()
        h.push(4)
        self.assertEqual(h.peek(), 4)
        h.push(2)
        self.assertEqual(h.peek(), 2)
        h.push(6)
        self.assertEqual(h.peek(), 2)
        h.push(1)
        self.assertEqual(h.peek(), 1)

    def test_pop_decrements_size(self):
        h = LeftistHeap([3, 1, 2])
        self.assertEqual(h.pop(), 1)
        self.assertEqual(len(h), 2)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(len(h), 1)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(len(h), 0)

    def test_pop_all_sorted(self):
        import random
        data = list(range(200))
        random.seed(42)
        random.shuffle(data)
        h = LeftistHeap(data)
        out = [h.pop() for _ in range(len(h))]
        self.assertEqual(out, sorted(data))

    def test_duplicates_preserved(self):
        h = LeftistHeap([5, 5, 5, 3, 3, 1, 1])
        out = []
        while h:
            out.append(h.pop())
        self.assertEqual(out, [1, 1, 3, 3, 5, 5, 5])

    def test_negatives(self):
        h = LeftistHeap([-5, 3, -10, 0, 7, -1])
        out = []
        while h:
            out.append(h.pop())
        self.assertEqual(out, sorted([-5, 3, -10, 0, 7, -1]))

    def test_bool(self):
        h = LeftistHeap()
        self.assertFalse(h)
        h.push(1)
        self.assertTrue(h)
        h.pop()
        self.assertFalse(h)


class TestMerge(unittest.TestCase):
    def test_merge_two_nonempty(self):
        a = LeftistHeap([5, 1, 3, 7])
        b = LeftistHeap([2, 6, 0, 4])
        a.merge(b)
        self.assertEqual(len(a), 8)
        self.assertEqual(len(b), 0)
        self.assertFalse(b)
        out = [a.pop() for _ in range(len(a))]
        self.assertEqual(out, [0, 1, 2, 3, 4, 5, 6, 7])

    def test_merge_into_empty(self):
        a = LeftistHeap()
        b = LeftistHeap([3, 1, 2])
        a.merge(b)
        self.assertEqual(len(a), 3)
        self.assertEqual([a.pop() for _ in range(len(a))], [1, 2, 3])

    def test_merge_empty_into_nonempty(self):
        a = LeftistHeap([3, 1, 2])
        b = LeftistHeap()
        a.merge(b)
        self.assertEqual(len(a), 3)
        self.assertEqual(a.pop(), 1)

    def test_merge_two_empty(self):
        a = LeftistHeap()
        b = LeftistHeap()
        a.merge(b)
        self.assertEqual(len(a), 0)
        self.assertEqual(len(b), 0)

    def test_merge_leaves_source_empty(self):
        a = LeftistHeap([1, 2, 3])
        b = LeftistHeap([4, 5, 6])
        a.merge(b)
        self.assertFalse(b)
        with self.assertRaises(IndexError):
            b.pop()

    def test_merge_chained(self):
        heaps = [LeftistHeap([i * 3, i * 3 + 1, i * 3 + 2]) for i in range(5)]
        acc = heaps[0]
        for h in heaps[1:]:
            acc.merge(h)
        self.assertEqual(len(acc), 15)
        self.assertEqual([acc.pop() for _ in range(15)], list(range(15)))

    def test_merge_type_error(self):
        a = LeftistHeap([1, 2])
        with self.assertRaises(TypeError):
            a.merge([3, 4])


class TestIteration(unittest.TestCase):
    def test_iter_yields_all(self):
        h = LeftistHeap([9, 3, 7, 1, 5])
        self.assertEqual(sorted(h), [1, 3, 5, 7, 9])

    def test_iter_empty(self):
        self.assertEqual(list(LeftistHeap()), [])


class TestStabilityProperty(unittest.TestCase):
    def test_leftist_property_after_inserts(self):
        h = LeftistHeap(list(range(1, 50)))
        bad = []
        stack = [h._root] if h._root else []
        while stack:
            node = stack.pop()
            ls = node.left.sval if node.left else 0
            rs = node.right.sval if node.right else 0
            if ls < rs:
                bad.append(node.key)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        self.assertEqual(bad, [])

    def test_sval_is_shortest_path_to_null(self):
        import random
        random.seed(7)
        h = LeftistHeap(random.randint(0, 1000) for _ in range(100))
        stack = [h._root] if h._root else []
        while stack:
            node = stack.pop()
            if node.left is None and node.right is None:
                self.assertEqual(node.sval, 1)
            elif node.right is None:
                self.assertEqual(node.sval, 1)
            else:
                self.assertEqual(node.sval, node.right.sval + 1)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)


if __name__ == "__main__":
    unittest.main()
