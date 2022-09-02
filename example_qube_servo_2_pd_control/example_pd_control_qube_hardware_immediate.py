## example_pd_control_qube_hardware_immediate.py
# This example sets up a PD controller to control the position of the QUBE Servo 2 Disk. This example uses 
# a physical QUBE Servo 2 device, in an immediate IO mode where you have to handle timing yourself explicity.
# Use a time-based sleep to help with timing, but note that this mode is not recommended. 
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Pathing imports
import sys
pathToCommon = '../common/'
sys.path.append(pathToCommon)
from library_pathing import append_path 
append_path(pathToCommon)

# Other imports
from library_qube import QubeServo2
from library_math import SignalGenerator
import time
import numpy as np
from matplotlib import pyplot as plt

#region: Setup
startTime = time.time()
def elapsed_time():
    return time.time() - startTime
startTime = time.time()
sampleTime = 0.02 # 50 Hz
simulationTime = 10
data_des_position, data_meas_position, data_meas_speed, data_cmd_voltage, data_time = ([0] for i in range(5))
timestamp = 0
color = np.array([0, 1, 0], dtype=np.float64)

squareWave = SignalGenerator.square(np.pi/4, 5)
next(squareWave)
#endregion

# Initialize QUBE Servo 2 
myQube = QubeServo2(id='0', hardware=1, readMode=0) # Immediate Mode with Hardware
# myQube.frequency

k_p, k_d = (4.000, 0.175)

try:
    while timestamp < simulationTime:
        start = elapsed_time()
        # Read sensor information
        myQube.read_position_speed_and_current()
        
        # Command square wave
        desiredPosition = squareWave.send(timestamp)

        # Controller
        voltage = k_p * (desiredPosition - myQube.motorPosition) - k_d * ( myQube.motorSpeed )

        # Write commands
        myQube.write_led(color)
        myQube.write_voltage(voltage)

        #region: Logging Data
        data_des_position.append(desiredPosition)
        data_meas_position.append(myQube.motorPosition)
        data_meas_speed.append(myQube.motorSpeed)
        data_cmd_voltage.append(voltage)
        data_time.append(timestamp)
        #endregion

        end = elapsed_time()

        computationTime = (end - start) % sampleTime
    
        time.sleep(sampleTime - computationTime)
        timestamp = elapsed_time()

except:
    pass
finally:

    # Terminate QUBE Servo 2 gracefully
    myQube.terminate()

    #region: Plotting
    fig1, ax1 = plt.subplots()
    plt.grid(visible=True)
    ax1.plot(data_time, data_meas_position, 'r--', label='Measured Position')
    ax1.plot(data_time, data_des_position, 'k', label='Desired Position')
    ax1.legend(loc='lower right', shadow=True)

    fig2, ax2 = plt.subplots()
    plt.grid(visible=True)
    ax2.plot(data_time, data_cmd_voltage, 'k', label='Commanded voltage')
    ax2.legend(loc='lower right', shadow=True)

    plt.show()
    #endregion
 