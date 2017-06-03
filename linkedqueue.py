from node import QueueNode as Node

class LinkedQueue:
    """
    this class represents a queue of python objects
    """
    def __init__(self):
        """
        initializes an empty queue
        """
        self._front = None
        self._size = 0

    def __len__(self):
        """
        Returns:
             number of elemets, that are in the queue
        """
        return self._size

    def isEmpty(self):
        """
        Returns:
             True if thre is no elements in the queue,
             False otherwise
        """
        return len(self) == 0

    def push(self, data):
        """
        adds elemets to the front of the queue

        Args:
            data(object): python object that will be added to the queue
        """
        self._front = Node(data, self._front)
        self._size += 1

    def front(self):
        """
        Returns:
             front element in the queue
        """
        return self._front

    def clear(self):
        """
        Deletes all elements from the queue
        """
        self.__init__()

    def pop(self):
        """
        deletes front element in the queue and returns it

        Returns:
            object: from element in the queue
        Raises:
            AssertionError if queue is empty
        """
        assert(len(self) >= 1), "cannot pop an empty queue"
        if len(self) == 1:
            res = self._front.data
            self.clear()
            return res
        else:
            self._size -= 1
            res = self._front.data
            self._front = self._front.next
            return res