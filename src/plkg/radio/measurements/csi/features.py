import numpy as np

from plkg.core.models import CsiObservation, FeatureSeries


class CsiAmplitudeExtractor:
    def extract(self, observation: CsiObservation) -> FeatureSeries:
        if not isinstance(observation, CsiObservation):
            raise TypeError("CsiAmplitudeExtractor requires CsiObservation")
        return FeatureSeries(
            values=np.abs(observation.values),
            name="csi_amplitude",
        )
