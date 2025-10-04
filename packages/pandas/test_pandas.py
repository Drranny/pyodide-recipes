import random
from typing import Any

import pytest


def generate_largish_json(n_rows: int = 91746) -> dict[str, Any]:
    # with n_rows = 91746, the output JSON size will be ~15 MB/10k rows

    # Note: we don't fix the random seed here, but the actual values
    # shouldn't matter
    columns = [
        ("column0", lambda: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"),
        (
            "column1",
            lambda: random.choice(
                [
                    "notification-interval-longer",
                    "notification-interval-short",
                    "control",
                ]
            ),
        ),
        ("column2", lambda: random.choice([True, False])),
        ("column3", lambda: random.randint(0, 4)),
        ("column4", lambda: random.randint(0, 4)),
        ("column5", lambda: random.randint(0, 4)),
        ("column6", lambda: random.randint(0, 4)),
        ("column7", lambda: random.randint(0, 4)),
    ]
    data = {}
    for name, generator in columns:
        data[name] = [generator() for _ in range(n_rows)]
    return data


@pytest.mark.driver_timeout(30)
def test_extra_import(selenium, request):
    selenium.load_package("pandas")
    selenium.run("from pandas import Series, DataFrame")


@pytest.mark.xfail_browsers(
    chrome="test_load_largish_file triggers a fatal runtime error in Chrome 89 see #1495",
    node="open_url doesn't work in node",
    firefox="matplotlib now disabled",
)
@pytest.mark.driver_timeout(40)
@pytest.mark.skip_refcount_check
def test_load_largish_file(selenium_standalone, request, httpserver):
    selenium = selenium_standalone
    selenium.load_package("pandas")
    selenium.load_package("matplotlib")

    n_rows = 91746

    data = generate_largish_json(n_rows)

    httpserver.expect_oneshot_request("/pandas_largish").respond_with_json(
        data, headers={"Access-Control-Allow-Origin": "*"}
    )
    request_url = httpserver.url_for("/pandas_largish")

    selenium.run(
        f"""
        import pyodide.http
        import matplotlib.pyplot as plt
        import pandas as pd

        df = pd.read_json(pyodide.http.open_url('{request_url}'))
        assert df.shape == ({n_rows}, 8)
        """
    )


# CI 검증용 더미 실패 테스트들 - pytest-results-action 동작 확인용
@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["pandas"])
def test_ci_verification_pandas_fail_1(selenium):
    """CI 검증용 pandas 실패 테스트 1 - DataFrame 크기 비교 실패"""
    import pandas as pd
    df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    df2 = pd.DataFrame({'A': [1, 2], 'B': [4, 5]})
    assert df1.shape == df2.shape, f"DataFrame shape mismatch: {df1.shape} != {df2.shape}"

@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["pandas"])
def test_ci_verification_pandas_fail_2(selenium):
    """CI 검증용 pandas 실패 테스트 2 - Series 값 비교 실패"""
    import pandas as pd
    s1 = pd.Series([1, 2, 3, 4])
    s2 = pd.Series([1, 2, 3, 5])
    pd.testing.assert_series_equal(s1, s2, "Series values don't match")

@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["pandas"])
def test_ci_verification_pandas_fail_3(selenium):
    """CI 검증용 pandas 실패 테스트 3 - 인덱스 비교 실패"""
    import pandas as pd
    df = pd.DataFrame({'A': [1, 2, 3]}, index=['a', 'b', 'c'])
    expected_index = ['x', 'y', 'z']
    assert list(df.index) == expected_index, f"Index mismatch: {list(df.index)} != {expected_index}"
