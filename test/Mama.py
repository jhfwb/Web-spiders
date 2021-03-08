class Animal():
    name = "candy"

    def __init__(self, age,height=111111):
        self.age = age

        self.height = height


class Dog(Animal):
    hand = "have"

    def __init__(self, colour):
        self.colour = colour

        self.length = 19

        super().__init__(age=11)

if __name__ == '__main__':

    dog = Dog("yellow")

    print(dog.colour, dog.height, dog.age, dog.length, dog.name, dog.hand)