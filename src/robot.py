from typing import List, Optional, Union
import rtde_receive
import rtde_control
import numpy as np

class Robot:
    TRANSLATION_ROTATION = (0, 1, 2, 3, 4, 5)
    X, Y, Z, THETA_X, THETA_Y, THETA_Z = TRANSLATION_ROTATION
    TRANSLATION = (X, Y, Z)
    ROTATION = (THETA_X, THETA_Y, THETA_Z)
    TRANSLATION_ROTATION_SEPARATED = (TRANSLATION, ROTATION)

    @staticmethod
    def _extract_axes(translation_rotation: List[float], axes: Union[int, List[int]]):
        if isinstance(axes, int):
            return translation_rotation[axes]
        return np.asarray([translation_rotation[ax] for ax in axes])

    @staticmethod
    def get_axes(translation_rotation: List[float], axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        if axes is None:
            axes = Robot.TRANSLATION_ROTATION

        if isinstance(axes, int):
            return translation_rotation[axes]
        elif isinstance(axes, (tuple, list)):
            if all(isinstance(subset, (tuple, list)) for subset in axes):
                return tuple(Robot._extract_axes(translation_rotation, subset) for subset in axes)
        return Robot._extract_axes(translation_rotation, axes)
    
    @staticmethod
    def _update_axes(translation_rotation: List[float], input: List[float], axes: List[int]):
        for i, ax in enumerate(axes):
            translation_rotation[ax] = input[i]

    @staticmethod
    def set_axes(translation_rotation: List[float], input: Union[float, List[float]], axes: Optional[Union[int, List[int]]] = None, reset_unspecified: bool = False):
        if axes is None:
            axes = Robot.TRANSLATION_ROTATION

        if isinstance(axes, int):
            axes = [axes]
            input = [input]

        if isinstance(axes, (tuple, list)):
            if all(isinstance(subset, (tuple, list)) for subset in axes):
                for subset_input, subset_axes in zip(input, axes):
                    Robot._update_axes(translation_rotation, subset_input, subset_axes)
                axes = set(ax for subset_axes in axes for ax in subset_axes)
            else:
                Robot._update_axes(translation_rotation, input, axes)

        if reset_unspecified:
            for i in Robot.TRANSLATION_ROTATION:
                if i not in axes:
                    translation_rotation[i] = 0.0

    @staticmethod
    def zeroed_translation_rotation():
        return np.zeros(6)

    def __init__(self, ip: str):
        self.receive = rtde_receive.RTDEReceiveInterface(ip)
        self.control = rtde_control.RTDEControlInterface(ip)
        self._pose_input = Robot.zeroed_translation_rotation()
        self._velocity_input = Robot.zeroed_translation_rotation()

    def getPose(self, axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        return self.get_axes(self.receive.getActualTCPPose(), axes)
    
    def setPose(self, input: Union[float, List[float]], axes: Optional[Union[int, List[int]]] = None, reset_unspecified: bool = False, speed: float = 0.25, acceleration: float = 1.2, asynchronous: bool = False):
        self.set_axes(self._pose_input, input, axes, reset_unspecified)
        self.control.moveL(self._pose_input, speed, acceleration, asynchronous)

    def getVelocity(self, axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        return self.get_axes(self.receive.getActualTCPSpeed(), axes)
    
    def setVelocity(self, input: Union[float, List[float]], axes: Optional[Union[int, List[int]]] = None, reset_unspecified: bool = False, acceleration: float = 0.25, time: float = 0.0):
        self.set_axes(self._velocity_input, input, axes, reset_unspecified)
        self.control.speedL(self._velocity_input, acceleration, time)

    def getForce(self, axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        return self.get_axes(self.receive.getActualTCPForce(), axes)