"""
CI 검증용 더미 실패 테스트
이 파일은 CI 파이프라인이 실패를 제대로 감지하는지 확인하기 위한 용도입니다.
실제 테스트가 아니므로 CI 검증 후 삭제해야 합니다.
"""

import pytest


def test_ci_fail_dummy():
    """
    CI 검증용 더미 실패 테스트
    이 테스트는 의도적으로 실패하도록 작성되었습니다.
    """
    # 의도적으로 실패하는 assertion
    assert 1 == 2, "This is an intentional failure for CI verification"


def test_ci_fail_dummy_import():
    """
    CI 검증용 더미 실패 테스트 - import 에러 시뮬레이션
    """
    # 존재하지 않는 모듈을 import하려고 시도
    import nonexistent_module_for_ci_test  # noqa: F401
    assert True


if __name__ == "__main__":
    # 직접 실행 시에도 실패하도록
    test_ci_fail_dummy()
