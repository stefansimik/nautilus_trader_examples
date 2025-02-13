from enum import IntEnum
from typing import Dict, Tuple

from nautilus_trader.core.fsm import FiniteStateMachine, InvalidStateTrigger


# Step 1: Define states
class AppState(IntEnum):  # Only IntEnum is supported for Nautilus State Machine
    """
    Represents the possible states of our application.
    """

    INITIALIZED = 0
    READY = 1
    ACTIVE = 2
    PAUSED = 3
    STOPPED = 4


# Step 2: Define triggers (actions)
class AppTrigger(IntEnum):  # Only IntEnum is supported for Nautilus State Machine
    """
    Represents the possible triggers that can cause transitions between states
    """

    START = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3


# Step 3: Define transitions
# Each line contains: (OLD_STATE, TRIGGER) -> NEW STATE
STATE_TRANSITIONS: Dict[Tuple[AppState, AppTrigger], AppState] = {
    (AppState.READY, AppTrigger.START): AppState.ACTIVE,
    (AppState.ACTIVE, AppTrigger.PAUSE): AppState.PAUSED,
    (AppState.ACTIVE, AppTrigger.STOP): AppState.STOPPED,
    (AppState.PAUSED, AppTrigger.RESUME): AppState.ACTIVE,
    (AppState.PAUSED, AppTrigger.STOP): AppState.STOPPED,
}

# ---------------------------------------
# Example how to create State Machine
# ---------------------------------------

fsm = FiniteStateMachine(
    state_transition_table=STATE_TRANSITIONS,
    initial_state=AppState.READY,
    # Next 2 parameters refer to function(s), that convert enum number -> string
    state_parser=lambda code: {enum.value: enum.name for enum in AppState}[
        code
    ],  # lambda function, that converts enum-value to enum-name visible in `fsm.state_string`. This is good default implementation
    trigger_parser=lambda code: {enum.value: enum.name for enum in AppTrigger}[code],  # -||-
)

# ---------------------------------------
# Testing State Machine:
# Using State Machine simply means invoking triggers (actions)
# ---------------------------------------

print(f"Initial state: {fsm.state_string}")

print(f"Invoking trigger: {AppTrigger.START}")
fsm.trigger(AppTrigger.START)
print(f"Current state: {fsm.state_string}")

print(f"Invoking trigger: {AppTrigger.PAUSE}")
fsm.trigger(AppTrigger.PAUSE)
print(f"Current state: {fsm.state_string}")

print(f"Invoking trigger: {AppTrigger.RESUME}")
fsm.trigger(AppTrigger.RESUME)
print(f"Current state: {fsm.state_string}")

print(f"Invoking trigger: {AppTrigger.STOP}")
fsm.trigger(AppTrigger.STOP)
print(f"Current state: {fsm.state_string}")

# Example - let's try invalid action:
# We cannot RESUME, after state-machine was STOPPED.
try:
    print(f"Invoking trigger: {AppTrigger.RESUME}")
    fsm.trigger(AppTrigger.RESUME)
except InvalidStateTrigger:
    # We expect this exception be thrown, as we intentionally invoke invalid trigger/action.
    print("We got expected exception: InvalidStateTrigger")
