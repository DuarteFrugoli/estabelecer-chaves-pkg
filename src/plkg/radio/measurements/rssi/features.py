from plkg.core.models import FeatureSeries, RssiObservation


class RssiLevelExtractor:
    def extract(self, observation: RssiObservation) -> FeatureSeries:
        if not isinstance(observation, RssiObservation):
            raise TypeError("RssiLevelExtractor requires RssiObservation")
        return FeatureSeries(values=observation.values_dbm, name="rssi_level")
