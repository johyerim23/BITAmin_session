# AGENTS.md
## Goal
이 프로젝트는 머신러닝 모델 코드에 대해
테스트 코드 생성과 리팩토링을 수행하는 것을 목표로 한다.
## Task
1. train.py를 분석한다.
2. 테스트 코드(test_train.py)를 생성한다.
3. 코드 구조를 개선한 리팩토링 버전을 생성한다.
## Test Requirements
- pytest 기반 테스트 코드 생성
- train_and_evaluate() 함수 테스트
- 반환값이 dict인지 검증
- accuracy 값이 0~1 사이인지 검증
- results.json 파일 생성 여부 확인
## Refactoring Requirements
- 함수 분리 (데이터 로드 / 모델 생성 / 평가)
- 코드 가독성 개선
- 하나의 함수에 몰린 로직 분리
## Commands
pytest
## Completion Criteria
- test_train.py 생성
- pytest 실행 성공
- train_refactored.py 생성