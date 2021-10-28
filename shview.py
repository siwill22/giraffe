#shview

import geoviews as gv
import geoviews.feature as gf
import xarray as xr
import cartopy.crs as ccrs

gv.extension('bokeh')



def mag_view(mag, clim=(-1000, 1000), projection=ccrs.Robinson(), cols=1, cmap='seismic', width=500):
    
    image_radial = gv.Dataset(mag.rad.to_xarray(), ['lon', 'lat'], 'radial', crs=ccrs.PlateCarree()).redim.range(radial=clim).to(gv.Image)
    image_theta = gv.Dataset(mag.theta.to_xarray(), ['lon', 'lat'], 'theta', crs=ccrs.PlateCarree()).redim.range(theta=clim).to(gv.Image)
    image_phi = gv.Dataset(mag.phi.to_xarray(), ['lon', 'lat'], 'phi', crs=ccrs.PlateCarree()).redim.range(phi=clim).to(gv.Image)


    dim = width

    ((image_radial.opts(cmap=cmap, colorbar=True, width=dim*2, height=dim, projection=projection) * gf.coastline) +\
    (image_theta.opts(cmap=cmap, colorbar=True, width=dim*2, height=dim, projection=projection) * gf.coastline) +\
    (image_phi.opts(cmap=cmap, colorbar=True, width=dim*2, height=dim, projection=projection) * gf.coastline)).cols(cols)


