from collections import deque


class BehaviorModel:
    def __init__(self, window=16):
        # window = number of frames to consider for behavior analysis
        self.window = window
        self.buffer = {}  # stores features per tracked student (track_id)

    def update(self, track_id, features):
        """
        track_id  : unique ID assigned by YOLO tracker for each person
        features  : numeric value extracted per frame (placeholder)
                    e.g., mouth openness, head pose score, etc.
        """
        if track_id not in self.buffer:
            # create a new queue for this student
            self.buffer[track_id] = deque(maxlen=self.window)

        self.buffer[track_id].append(features)

    def predict(self, track_id):
        """
        Predict behavior based on last N frames.
        Returns dictionary of behavior probabilities.
        """

        buf = self.buffer.get(track_id, [])

        if not buf:
            # no history available
            return {'yawn': 0.0, 'looking_away': 0.0, 'phone': 0.0}

        avg = sum(buf) / len(buf)

        # Fake simple heuristics:
        # - avg > 0.6 → yawning detected
        # - avg < 0.2 → looking away / not attentive

        return {
            'yawn': float(avg > 0.6),
            'looking_away': float(avg < 0.2),
            'phone': 0.0  # not implemented yet
        }
