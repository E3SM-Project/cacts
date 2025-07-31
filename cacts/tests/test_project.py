"""Tests for the Project class in cacts.project module."""
import pytest

from cacts.project import Project


@pytest.fixture
def project():
    """Create a Project instance for testing"""
    project_specs = {
        'name': 'TestProject',
        'baseline_gen_label': 'gen_label',
        'baseline_cmp_label': 'cmp_label',
        'baseline_summary_file': 'summary_file',
        'cmake_settings': {
            'baselines_on': {'var1': 'value1'},
            'baselines_off': {'var2': 'value2'}
        },
        'cdash': {'key1': 'value1'}
    }
    root_dir = '/path/to/root'
    return Project(project_specs, root_dir)


def test_initialization(project):
    """Test Project initialization"""
    assert project.name == 'TestProject'
    assert project.baselines_gen_label == 'gen_label'
    assert project.baselines_cmp_label == 'cmp_label'
    assert project.baselines_summary_file == 'summary_file'
    assert project.cdash == {'key1': 'value1'}
    assert project.root_dir == '/path/to/root'


def test_missing_name():
    """Test Project with missing name field"""
    project_specs = {
        'baseline_gen_label': 'gen_label'
    }

    with pytest.raises(RuntimeError, match="Missing required field 'name'"):
        Project(project_specs, '/path/to/root')


def test_unrecognized_keys():
    """Test Project with unrecognized keys"""
    project_specs = {
        'name': 'TestProject',
        'invalid_key': 'invalid_value'
    }

    with pytest.raises(RuntimeError, match="Unrecognized keys in project_specs: invalid_key"):
        Project(project_specs, '/path/to/root')


def test_invalid_project_specs_type():
    """Test Project with invalid project_specs type"""
    with pytest.raises(RuntimeError, match="Project constructor expects a dict object"):
        Project("not_a_dict", '/path/to/root')


def test_default_values():
    """Test Project with minimal configuration"""
    project_specs = {
        'name': 'MinimalProject'
    }
    project = Project(project_specs, '/test/path')

    assert project.name == 'MinimalProject'
    assert project.baselines_gen_label is None
    assert project.baselines_cmp_label is None
    assert project.baselines_summary_file is None
    assert project.cdash == {}
    assert project.root_dir == '/test/path'

    # Check that cmake_settings subdicts are created
    assert 'baselines_on' in project.cmake_settings
    assert 'baselines_off' in project.cmake_settings
    assert 'baselines_only' in project.cmake_settings
