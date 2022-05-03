from typing import Callable
from game_engine.helpers import Singleton


PyGame_EventType = int
PyGame_EventKey = int
# Make a lambda with 2 parameters
EmptyCallback = lambda e: None
"""EmptyCallback is a lambda function that takes a pygame event as a parameter."""
class EventListenerInstance:
    """Event Listener object. Used to detect input"""
    def __init__(self):
        self.event_listener: dict[PyGame_EventType, dict[int, Callable]] = {}
        self._remove_queue: dict[PyGame_EventType, list[int]] = {}
        self._add_queue: dict[PyGame_EventType, dict[int, Callable]] = {}

    def update(self, event_type: PyGame_EventType,
               obj:object, callback: Callable):
        # Check if callback have 1 argument
        if len(callback.__code__.co_varnames) != 1:
            raise ValueError("Callback must have 1 argument")
        if event_type not in self.event_listener:
            if event_type not in self._add_queue:
                self._add_queue[event_type] = {}
            self._add_queue[event_type][id(obj)] = callback
        else:
            if id(obj) not in self.event_listener[event_type]:
                if event_type not in self._add_queue:
                    self._add_queue[event_type] = {}
                self._add_queue[event_type][id(obj)] = callback
            else:
                self.event_listener[event_type][id(obj)] = callback

    def remove(self, obj:object):
        for event_type in self.event_listener:
            if id(obj) in self.event_listener[event_type]:
                if event_type not in self._remove_queue:
                    self._remove_queue[event_type] = []
                self._remove_queue[event_type].append(id(obj))

    def commit(self):
        # Append add queue to on_event_listener
        for add_type in self._add_queue:
            if add_type not in self.event_listener:
                self.event_listener[add_type] = {}
            self.event_listener[add_type].update(self._add_queue[add_type])
        self._add_queue = {}
        # Remove remove queue from on_event_listener
        for remove_type in self._remove_queue:
            for id_to_remove in self._remove_queue[remove_type]:
                self.event_listener[remove_type].pop(id_to_remove, None)
        self._remove_queue = {}

    def get(self, event_type: PyGame_EventType):
        if event_type in self.event_listener:
            return self.event_listener[event_type]
        return {}


@Singleton[EventListenerInstance]
class EventListener(EventListenerInstance):
    pass
