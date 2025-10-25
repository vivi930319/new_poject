class Ball:
    def __init__(self, color):
      self.__color = color
    def get_color(self):
      return self.__color
def main():
    color = input("Enter the color for the ball: ")
    ball = Ball(color)
    print(f"The color of the ball is {ball.get_color()}")

main()
