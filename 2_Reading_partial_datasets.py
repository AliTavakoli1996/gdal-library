
import os
from osgeo import gdal



os.chdir(r'C:\Users\Ali\Desktop\khn-ut\raster\data\osgeopy-data-landsat-washington\/'
         r'osgeopy-data\Landsat\Washington')

band1_fn = 'p047r027_7t20000730_z10_nn10.tif'
band2_fn = 'p047r027_7t20000730_z10_nn20.tif'
band3_fn = 'p047r027_7t20000730_z10_nn30.tif'

in_ds = gdal.Open(band1_fn)
in_band = in_ds.GetRasterBand(1)

in_data = in_band.ReadAsArray()
in_data = in_band.ReadAsArray(1400, 6000, 6, 3)

import numpy as np
data = np.empty((50, 50), dtype=float)
in_band.ReadAsArray(1400, 6000, 50, 50, buf_obj=data)



