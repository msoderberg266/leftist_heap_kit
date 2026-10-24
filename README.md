# leftist_heap_kit

A pure-Python, zero-dependency leftist heap: a min-priority queue whose `merge` operation runs in O(log n) time.

```python
from leftist_heap_kit import LeftistHeap

a = LeftistHeap([5, 1, 3, 7])
b = LeftistHeap([2, 6, 0, 4])
a.merge(b)          # b is now empty; a holds all 8 items
print(a.peek())     # 0
print(a.pop())      # 0
print(list(a))      # yields remaining elements (unspecified order)
```

## Why

Binary heaps merge in O(n) time because you must rebuild. Leftist heaps add a single field per node — the length of the shortest path to a null child — and use it to keep the right spine short. Merging two heaps is a recursive zip along their right spines, giving O(log n) merges without any rebuild step. The cost is a larger constant factor and slightly worse cache locality than an array-backed binary heap. Use this library when merging priority queues is the bottleneck.

## Edge cases

`merge` moves all elements from the argument heap into the target and leaves the argument empty — it does not copy. If you need to preserve the source, construct a second heap and merge that instead.

All keys must be mutually comparable with `<`. The heap has no notion of an explicit capacity.
