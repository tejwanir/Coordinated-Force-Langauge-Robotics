from common.item_selecting import get_selected_items, set_selected_items
import numpy as np
import rtde_receive
import rtde_control

class RobotInterface:
    class Axes:
        TRANSLATION_ROTATION = (0, 1, 2, 3, 4, 5)
        X, Y, Z, THETA_X, THETA_Y, THETA_Z = TRANSLATION_ROTATION
        TRANSLATION = (X, Y, Z)
        ROTATION = (THETA_X, THETA_Y, THETA_Z)
        TRANSLATION_ROTATION_SEPARATED = (TRANSLATION, ROTATION)
            
        @staticmethod
        def get(axes, axes_selection=None):
            if axes_selection is None:
                axes_selection = RobotInterface.Axes.TRANSLATION_ROTATION
            selected_axes = get_selected_items(axes, axes_selection)
            if isinstance(selected_axes, (list, tuple)):
                if all(isinstance(ax, int) for ax in selected_axes):
                    return np.array(selected_axes)
                else:
                    formatted_selected_axes = ()
                    for subselected_axes in selected_axes:
                        if isinstance(subselected_axes, (list, tuple)):
                            formatted_selected_axes += (np.array(subselected_axes),)
                        elif isinstance(subselected_axes, int):
                            formatted_selected_axes += (subselected_axes,)
                    return formatted_selected_axes
            elif isinstance(axes_selection, int):
                return selected_axes
            
        @staticmethod
        def set(axes, values, axes_selection=None):
            if axes_selection is None:
                axes_selection = RobotInterface.Axes.TRANSLATION_ROTATION
            set_selected_items(axes, axes_selection, values)
            
        @staticmethod
        def zeros(axes_selection=None):
            return RobotInterface.Axes.get([0]*len(RobotInterface.Axes.TRANSLATION_ROTATION), axes_selection)

    def __init__(self, ip: str, *, translational_force_deadband=0, rotational_force_deadband=0):
        self.receive = rtde_receive.RTDEReceiveInterface(ip)
        self.control = rtde_control.RTDEControlInterface(ip)
        self.translational_force_deadband = translational_force_deadband
        self.rotational_force_deadband = rotational_force_deadband
        self._pose_input = RobotInterface.Axes.zeros()
        self._velocity_input = RobotInterface.Axes.zeros()

    def get_pose(self, axes_selection=None):
        return RobotInterface.Axes.get(self.receive.getActualTCPPose(), axes_selection)
    
    def set_pose(self, values, axes_selection=None, speed=0.25, acceleration=1.2, asynchronous=False):
        RobotInterface.Axes.set(self._pose_input, values, axes_selection)
        self.control.moveL(self._pose_input, speed, acceleration, asynchronous)

    def get_velocity(self, axes_selection=None):
        return RobotInterface.Axes.get(self.receive.getActualTCPSpeed(), axes_selection)
    
    def set_velocity(self, values, axes_selection=None, acceleration=0.25, time=0.0):
        RobotInterface.Axes.set(self._velocity_input, values, axes_selection)
        self.control.speedL(self._velocity_input, acceleration, time)

    def get_force(self, axes_selection=None):
        force = RobotInterface.Axes.get(self.receive.getActualTCPForce())

        for deadband, axes_to_deadband in zip((self.translational_force_deadband, self.rotational_force_deadband), RobotInterface.Axes.TRANSLATION_ROTATION_SEPARATED):
            magnitude = np.linalg.norm(self.get_axes(force, axes_to_deadband))

            if deadband is not None and magnitude < deadband:
                new_magnitude = max(0, 2 * magnitude - deadband)
                new_force = new_magnitude * force / magnitude
                self.set_axes(force, new_force, axes_to_deadband)
        
        return RobotInterface.Axes.get(force, axes_selection)
    
    def __enter__(self):
        self.control.zeroFtSensor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_velocity(RobotInterface.Axes.zeros())