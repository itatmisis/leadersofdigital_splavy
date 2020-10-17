from typing import Dict, Any

import numpy as np
from sklearn.neighbors import BallTree, DistanceMetric

from database.entities.geographical_point import GeographicalPoint


def get_radius_objects(center: GeographicalPoint, radius: float, objects: Dict[Any, GeographicalPoint]) \
        -> Dict[Any, GeographicalPoint]:
    object_points = np.array([[point.latitude, point.longitude] for point in list(objects.values())])
    tree = BallTree(object_points, leaf_size=2, metric=DistanceMetric.get_metric("haversine"))
    object_idxs = tree.query_radius([center.latitude, center.longitude], r=radius)
    objects = {list(objects.keys())[idx]: list(objects.values())[idx] for idx in object_idxs}

    return objects
