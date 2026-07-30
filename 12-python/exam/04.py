class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def remove(self, value):
        if not self.head:
            return
        if self.head.value == value:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return
            current = current.next

    def __repr__(self):
        result, current = [], self.head
        while current:
            result.append(str(current.value))
            current = current.next
        return " ".join(result)


ll = LinkedList()
for x in range(10):
    ll.add(x)
print("Изначальный:", ll)
ll.add(20)
ll.add(30)
ll.add(40)
print("1) Добавили:", ll)
ll.remove(5)
print("2) Убрали 5:", ll)
ll.add(101)
ll.add(366)
print("3) Добавили:", ll)
ll.remove(30)
ll.remove(366)
print("4) Удалили 30 и 366:", ll)
