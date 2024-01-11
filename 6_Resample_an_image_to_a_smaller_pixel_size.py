import os
from osgeo import gdal


os.chdir(r'C:\Users\Ali\Desktop\khn-ut\raster\data\osgeopy-data-landsat-washington\/'
         r'osgeopy-data\Landsat\Washington')
in_ds = gdal.Open('p047r027_7t20000730_z10_nn10.tif')
in_band = in_ds.GetRasterBand(1)

# Get number of outputs rows and columns

out_rows = in_band.YSize * 2
out_columns = in_band.XSize * 2

# Creae output of data set

gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('band11_resampled.tif', out_columns, out_rows)

out_ds.SetProjection(in_ds.GetProjection())
geotransform = list(in_ds.GetGeoTransform())

# edit the geotransform so pixel are one-quarter previous size

geotransform [1] /= 2
geotransform [5] /= 2
out_ds.SetGeoTransform(geotransform)

# Specify a larger buffer size when reading data

data = in_band.ReadAsArray(buf_xsize=out_columns, buf_ysize=out_rows)
out_band = out_ds.GetRasterBand(1)
out_band.WriteArray(data)
out_band.FlushCache()
out_band.ComputeStatistics(False)
out_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64])

del out_ds