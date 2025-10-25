class Student:
    def _init_(self,name,score1,score2):
        self._name=name
        self._score1=score1
        self._score2=score2
        
    def calculate_average(self):
        return (self._score1+self._score2)/2
    
    def get_name(self):
        return (self._name)
def main():
    s1=Student('Mary',90,80)
    s2=Student('John',82,86)

    print (f"The average score for {s1.get_name()} is {s1.calculate_average()}")
    print (f"The average score for {s2.get_name()} is {s2.calculate_average()}")

main ()
