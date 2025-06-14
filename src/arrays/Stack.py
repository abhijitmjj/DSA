from DynamicArrays import Array


class Stack:
    def __init__(self):
        # Use the custom Array class as the underlying storage
        self.container = Array(initial_capacity=2)  # Or any desired initial capacity

    def push(self, n):
        """Adds an item to the top of the stack."""
        self.container.pushback(n)  # Use Array's pushback

    def pop(self):
        """Removes and returns the item from the top of the stack.
        Raises IndexError if the stack is empty."""
        # Array's popback already raises IndexError if empty
        return self.container.popback()

    def peek(self):
        """Returns the item at the top of the stack without removing it.
        Raises IndexError if the stack is empty."""
        if len(self.container) == 0:
            raise IndexError("peek from empty stack")
        return self.container[
            len(self.container) - 1
        ]  # Access last element using Array's __getitem__

    def is_empty(self):
        """Returns True if the stack is empty, False otherwise."""
        return len(self.container) == 0

    def __len__(self):
        """Returns the number of items in the stack."""
        return len(self.container)  # Relies on Array's __len__

    def __str__(self):
        """Returns a string representation of the stack."""
        # Modify to show "top" of stack appropriately if desired,
        # for now, just delegate to Array's __str__
        return f"Stack(top->{str(self.container)})"


class StackWithPythonList:
    def __init__(self):
        self._items = []  # Using _items to denote internal storage

    def push(self, n):
        """Adds an item to the top of the stack."""
        self._items.append(n)

    def pop(self):
        """Removes and returns the item from the top of the stack.
        Raises IndexError if the stack is empty."""
        if not self._items:  # or if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Returns the item at the top of the stack without removing it.
        Raises IndexError if the stack is empty."""
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """Returns True if the stack is empty, False otherwise."""
        return len(self._items) == 0  # or return not self._items

    def __len__(self):
        """Returns the number of items in the stack."""
        return len(self._items)

    def __str__(self):
        """Returns a string representation of the stack."""
        return f"Stack({self._items})"


# --- Example Usage (Stack with custom Array) ---
if __name__ == "__main__":
    print("\n--- Testing Stack with custom Array ---")
    s_custom = Stack()
    s_custom.push(10)
    s_custom.push(20)
    s_custom.push(
        30
    )  # Should trigger resize in underlying Array if initial_capacity was 2
    print(s_custom)
    print(f"Length: {len(s_custom)}")
    print(f"Peek: {s_custom.peek()}")
    print(f"Pop: {s_custom.pop()}")
    print(f"After pop: {s_custom}")
    print(f"Peek: {s_custom.peek()}")
    print(f"Is empty? {s_custom.is_empty()}")
    s_custom.pop()
    s_custom.pop()
    print(f"Is empty after more pops? {s_custom.is_empty()}")
    print(f"After all pops: {s_custom}")

    try:
        s_custom.pop()
    except IndexError as e:
        print(f"Caught expected error: {e}")

    try:
        s_custom.peek()
    except IndexError as e:
        print(f"Caught expected error: {e}")

    s_custom.push(100)
    print(f"After pushing 100: {s_custom}")
    print(f"Peek: {s_custom.peek()}")
