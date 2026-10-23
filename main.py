import math
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = "192.168.0.10"  

# connect to the RTDE receive interface (port 30004)
rtde_r = RTDEReceiveInterface(ROBOT_IP)

# -----------------------------------------------------------
# tcp pose
# -----------------------------------------------------------
tcp_pose = rtde_r.getActualTCPPose()
x, y, z, rx, ry, rz = tcp_pose

print("--- TCP Pose ---")
print(f"Position (mm): X={x*1000:.2f}, Y={y*1000:.2f}, Z={z*1000:.2f}")
print(f"Orientation (rad): Rx={rx:.4f}, Ry={ry:.4f}, Rz={rz:.4f}")

# -----------------------------------------------------------
# joint angles in rad (Base, Shoulder, Elbow, Wrist 1, Wrist 2, Wrist 3)
# -----------------------------------------------------------
actual_q = rtde_r.getActualQ()
actual_q_deg = [math.degrees(q) for q in actual_q]

print("\n--- Joint Positions ---")
print("Radians:", [round(q, 4) for q in actual_q])
# convert to deg
print("Degrees:", [round(deg, 2) for deg in actual_q_deg])

# Disconnect    
rtde_r.disconnect()