"""
MVP: US-only validation using approximate bounding boxes.
Contiguous US, Alaska, and Hawaii. International support deferred.
"""

# (lat_min, lat_max, lon_min, lon_max) for each region
_CONTIGUOUS_US = (24.5, 49.0, -125.0, -66.0)   # Lower 48
_ALASKA = (51.0, 71.5, -180.0, -129.0)
_HAWAII = (18.5, 22.5, -160.5, -154.5)

_REGIONS = [_CONTIGUOUS_US, _ALASKA, _HAWAII]


def is_in_us(latitude: float, longitude: float) -> bool:
    """Return True if (latitude, longitude) falls within US territory (contiguous, Alaska, Hawaii)."""
    for lat_min, lat_max, lon_min, lon_max in _REGIONS:
        if lat_min <= latitude <= lat_max and lon_min <= longitude <= lon_max:
            return True
    return False
