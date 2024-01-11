import shutil
from osgeo import gdal, osr

orig_fn = r'C:\Users\Ali\Desktop\khn-ut\raster\data\Utah\cache_no_gcp.tif'
fn = r'C:\Users\Ali\Desktop\khn-ut\raster\data\Utah\cache.tif'

# Make a copy of the file to work with

shutil.copy(orig_fn, fn)

ds = gdal.Open(fn, gdal.GA_Update)

sr = osr.SpatialReference()
sr.SetWellKnownGeogCS('WGS84')
gcps = [
    gdal.GCP(-111.931075, 41.745836, 0, 1078, 648),
    gdal.GCP(-111.901655, 41.749269, 0, 3531, 295),
    gdal.GCP(-111.899180, 41.739882, 0, 3722, 1334),
    gdal.GCP(-111.930510, 41.728719, 0, 1102, 2548)
]

ds.SetGCPs(gcps, sr.ExportToWkt())


ds.GetRasterBand(1).ComputeStatistics(False)
ds.BuildOverviews('average', [2, 4, 8, 16, 32])
ds = None

