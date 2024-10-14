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
    def _get_axes(translation_rotation: List[float], axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        if axes is None:
            axes = Robot.TRANSLATION_ROTATION

        if isinstance(axes, int):
            axes = [axes]

        if all(isinstance(subset, (tuple, list)) for subset in axes):
            return tuple(Robot._extract_axes(translation_rotation, subset) for subset in axes)
        return Robot._extract_axes(translation_rotation, axes)

    @staticmethod
    def _set_axes(translation_rotation: List[float], input: Union[float, List[float]], axes: Optional[Union[int, List[int]]] = None, reset_unspecified: bool = False):
        if axes is None:
            axes = Robot.TRANSLATION_ROTATION

        if isinstance(axes, int):
            axes = [axes]
            input = [input]
            
        for i, ax in enumerate(axes):
            translation_rotation[ax] = input[i]

        if reset_unspecified:
            for i in range(len(translation_rotation)):
                if i not in axes:
                    translation_rotation[i] = 0.0

    @staticmethod
    def _zeroed_translation_rotation():
        return np.zeros(6)

    def __init__(self, ip: str):
        self.receive = rtde_receive.RTDEReceiveInterface(ip)
        self.control = rtde_control.RTDEControlInterface(ip)
        self._pose = Robot._zeroed_translation_rotation()
        self._velocity = Robot._zeroed_translation_rotation()

    def getPose(self, axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        return self._get_axes(self.receive.getActualTCPPose(), axes)
    
    def setPose(self, input: Union[float, List[float]], axes: Optional[Union[int, List[int]]] = None, reset_unspecified: bool = False, speed: float = 0.25, acceleration: float = 1.2, asynchronous: bool = False):
        self._set_axes(self._pose, input, axes, reset_unspecified)
        self.control.moveL(self._pose, speed, acceleration, asynchronous)

    def getVelocity(self, axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        return self._get_axes(self.receive.getActualTCPSpeed(), axes)
    
    def setVelocity(self, input: Union[float, List[float]], axes: Optional[Union[int, List[int]]] = None, reset_unspecified: bool = False, acceleration: float = 0.25, time: float = 0.0):
        self._set_axes(self._velocity, input, axes, reset_unspecified)
        self.control.speedL(self._velocity, acceleration, time)

    def getForce(self, axes: Optional[Union[int, List[int], List[List[int]]]] = None):
        return self._get_axes(self.receive.getActualTCPForce(), axes)