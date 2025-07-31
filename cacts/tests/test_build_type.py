"""Tests for the BuildType class in cacts.build_type module."""
import types

import pytest

from cacts.build_type import BuildType


@pytest.fixture
def build_type():
    """Create a BuildType instance for testing"""
    name = 'test_build'
    project = types.SimpleNamespace(name="TestProject")
    machine = types.SimpleNamespace(name="TestMachine", env_setup=["echo 'Setting up environment'"])
    builds_specs = {
        'default': {
            'longname': 'default_longname',
            'description': 'default_description',
            'uses_baselines': 'True',
            'on_by_default': 'True',
            'cmake_args': {'arg1': 'value1'}
        },
        'test_build': {
            'longname': 'test_longname',
            'description': 'test_description',
            'uses_baselines': 'False',
            'on_by_default': 'False',
            'cmake_args': {'arg2': 'value2'}
        }
    }
    bt = BuildType(name, project, machine, builds_specs)
    return bt


def test_initialization(build_type):
    """Test BuildType initialization"""
    assert build_type.name == 'test_build'
    assert build_type.longname == 'test_longname'
    assert build_type.description == 'test_description'
    # Note: BuildType uses str_to_bool internally, so these should be boolean
    assert build_type.uses_baselines is False
    assert build_type.on_by_default is False
    # cmake_args should merge default and specific build args
    assert 'arg1' in build_type.cmake_args
    assert 'arg2' in build_type.cmake_args


def test_invalid_build_name():
    """Test BuildType with invalid build name"""
    project = types.SimpleNamespace(name="TestProject")
    machine = types.SimpleNamespace(name="TestMachine")
    builds_specs = {
        'default': {},
        'valid_build': {}
    }

    with pytest.raises(RuntimeError, match="BuildType 'invalid_build' not found"):
        BuildType('invalid_build', project, machine, builds_specs)


def test_invalid_builds_specs_type():
    """Test BuildType with invalid builds_specs type"""
    project = types.SimpleNamespace(name="TestProject")
    machine = types.SimpleNamespace(name="TestMachine")

    with pytest.raises(RuntimeError, match="BuildType constructor expects a dict object"):
        BuildType('test', project, machine, "not_a_dict")
