def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    from collections import deque

    if not nums or k <= 0:
        return []

    result = []
    deq = deque()

    for i in range(len(nums)):
        # Remove elements not in the current window
        if deq and deq[0] < i - k + 1:
            deq.popleft()

        # Remove elements smaller than the current element from the deque
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()

        deq.append(i)

        # Append the maximum for the current window to the result
        if i >= k - 1:
            result.append(nums[deq[0]])

    return result

if __name__ == "__main__":
    # Example usage
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(sliding_window_maximum(nums, k))  # Output: [3, 3, 5, 5, 6, 7]
    