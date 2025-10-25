class Ball:
    def _init_(self,color):
        self._color=color
    def get_color(self):
        return self._color
def main():
    color=input("Enter the color for the ball")
    ball=Ball(color)
    print(f"The color of the ball is{ball.get_color()}")
main()
