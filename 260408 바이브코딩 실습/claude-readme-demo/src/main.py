from src.calculator import add, subtract, multiply, divide

def main():
    print("간단한 계산기 예제")
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
    print("4 * 6 =", multiply(4, 6))
    print("8 / 2 =", divide(8, 2))

if __name__ == "__main__":
    main()
