import pytest
from pytest_pyodide import run_in_pyodide


@pytest.mark.xfail(
    reason="Takes too long, TODO: test less stuff or split up between multiple tests"
)
@run_in_pyodide(packages=["geopandas", "geopandas-tests", "pytest"])
def test_runtest(selenium):
    from pathlib import Path

    import geopandas
    import pytest

    test_path = Path(geopandas.__file__).parent / "tests"

    def runtest(test_filter, ignore_filters):
        ignore_filter = []
        for ignore in ignore_filters:
            ignore_filter.append("--ignore-glob")
            ignore_filter.append(ignore)

        ret = pytest.main(
            [
                "--pyargs",
                str(test_path),
                "--continue-on-collection-errors",
                # "-v",
                *ignore_filter,
                "-k",
                test_filter,
                # "--durations",
                # "20",
            ]
        )
        assert ret == 0

    runtest(
        (
            "not test_transform2 "  # CppException std::invalid_argument: non double value
            "and not test_no_additional_imports "  # subprocess
            "and not test_pandas_kind "  # scipy required
        ),
        [
            str(
                test_path / "test_dissolve.py"
            ),  # CppException osgeo::proj::io::ParsingException: unrecognized format / unknown name
            str(
                test_path / "test_geodataframe.py"
            ),  # CppException osgeo::proj::io::ParsingException: unrecognized format / unknown name
            str(
                test_path / "test_testing.py"
            ),  # CppException osgeo::proj::io::ParsingException: unrecognized format / unknown name
            str(test_path / "test_array.py"),  # libc.so required
            # These tests passes, but disabled because they takes too long to run in CI.
            str(test_path / "test_plotting.py"),
            str(test_path / "test_datasets.py"),
            str(test_path / "test_extension_array.py"),
            str(test_path / "test_crs.py"),
            str(test_path / "test_testing.py"),
            str(test_path / "test_merge.py"),
            str(test_path / "test_explore.py"),
        ],
    )


# CI 검증용 더미 실패 테스트들 - pytest-results-action 동작 확인용
@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["geopandas"])
def test_ci_verification_dummy_fail_1(selenium):
    """CI 검증용 더미 실패 테스트 1 - 기본 assertion 실패"""
    assert 1 == 2, "Intentional failure for CI verification of pytest-results-action"

@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["geopandas"])
def test_ci_verification_dummy_fail_2(selenium):
    """CI 검증용 더미 실패 테스트 2 - 문자열 비교 실패"""
    expected = "Hello World"
    actual = "Hello Pyodide"
    assert expected == actual, f"Expected '{expected}' but got '{actual}'"

@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["geopandas"])
def test_ci_verification_dummy_fail_3(selenium):
    """CI 검증용 더미 실패 테스트 3 - 리스트 비교 실패"""
    expected_list = [1, 2, 3, 4, 5]
    actual_list = [1, 2, 3, 4, 6]
    assert expected_list == actual_list, f"List mismatch: {expected_list} != {actual_list}"
