def test_eed_basic_utils_import():
    try:
        import eed_basic_utils  # noqa: F401
    except ImportError as e:
        raise ImportError("eed_basic_utils module could not be imported") from e

    try:
        from eed_basic_utils import os, time  # noqa: F401
    except ImportError as e:
        raise ImportError("eed_basic_utils submodules could not be imported") from e
