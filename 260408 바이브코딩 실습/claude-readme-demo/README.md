# 간단한 계산기 프로젝트

## 1. 프로젝트 개요

Python으로 만든 간단한 계산기 프로그램입니다.  
더하기, 빼기, 곱하기, 나누기 기능을 제공하며, 테스트 코드도 함께 포함되어 있습니다.  
Python을 처음 배우는 분들도 쉽게 이해할 수 있도록 구성되어 있습니다.

---

## 2. 폴더 구조

```
claude-readme-demo/
├── src/
│   ├── __init__.py          # 패키지 인식 파일
│   ├── calculator.py        # 계산기 핵심 함수 모음
│   └── main.py              # 프로그램 실행 진입점
├── tests/
│   ├── __init__.py          # 테스트 패키지 인식 파일
│   └── test_calculator.py   # 계산기 함수 테스트 코드
├── requirements.txt         # 필요한 패키지 목록
├── AGENTS.md                # AI 에이전트 작업 규칙
└── README.md                # 프로젝트 설명 파일
```

---

## 3. 설치 방법

### 사전 조건
- Python 3.8 이상이 설치되어 있어야 합니다.

### 패키지 설치

```bash
pip install -r requirements.txt
```

---

## 4. 실행 방법

프로젝트 루트 폴더(`claude-readme-demo`)에서 아래 명령어를 실행합니다.

```bash
python -m src.main
```

### 실행 결과 예시

```
간단한 계산기 예제
2 + 3 = 5
5 - 2 = 3
4 * 6 = 24
8 / 2 = 4.0
```

---

## 5. 테스트 방법

프로젝트 루트 폴더에서 아래 명령어를 실행합니다.

```bash
pytest
```

### 테스트 항목

| 테스트 함수           | 설명                              |
|----------------------|-----------------------------------|
| `test_add`           | 2 + 3 = 5 인지 확인               |
| `test_subtract`      | 5 - 2 = 3 인지 확인               |
| `test_multiply`      | 4 × 3 = 12 인지 확인              |
| `test_divide`        | 8 / 2 = 4 인지 확인               |
| `test_divide_by_zero`| 0으로 나눌 때 오류 발생 확인       |

---

## 6. 주요 함수 설명

모든 계산 함수는 `src/calculator.py` 에 정의되어 있습니다.

### `add(a, b)` — 더하기

두 숫자를 더한 결과를 반환합니다.

```python
add(2, 3)  # 결과: 5
```

### `subtract(a, b)` — 빼기

첫 번째 숫자에서 두 번째 숫자를 뺀 결과를 반환합니다.

```python
subtract(5, 2)  # 결과: 3
```

### `multiply(a, b)` — 곱하기

두 숫자를 곱한 결과를 반환합니다.

```python
multiply(4, 6)  # 결과: 24
```

### `divide(a, b)` — 나누기

첫 번째 숫자를 두 번째 숫자로 나눈 결과를 반환합니다.  
**주의:** `b`가 0이면 `ValueError`가 발생합니다.

```python
divide(8, 2)   # 결과: 4.0
divide(10, 0)  # 오류: ValueError - 0으로 나눌 수 없습니다.
```
