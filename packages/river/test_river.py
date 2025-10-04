import pytest
from pytest_pyodide import run_in_pyodide


@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["river"])
def test_linear_regression(selenium):
    from river import datasets, evaluate, linear_model, metrics, preprocessing

    dataset = datasets.TrumpApproval()

    model = preprocessing.StandardScaler() | linear_model.LinearRegression(
        intercept_lr=0.1
    )
    metric = metrics.MAE()

    evaluate.progressive_val_score(dataset, model, metric)


# CI 검증용 더미 실패 테스트 - 테스트 결과 파싱 로직 검증용
@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["river"])
def test_ci_verification_dummy_fail(selenium):
    """CI 검증용 더미 실패 테스트 - 테스트 결과 파싱 로직 검증"""
    # 의도적으로 실패하는 assertion
    assert 1 == 2, "Intentional failure for CI verification of test result parsing"
