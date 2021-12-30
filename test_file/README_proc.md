# qlin_control ROS package

Launch definition and kinematics scripts for pathology tele-operation


[comment]: # (TOC generator marker start)
- [qlin_control ROS package](#qlin_control-ros-package)
  * [1. Directory Structure](#1-directory-structure)
     * [a. launch](#a-launch)
        * [<a href="launch/qlin_teleoperation.launch">qlin_teleoperation.launch</a>](#qlin_teleoperationlaunch)
        * [<a href="launch/qlin_teleoperation_joystick.launch">qlin_teleoperation_joystick.launch</a>](#qlin_teleoperation_joysticklaunch)
        * [<a href="launch/qlin_replay.launch">qlin_replay.launch</a>](#qlin_replaylaunch)
        * [<a href="launch/qlin_ui_replay.launch">qlin_ui_replay.launch</a> (In progress)](#qlin_ui_replaylaunch-in-progress)
     * [b. robots](#b-robots)
        * [json parameters](#json-parameters)
           * [<del><a href="robots/denso_vs050_pathology_arm.json">denso_vs050_pathology_arm.json</a></del> (Incorrect version)](#denso_vs050_pathology_armjson-incorrect-version)
           * [<a href="robots/denso_vs050_denso_11U473.json">denso_vs050_denso_11U473.json</a>, <a href="robots/denso_vs050_denso_11U483.json">denso_vs050_denso_11U483.json</a>](#denso_vs050_denso_11u473json-denso_vs050_denso_11u483json)
           * [<a href="robots/denso_vs050_official_arm.json">denso_vs050_official_arm.json</a>](#denso_vs050_official_armjson)
        * [Import Wrapper](#import-wrapper)
           * [<del><a href="robots/VS050RobotDH_pathology.py">VS050RobotDH_pathology.py</a></del> (No longer applicable)](#vs050robotdh_pathologypy-no-longer-applicable)
           * [<a href="robots/VS050Robot_pathology.py">VS050Robot_pathology.py</a>](#vs050robot_pathologypy)
     * [c. scripts](#c-scripts)
     * [d. src](#d-src)
  * [2. Components Explain](#2-components-explain)
     * [a. qlin_kinematic_node.py](#a-qlin_kinematic_nodepy)
     * [b. sss_operator_side_receiver_udp_node](#b-sss_operator_side_receiver_udp_node)
     * [c. qlin_patient_side_manager_node.py [or] sss_patient_side_manager_node](#c-qlin_patient_side_manager_nodepy-or-sss_patient_side_manager_node)
     * [d. moonshot_drill_robot_node](#d-moonshot_drill_robot_node)

[comment]: # (TOC generator marker end)


## 1. Directory Structure

### a. launch

In the following figure dependency and data flow direction are labeled as follow:

![Figure Label](media/label_convention.png)



#### [qlin_teleoperation.launch](launch/qlin_teleoperation.launch)


This launch file is the main launch mode for the teleoperation mode of the pathology robot. Using the UDP connection with Master Interface exist locally or on remote computer for operation. A more detail description of the each components will be discussed below in the later section.  

![Normal Components](media/qlin_teleoperation_diagram.png)

#### [qlin_teleoperation_joystick.launch](launch/qlin_teleoperation_joystick.launch)

This launch mode is nearly identical to the previous. with the exception that the UDP master interface connection is replaced with the "joystick_interface_node" that is ran locally, The script exist in the *qlin_nonstandard_control* ROS package. This take advantage of the much more easily accessible XBox Controller for control

![Joystick Interface](media/qlin_joystick_diagram.png)

#### [qlin_replay.launch](launch/qlin_replay.launch)

This launch mode takes an existing .mat record and run through the replay. It is still done through a similar kinematic node to ensure all constrain is still enforced. data is substituted at the kinematic node level, require master to be connected to start, but clutch or other master control is not required.

#### [qlin_ui_replay.launch](launch/qlin_ui_replay.launch) (In progress)

This launch mode takes an existing trajectory.mat record and run through the replay. It is still done through a similar kinematic node to ensure all constrain is still enforced.

(working of which is very much like the base kinematic node. not yet implemented, but the following iteration robot kinematic interface will be replaced with module read data from the logged data of other teleoperation.)



### b. robots

#### json parameters

##### ~~[denso_vs050_pathology_arm.json](robots/denso_vs050_pathology_arm.json)~~ (Incorrect version)

Robot definition for the VS050 robot model. This is the older version inherited from Mori-san (pathology project). However, there was discrepancy between this and the real parameters. Therefore, this version should not be used.

##### [denso_vs050_denso_11U473.json](robots/denso_vs050_denso_11U473.json), [denso_vs050_denso_11U483.json](robots/denso_vs050_denso_11U483.json)

Robot definition for the two Pathology arm. The parameter is in the format of high accuracy Denso parameters. For actual operation, this parameter should be used.

- 11U483: Left Arm
- 11U473: Right Arm

##### [denso_vs050_official_arm.json](robots/denso_vs050_official_arm.json)

Robot definition for the Denso VS050 arm in DH format. As there is no calibration for the real robot arm. This parameter is only applicable for simulation or which precision is not require.



#### Import Wrapper

##### ~~[VS050RobotDH_pathology.py](robots/VS050RobotDH_pathology.py)~~ (No longer applicable)

implementation of the basic json reader into dqrobotics kinematics. This file also include some function specifically to set the pathology robot end effector. the definition of which are given in the following functions

- robot  get_end_effector_dq_knife_config1(robot)
- robot  get_end_effector_dq_twizer_config1(robot)

##### [VS050Robot_pathology.py](robots/VS050Robot_pathology.py)

Import wrapper using the dqrobotics json importer. Optionally, the class allow both Denso or DH parameter given by the "type" field in the json. This file also include some function specifically to set the pathology robot end effector. The definition of which are given in the following functions

- robot  get_end_effector_dq_knife_config1(robot)
- robot  get_end_effector_dq_twizer_config1(robot)

### c. scripts



### d. src



## 2. Components Explain

### a. qlin_kinematic_node.py

Kinematics calculation for the tele-operation. The node takes advantage of the RobotKinematicsProvider and RobotDriverInterface modules to interface with other components. it also have the optional Vrep connection that can be toggle in the parameter file for visualizing desire components in vrep.

![](media/qlin_kinematics_diagram.png)

### b. sss_operator_side_receiver_udp_node

The node share basically identical functionality in ROS perspective compare to the qlin_joystick_interface.py. With its diagram below

 ![](media/operator_side_receiver_diagram.png)



### c. qlin_patient_side_manager_node.py [or] sss_patient_side_manager_node

Currently, the two file has very similar implementation. Except for the sss_patient_side_manager_node is using cpp while the other is written in python.

![](media/patient_side_manager_diagram.png)

### d. moonshot_drill_robot_node
### d. moonshot_drill_robot_node
### d. moonshot_drill_robot_noeas
### d. moonshot_drill_robot_noeas
### d. moonshot_drill_robot_node
### d. moonshot_drill_robot_noe
### d. moonshot_drill_robot_noe

![](media/robot_driver_diagram.png)
