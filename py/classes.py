class Artifact:
    id = ''
    group = ''
    version = ''

class Waiter:
    queue = ['\\', '|', '/', '-']
    current = 0

    def print(self):
        print(self.queue[self.current], end='\r')
        self.current += 1
        if (self.current >= len(self.queue)):
            self.current = 0