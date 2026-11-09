"""Generated explicit firmware API; regenerate with tools/generate_api.py."""

from __future__ import annotations

from collections.abc import Sequence
from .protocol import Response, Scalar
from .client_base import AsyncClientBase


class AsyncPF400(AsyncClientBase):
    """82 non-vision TCS commands. See docs/API.md for wire semantics."""

    async def version(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""Version — Cmd.gpl:301.

        Cmd_Version - Return the software version number

          No parameters"""
        return await self._call("version", channel=channel, timeout=timeout)

    async def nop(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""Nop — Cmd.gpl:354.

        Cmd_Nop -- KDo nothing except return success.

         ABSTRACT:  Does nothing except return success.  Tests if the command
              server is active and there are no pending errors.

         No parameters"""
        return await self._call("nop", channel=channel, timeout=timeout)

    async def sys_state(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""SysState — Cmd.gpl:367.

        Cmd_SysState -- Return the  status of controller (e-stop, power, execution)

         ABSTRACT:  Returns the value of DataID 234.  See the GPL documentation
                    for details on these values.

         No parameters"""
        return await self._call("sys_state", channel=channel, timeout=timeout)

    async def home(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""Home — Cmd.gpl:582.

        Cmd_Home -- Homes the current robot.

         ABSTRACT:  Homes the current robot only.  Do not home any other robots.

         No parameters"""
        return await self._call("home", channel=channel, timeout=timeout)

    async def home_all(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""HomeAll — Cmd.gpl:594.

        Cmd_HomeAll -- Homes all robots.

         ABSTRACT:  Homes all robots.

         No parameters"""
        return await self._call("home_all", channel=channel, timeout=timeout)

    async def where(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""Where — Cmd.gpl:1415.

        Cmd_Where -- Gets the robot Cartesian and Angles location

         ABSTRACT:  Gets the robot Cartesian and Angles location

         No parameters"""
        return await self._call("where", channel=channel, timeout=timeout)

    async def where_c(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""WhereC — Cmd.gpl:1449.

        Cmd_WhereC -- Gets the robot Cartesian location

         ABSTRACT:  Gets the robot Cartesian location and config

         No parameters"""
        return await self._call("where_c", channel=channel, timeout=timeout)

    async def where_j(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""WhereJ — Cmd.gpl:1472.

        Cmd_WhereJ -- Gets the robot Angles location

         ABSTRACT:  Gets the robot Angles location

         No parameters"""
        return await self._call("where_j", channel=channel, timeout=timeout)

    async def wait_for_eom(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""WaitForEom — Cmd.gpl:1853.

        Cmd_WaitForEom -- Waits for the robot to reach the end of motion

         ABSTRACT:  Waits until the robot reaches the end of the current
              motion or until the robot is stopped by some other means.

         No parameters"""
        return await self._call("wait_for_eom", channel=channel, timeout=timeout)

    async def state(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""State — Cmd.gpl:1996.

        Cmd_State -- Gets the robot motion state.

         ABSTRACT:  Gets the robot motion state.

         No parameters"""
        return await self._call("state", channel=channel, timeout=timeout)

    async def halt(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""Halt — Cmd.gpl:2020.

        Cmd_Halt -- Stops the robot motion immediately

         ABSTRACT:  Stops the robot motion immediately but leaves power on

         No parameters"""
        return await self._call("halt", channel=channel, timeout=timeout)

    async def move_to_safe(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""MoveToSafe — PARobot.gpl:524.

        Cmd_MoveToSafe -- Move robot to a safe postion

        ABSTRACT: Command to Move a Robot to Safe Position
                  Function applicable only to
                  PF400/PF300/C3
                  PFDD4,PFC10/PFDD6,PFC8A
                  C5
                  Robots With a PreciseFlex
                  Servo or Pneumatic Gripper

                  This routine doesn't includes check for collision inside
                  Work volume of the robot and can be customized by user for their
                  workcell configuration

        No parameters"""
        return await self._call("move_to_safe", channel=channel, timeout=timeout)

    async def home_all_if_no_plate(
        self, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""HomeAll_IfNoPlate — PARobot.gpl:3575.

        Cmd_HomeAll_IfNoPlate -- Enable power and home if no plate

        ABSTRACT: Command to test if the gripper is holding a plate.
              If not, enable power and home all robots.

        No parameters

              Returns value -1 if no plate and command succeeded
              Returns value 0 if a plate detected"""
        return await self._call("home_all_if_no_plate", channel=channel, timeout=timeout)

    async def is_fully_closed(self, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""IsFullyClosed — PARobot.gpl:3750.

        Cmd_IsFullyClosed -- Command to test if gripper is fully closed

        ABSTRACT:  Command to test if the gripper is fully closed to its
          lower hardstop by checking the end-of-travel sensor.  The end-of-travel
          sensor signal is high if the spring gripper is within 2 mm of being
          fully closed.

        No parameters

        RETURNS:
          If Standard Gripper:
                  True (-1) If the gripper Is closed To within 2 mm of its fully
                      closed position
                  False (0) or error code and message.
          If Dual Gripper
                  0, 1, 2, 3 = a bit mask where a bit set represents the
                      corresponding gripper being closed.
                      gripper 1 is bit 0
                      gripper 2 is bit 1"""
        return await self._call("is_fully_closed", channel=channel, timeout=timeout)

    async def get_active_gripper(
        self, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""GetActiveGripper — PARobot.gpl:3893."""
        return await self._call("get_active_gripper", channel=channel, timeout=timeout)

    async def exit(self, *, channel: str | None = None, timeout: float | None = None) -> None:
        r"""Exit — Cmd.gpl:2275.

        Cmd_Exit -- Exit from this Telnet session

         ABSTRACT:  Issue a special reply that causes the caller to close the
              Telnet session.  Has no effect on serial connections.

         No parameters"""
        return await self._call("exit", channel=channel, timeout=timeout)

    async def mode(
        self, value: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Mode — Cmd.gpl:326.

        Cmd_Mode - Get or Set the operation mode

        Parameter 1: Optional. If omitted, returns the current mode.
                               If specified, sets the mode:
                                  0 for normal mode,
                                  <> 0 for Telnet mode."""
        return await self._call("mode", value, channel=channel, timeout=timeout)

    async def attach(
        self, value: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Attach — Cmd.gpl:548.

        Cmd_Attach -- Attaches or releases the robot for control

         ABSTRACT:  Attaches or releases the robot for control by the client.

              Or inquires about the current state of attachment.

         Parameter 1: Optional.
                      If omitted, this command returns the current attachment state.
                      If specified, 0 to release the robot, <> 0 to attach it."""
        return await self._call("attach", value, channel=channel, timeout=timeout)

    async def select_robot(
        self, robot_id: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""SelectRobot — Cmd.gpl:732.

        Cmd_SelectRobot -- Sets or Gets the selected robot number.

         ABSTRACT:  Set or gets the number of the robot currently associated
              with this thread.

              The status thread select any robot or 0.

              A robot thread may only select a robot that is not already selected
              by a different robot thread.

         Parameter 1: Optional.
                      If omitted, this command returns the current robot number.
                      If specified, contains the robot number."""
        return await self._call("select_robot", robot_id, channel=channel, timeout=timeout)

    async def mspeed(
        self, value: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Mspeed — Cmd.gpl:701.

        Cmd_Mspeed -- Sets or Gets the master robot speed factor

         ABSTRACT:  Set or gets the master system (monitor) speed factor.
              This speed scales the speed of all robot motions.

         Parameter 1: Optional.
                      If omitted, this command returns the current system speed.
                      If specified, contains the new system speed as a percentage."""
        return await self._call("mspeed", value, channel=channel, timeout=timeout)

    async def payload(
        self, value: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Payload — Cmd.gpl:1969.

        Cmd_Payload -- Sets or displays the payload for the current robot

         ABSTRACT:  Sets or displays the payload for the current robot

              Does not go into effect until the next robot motion

         Parameter 1: Optional.
                      If omitted, this command returns the current payload value.
                      If specified, the payload percent value to be set."""
        return await self._call("payload", value, channel=channel, timeout=timeout)

    async def dest_c(
        self,
        destination_only: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""DestC — Cmd.gpl:612.

        Cmd_DestC -- Gets the robot Cartesian destination

         ABSTRACT:  Gets the robot Cartesian destination + config

         Parameter 1: Optional.
                      If omitted, or zero, and the robot is not moving,
                      returns the Where value.

                      If specified, and value is 1, always returns the
                      Cartesian destination + config"""
        return await self._call("dest_c", destination_only, channel=channel, timeout=timeout)

    async def dest_j(
        self,
        destination_only: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""DestJ — Cmd.gpl:658.

        Cmd_DestJ -- Gets the robot Angles destination

         ABSTRACT:  Gets the robot Angles destination

         Parameter 1: Optional.
                      If omitted, or zero, and the robot is not moving,
                      returns the WhereJ value.

                      If specified, and value is 1, always returns the
                      robot angles destination"""
        return await self._call("dest_j", destination_only, channel=channel, timeout=timeout)

    async def grip_open_pos(
        self, width: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""GripOpenPos — PARobot.gpl:2121.

        Cmd_GripOpenPos -- Set and get the gripper open position

        ABSTRACT: Command to Set & Get Gripper Open Position
              Used only for Servo Gripper. For Pneumatics Gripper - Adjust Hardware

        Parameter 1:  Optional.  If omitted, return the gripper open position.
                      If specified, the new value for the gripper open position"""
        return await self._call("grip_open_pos", width, channel=channel, timeout=timeout)

    async def grip_close_pos(
        self, width: float | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""GripClosePos — PARobot.gpl:2160.

        Cmd_GripClosePos -- Set and get the gripper close position

        ABSTRACT: Command to Set & Get Gripper Close Position
              Used only for Servo Gripper. For Pneumatics Gripper - Adjust Hardware

        Parameter 1:  Optional.  If omitted, return the gripper close position.
                      If specified, the new value for the gripper close position"""
        return await self._call("grip_close_pos", width, channel=channel, timeout=timeout)

    async def hp(
        self,
        value: int | None = None,
        wait: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Hp — Cmd.gpl:511.

        Cmd_Hp -- High Power control

         ABSTRACT:  Enable or disable high power

                    If no parameters, return the state of power.

         Parameter 1: 0 to disable power, 1 to enable power.
         Parameter 2: Optional if enabling power.
                      -1 means wait forever for power to come one.
                      0 or omitted means do not wait at all.
                      > 0 means wait for this many seconds.  An error is returned.
                      If power does not come one within this time."""
        return await self._call("hp", value, wait, channel=channel, timeout=timeout)

    async def pd(
        self,
        parameter_id: int,
        index1: int | None = None,
        index2: int | None = None,
        index3: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Pd — Cmd.gpl:395.

        Cmd_Pd -- Parameter Display

         ABSTRACT:  Return a parameter database value.

         Parameter 1: The paramemter ID code.
         Parameters 2-4:  Optional.  Correspond to the additional parameters
                          of the GPL "pd" console command.  Assumed to be
                          zero if omitted."""
        return await self._call("pd", parameter_id, index1, index2, index3, channel=channel, timeout=timeout)

    async def pc(
        self,
        parameter_id: int,
        value: Scalar,
        *,
        indices: Sequence[int] | None = None,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Pc — Cmd.gpl:437.

        Cmd_Pc -- Parameter Change

         ABSTRACT:  Change a parameter database value.

              Accepts 2 or 5 parameters.

              If 2 parameters are specified:

                      Parameter 1: The paramemter ID code.
                      Parameter 2: The new parameter value
                                   String values must be inside quotes.

              If 5 parameters are specified:

                      Parameter 1: The paramemter ID code.
                      Parameters 2-4:  Correspond to the additional parameters
                                       of the GPL "pc" console command.
                      Parameter 5: The new parameter value
                                   String values must be inside quotes."""
        return await self._call("pc", parameter_id, value, indices=indices, channel=channel, timeout=timeout)

    async def speed(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Speed — Cmd.gpl:779.

        Cmd_Speed -- Sets or Gets the motion profile Speed.

         ABSTRACT:  Set or gets the Speed property for the specified
              motion profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile Speed value.
                      If specified, contains the new profile Speed value."""
        return await self._call("speed", profile_index, value, channel=channel, timeout=timeout)

    async def speed2(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Speed2 — Cmd.gpl:820.

        Cmd_Speed2 -- Sets or Gets the motion profile Speed2.

         ABSTRACT:  Set or gets the Speed2 property for the specified
              motion profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile Speed2 value.
                      If specified, contains the new profile Speed2 value."""
        return await self._call("speed2", profile_index, value, channel=channel, timeout=timeout)

    async def accel(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Accel — Cmd.gpl:860.

        Cmd_Accel -- Sets or Gets the motion profile accel.

         ABSTRACT:  Set or gets the Accel property for the specified motion
              profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile accel.
                      If specified, contains the new profile accel."""
        return await self._call("accel", profile_index, value, channel=channel, timeout=timeout)

    async def decel(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Decel — Cmd.gpl:900.

        Cmd_Decel -- Sets or Gets the motion profile decel.

         ABSTRACT:  Set or gets the Decel property for the specified motion
              profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile decel.
                      If specified, contains the new profile decel."""
        return await self._call("decel", profile_index, value, channel=channel, timeout=timeout)

    async def acc_ramp(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""AccRamp — Cmd.gpl:940.

        Cmd_AccRamp -- Sets or Gets the motion profile AccelRamp.

         ABSTRACT:  Set or gets the AccelRamp property for the specified
              motion profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile AccelRamp.
                      If specified, contains the new profile AccelRamp."""
        return await self._call("acc_ramp", profile_index, value, channel=channel, timeout=timeout)

    async def dec_ramp(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""DecRamp — Cmd.gpl:980.

        Cmd_DecRamp -- Sets or Gets the motion profile DecelRamp.

         ABSTRACT:  Set or gets the DecelRamp property for the specified
              selected motion profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile DecelRamp.
                      If specified, contains the new profile DecelRamp."""
        return await self._call("dec_ramp", profile_index, value, channel=channel, timeout=timeout)

    async def in_range(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""InRange — Cmd.gpl:1020.

        Cmd_InRange -- Sets or Gets the motion profile InRange.

         ABSTRACT:  Set or gets the InRange property for the currently
              selected motion profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile InRange.
                      If specified, contains the new profile InRange."""
        return await self._call("in_range", profile_index, value, channel=channel, timeout=timeout)

    async def straight(
        self,
        profile_index: int,
        value: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Straight — Cmd.gpl:1061.

        Cmd_Straight -- Sets or Gets the motion profile Straight.

         ABSTRACT:  Set or gets the Straight property for the specified
              motion profile.

         Parameter 1: Specifies the profile index to use.

         Parameter 2: Optional.
                      If omitted, this command returns the profile Straight value.
                      If specified, contains the new profile Straight value."""
        return await self._call("straight", profile_index, value, channel=channel, timeout=timeout)

    async def profile(
        self,
        profile_index: int,
        values: Sequence[float] | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Profile — Cmd.gpl:1112.

        Cmd_Profile -- Sets or Gets the entry motion Profile.

         ABSTRACT:  Set or gets the specified Profile

         Parameter 1: Specifies the index of the profile for this robot.
         Parameter 2-9: Optional.
                      If omitted, this command returns specified Profile value.
                      If specified, these parameters contain the new Profile value.
                          2: Speed
                          3: Speed2
                          4: Accel
                          5: Decel
                          6: AccelRamp
                          7: DecelRamp
                          8: InRange
                          9: Straight"""
        return await self._call("profile", profile_index, values, channel=channel, timeout=timeout)

    async def loc(self, index: int, *, channel: str | None = None, timeout: float | None = None) -> Response:
        r"""Loc — Cmd.gpl:1168.

        Cmd_Loc -- Gets the motion location Loc or Angles.

         ABSTRACT:  Gets the Cartesian position or Angles values for the
              specified motion location.

         Parameter 1: Returns the currently selected motion location values."""
        return await self._call("loc", index, channel=channel, timeout=timeout)

    async def loc_angles(
        self,
        index: int,
        joints: Sequence[float] | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""LocAngles — Cmd.gpl:1228.

        Cmd_LocAngles -- Gets or sets the motion location Angles.

         ABSTRACT:  Gets or sets the specified the specified location.

              For Get, an error is returned if the specified location is
              not of type "Angles".

              For Set, the specified location is change to type "Angles".

         Parameter 1: The location index

         Parameter 2-13: Optional.
                      If omitted, this command returns specified location value.
                      If specified, these parameters contain the new location
                          angles.
                      If the number of angles > the number of axes, the extra
                          values are ignored.
                      If the number of angles < the number of axes, the missing
                          values are assumed to be zero."""
        return await self._call("loc_angles", index, joints, channel=channel, timeout=timeout)

    async def loc_xyz(
        self,
        index: int,
        pose: Sequence[float] | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""LocXyz — Cmd.gpl:1286.

        Cmd_LocXyz -- Gets or sets the motion location Cartesian values

         ABSTRACT:  Gets or sets the specified the specified location.

              For Get, an error is returned if the specified location is
              not of type "Cartesian".

              For Set, the specified location is change to type "Cartesian".

              Does not change the currently selected motion index.

         Parameter 1: The location index

         Parameter 2-7: Optional.
                      If omitted, this command returns specified location value.
                      If specified, these parameters contain the new location
                          Cartesian values.  All values must be specified."""
        return await self._call("loc_xyz", index, pose, channel=channel, timeout=timeout)

    async def loc_z_clearance(
        self,
        index: int,
        clearance: float | None = None,
        world: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""LocZClearance — Cmd.gpl:1339.

        Cmd_LocZClearance -- Sets or Gets the motion location ZClearance.

         ABSTRACT:  Set or gets the ZClearance property for the specified
              motion location.

         Parameter 1: The location index

         Parameter 2: Optional.
                      If omitted, this command returns the location ZClearance
                      and ZWorld values

                      If specified, contains the new location ZClearance value.

         Parameter 3: Optional.
                      If omitted or 0, the ZWorld value is set to False
                      If specified and non-zero, the ZWorld value is set to True"""
        return await self._call("loc_z_clearance", index, clearance, world, channel=channel, timeout=timeout)

    async def loc_config(
        self,
        index: int,
        config: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""LocConfig — Cmd.gpl:1381.

        Cmd_LocConfig -- Sets or Gets the motion location configuration

         ABSTRACT:  Set or gets the configuration property for the specified
              motion location.

         Parameter 1: The location index

         Parameter 2: Optional.
                      If omitted, this command returns the location config value.
                      If specified, contains the new location config value."""
        return await self._call("loc_config", index, config, channel=channel, timeout=timeout)

    async def here_j(
        self, index: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""HereJ — Cmd.gpl:1493.

        Cmd_HereJ -- Sets the specified robot location to the current Angles

         ABSTRACT:  Sets the specified robot location to the current Angles values.

         Parameter 1: The location index"""
        return await self._call("here_j", index, channel=channel, timeout=timeout)

    async def here_c(
        self, index: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""HereC — Cmd.gpl:1525.

        Cmd_HereC -- Sets the specified robot location to the current Cartesian values

         ABSTRACT:  Sets the specified robot location to the current Cartesian values.

         Parameter 1: The location index"""
        return await self._call("here_c", index, channel=channel, timeout=timeout)

    async def release_brake(
        self, axis: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""ReleaseBrake — Cmd.gpl:1612.

        Cmd_ReleaseBrake -- Release the brake for a robot axis

         ABSTRACT:  Releases the brake for a robot axis.

              Releases the brake immediately, without regard to the robot
              servo state.  May cause the robot axis to fall if servos
              are not active.

         Parameter 1: The number of the axis to release."""
        return await self._call("release_brake", axis, channel=channel, timeout=timeout)

    async def set_brake(
        self, axis: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""SetBrake — Cmd.gpl:1631.

        Cmd_SetBrake -- Set the brake for a robot axis

         ABSTRACT:  Sets the brake for a robot axis.

              Sets the brake immediately, without regard to the robot
              servo state.  May cause an error if the axis is moving.

         Parameter 1: The number of the axis to set."""
        return await self._call("set_brake", axis, channel=channel, timeout=timeout)

    async def reset(
        self, thread_id: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Reset — Cmd.gpl:2065.

        Cmd_Reset -- Resets a robot thread

         ABSTRACT:  Resets a robot thread by stopping and starting it.

         Parameter 1: The number of the thread to reset, from 1 to n."""
        return await self._call("reset", thread_id, channel=channel, timeout=timeout)

    async def change_config(
        self, gripper_mode: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""ChangeConfig — PARobot.gpl:666.

        Cmd_ChangeConfig -- Change robot configuration between right and lefty

        ABSTRACT: Command to change Robot configuration between Righty and Lefty
                  Function applicable only to
                  PF400/PF300/C3
                  DD4/DD6
                  C10/C8A
                  C5
                  Robots With a PreciseFlex
                  Servo & Pneumatic Gripper

                  This routine doesn't includes check for collision inside
                  Work volume of the robot and can be customized by user for their
                  workcell configuration

        Parameter 1:  The gripper mode.
                      0 to not change the gripper.
                      1 to open the gripper,
                      2 to close the gripper"""
        return await self._call("change_config", gripper_mode, channel=channel, timeout=timeout)

    async def change_config2(
        self, gripper_mode: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""ChangeConfig2 — PARobot.gpl:874.

        Cmd_ChangeConfig2 -- Change robot configuration between right and lefty

        ABSTRACT: Command to change Robot configuration between Righty and Lefty
                  Function applicable only to
                  PF400/PF300/C3
                  DD4/DD6
                  C10/C8A
                  C5
                  Robots With a PreciseFlex
                  Servo & Pneumatic Gripper

                  This routine doesn't includes check for collision inside
                  Work volume of the robot and can be customized by user for their
                  workcell configuration

                  Alternate routine does not move to safe location.
                  Attempts to minimize extra moves.

        Parameter 1:  The gripper mode.
                      0 to not change the gripper.
                      1 to open the gripper,
                      2 to close the gripper"""
        return await self._call("change_config2", gripper_mode, channel=channel, timeout=timeout)

    async def gripper(
        self, action: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Gripper — PARobot.gpl:1990.

        Cmd_Gripper -- Open or close a gripper

        ABSTRACT: Command to open or close Gripper.
              Handles either a servoed electric gripper or a pnenumatic gripper.
        Parameter 1: 1 - Open Gripper, 2 - Close Gripper"""
        return await self._call("gripper", action, channel=channel, timeout=timeout)

    async def free_mode(
        self, axis: int, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""FreeMode — PARobot.gpl:2048.

        Cmd_FreeMode -- Free selected axes

        ABSTRACT: Command to Free all or one selected axis
              The eGripper, if any, is usually axis 5.

              Requires robot to be attached to enter free mode.

        Parameter 1:  The axes selection to free.
                       Axis = 0                   Free all axes
                       Axis  = 1 to RobNumAxes    Free this axis only
                       Axis = -1                  Turn off Free mode for all axes"""
        return await self._call("free_mode", axis, channel=channel, timeout=timeout)

    async def zero_torque(
        self,
        enabled: int,
        axis_mask: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""ZeroTorque — Cmd.gpl:1582.

        Cmd_ZeroTorque -- Enable/Disable selected robot axes for zero torque mode

         ABSTRACT:  Enables or disables zero torque mode for a set of robot axes.
              In this mode, the selected axes are set to torque mode with
              a constant torque equal to the torque value sampled when this
              command was issued.  The effect is to balance the axes against
              any gravity loading.

         Parameter 1: 0 to disable zero torque mode for the entire robot.
                      1 to enable zero torque mode for the selected axes.
         Parameter 2: Required when enabling zero torque mode.
                      A bit mask with a bit set for each axes to be placed in
                      torque mode."""
        return await self._call("zero_torque", enabled, axis_mask, channel=channel, timeout=timeout)

    async def base(
        self, pose: Sequence[float] | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Base — Cmd.gpl:1651.

        Cmd_Base -- Sets or Gets the base transformation

         ABSTRACT:  Set or gets the BASE transformation for the current
              robot.  Causes a break in any active robot motion.

         Parameter 1-4: Optional
                      If omitted, this command returns the base value.
                      If specified, parameters 1 through 4 contain the
                          X, Y, Z and rotation-about-Z values."""
        return await self._call("base", pose, channel=channel, timeout=timeout)

    async def tool(
        self, pose: Sequence[float] | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Tool — Cmd.gpl:1688.

        Cmd_Tool -- Sets or Gets the tool transformation

         ABSTRACT:  Set or gets the TOOL transformation for the current
              robot.  Causes a break in any active robot motion.

         Parameter 1-6: Optional
                      If omitted, this command returns the tool value.
                      If specified, parameters 1 through 6 contain the
                          X, Y, Z, yaw, pitch, roll values"""
        return await self._call("tool", pose, channel=channel, timeout=timeout)

    async def move(
        self,
        location_index: int,
        profile_index: int,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Move — Cmd.gpl:1724.

        Cmd_Move -- Moves the robot

         ABSTRACT:  Moves the robot to one of the saved locations
              using a saved profile.

         Parameter 1: The index of the destination location

         Parameter 2: The index of the profile to use."""
        return await self._call("move", location_index, profile_index, channel=channel, timeout=timeout)

    async def move_appro(
        self,
        location_index: int,
        profile_index: int,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""MoveAppro — Cmd.gpl:1758.

        Cmd_MoveAppro -- Moves the robot to approach a location

         ABSTRACT:  Moves the robot to approach one of the saved locations
              using a saved profile.

         Parameter 1: The index of the destination location

         Parameter 2: The index of the profile to use."""
        return await self._call("move_appro", location_index, profile_index, channel=channel, timeout=timeout)

    async def move_extra_axis(
        self,
        position1: float,
        position2: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""MoveExtraAxis — Cmd.gpl:1795.

        Cmd_MoveExtraAxis -- Move an extra axis during the next motion

         ABSTRACT:  This command posts a move for the extra axes during
              the next move to a Cartesian location.
              Does not actually cause the robot to move.

              Only some kinematic modules support extra axes.

         Parameter 1: The destination position for the 1st extra axis
         Parameter 2: Optional. The destination position for the 2nd extra axis.
                      If omitted, only the 1st axis is moved"""
        return await self._call("move_extra_axis", position1, position2, channel=channel, timeout=timeout)

    async def move_one_axis(
        self,
        axis: int,
        position: float,
        profile_index: int,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""MoveOneAxis — Cmd.gpl:1825.

        Cmd_MoveOneAxis -- Moves a single axis to the specified position.

         ABSTRACT:  Moves a single axis of the current robot.

              Does not wait for the motion to complete

         Parameter 1: The number of the axis to move.

         Parameter 2: The destination position for the axis

         Parameter 3: The index of the profile to use."""
        return await self._call(
            "move_one_axis", axis, position, profile_index, channel=channel, timeout=timeout
        )

    async def move_j(
        self,
        profile_index: int,
        joints: Sequence[float],
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""MoveJ — Cmd.gpl:1882.

        Cmd_MoveJ -- Move to a location defined by angles.

         ABSTRACT:  Move to the location defined by angles using
              the specified profile.

              Does not change any location values.

         Parameter 1:   The index of the profile to use
         Parameters 2+: Up to 12 parameters
                      These parameters contain the location angles.
                      The number of parameters must equal or greater than
                      the number of axes."""
        return await self._call("move_j", profile_index, joints, channel=channel, timeout=timeout)

    async def move_c(
        self,
        profile_index: int,
        pose: Sequence[float],
        config: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""MoveC — Cmd.gpl:1928.

        Cmd_MoveC -- Move to a Cartesian location.

         ABSTRACT:  Move to the specified Cartesian location using the
              specified profile index.

         Parameter 1:   The index of the profile to use
         Parameter 2-7
                      These parameters contain the new location Cartesian
                      coordinates:  X, Y, Z, y, p, r
                      All 6 parameters must be present

         Parameter 8  Optional configuration.  Assume 0 if omitted."""
        return await self._call("move_c", profile_index, pose, config, channel=channel, timeout=timeout)

    async def sig(
        self,
        signal: int,
        value: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Sig — Cmd.gpl:2036.

        Cmd_Sig -- Sets or Gets a digital signal

         ABSTRACT:  Set a digital signal or gets the current value.

         Parameter 1: The number of the signal to get or set.  If set, the
                      signal must be a digital output.
         Parameter 2: Optional
                      If omitted, this command returns the digital signal value.
                      If specified, contains the new digital signal value."""
        return await self._call("sig", signal, value, channel=channel, timeout=timeout)

    async def load_file(
        self, filename: str | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""LoadFile — Load_save.gpl:57.

        Cmd_LoadFile -- Load a file containing locations and profiles

        ABSTRACT: This command loads a named file into memory.

              The locations and profiles contained in the file are loaded
              into the current robot.

              Any existing values are lost.

         Parameter 1: Optional - The name of the file to be loaded.
                      If not specified, the file Tcs.gpo is loaded.
                      If an extension is not specified, the default is .gpo"""
        return await self._call("load_file", filename, channel=channel, timeout=timeout)

    async def store_file(
        self, filename: str | None = None, *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""StoreFile — Load_save.gpl:101.

        Cmd_StoreFile -- Store the location and profiles data in a file

        ABSTRACT: This command stores the named file by writing the
              locations and profiles for the current robot to the file.

         Parameter 1: Optional - The name of the file.
                      If not specified, the file Tcs.gpo is used.
                      If an extension is not specified, the default is .gpo"""
        return await self._call("store_file", filename, channel=channel, timeout=timeout)

    async def pick_plate(
        self,
        station_id: int,
        compliance: int | None = None,
        holding_torque_percent: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PickPlate — PARobot.gpl:1172.

        Cmd_PickPlate -- Pick up a plate   %%%%BES NOT UPDATED%%%%

        ABSTRACT: Command that goes to a nest position and picks up
              a plate.  If the arm must change configuration, it automatically
              goes through the Park position.

              At the conclusion of this routine, the arm is left gripping the
              plate and stopped at the nest approach position.

              The pick position of the plate is obtained from the indicated station.
              The ZClearance should be set to the distance required to withdraw the
              gripper at the height of the plate pick up position.  The Config bits
              must be set properly for the desired RIGHTY / LEFTY configuration.

              If this operation is for a PF400 for stacks or hotels (STA_FL_VERT = 0),
              an extra World Z motion lifts the grasped plate by z_above before the
              depart motion is performed.

              After the plate is grasped, z_grasp_offset is added to the ZClearance
              to determine the depart location.

        Parameter 1:  The pick station ID, from 1 to N

        Parameter 2:  Optional.  If specified and value 1, enable horizontal
                      compliance during the gripper close operation.
                      Otherwise do not use compliance.
        Parameter 3:  Optional.  The % of the orginal horizontal holding torque
                      to be applied during compliance, from 0 to 100.  If
                      omitted, 0 is assumed, resulting in no horizontal holding
                      torque.

        RETURNS:  True (-1) if a plate has been grasped (as determined by the final
          gripper motor torque level) else False (0)."""
        return await self._call(
            "pick_plate", station_id, compliance, holding_torque_percent, channel=channel, timeout=timeout
        )

    async def place_plate(
        self,
        station_id: int,
        compliance: int | None = None,
        holding_torque_percent: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PlacePlate — PARobot.gpl:1497.

        Cmd_PlacePlate -- Place a plate      %%%%BES NOT UPDATED%%%%

        ABSTRACT: Command that goes to a nest position and places a
              plate that is initially held in the gripper.  If the arm must
              change configuration, it automatically goes through the Park position.

              The place position of the plate is obtained from the indicated station.
              The ZClearance should be set to the distance required to withdraw the
              gripper at the height of the plate place position or the required
              height above the place position with no part in hand.  The Config bits
              must be set properly for the desired RIGHTY / LEFTY configuration.

              The approach position is computed based upon sum of the ZClearance
              property and an extra z_grasp_offset that accounts for the size of
              part being held in the hand.

              If this operation is for a PF400 for stacks or hotels (STA_FL_VERT = 0),
              the approach position is positioned z_above distance higher in Z
              than the place position.  And, an extra move to z_above the place
              position is performed after the approach and before the move to the
              final placement position.

              At the conclusion of this routine, the arm is left with the gripper
              open, not gripping a plate, and stopped at the nest approach
              ZClearance position.

        Parameter 1:  The place station ID, from 1 to n

        Parameter 2:  Optional.  If specified and value 1, enable horizontal
                      compliance during the placment move.
                      Otherwise do not use compliance.
        Parameter 3:  Optional.  The % of the orginal horizontal holding torque
                      to be applied during compliance, from 0 to 100.  If
                      omitted, 0 is assumed, resulting in no horizontal holding
                      torque."""
        return await self._call(
            "place_plate", station_id, compliance, holding_torque_percent, channel=channel, timeout=timeout
        )

    async def teach_plate(
        self,
        station_id: int,
        z_clearance: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""TeachPlate — PARobot.gpl:1795.

        Cmd_TeachPlate -- Teach a plate location

        ABSTRACT: Command to teach a Plate Location for a PreciseFlex robot with
                  a Servo Gripper.  This routine assumes the robot is at the location
                  to be taught. Free Mode can be used to move the robot to the
                  desired position.

        Parameter 1:  The station ID for the Plate location to be taught,
                      from 1 to n

        Parameter 2:  Optional.  The ZClearance value in millimeters for this station
                      If omitted, the default value Z_CLEARANCE is used.

                      The ZClearance should be set to the distance required to
                      withdraw the gripper at the height of the
                      plate position.  The Config bits
                      must be set properly for the desired RIGHTY /
                      LEFTY configuration.
                      Station ID locations are Cartesian Type"""
        return await self._call("teach_plate", station_id, z_clearance, channel=channel, timeout=timeout)

    async def move_rail(
        self,
        station_id: int,
        mode: int | None = None,
        position: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""MoveRail — PARobot.gpl:1883.

        Cmd_MoveRail -- Move the linear rail axis

        ABSTRACT: Command to move the linear rail axis to a station.
              The move may occur immediately or during the next pick or place.

        Parameter 1:  The destination station ID.
        Parameter 2:  Optional.  The motion mode.
                      If omitted or zero, do not move the rail.
                          Cancel any pending rail move.
                      1 = Move the rail immediately.
                      2 = Move the rail during the next pick or place.
        Parameter 3:  Optional. If specified, move the rail axis to this
                      position instead of the station location."""
        return await self._call("move_rail", station_id, mode, position, channel=channel, timeout=timeout)

    async def rail(
        self,
        station_id: int,
        position: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""Rail — PARobot.gpl:1942.

        Cmd_Rail -- Gets or sets the linear rail value

         ABSTRACT:  Gets or sets the specified the rail value for a station

         Parameter 1: The station index from 1 to n.

         Parameter 2: Optional.
                      If omitted, this command returns specified rail value.
                      If specified, this value becomes the new rail value."""
        return await self._call("rail", station_id, position, channel=channel, timeout=timeout)

    async def grasp_data(
        self,
        width: float | None = None,
        speed: float | None = None,
        force: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""GraspData — PARobot.gpl:2208.

        Cmd_GraspData -- Set and get the grasp data

        ABSTRACT: Command to Set & Get the grasp data used by PickPlate.
              Used only for Servo Gripper. For Pneumatic Gripper - Adjust Hardware

        Parameter 1:  Optional.  If omitted, return the parameter values
                      If specified, this is the new value for the plate width.
                      If specified, all remaining parameters must be specified.

        Parameter 2:  Optional. If specified, the new value for the finger speed
                      during grasp, where 100 represents 100%.

        Parameter 3:  Optional. If specified, the new value for the gripper
                      squeeze force, in Nt.  Positive values indicate that the
                      fingers must squeeze close to grasp the plate.  Negative
                      values indicate that the fingers must open to grasp."""
        return await self._call("grasp_data", width, speed, force, channel=channel, timeout=timeout)

    async def station_type(
        self,
        station_id: int,
        access: int | None = None,
        pallet_type: int | None = None,
        z_clearance: float | None = None,
        z_above: float | None = None,
        z_grasp_offset: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""StationType — PARobot.gpl:2263.

        Cmd_StationType -- Set and get the station type

        ABSTRACT: Command to Set & Get the station type and indexing type.

              If parameters 2 - 5 are omitted, return the current types

        Parameter 1: The station index from 1 to n.

        Parameter 2: optional.  The station access code:
                     -1 = Do not change
                     0 = Horizontal access, from the side
                     1 = Vertical access, from the top
        Parameter 3: optional.  The station pallet type
                     -1 = Do not change
                     0 = Normal, single location.
                     1 = Indexing pallet, 1,2,or 3 dimensional
        Parameter 4: optional.  The Z-clearance value for this location
        Parameter 5: optional.  The Z-above distance for robots using
                     horizontal access.
        Parameter 6: optional.  The Z grasp offset applied when grasping
                     a part."""
        return await self._call(
            "station_type",
            station_id,
            access,
            pallet_type,
            z_clearance,
            z_above,
            z_grasp_offset,
            channel=channel,
            timeout=timeout,
        )

    async def pallet_origin(
        self,
        station_id: int,
        pose: Sequence[float] | None = None,
        config: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PalletOrigin — PARobot.gpl:2415.

        Cmd_PalletOrigin -- Gets or sets the pallet origin value

         ABSTRACT:  Gets or sets the specified the station pallet origin

                  If parameters 2-8 are omitted, returns the pallet origin info.

                  Until PalletX and PalletY are executed, the pallet is
                  assumed to be in the X-Y plane.

         Parameter 1:     The station index from 1 to n.

         Parameters 2-7:  Optional.  The world location of the pallet orgin.
                          X Y Z yaw pitch roll
                          Corresponds to pallet index 1,1,1

         Parameter 8:     Optional.  The configuration flags for this location
                          Assumed to be 0 if not specified."""
        return await self._call("pallet_origin", station_id, pose, config, channel=channel, timeout=timeout)

    async def pallet_x(
        self,
        station_id: int,
        count: int | None = None,
        xyz: Sequence[float] | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PalletX — PARobot.gpl:2498.

        Cmd_PalletX -- Gets or sets the pallet X value

         ABSTRACT:  Gets or sets the specified the station pallet X direction,
                  count, and pitch for a 1, 2, or 3-dimensional pallet.
                  It must be called for all pallets.

                  PalletOrigin must be executed before this instruction.

                  If parameters 2-5 are omitted, returns the pallet X info.

         Parameter 1:     The station index from 1 to n.

         Parameter 2:     Optional.  The number of pallet index positions
                          in the X direction.

         Parameters 3-5:  Optional.  The world location of maximum pallet
                          position: X Y Z.
                          Corresponds to pallet index n,1,1"""
        return await self._call("pallet_x", station_id, count, xyz, channel=channel, timeout=timeout)

    async def pallet_y(
        self,
        station_id: int,
        count: int | None = None,
        xyz: Sequence[float] | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PalletY — PARobot.gpl:2640.

        Cmd_PalletY -- Gets or sets the pallet Y value

         ABSTRACT:  Gets or sets the specified the station pallet Y direction,
                  count, and pitch for a 2 or 3-dimensional pallet.
                  It does not need to be called for 1-dimensional pallets.

                  It does not change the X direction of the pallet, only the
                  Y direction.

                  PalletOrigin and PalletX must be called before this instruction.

                  If parameters 2-5 are omitted, returns the pallet Y info.

         Parameter 1:     The station index from 1 to n.

         Parameter 2:     Optional.  The number of pallet index positions
                          in the Y direction.

         Parameters 3-5:  Optional.  The world location of maximum pallet
                          position: X Y Z.
                          Corresponds to pallet index 1,n,1"""
        return await self._call("pallet_y", station_id, count, xyz, channel=channel, timeout=timeout)

    async def pallet_z(
        self,
        station_id: int,
        count: int | None = None,
        xyz: Sequence[float] | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PalletZ — PARobot.gpl:2772.

        Cmd_PalletZ -- Gets or sets the pallet Z value

         ABSTRACT:  Gets or sets the specified the station pallet Z count
                  and pitch for a 3-dimensional pallet.
                  It does not need to be called for 1 or 2-dimensional pallets.

                  It does not change the orientation of the pallet.
                  It only establishes the Z index pitch and count.

                  PalletOrigin, PalletX, and PalletZ must all be called
                  before this instruction.

                  If parameters 2-5 are omitted, returns the pallet Z info.

         Parameter 1:     The station index from 1 to n.

         Parameter 2:     Optional.  The number of pallet index positions
                          in the Z direction.

         Parameters 3-5:  Optional.  The world location of maximum pallet
                          position: X Y Z.
                          Corresponds to pallet index 1,1,n"""
        return await self._call("pallet_z", station_id, count, xyz, channel=channel, timeout=timeout)

    async def pallet_index(
        self,
        station_id: int,
        x: int | None = None,
        y: int | None = None,
        z: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""PalletIndex — PARobot.gpl:2875.

        Cmd_PalletIndex -- Gets or sets the pallet index value

         ABSTRACT:  Gets or sets the specified the station pallet index
                  positions.

                  If parameters 2-4 are omitted, returns current index values.

         Parameter 1:     The station index from 1 to n.

         Parameter 2-4:   Optional.  The X, Y, and Z index values, from 1 to n.
                          If set to 0, the corresponding index is not changed."""
        return await self._call("pallet_index", station_id, x, y, z, channel=channel, timeout=timeout)

    async def grasp_plate(
        self,
        width: float,
        speed: float,
        force: float,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""GraspPlate — PARobot.gpl:3650.

        Cmd_GraspPlate - Command to grasp a plate with limited force

        ABSTRACT:  This command grasps a plate of a specified width at the
          defined speed and limits the maximum gripping force.  The width
          should be accurate to within approximately a mm since this routine
          closes the fingers narrower than this width.  The difference between
          the width of the plate and the commanded gripper position generates
          a position error that the PID servo loop converts into the gripping
          force.

          At the end of the gripping motion, the gripper motor torque is
          tested to confirm that the grasping operation has been successful.

        Paramter 1:           Width of the plate to be grasped in mm.  This
                              dimension does not need to be exact but should
                              be accurate to within a mm or so to ensure that
                              this routine generates a sufficiently large
                              gripping force.

        Parameter 2:          Speed at which the fingers are to close where
                              100 represents the 100% speed.

        Parameter 3:          Maximum gripper squeeze force to be applied in
                              Nt.  Positive numbers indicate that the gripper
                              will be closed to grasp the plate.  Negative
                              numbers indicate that the gripper will be
                              opened.  Due to noise, friction, and variations
                              in the gripper spring force, the actual maximum
                              gripper force will have some variability.

        OUTPUTS:  None

        RETURNS:  True (-1) if a plate has been grasped (as determined by the final
          gripper motor torque level) else False (0)."""
        return await self._call("grasp_plate", width, speed, force, channel=channel, timeout=timeout)

    async def release_plate(
        self,
        width: float,
        speed: float,
        in_range: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""ReleasePlate — PARobot.gpl:3707.

        Cmd_ReleasePlate -- Command to release a plate after GraspPlate

        ABSTRACT:  This command opens the gripper to a specified width and turns
          off the restriction on the gripper's peak force.  The force limit
          is not eliminated until the plate is released to avoid applying
          an excessive force to the plate.  An independent thread cancels
          the force limit to prevent blocking execution of the main thread.

        Parameter 1           Distance in mm to which the fingers are to open.

        Parameter 2           Speed at which the fingers are to open where
                              100 represents the 100% speed.

        Parameter 3           Optional. Standard InRange profile parameter for the motion
                              to open the gripper.  Permits the caller to
                              have this gripper open motion blended or not blended
                              with the next motion.
                              If not specified, the value 0 is assumed"""
        return await self._call("release_plate", width, speed, in_range, channel=channel, timeout=timeout)

    async def set_active_gripper(
        self,
        gripper: int,
        spin: int | None = None,
        profile_index: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""SetActiveGripper — PARobot.gpl:3794."""
        return await self._call(
            "set_active_gripper", gripper, spin, profile_index, channel=channel, timeout=timeout
        )

    async def height_detect(
        self,
        quick_mode: int | None = None,
        search_limit: float | None = None,
        max_force: float | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""HeightDetect — PARobot_auto_center_intf.gpl:102.

        Cmd_HeightDetect -- Command handler for executing HeightDetect function

        ABSTRACT:  Executes the HeightDetect function that moves the gripper
              down and detects the height of a stack of plates or the height of a
              nest using motor force sensing.  Please see the documentation on
              this function for complete information.

              Given the complexity of this function, this command does not return
              until the height detection operation has completed.

              If no parameters are specified, they are all set to their default
              values.

        INPUTS:

         Parameter 1: QuickMode - 1 for quick execution only and 2 for execution
                      of the thorough mode.  Set to 2 by default
         Parameter 2: rXSearchLimit -  Maximum distance that the gripper is
                      permitted to move down relative to the starting position,
                      in mm.  Set to -1E6 by default.
         Parameter 3: XMaxForce - Maximum vertical force to be applied when searching
                      for the stack height, in Nt.  Set to -15 by default.

        OUPUTS:   If successful, returns the detected height in mm in absolute
                  robot coordinates."""
        return await self._call(
            "height_detect", quick_mode, search_limit, max_force, channel=channel, timeout=timeout
        )

    async def custom(
        self, *values: float, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""Custom — Custom.gpl:101.

        Cmd_Custom -- Command handler for the "Custom" command

        INPUTS:   Cmd     An object of the class "Command" which contains the parsed
                          command message from the remote client.

                          See the Class Command definition in the Class_command.gpl.

                              Cmd.Rob.RobNum  is the assigned robot number, or 0
                                              if the status thread.
                              Cmd.Rob.RobNumAxes is the number of axes for this robot.
                              Cmd.sData(0)    is the command that invoked this routine
                              Cmd.Nparm       is the number of parameters
                              Cmd.sData(1...) are the parameter strings.
                              Cmd.cData(1...) are the parameter numeric values after
                                              StringToDouble is called.

        OUPUTS:   Reply   The string sent to the client in response to this command.

                          In normal mode, success is indicated a zero "0" as the
                          first field and failure is indicated by a negative error
                          code.

                          In Telnet mode, which is intended to be read by humans,
                          success is indicated by the string "Ok" and errors by
                          an error message string.

                          Arbitrary string data may be appended afterwards.

                          The default value upon entry is "0" if normal mode
                          and "Ok" if Telnet mode."""
        return await self._call("custom", *values, channel=channel, timeout=timeout)

    async def convert_joint_to_cartesian(
        self, joints: Sequence[float], *, channel: str | None = None, timeout: float | None = None
    ) -> Response:
        r"""ConvertJointToCartesian — Custom.gpl:134.

        ConvertJointToCartesian -- Convert joint values with the controller KineSol.

        Parameters 1..N: Joint values. N must match the configured robot axes.
        Returns: X Y Z Yaw Pitch Roll Config."""
        return await self._call("convert_joint_to_cartesian", joints, channel=channel, timeout=timeout)

    async def convert_cartesian_to_joint(
        self,
        pose: Sequence[float],
        config: int | None = None,
        *,
        channel: str | None = None,
        timeout: float | None = None,
    ) -> Response:
        r"""ConvertCartesianToJoint — Custom.gpl:173.

        ConvertCartesianToJoint -- Convert Cartesian values with the controller KineSol.

        Parameters 1..6: X Y Z Yaw Pitch Roll.
        Parameter 7: Optional Config. Defaults to 0.
        Returns: configured robot joint values."""
        return await self._call("convert_cartesian_to_joint", pose, config, channel=channel, timeout=timeout)
