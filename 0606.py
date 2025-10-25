class Student:
    def __init__(self, name, score1, score2):
        self.__name = name
        self.__score1 = score1
        self.__score2 = score2

    def calculate_average(self):
        return (self.__score1 + self.__score2) / 2

    def get_name(self):
        return (self.__name)

def main():
    s1 = Student('Mary', 90, 80)
    s2 = Student('John', 82, 86)

    print(f"The average score for {s1.get_name()} is {s1.calculate_average()}")
    print(f"The average score for {s2.get_name()} is {s2.calculate_average()}")
main()
