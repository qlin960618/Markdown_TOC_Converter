# qlin_robot_switch_manager ROS package

[TOC]

## Modules

### 1. RobotMutex

#### methods

- \_\_init\_\_(lock_name, verbose=False):

  `lock_name`is the lock identifier for cross process system-wide file lock. This need to be the same for all lock for the program to function as desire.

  `verbose`default to *False*, possible value give from *True* to *2*. Larger the value, more information will be printed for debugging

- is_lock():

  For testing if the lock has been acquired by either self or another process

- has_lock():

  return *True* only when *self* has the lock

- lock(timeout=0):

  Try to acquire the lock and return *False* if acquisition failed.

  `timeout` gives how long should the locker try before timeout. Default is **0** which return after single attempt. if given **None** the program will block until lock is avaliable

- release():

  Release the lock

#### Future work

currently the implementation is base on the python build in fileio and os package. However, the performance may not be desirable. Possible replacement for the standard filesystem lock is `portalocker` (also filesystem lock but probably more efficient). Also could consider directly placing the lockfile in tmp file without trying to put it in a directory.

Also to make sure there is no unexpected race condition. the module will need **MORE TESTING**

### 2. KinematicsSwitchProvider

- is_enabled():

  Return True when the interface received first message

- get_trajectory_status():

  Get the current auto trajectory sequence status. The function return tuple of size 2, `(percentage, done)`The information should only be published by the auto kinematics node

- toggle_auto_control():

  Toggle the control mode into auto control mode

- toggle_manual_control():

  Toggle the control mode into manual control mode

- is_auto_control_enabled():

  as stated

- is_manual_control_enabled():

  as stated

### 3. KinematicsSwitchInterface

- is_enabled():

  Return True when the interface received first message

- is_auto_control_enabled():

  return True if signal from patient_side_manager to be in auto control mode

- is_manual_control_enabled():

  return True if signal from patient_side_manager to be in manual control mode

- is_auto_control_first_enabled():

  return True when this function is first called in the auto control mode

- is_manual_control_first_enabled():

  return True when this function is first called in the manual control mode

- send_trajectory_status(percentage, done):

  As stated, this should only be used in the auto sequence kinematics node.

## Test Scripts

1. switch_manager_interface_tester.py
2. switch_manager_provider_tester.py
3. test_lock.py

## Concept

The concept of the two kinematics node switching is shown in the figure below. Where the individual kinematics node structure stays mostly identical to the original version. The figure is only showing the added components and with the original parts simplified. `switch_mutex` exist here as mainly a safety feature to ensure there is no race condition in sending two different joint value to the robot. Therefore, in this either node will have priority over another. However, as program will start with manual control, manual node will in general have operation priority over the other.

![switch manager components diagram](../media/switch_manager_concept.png)

For the manual control kinematics, the program flow is mostly the same. The added switch will only disengage the robot when signal is given by the patient_side_manager. As for the auto kinematics node, there are more involve. The figure below shows the general program flow. Bold line represent the main flow path when node is in enabled state.

![auto kinematic node simplified flow](../media/auto_node_example_flow.png)
