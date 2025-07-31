"""Tests for the main Driver class and entry points in cacts.cacts module."""
import os
import tempfile
from unittest.mock import patch

import pytest
from cacts.cacts import Driver, parse_command_line


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing"""
    config_content = """
project:
  name: TestProject

machines:
  default:
    num_bld_res: 4
    num_run_res: 8
    env_setup: []
  test_machine:
    num_bld_res: 2
    num_run_res: 4
    env_setup: []

configurations:
  default:
    longname: Default Build
    cmake_args: {}
  debug:
    longname: Debug Build
    cmake_args:
      CMAKE_BUILD_TYPE: Debug
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        f.flush()
        yield f.name

    # Cleanup
    os.unlink(f.name)


def test_driver_initialization():
    """Test Driver class initialization"""
    # Create a temporary config file
    config_content = """
project:
  name: TestProject

machines:
  default:
    num_bld_res: 4
    num_run_res: 8
    env_setup: []
  test_machine:
    num_bld_res: 2
    num_run_res: 4
    env_setup: []

configurations:
  default:
    longname: Default Build
    cmake_args: {}
  debug:
    longname: Debug Build
    cmake_args:
      CMAKE_BUILD_TYPE: Debug
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        f.flush()

        try:
            driver = Driver(
                config_file=f.name,
                machine_name='test_machine',
                build_types=['debug'],
                work_dir='/tmp/test',
                verbose=True
            )

            assert driver._verbose is True
            assert str(driver._work_dir).endswith('test')
        finally:
            os.unlink(f.name)


@patch('cacts.cacts.pathlib.Path.exists')
@patch('yaml.load')
def test_driver_with_config_file(mock_yaml_load, mock_exists, temp_config_file):
    """Test Driver initialization with config file"""
    mock_exists.return_value = True
    mock_yaml_load.return_value = {
        'project': {'name': 'TestProject'},
        'machines': {
            'default': {'num_bld_res': 4, 'num_run_res': 8, 'env_setup': []},
            'test_machine': {'num_bld_res': 2, 'num_run_res': 4, 'env_setup': []}
        },
        'configurations': {
            'default': {'longname': 'Default Build', 'cmake_args': {}},
            'debug': {'longname': 'Debug Build', 'cmake_args': {'CMAKE_BUILD_TYPE': 'Debug'}}
        }
    }

    driver = Driver(
        config_file=temp_config_file,
        machine_name='test_machine',
        build_types=['debug']
    )

    # Basic initialization test - detailed testing would require more complex mocking
    assert str(driver._config_file) == temp_config_file


def test_parse_command_line():
    """Test command line parsing"""
    args = [
        'cacts',
        '--machine-name', 'test_machine',
        '--build-types', 'debug',
        '--verbose'
    ]

    parsed_args = parse_command_line(args, "Test description", "1.0.0")

    assert parsed_args.machine_name == 'test_machine'
    assert parsed_args.build_types == ['debug']
    assert parsed_args.verbose is True


def test_parse_command_line_minimal():
    """Test command line parsing with minimal arguments"""
    args = ['cacts']

    parsed_args = parse_command_line(args, "Test description", "1.0.0")

    # Test default values
    assert parsed_args.machine_name is None
    assert parsed_args.verbose is False
    assert parsed_args.parallel is False


@patch('cacts.cacts.Driver.run')
@patch('cacts.cacts.parse_command_line')
def test_main_function_success(mock_parse_command_line, mock_run):
    """Test main function with successful run"""
    # Create a mock namespace object instead of MagicMock
    mock_args = type('MockArgs', (), {
        'config_file': None,
        'machine_name': 'test_machine',
        'local': False,
        'build_types': ['debug'],
        'work_dir': None,
        'root_dir': None,
        'baseline_dir': None,
        'cmake_args': None,
        'test_regex': None,
        'test_labels': None,
        'config_only': False,
        'build_only': False,
        'skip_config': False,
        'skip_build': False,
        'generate': False,
        'submit': False,
        'parallel': False,
        'verbose': False
    })()

    mock_parse_command_line.return_value = mock_args
    mock_run.return_value = True

    from cacts.cacts import main

    with patch('cacts.cacts.Driver.__init__', return_value=None):
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_run.assert_called_once()


@patch('cacts.cacts.Driver.run')
@patch('cacts.cacts.parse_command_line')
def test_main_function_failure(mock_parse_command_line, mock_run):
    """Test main function with failed run"""
    # Create a mock namespace object instead of MagicMock
    mock_args = type('MockArgs', (), {
        'config_file': None,
        'machine_name': 'test_machine',
        'local': False,
        'build_types': ['debug'],
        'work_dir': None,
        'root_dir': None,
        'baseline_dir': None,
        'cmake_args': None,
        'test_regex': None,
        'test_labels': None,
        'config_only': False,
        'build_only': False,
        'skip_config': False,
        'skip_build': False,
        'generate': False,
        'submit': False,
        'parallel': False,
        'verbose': False
    })()

    mock_parse_command_line.return_value = mock_args
    mock_run.return_value = False

    from cacts.cacts import main

    with patch('cacts.cacts.Driver.__init__', return_value=None):
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        mock_run.assert_called_once()
