import pygplates
from gprm.utils.create_gpml import gpml2gdf
import numpy as np
import geoviews as gv
from cartopy import crs as ccrs



def wrap_reconstructed_features(reconstructed_features, central_longitude = 0., tesselation_degrees = 1.):

    date_line_wrapper = pygplates.DateLineWrapper(central_meridian=central_longitude)

    wrapped_features = []
    for reconstructed_feature in reconstructed_features:
        geometry = reconstructed_feature.get_reconstructed_geometry()
        if geometry is not None:
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
                f.set_name(reconstructed_feature.get_feature().get_name())
                f.set_reconstruction_plate_id(reconstructed_feature.get_feature().get_reconstruction_plate_id())
                f.set_valid_time(reconstructed_feature.get_feature().get_valid_time()[0], 
                                 reconstructed_feature.get_feature().get_valid_time()[1])
                wrapped_features.append(f)

    return gpml2gdf(wrapped_features)


def wrap_features(features, central_longitude = 0., tesselation_degrees = 1.):

    date_line_wrapper = pygplates.DateLineWrapper(central_meridian=central_longitude)

    wrapped_features = []
    for feature in features:  
        geometry = feature.get_geometry()
        if geometry is not None:
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


def polygon_view(reconstruction_model, reconstruction_time, polygon_type='continents', 
                 anchor_plate_id=0,
                 dim=400, projection=ccrs.Robinson(),
                 vdims=['NAME', 'PLATEID1', 'FROMAGE']):
    
    snapshot = reconstruction_model.polygon_snapshot(polygon_type, reconstruction_time, anchor_plate_id=anchor_plate_id)
    
    return gv.Polygons(wrap_reconstructed_features(snapshot.reconstructed_polygons), 
                       vdims=vdims).opts(tools=['hover'], 
                                         height=dim, 
                                         width=int(dim*1.9), 
                                         projection=projection, 
                                         color_index='FROMAGE',
                                         cmap='inferno_r'
                                        )
    
    
def topology_view(reconstruction_model, reconstruction_time, 
                  anchor_plate_id=0,
                  dim=400, projection=ccrs.Robinson()):
    
    plates = reconstruction_model.plate_snapshot(reconstruction_time, anchor_plate_id=anchor_plate_id)
    features = [resolved_topology.get_resolved_feature() for resolved_topology in plates.resolved_topologies]

    return gv.Polygons(wrap_features(features), 
                       vdims=['NAME', 'PLATEID1']).opts(height=dim, 
                                                        width=int(dim*1.9), 
                                                        projection=projection, 
                                                        fill_color='red'
                                                       )
    
    
def velocity_view(reconstruction_model, reconstruction_time, 
                  anchor_plate_id=0,
                  dim=400, projection=ccrs.Robinson()):
    
    plates = reconstruction_model.plate_snapshot(reconstruction_time, anchor_plate_id=anchor_plate_id)
    velocities = plates.velocity_field()
    
    azimuths = np.radians(90.-np.degrees(+np.array(velocities.velocity_azimuth)))
    magnitudes = np.array(velocities.velocity_magnitude)

    vectorfield = gv.VectorField((velocities.longitude, 
                                  velocities.latitude, 
                                  azimuths,
                                  magnitudes*0.04))

    return vectorfield.opts(magnitude='Magnitude', 
                            color='Magnitude', 
                            cmap='fire', 
                            height=dim, 
                            width=int(dim*1.9),
                            projection=projection, 
                            global_extent=True, 
                            normalize_lengths=False)
    
    
    
