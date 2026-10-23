import time
from rtde_io import RTDEIOInterface
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = "192.168.0.10"

rtde_io = RTDEIOInterface(ROBOT_IP)
rtde_r = RTDEReceiveInterface(ROBOT_IP)

try:
    # DO[1] on
    print("Turning ON DO[1]")
    rtde_io.setStandardDigitalOut(1, True)
    time.sleep(0.1)
    print(f"DO[1] State: {rtde_r.getDigitalOutState(1)}")

    # 2. Wait 5 seconds
    time.sleep(5.0)

    # DO[1] on
    print("Turning OFF DO[1]")
    rtde_io.setStandardDigitalOut(1, False)
    time.sleep(0.1)
    print(f"DO[1] State: {rtde_r.getDigitalOutState(1)}")

finally:
    rtde_io.disconnect()
    rtde_r.disconnect()
    print("disconnected")