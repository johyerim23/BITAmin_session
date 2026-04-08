from src.calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 2) == 3

def test_multiply():
    assert multiply(4, 3) == 12

def test_divide():
    assert divide(8, 2) == 4

def test_divide_by_zero():
    try:
        divide(10, 0)
        assert False, "ValueError가 발생해야 합니다."
    except ValueError:
        assert True
