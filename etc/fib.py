class Fib:
    def __init__(self):
        self.lazy = {}
    def value(self, x):
        if x <= 1: return 1
        elif not x in self.lazy:
            self.lazy[x] =  x * self.value(x-1)
        return self.lazy[x]

if __name__ == "__main__":
    x = Fib()
    print x.value(5)
    print x.value(10)

