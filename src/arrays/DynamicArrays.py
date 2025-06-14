from typing import Optional


class Array:
    def __init__(self, initial_capacity: int = 2):
        # Allow customizing initial capacity, with a default
        if initial_capacity < 1:
            raise ValueError("Initial capacity must be at least 1")
        self.capacity = initial_capacity
        self.length = 0

        self.arr: list[Optional[int]] = [
            None
        ] * self.capacity  # Use None for uninitialized slots

    def __len__(self):
        """Return the number of elements in the array."""
        return self.length

    def _resize(self, new_capacity: int):
        """Resize the internal array to a new capacity."""
        new_arr: list[Optional[int]] = [None] * new_capacity
        for i in range(self.length):
            new_arr[i] = self.arr[i]
        self.arr = new_arr
        self.capacity = new_capacity

    def pushback(self, n: int):
        """Insert n at the last position of the array."""
        if self.length == self.capacity:
            self._resize(2 * self.capacity)  # Double the capacity

        self.arr[self.length] = n
        self.length += 1

    def popback(self) -> int:
        """Remove and return the last element in the array.
        Raises IndexError if the array is empty."""
        if self.length == 0:
            raise IndexError("pop from empty array")

        # (Optional) Shrink array if it's too empty
        # For example, if length is 1/4 of capacity and capacity > min_capacity
        # if self.length > 0 and self.length <= self.capacity // 4 and self.capacity > 2: # Avoid shrinking too small
        #     self._resize(self.capacity // 2)

        self.length -= 1
        popped_value = self.arr[self.length]
        assert popped_value is not None, "Value being popped should not be None"
        self.arr[self.length] = None  # Clear the reference (good practice)
        return popped_value

    def __getitem__(self, i: int) -> Optional[int]:
        """Get value at i-th index. Supports my_array[i]."""
        if not (0 <= i < self.length):  # Check for valid positive index
            raise IndexError("Index out of bounds")
        return self.arr[i]

    # For convenience, an explicit get method
    def get(self, i: int) -> Optional[int]:
        """Get value at i-th index."""
        return self.__getitem__(i)

    def __setitem__(self, i: int, n: int):
        """Set value at i-th index to n. Supports my_array[i] = n."""
        if not (0 <= i < self.length):  # Check for valid positive index
            raise IndexError("Index out of bounds")
        self.arr[i] = n

    def insert(self, i: int, n: int):
        """Insert n at i-th index, shifting subsequent elements."""
        if not (0 <= i <= self.length):  # Can insert at index 'length' (append)
            raise IndexError("Index out of bounds for insert")

        if self.length == self.capacity:
            self._resize(2 * self.capacity)

        # Shift elements to the right from the end towards index i
        for j in range(self.length, i, -1):
            self.arr[j] = self.arr[j - 1]

        self.arr[i] = n
        self.length += 1

    def __str__(self):
        """Return a string representation of the array, e.g., [1, 2, 3]."""
        if self.length == 0:
            return "[]"
        # Only include elements up to self.length
        return "[" + ", ".join(str(self.arr[k]) for k in range(self.length)) + "]"

    def __repr__(self):
        """Return a more detailed string representation for debugging."""
        return f"Array(length={self.length}, capacity={self.capacity}, data={self.__str__()})"

    # The original print method can be kept or removed if __str__ is sufficient
    def print_elements(self):  # Renamed to avoid conflict with built-in print
        """Prints each element on a new line."""
        for i in range(self.length):
            print(self.arr[i])
        if self.length > 0:  # Add newline only if something was printed
            print()


# --- Example Usage ---
if __name__ == "__main__":
    arr = Array()
    print(f"Initial: {arr!r}")  # Uses __repr__

    arr.pushback(10)
    arr.pushback(20)
    arr.pushback(30)
    print(f"After pushbacks: {arr}")  # Uses __str__
    print(f"Details: {arr!r}")

    print(f"Element at index 1: {arr[1]}")  # Uses __getitem__
    print(f"Length: {len(arr)}")  # Uses __len__

    arr.insert(1, 15)  # Insert 15 at index 1
    print(f"After insert(1, 15): {arr}")
    print(f"Details: {arr!r}")

    arr.pushback(40)
    arr.pushback(50)  # This should trigger a resize
    print(f"After more pushbacks (resize expected): {arr}")
    print(f"Details: {arr!r}")

    arr[0] = 5  # Set element at index 0 using __setitem__
    print(f"After arr[0] = 5: {arr}")

    popped = arr.popback()
    print(f"Popped: {popped}, Array after pop: {arr}")
    print(f"Details: {arr!r}")

    popped = arr.popback()
    print(f"Popped: {popped}, Array after pop: {arr}")

    print("Printing elements one by one:")
    arr.print_elements()

    # Test edge cases / errors
    try:
        print(arr[100])
    except IndexError as e:
        print(f"Caught expected error: {e}")

    try:
        empty_arr = Array(1)
        empty_arr.popback()
    except IndexError as e:
        print(f"Caught expected error: {e}")

    try:
        arr.insert(100, 99)  # Invalid index
    except IndexError as e:
        print(f"Caught expected error: {e}")

    arr.insert(len(arr), 60)  # Valid: insert at the end
    print(f"After insert(len(arr), 60): {arr}")
