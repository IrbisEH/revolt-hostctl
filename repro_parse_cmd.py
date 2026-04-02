import os
import shutil
from pathlib import Path
from revolt_hostctl.app.app import App

def setup_test_env():
    test_dir = Path("test_vm_dir")
    test_dir.mkdir(exist_ok=True)
    
    vm1_dir = test_dir / "vm1"
    vm1_dir.mkdir(exist_ok=True)
    vm1_vmx = vm1_dir / "vm1.vmx"
    vm1_vmx.write_text('ethernet0.address = "00:0C:29:C4:6D:27"\nother_config = "value"', encoding='utf-8')
    
    vm2_dir = test_dir / "vm2"
    vm2_dir.mkdir(exist_ok=True)
    vm2_vmx = vm2_dir / "vm2.vmx"
    vm2_vmx.write_text('some_config = "abc"\nethernet0.address = "00:0C:29:A1:B2:C3"', encoding='utf-8')
    
    return test_dir

def cleanup_test_env(test_dir):
    if test_dir.exists():
        shutil.rmtree(test_dir)

def test_parse_cmd():
    test_dir = setup_test_env()
    try:
        app = App()
        # Mock storage for transaction decorators if needed, 
        # but parse_cmd in the provided code doesn't seem to use storage for anything other than transaction logic
        # and it returns mac_addresses.
        
        # We need to ensure storage.load_state/save_state don't fail if they are called.
        # Since App initializes ShelveAdapter, it might create some files.
        
        macs = app.parse_cmd([str(test_dir)])
        print(f"Extracted MACs: {macs}")
        assert "00:0C:29:C4:6D:27" in macs
        assert "00:0C:29:A1:B2:C3" in macs
        assert len(macs) == 2
        print("Test passed!")
    finally:
        cleanup_test_env(test_dir)

if __name__ == "__main__":
    test_parse_cmd()
