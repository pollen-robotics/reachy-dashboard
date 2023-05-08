import asyncio
from typing import Dict
from numpy import rad2deg

import grpc
from grpc._channel import _InactiveRpcError

from google.protobuf.empty_pb2 import Empty
from google.protobuf.wrappers_pb2 import BoolValue, FloatValue

from reachy_sdk_api import fan_pb2_grpc
from reachy_sdk_api import joint_pb2_grpc
from reachy_sdk_api.joint_pb2 import JointsCommand, JointCommand, JointId, JointsStateRequest, JointField
from reachy_sdk.fan import Fan


part_to_joints = {
    'Left arm': [
        'l_shoulder_pitch', 'l_shoulder_roll', 'l_arm_yaw',
        'l_elbow_pitch', 'l_forearm_yaw', 'l_wrist_pitch',
        'l_wrist_roll', 'l_gripper',
    ],
    'Right arm': [
        'r_shoulder_pitch', 'r_shoulder_roll', 'r_arm_yaw',
        'r_elbow_pitch', 'r_forearm_yaw', 'r_wrist_pitch',
        'r_wrist_roll', 'r_gripper',
    ],
    'Head': [
        'l_antenna', 'r_antenna', 'neck_roll',
        'neck_pitch', 'neck_yaw',
    ],
}


class ReachyDashboard:
    def __init__(self, host: str = 'localhost', sdk_port: int = 50055) -> None:
        self._host = host
        self._sdk_port = sdk_port
        self._fans: Dict[str, Fan] = {}
        self._joint_names = []
        self.connection_succeed = True
        self._parts = []

        self.joints = {}

        try:
            self._grpc_channel = grpc.insecure_channel(f'{self._host}:{self._sdk_port}')
        except _InactiveRpcError:
            self.connection_succeed = False
            return

        self._setup_fans()
        self._setup_joints()

    def _setup_fans(self):
        fans_stub = fan_pb2_grpc.FanControllerServiceStub(self._grpc_channel)
        resp = fans_stub.GetAllFansId(Empty())
        for name, uid in zip(resp.names, resp.uids):
            fan = Fan(name, uid, stub=fans_stub)
            if name == 'neck_fan':
                continue
            self._fans[name] = fan

    def _setup_joints(self):
        self.joint_stub = joint_pb2_grpc.JointServiceStub(self._grpc_channel)

        joint_ids = self.joint_stub.GetAllJointsId(Empty())
        self.joint_names = joint_ids.names

        if 'l_shoulder_pitch' in self.joint_names:
            self._parts.append('Left arm')

        if 'r_shoulder_pitch' in self.joint_names:
            self._parts.append('Right arm')

        if 'l_antenna' in self.joint_names:
            self._parts.append('Head')

        for part in self._parts:
            self.joints[part] = part_to_joints[part]

        self._set_part_compliance_config()

    def change_compliancy(self, part: str, compliance: bool):
        all_req_joints = [self.joints[p] for p in self._compliance_config[part]]
        flat_joint_list = [joint for p in all_req_joints for joint in p]
        cmd_msg = JointsCommand(
            commands=[self._build_compliance_cmd_msg(joint, compliance) for joint in flat_joint_list]
        )
        self.joint_stub.SendJointsCommands(cmd_msg)

    def _build_compliance_cmd_msg(self, joint_name, compliance):
        msg = JointCommand(
            id=JointId(name=joint_name),
            compliant=BoolValue(value=compliance),
        )
        return msg

    def _build_torque_limit_cmd_msg(self, joint_name, torque_limit):
        msg = JointCommand(
            id=JointId(name=joint_name),
            torque_limit=FloatValue(value=torque_limit),
        )
        return msg

    async def turn_off_smoothly(self, part: str):
        all_req_joints = [self.joints[p] for p in self._compliance_config[part]]
        flat_joint_list = [joint for p in all_req_joints for joint in p]

        cmd_msg = JointsCommand(
            commands=[self._build_torque_limit_cmd_msg(joint, 0) for joint in flat_joint_list]
        )
        self.joint_stub.SendJointsCommands(cmd_msg)

        await asyncio.sleep(2.0)

        cmd_msg = JointsCommand(
            commands=[self._build_compliance_cmd_msg(joint, True) for joint in flat_joint_list]
        )
        self.joint_stub.SendJointsCommands(cmd_msg)

        cmd_msg = JointsCommand(
            commands=[self._build_torque_limit_cmd_msg(joint, 100) for joint in flat_joint_list]
        )
        self.joint_stub.SendJointsCommands(cmd_msg)

    def _set_part_compliance_config(self):
        self._compliance_config = {}

        for part in self._parts:
            self._compliance_config[part] = [part]

        if len(self._parts) > 1:
            self._compliance_config['Robot'] = self._parts

        if 'Left arm' and 'Right arm' in self._parts:
            self._compliance_config['Both arms'] = ['Left arm', 'Right arm']

    def get_fans_info(self):
        fans_info = {}
        for f in self._fans.values():
            if f.is_on:
                fans_info[f.name] = 'on'
            else:
                fans_info[f.name] = 'off'
        return fans_info

    def set_fan_state(self, fan, state):
        if state == 'on':
            self._fans[fan].on()
        else:
            self._fans[fan].off()

    def get_temperatures(self):
        temperatures = {}

        for part in self.joints:
            temp_part = {}
            ids = [JointId(name=joint) for joint in self.joints[part]]
            request = JointsStateRequest(ids=ids, requested_fields=[JointField.TEMPERATURE])
            res = self.joint_stub.GetJointsState(request)

            for (joint_id, state) in zip(res.ids, res.states):
                temp_part[joint_id.name] = int(state.temperature.value)

            temperatures[part] = temp_part

        return temperatures

    def get_states(self):
        states = {}

        for part in self.joints:
            state_part = {}
            ids = [JointId(name=joint) for joint in self.joints[part]]
            request = JointsStateRequest(
                ids=ids,
                requested_fields=[JointField.TEMPERATURE, JointField.PRESENT_POSITION])
            res = self.joint_stub.GetJointsState(request)

            for (joint_id, state) in zip(res.ids, res.states):
                state_joint = {}

                try:
                    state_joint['temperature'] = int(state.temperature.value)
                except ValueError:
                    state_joint['temperature'] = 0

                state_joint['position'] = int(rad2deg(state.present_position.value))
                state_part[joint_id.name] = state_joint

            states[part] = state_part

        return states

    def __exit__(self):
        self._grpc_channel.close()
