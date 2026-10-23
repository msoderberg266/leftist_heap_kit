from __future__ import annotations


class _Node:
    __slots__ = ("key", "left", "right", "sval")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.sval = 1


class LeftistHeap:
    """A leftist heap (min-heap) with O(log n) merge."""

    def __init__(self, items=None):
        self._root = None
        self._size = 0
        if items is not None:
            for x in items:
                self.push(x)

    def __len__(self):
        return self._size

    def __bool__(self):
        return self._size > 0

    def __iter__(self):
        aux = []
        if self._root is not None:
            aux.append(self._root)
        while aux:
            node = aux.pop()
            yield node.key
            if node.left is not None:
                aux.append(node.left)
            if node.right is not None:
                aux.append(node.right)

    def push(self, key):
        self._root = self._merge_nodes(self._root, _Node(key))
        self._size += 1

    def peek(self):
        if self._root is None:
            raise IndexError("peek from empty heap")
        return self._root.key

    def pop(self):
        if self._root is None:
            raise IndexError("pop from empty heap")
        node = self._root
        self._root = self._merge_nodes(node.left, node.right)
        self._size -= 1
        return node.key

    def merge(self, other):
        if not isinstance(other, LeftistHeap):
            raise TypeError("merge requires a LeftistHeap")
        self._root = self._merge_nodes(self._root, other._root)
        self._size += other._size
        other._root = None
        other._size = 0

    @classmethod
    def _merge_nodes(cls, a, b):
        if a is None:
            return b
        if b is None:
            return a
        if b.key < a.key:
            a, b = b, a
        a.right = cls._merge_nodes(a.right, b)
        ls = a.left.sval if a.left is not None else 0
        rs = a.right.sval if a.right is not None else 0
        if ls < rs:
            a.left, a.right = a.right, a.left
        a.sval = (a.right.sval if a.right is not None else 0) + 1
        return a
