import os
import json
import pypot.dynamixel
import poppy_humanoid

# 1. Perform real-time hardware scan
found_ids = []
try:
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        print("[ERROR] No USB port found!")
    else:
        port = ports[0]
        # Open the port and actually scan all motors between 0-253
        with pypot.dynamixel.DxlIO(port) as dxl_io:
            print("Scanning hardware, please wait...")
            found_ids = dxl_io.scan(range(254))
except Exception as e:
    print(f"Hardware scan error: {e}")

# 2. Read the Poppy configuration file
try:
    config_path = os.path.join(os.path.dirname(poppy_humanoid.__file__), 'configuration', 'poppy_humanoid.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    expected_motors = config.get('motors', {})
except Exception as e:
    print(f"Can not read configuration file: {e}")
    expected_motors = {}

# 3. Compare the actually found IDs (found_ids) with the expected ones
if expected_motors:
    print(f"\n{'Motor Name':<22} | {'Waited ID':<12} | {'Status':<15}")
    print("=" * 56)
    
    missing_count = 0
    # Check in order of ID
    for name, info in sorted(expected_motors.items(), key=lambda x: x[1].get('id', 0)):
        m_id = info.get('id')
        
        # Now it looks at the list returned from the hardware, not the manually written list
        if m_id in found_ids:
            status = "✅ Connection OK"
        else:
            status = "❌ Can not connected"
            missing_count += 1
            
        print(f"{name:<22} | {m_id:<12} | {status:<15}")
        
    print("=" * 56)
    print(f"Result: {len(found_ids)} motors axis connected. {missing_count} motors axis can not connected!")