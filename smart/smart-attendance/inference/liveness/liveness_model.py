import numpy as np


class LivenessModel:
    def __init__(self):
        # For demo, we don't load any heavy DL model
        # In production, load a trained CNN here (e.g., MobileNetV2)
        pass

    def predict(self, face_crop):
        """
        face_crop : numpy array (cropped face image)

        Returns:
            float score between 0 and 1
            Higher score = more likely live face
        """

        # Heuristic:
        # Real faces have texture → higher pixel variance
        # Printed / screen faces look flat → low variance

        score = np.var(face_crop) / 1000.0

        # clamp score into [0,1]
        score = max(0.0, min(1.0, score))

        return float(score)
