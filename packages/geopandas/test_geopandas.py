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


# CI 검증용 더미 실패 테스트 - pytest-results-action 동작 확인용
@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["geopandas"])
def test_ci_verification_dummy_fail(selenium):
    """CI 검증용 더미 실패 테스트 - pytest-results-action이 실패한 테스트만 표시하는지 확인"""
    # 의도적으로 실패하는 assertion
    assert 1 == 2, "Intentional failure for CI verification of pytest-results-action"
