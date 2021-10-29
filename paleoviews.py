import pygplates
from gprm.utils.create_gpml import gpml2gdf


def wrap_reconstructed_features(reconstructed_features, central_longitude = 0., tesselation_degrees = 1.):

    date_line_wrapper = pygplates.DateLineWrapper(central_meridian=central_longitude)

    wrapped_features = []
    for reconstructed_feature in reconstructed_features:
        geometry = reconstructed_feature.get_reconstructed_geometry()
        split_polygons = date_line_wrapper.wrap(geometry, tesselation_degrees)
        for split_polygon in split_polygons:
            f = pygplates.Feature()
            if isinstance(split_geometry, date_line_wrapper.LatLonPolyline):
                f.set_geometry(pygplates.PolylineOnSphere(
                    (wrapped_point.get_latitude(), wrapped_point.get_longitude()) for wrapped_point in split_geometry.get_points())
                              )
            elif isinstance(split_geometry, date_line_wrapper.LatLonPolygon):   
                f.set_geometry(pygplates.PolygonOnSphere(
                    (wrapped_point.get_latitude(), wrapped_point.get_longitude()) for wrapped_point in split_geometry.get_exterior_points())
                              )
            f.set_name(feature.get_feature().get_name())
            f.set_reconstruction_plate_id(feature.get_feature().get_reconstruction_plate_id())
            f.set_valid_time(feature.get_feature().get_valid_time()[0], feature.get_feature().get_valid_time()[1])
            wrapped_features.append(f)

    return gpml2gdf(wrapped_features)


def wrap_features(features, central_longitude = 0., tesselation_degrees = 1.):

    date_line_wrapper = pygplates.DateLineWrapper(central_meridian=central_longitude)

    wrapped_features = []
    for feature in features:  
        geometry = feature.get_geometry()
        split_geometries = date_line_wrapper.wrap(geometry, tesselation_degrees)
        for split_geometry in split_geometries:
            f = pygplates.Feature()
            if isinstance(split_geometry, date_line_wrapper.LatLonPolyline):
                f.set_geometry(pygplates.PolylineOnSphere(
                    (wrapped_point.get_latitude(), wrapped_point.get_longitude()) for wrapped_point in split_geometry.get_points())
                              )
            elif isinstance(split_geometry, date_line_wrapper.LatLonPolygon):    
                f.set_geometry(pygplates.PolygonOnSphere(
                    (wrapped_point.get_latitude(), wrapped_point.get_longitude()) for wrapped_point in split_geometry.get_exterior_points())
                              )
            f.set_name(feature.get_name())
            f.set_reconstruction_plate_id(feature.get_reconstruction_plate_id())
            f.set_valid_time(feature.get_valid_time()[0], feature.get_valid_time()[1])
            wrapped_features.append(f)

    return gpml2gdf(wrapped_features)


