import socket
import time

ROBOT_IP = "192.168.0.10"
SOCKET_PORT = 30002

def send_urscript(cmd_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((ROBOT_IP, SOCKET_PORT))
        s.sendall((cmd_str + "\n").encode("utf-8"))

def rg6_grip(width_mm: float, force_n: float):
    # This script executes locally on the robot, so it easily bypasses the HTTP firewall 
    # and connects to the OnRobot Docker container via PolyScope X's 'servicegateway'
    script = f"""def onrobot_minimove():
    on_tool_xmlrpc = rpc_factory("xmlrpc", "http://servicegateway/onrobot/onrobot-urcap/cpp_comm_docker/xmlrpc/RPC2")
    
    # Command the gripper: rg_grip(slot, width, force)
    # (Slot is 0 for a single gripper plugged directly into the flange)
    on_tool_xmlrpc.rg_grip(0, {width_mm:.2f}, {force_n:.2f})
end
"""
    print(f"Sending command: {width_mm}mm at {force_n}N")
    send_urscript(script)

print("Starting minimove...")
rg6_grip(130.0, 40.0)
time.sleep(2.0)
rg6_grip(90.0, 40.0)
print("Done!")