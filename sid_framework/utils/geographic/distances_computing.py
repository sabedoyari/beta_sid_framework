import stateplane as sp
from sklearn.metrics.pairwise import nan_euclidean_distances



def get_metric_coordinates(lat, long):

    """
    
    """

    metric_coordinates = sp.from_latlon(
        lat = lat,
        lon = long,
        # epsg = '9377'
        epsg = 2866
    )
    metric_coordinates_dict = {
        'latitude': lat,
        'longitude': long,
        'metric_latitude': metric_coordinates[0],
        'metric_longitude': metric_coordinates[1]
    }

    return metric_coordinates_dict


def euclidean_distances(reference_points, comparison_points):

    """
    
    """

    distances = nan_euclidean_distances(reference_points, comparison_points)

    return distances
