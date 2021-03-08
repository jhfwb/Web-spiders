class A:
    name='张三'
    def __str__(self):
        return self.name
if __name__ == '__main__':
    print([A()])