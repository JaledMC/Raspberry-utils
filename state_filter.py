import time
from collections import deque


class StateFilter:
    """
    Many times, YOLO detected class for one object changes rapidly. This high
    frecuency bounce can be filter by time and by average, to catch the
    stable value.
    Args:
        current_state: filtered and stable state of the object class
        state_history: list with past states no filtered
        change_time: time treshold. Any class change which happens 
            before this time doesn't trigger an state change 
        momentum: threshold percentage for average_filter
    """
    def __init__(self, history_size, time_threshold, momentum=.6):
        self.current_state = None
        self.state_history = deque([], maxlen=history_size)
        self.time_threshold = time_threshold
        self.momentum = int(momentum * history_size)
        self.prev_time = time.time()

    def average_filter(self):
        """
        Counts the ocurrences of each class along the state_history.
        If any of them surpass the momentum value, returns the winner
        """
        average = {}
        for state in self.state_history:
            if state in average: 
                average[state] += 1
            else: 
                average[state] = 1
            if average[state] >= self.momentum:
                return state
        return None
    
    def time_filter(self):
        """
        Returns True if it had passed more time than time_threshold
        """
        return time.time() - self.prev_time > self.time_threshold

    def update(self, new_state):
        """
        Add new class detection to the history list, and apply both average
        and time filters, to refresh and return the filtered new current_state.
        current_state and new winner should be different to trigger a change.
        """
        self.state_history.append(new_state)
        winner = self.average_filter()
        if winner is not None and winner is not self.current_state and self.time_filter():
            self.current_state = winner
            self.prev_time = time.time()
        return self.current_state
