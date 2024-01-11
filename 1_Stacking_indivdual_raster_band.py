import os
from osgeo import gdal



os.chdir(r'C:\Users\Desktop\khn-ut\raster\data\osgeopy-data-landsat-washington\/'
         r'osgeopy-data\Landsat\Washington')

band1_fn = 'p047r027_7t20000730_z10_nn10.tif'
band2_fn = 'p047r027_7t20000730_z10_nn20.tif'
band3_fn = 'p047r027_7t20000730_z10_nn30.tif'

in_ds = gdal.Open(band1_fn)
in_band = in_ds.GetRasterBand(1)

gtiff_driver = gdal.GetDriverByName('GTiff')
# for another RasterDriver see this link: https://gdal.org/drivers/raster/index.html

out_ds = gtiff_driver.Create('nat_color11.tif', in_band.XSize, in_band.YSize, 3, in_band.DataType)

# in_ds.GetProjection(): Get Projection of data

out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())

# In a north up image, padfTransform[1] is the pixel width,
# and padfTransform[5] is the pixel height. The upper left
# corner of the upper left pixel is at position (padfTransform[0],padfTransform[3]).

in_data = in_band.ReadAsArray()

# in_band.ReadAsArray()
# in_band.ReadAsArray().size

out_band = out_ds.GetRasterBand(3)
out_band.WriteArray(in_data)



in_ds = gdal.Open(band2_fn)
out_band = out_ds.GetRasterBand(2)
out_band.WriteArray(in_ds.ReadAsArray())

out_ds.GetRasterBand(1).WriteArray(
gdal.Open(band3_fn).ReadAsArray())

# In the next bit of code, you compute statistics on each band in your dataset. This isn’t
# strictly necessary, but it makes it easier for some software to display it nicely.
# The statistics include mean, minimum, maximum, and standard deviation. A GIS can use this
# information to stretch the data on the screen and make it look better. You’ll see an
# example of how to stretch data manually in a later chapter.
# Before computing statistics, you have to ensure that the data have been written to disk instead of only cached
# in memory, so that’s what the call to FlushCache does. Then you loop through the
# bands and compute the statistics for each one. Passing False to this function tells it
# that you want actual statistics instead of estimates, which it might get from overview
# layers (which don’t exist yet) or from sampling a subset of the pixels. If an estimate is
# acceptable, then you can pass True instead

out_ds.FlushCache()
for i in range(1, 4):
    out_ds.GetRasterBand(i).ComputeStatistics(False)
out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])
del out_ds
print('ok')




