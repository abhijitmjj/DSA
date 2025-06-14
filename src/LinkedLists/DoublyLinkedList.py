from typing import Optional, Any, List


class ListNode:
    def __init__(
        self,
        val: Any = 0,
        prev: "Optional[ListNode]" = None,
        next: "Optional[ListNode]" = None,
    ):
        self.val: Any = val
        self.prev: Optional[ListNode] = prev
        self.next: Optional[ListNode] = next


class MyLinkedList:
    def __init__(self):
        self.head: ListNode = ListNode(-1)  # Dummy head
        self.tail: ListNode = ListNode(-1)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size: int = 0

    def _get_node_at_actual_index(self, index: int) -> Optional[ListNode]:
        """Helper to get the actual data node at 0-based index. Returns None if invalid."""
        if index < 0 or index >= self.size:
            return None

        # Optimized traversal
        if index <= self.size // 2:
            curr = self.head.next  # Start from first actual node
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev  # Start from last actual node
            # Steps back from last actual node to reach node at 'index'
            # (size-1) is last index. (size-1) - index = steps back
            for _ in range(self.size - 1 - index):
                curr = curr.prev
        return curr

    def get(self, index: int) -> int:
        node = self._get_node_at_actual_index(index)
        return node.val if node else -1

    def addAtHead(self, val: int) -> None:
        predecessor = self.head
        successor = self.head.next

        new_node = ListNode(val)
        new_node.prev = predecessor
        new_node.next = successor

        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1

    def addAtTail(self, val: int) -> None:
        predecessor = self.tail.prev  # Last actual node
        successor = self.tail  # Dummy tail

        new_node = ListNode(val)
        new_node.prev = predecessor
        new_node.next = successor

        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0:  # Interpret negative index as 0 for LeetCode problem style
            index = 0
        if index > self.size:  # Cannot insert beyond current_size + 1 (append)
            return

        if index == 0:
            self.addAtHead(val)
            return
        if index == self.size:
            self.addAtTail(val)
            return

        # Find the node that will be *after* the new node (successor)
        # Optimized way to find the successor node at 'index'
        successor = self.head.next  # Start from the first actual data node
        if index <= self.size // 2:
            for _ in range(index):
                successor = successor.next
        else:
            successor = self.tail  # Start from dummy tail
            for _ in range(self.size - index):  # Number of steps back from dummy tail
                successor = successor.prev

        predecessor = successor.prev  # Guaranteed to exist because index > 0

        new_node = ListNode(val)
        new_node.prev = predecessor
        new_node.next = successor

        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        node_to_delete = self._get_node_at_actual_index(index)
        if not node_to_delete:  # Should be caught by size check already
            return

        predecessor = node_to_delete.prev
        successor = node_to_delete.next

        # predecessor and successor are guaranteed to be non-None because of dummy nodes
        # and index < self.size (so node_to_delete is not self.tail)
        predecessor.next = successor
        successor.prev = predecessor

        self.size -= 1

    def get_values(self) -> List[Any]:
        values = []
        curr = self.head.next
        while curr != self.tail:
            values.append(curr.val)
            curr = curr.next
        return values


# Test cases again:
ll = MyLinkedList()
print("Initial:", ll.get_values(), "Size:", ll.size)

ll.addAtHead(1)
print("addAtHead(1):", ll.get_values(), "Size:", ll.size)  # [1]

ll.addAtTail(3)
print("addAtTail(3):", ll.get_values(), "Size:", ll.size)  # [1, 3] Correct now.

ll.addAtIndex(1, 2)
print("addAtIndex(1, 2):", ll.get_values(), "Size:", ll.size)  # [1, 2, 3]

print("get(1):", ll.get(1))  # Expected: 2

ll.deleteAtIndex(0)
print("deleteAtIndex(0):", ll.get_values(), "Size:", ll.size)  # [2, 3]

ll.addAtIndex(0, 10)
print("addAtIndex(0,10):", ll.get_values(), "Size:", ll.size)  # [10, 2, 3]

ll.addAtIndex(3, 20)
print("addAtIndex(3,20):", ll.get_values(), "Size:", ll.size)  # [10, 2, 3, 20]

print("get(3):", ll.get(3))  # Expected: 20
print("get(0):", ll.get(0))  # Expected: 10
print("head value:", ll.head.next.val)  # Expected: 10
print("tail value:", ll.tail.prev.val)  # Expected: 20

ll.deleteAtIndex(3)
print("deleteAtIndex(3):", ll.get_values(), "Size:", ll.size)  # [10, 2, 3]

ll.deleteAtIndex(1)
print("deleteAtIndex(1):", ll.get_values(), "Size:", ll.size)  # [10, 3]

print("Testing get with optimized path (index > size//2):")
ll.addAtTail(4)
ll.addAtTail(5)
print(f"Current List: {ll.get_values()}")  # [10,3,4,5]
print("get(3):", ll.get(3))  # Expected 5.

ll.deleteAtIndex(ll.size - 1)
print("deleteAtIndex(last):", ll.get_values(), "Size:", ll.size)

ll.deleteAtIndex(0)
print("deleteAtIndex(0):", ll.get_values(), "Size:", ll.size)

ll.deleteAtIndex(1)
print("deleteAtIndex(1):", ll.get_values(), "Size:", ll.size)
ll.deleteAtIndex(0)
print("deleteAtIndex(0):", ll.get_values(), "Size:", ll.size)

print("get from empty list:", ll.get(0))

ll.addAtTail(77)
print("addAtTail(77) to empty:", ll.get_values(), "Size:", ll.size)
ll.deleteAtIndex(0)
print("delete from list with 1 elem:", ll.get_values(), "Size:", ll.size)

ll.addAtIndex(0, 7)
print("addAtIndex(0,7):", ll.get_values(), "Size:", ll.size)
ll.addAtHead(1)
print("addAtHead(1):", ll.get_values(), "Size:", ll.size)
print("get(1):", ll.get(1))
