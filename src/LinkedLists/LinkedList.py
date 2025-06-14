from __future__ import annotations
from typing import Optional

# class ListNode:
#     def __init__(self, val):
#         self.val = val
#         self.next = None

# # Implementation for Singly Linked List
# class LinkedList:
#     def __init__(self):
#         # Init the list with a 'dummy' node which makes
#         # removing a node from the beginning of list easier.
#         self.head = ListNode(-1)
#         self.tail = self.head

#     def insertEnd(self, val):
#         self.tail.next = ListNode(val)
#         self.tail = self.tail.next

#     def remove(self, index):
#         i = 0
#         curr = self.head
#         while i < index and curr:
#             i += 1
#             curr = curr.next

#         # Remove the node ahead of curr
#         if curr and curr.next:
#             if curr.next == self.tail:
#                 self.tail = curr
#             curr.next = curr.next.next

#     def print(self):
#         curr = self.head.next
#         while curr:
#             print(curr.val, " -> ", end="")
#             curr = curr.next
#         print()


# LinkedList.py
class ListNode:
    def __init__(
        self, val: int = 0, next_node: Optional[ListNode] = None
    ):  # Added default for val, next_node
        self.val: int = val
        self.next: Optional[ListNode] = next_node

    def __repr__(self):
        return f"ListNode(val={self.val}, next={self.next})"


class LinkedList:
    def __init__(self):
        """
        Initializes the linked list with a dummy head node.
        This simplifies insertion and deletion operations, especially at the head.
        """
        self.head = ListNode(-1)  # Dummy node with an arbitrary value
        self.tail = self.head  # Initially, the tail is the dummy node
        self.size = 0  # Keep track of the number of actual elements

    def get(self, index: int) -> int:
        """
        Returns the value of the node at the given index.
        Raises IndexError if the index is out of bounds.
        Time complexity: O(index) which is O(N) in the worst case.
        """
        if not (0 <= index < self.size):
            raise IndexError("Index out of bounds")

        curr = self.head.next  # Start from the first actual node
        for _ in range(index):
            curr = curr.next
        return curr.val

    def insertHead(self, val: int) -> None:
        """
        Inserts a new node with the given value at the beginning of the list.
        Time complexity: O(1).
        """
        new_node = ListNode(val)
        new_node.next = self.head.next
        self.head.next = new_node
        if self.size == 0:  # If list was empty, new node is also the tail
            self.tail = new_node
        self.size += 1

    def insertEnd(
        self, val: int
    ) -> None:  # Original method, renamed for consistency if preferred: append
        """
        Inserts a new node with the given value at the end of the list.
        Time complexity: O(1).
        """
        new_node = ListNode(val)
        self.tail.next = new_node
        self.tail = new_node  # Update tail to the new node
        self.size += 1

    # Alias for insertEnd
    def append(self, val: int) -> None:
        self.insertEnd(val)

    def remove(self, index: int) -> bool:  # Changed to return bool for success
        """
        Removes the node at the given 0-based index.
        Returns True if removal was successful, False otherwise (e.g., index out of bounds).
        Time complexity: O(index) for finding, O(1) for removal, so O(N) worst case.
        """
        if not (0 <= index < self.size):
            # Or raise IndexError("Index out of bounds for remove operation")
            return False

        curr = self.head  # curr will be the node *before* the one to remove
        for _ in range(index):
            curr = curr.next

        node_to_remove = curr.next

        if node_to_remove == self.tail:  # If removing the tail node
            self.tail = curr  # The new tail is the node before it

        curr.next = node_to_remove.next  # Bypass the node
        # node_to_remove.next = None # Optional: clean up removed node's pointer

        self.size -= 1

        # If the list becomes empty, reset tail to dummy head
        if self.size == 0:
            self.tail = self.head

        return True

    def __len__(self) -> int:
        """Returns the number of actual elements in the list."""
        return self.size

    def is_empty(self) -> bool:
        """Checks if the list is empty."""
        return self.size == 0

    def __str__(self) -> str:
        """
        Returns a string representation of the linked list.
        e.g., [1 -> 2 -> 3]
        """
        if self.is_empty():
            return "[]"

        parts = []
        curr = self.head.next  # Start from the first actual node
        while curr:
            parts.append(str(curr.val))
            curr = curr.next
        return "[" + " -> ".join(parts) + "]"


# --- Example Usage ---
if __name__ == "__main__":
    ll = LinkedList()
    print(f"Initial: {ll}, Size: {len(ll)}, Empty: {ll.is_empty()}")

    ll.append(10)
    ll.append(20)
    ll.insertHead(5)
    print(
        f"After appends and insertHead: {ll}, Size: {len(ll)}"
    )  # Expected: [5 -> 10 -> 20]
    print(f"Tail value (should be 20): {ll.tail.val}")

    ll.append(30)
    print(f"After append(30): {ll}, Size: {len(ll)}")  # Expected: [5 -> 10 -> 20 -> 30]
    print(f"Tail value (should be 30): {ll.tail.val}")

    print(f"Value at index 0: {ll.get(0)}")  # Expected: 5
    print(f"Value at index 2: {ll.get(2)}")  # Expected: 20
    # print(f"Value at index 10: {ll.get(10)}") # Expected: IndexError

    print(f"Removing at index 1 (value 10): {ll.remove(1)}")  # True
    print(f"After removing index 1: {ll}, Size: {len(ll)}")  # Expected: [5 -> 20 -> 30]
    print(f"Tail value (should be 30): {ll.tail.val}")

    print(f"Removing at index 2 (value 30 - the tail): {ll.remove(2)}")  # True
    print(f"After removing index 2: {ll}, Size: {len(ll)}")  # Expected: [5 -> 20]
    print(f"Tail value (should be 20): {ll.tail.val if not ll.is_empty() else 'N/A'}")

    print(f"Removing at index 0 (value 5): {ll.remove(0)}")  # True
    print(f"After removing index 0: {ll}, Size: {len(ll)}")  # Expected: [20]
    print(f"Tail value (should be 20): {ll.tail.val if not ll.is_empty() else 'N/A'}")

    print(f"Removing at index 0 (value 20): {ll.remove(0)}")  # True
    print(
        f"After removing last element: {ll}, Size: {len(ll)}, Empty: {ll.is_empty()}"
    )  # Expected: [], Size: 0, Empty: True
    print(f"Tail value (should be dummy's -1): {ll.tail.val}")

    print(f"Attempt remove from empty list: {ll.remove(0)}")  # False
    ll.append(100)
    print(
        f"After adding 100 to empty: {ll}, Tail: {ll.tail.val}"
    )  # Expected: [100], Tail: 100
