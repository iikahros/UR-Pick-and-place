import socket
import time
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = "192.168.0.10"
SOCKET_PORT = 30002

# Connect to RTDE Receive (Port 30004)
rtde_r = RTDEReceiveInterface(ROBOT_IP)

def send_urscript(cmd_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((ROBOT_IP, SOCKET_PORT))
        s.sendall((cmd_str + "\n").encode("utf-8"))

# read x y z rx ry rz
start_pose = rtde_r.getActualTCPPose()
print(f"Start Pose (mm): X={start_pose[0]*1000:.2f}, Y={start_pose[1]*1000:.2f}, Z={start_pose[2]*1000:.2f}")

# step +10 mm in x
pose_plus_x = list(start_pose)
pose_plus_x[0] += 0.010

print("moving +10mm in x")
cmd_plus = f"movel(p[{pose_plus_x[0]:.6f}, {pose_plus_x[1]:.6f}, {pose_plus_x[2]:.6f}, {pose_plus_x[3]:.6f}, {pose_plus_x[4]:.6f}, {pose_plus_x[5]:.6f}], a=0.1, v=0.05)"
send_urscript(cmd_plus)
time.sleep(2.0) 

curr_pose = rtde_r.getActualTCPPose()
print(f"After +10 mm (mm): X={curr_pose[0]*1000:.2f}, Y={curr_pose[1]*1000:.2f}, Z={curr_pose[2]*1000:.2f}")

# step -10 mm in x
print("moving -10 mm in x")
cmd_minus = f"movel(p[{start_pose[0]:.6f}, {start_pose[1]:.6f}, {start_pose[2]:.6f}, {start_pose[3]:.6f}, {start_pose[4]:.6f}, {start_pose[5]:.6f}], a=0.1, v=0.05)"
send_urscript(cmd_minus)
time.sleep(2.0)

final_pose = rtde_r.getActualTCPPose()
print(f"Final Pose (mm): X={final_pose[0]*1000:.2f}, Y={final_pose[1]*1000:.2f}, Z={final_pose[2]*1000:.2f}")

rtde_r.disconnect()