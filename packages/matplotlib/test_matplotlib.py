import pathlib
from functools import reduce

import pytest
from pytest_pyodide import run_in_pyodide

REFERENCE_IMAGES_PATH = pathlib.Path(__file__).parent / "test_data"

DECORATORS = [
    pytest.mark.xfail_browsers(node="No supported matplotlib backends on node"),
    pytest.mark.skip_refcount_check,
    pytest.mark.skip_pyproxy_check,
    pytest.mark.driver_timeout(60),
]


def matplotlib_test_decorator(f):
    return reduce(lambda x, g: g(x), DECORATORS, f)


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_plot(selenium):
    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    plt.show()


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_plot_with_pause(selenium):
    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    plt.pause(0.001)
    plt.show()


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_svg(selenium):
    import io

    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    fd = io.BytesIO()
    plt.savefig(fd, format="svg")

    content = fd.getvalue().decode("utf8")
    assert len(content) == 15016
    assert content.startswith("<?xml")


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_pdf(selenium):
    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    import io

    fd = io.BytesIO()
    plt.savefig(fd, format="pdf")


@pytest.mark.xfail(reason="FIXME")
@run_in_pyodide(packages=["matplotlib"])
def test_font_manager(selenium):
    """
    Comparing vendored fontlist.json version with the one built
    by font_manager.py.

    If you try to update Matplotlib and this test fails, try to
    update fontlist.json.
    """
    import json
    import os

    from matplotlib import font_manager as fm

    # get fontlist form file
    fontist_file = os.path.join(os.path.dirname(fm.__file__), "fontlist.json")
    with open(fontist_file) as f:
        fontlist_vendor = json.loads(f.read())

    # get fontlist from build
    fontlist_built = json.loads(json.dumps(fm.FontManager(), cls=fm._JSONEncoder))

    # reordering list to compare
    for l in ("afmlist", "ttflist"):
        for fontlist in (fontlist_vendor, fontlist_built):
            fontlist[l].sort(key=lambda x: x["fname"])

    assert fontlist_built == fontlist_vendor


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_triangulation(selenium):
    """This test uses setjmp/longjmp so hopefully prevents any more screw ups
    with that...
    """
    import matplotlib.tri as tri
    import numpy as np

    # First create the x and y coordinates of the points.
    n_angles = 36
    n_radii = 8
    min_radius = 0.25
    radii = np.linspace(min_radius, 0.95, n_radii)

    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi / n_angles

    x = (radii * np.cos(angles)).flatten()
    y = (radii * np.sin(angles)).flatten()

    # Create the Triangulation; no triangles so Delaunay triangulation created.
    tri.Triangulation(x, y)


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_destroy(selenium):
    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    plt.show()
    plt.close()


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_call_close_multi_times(selenium):
    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    plt.show()
    plt.close()
    plt.close()


@matplotlib_test_decorator
@run_in_pyodide(packages=["matplotlib"])
def test_call_show_and_close_multi_times(selenium):
    from matplotlib import pyplot as plt

    plt.figure()
    plt.plot([1, 2, 3])
    plt.show()
    plt.close()
    plt.plot([1, 2, 3])
    plt.show()
    plt.close()


# CI 검증용 더미 실패 테스트들 - pytest-results-action 동작 확인용
@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["matplotlib"])
def test_ci_verification_matplotlib_fail_1(selenium):
    """CI 검증용 matplotlib 실패 테스트 1 - 잘못된 데이터로 플롯 생성"""
    from matplotlib import pyplot as plt
    import numpy as np
    
    # 잘못된 데이터 (None 값 포함)
    x_data = [1, 2, None, 4, 5]
    y_data = [1, 4, 9, 16, 25]
    
    plt.figure()
    plt.plot(x_data, y_data)
    plt.show()
    
    # 이 테스트는 실제로는 matplotlib가 None을 처리할 수 있어서 실패하지 않을 수 있음
    # 따라서 명시적으로 실패하도록 assertion 추가
    assert None not in x_data, "Data should not contain None values"

@pytest.mark.driver_timeout(60)
@run_in_pyodide(packages=["matplotlib"])
def test_ci_verification_matplotlib_fail_2(selenium):
    """CI 검증용 matplotlib 실패 테스트 2 - 잘못된 색상 값"""
    from matplotlib import pyplot as plt
    
    plt.figure()
    # 잘못된 색상 값
    invalid_color = "invalid_color_name"
    plt.plot([1, 2, 3], color=invalid_color)
    plt.show()
    
    # 색상이 유효한지 확인 (실제로는 matplotlib가 기본 색상으로 대체할 수 있음)
    assert invalid_color in plt.gca().get_lines()[0].get_color(), f"Expected color {invalid_color} but got different color"
