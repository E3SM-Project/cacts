import pytest
from cacts.machine import Machine
import types


@pytest.fixture
def machine():
    """Create a Machine instance for testing"""
    project = types.SimpleNamespace(name="TestProject")
    machines_specs = {
        'default': {
            'num_bld_res': 4,
            'num_run_res': 8,
            'env_setup': ['echo "Setting up environment"']
        },
        'test_machine': {
            'num_bld_res': 2,
            'num_run_res': 4,
            'env_setup': ['echo "Setting up test environment"']
        }
    }
    return Machine('test_machine', project, machines_specs)


def test_initialization(machine):
    """Test Machine initialization"""
    assert machine.name == 'test_machine'
    assert machine.num_bld_res == 2
    assert machine.num_run_res == 4
    assert machine.env_setup == ['echo "Setting up test environment"']


def test_uses_gpu(machine):
    """Test Machine uses_gpu method"""
    # Initially should not use GPU
    assert machine.uses_gpu() is False
    
    # After setting gpu_arch, should use GPU
    machine.gpu_arch = 'test_gpu_arch'
    assert machine.uses_gpu() is True


def test_invalid_machine_name():
    """Test Machine with invalid machine name"""
    project = types.SimpleNamespace(name="TestProject")
    machines_specs = {
        'default': {},
        'valid_machine': {}
    }
    
    with pytest.raises(RuntimeError, match="Machine 'invalid_machine' not found"):
        Machine('invalid_machine', project, machines_specs)


def test_invalid_machines_specs_type():
    """Test Machine with invalid machines_specs type"""
    project = types.SimpleNamespace(name="TestProject")
    
    with pytest.raises(RuntimeError, match="Machine constructor expects a dict object"):
        Machine('test', project, "not_a_dict")