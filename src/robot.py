from typing import List
import rtde_receive
import rtde_control
import numpy as np

class Robot:
    def __init__(self, ip: str):
        self.receive = rtde_receive.RTDEReceiveInterface(ip)
        self.control = rtde_control.RTDEControlInterface(ip)

    def getPose(self):
        return split_translation_rotation(self.receive.getActualTCPPose())
    
    def setPose(self, translation_pose: List[float], rotation_pose: List[float], speed: float = 0.25, acceleration: float = 1.2, asynchronous: bool = False):
        self.control.moveL(concat_translation_rotation(translation_pose, rotation_pose), speed, acceleration, asynchronous)

    def getVelocity(self):
        return split_translation_rotation(self.receive.getActualTCPSpeed())
    
    def setVelocity(self, translation_velocity: List[float], rotation_velocity: List[float], acceleration: float = 0.25, time: float = 0.0):
        self.control.speedL(concat_translation_rotation(translation_velocity, rotation_velocity), acceleration, time)

    def getForce(self):
        return split_translation_rotation(self.receive.getActualTCPForce())
    
def split_translation_rotation(translation_rotation: List[float]):
    return np.asarray(translation_rotation[:3]), np.asarray(translation_rotation[3:])

def concat_translation_rotation(translation: List[float], rotation: List[float]):
    return np.concat((translation, rotation))