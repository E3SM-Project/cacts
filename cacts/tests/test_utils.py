"""Tests for utility functions in the cacts.utils module."""

import pytest
from cacts.utils import (expect, run_cmd, run_cmd_no_fail, evaluate_py_expressions,
                        str_to_bool, is_git_repo)


def test_expect():
    """Test the expect function"""
    # Should not raise when condition is True
    expect(True, "This should not raise")

    # Should raise RuntimeError when condition is False
    with pytest.raises(RuntimeError, match="ERROR: This should raise"):
        expect(False, "This should raise")

    # Test custom exception type
    with pytest.raises(ValueError, match="ERROR: Custom exception"):
        expect(False, "Custom exception", exc_type=ValueError)


def test_run_cmd():
    """Test the run_cmd function"""
    stat, output, errput = run_cmd("echo Hello, World!")
    assert stat == 0
    assert output == "Hello, World!"
    assert errput == ""

    # Test command that fails
    stat, output, errput = run_cmd("exit 1")
    assert stat == 1


def test_run_cmd_no_fail():
    """Test the run_cmd_no_fail function"""
    output = run_cmd_no_fail("echo Hello, World!")
    assert output == "Hello, World!"

    # Test command that fails should raise exception
    with pytest.raises(RuntimeError):
        run_cmd_no_fail("exit 1")


def test_evaluate_py_expressions():
    """Test the evaluate_py_expressions function"""

    class MockObject:
        """Mock object for testing evaluate_py_expressions."""
        def __init__(self):
            self.name = "MockObject"
            self.value = "${project.name}_value"

    mock_obj = MockObject()
    result = evaluate_py_expressions(mock_obj, {'project': mock_obj})
    assert result.value == "MockObject_value"

    # Test dict evaluation
    test_dict = {"key": "${test_var}"}
    result = evaluate_py_expressions(test_dict, {'test_var': 'test_value'})
    assert result["key"] == "test_value"

    # Test list evaluation
    test_list = ["${test_var}"]
    result = evaluate_py_expressions(test_list, {'test_var': 'test_value'})
    assert result[0] == "test_value"


def test_str_to_bool():
    """Test the str_to_bool function"""
    assert str_to_bool("True", "test_var") is True
    assert str_to_bool("False", "test_var") is False

    with pytest.raises(ValueError, match="Invalid value 'Invalid' for 'test_var'"):
        str_to_bool("Invalid", "test_var")


def test_is_git_repo():
    """Test the is_git_repo function"""
    # Should return True since we're in a git repo
    assert is_git_repo() is True

    # Test with a path that's not a git repo
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        assert is_git_repo(temp_dir) is False
