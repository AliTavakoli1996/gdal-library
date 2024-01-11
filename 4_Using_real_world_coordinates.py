import os
from osgeo import gdal

# vashon_ulx, vashon_uly = 532000, 5262600
# vashon_lrx, vashon_lry = 548500, 5241500

os.chdir(r'C:\Users\Ali\Desktop\khn-ut\raster\data\nat')
in_ds = gdal.Open('nat_color.tif')
in_gt = in_ds.GetGeoTransform()
in_band = in_ds.GetRasterBand(1)

# 1 ==> Explain the following three functions:

## GetGeoTransform()
## InvGeoTransform()
## ApllyGeoTransform()

# 2

inv_gt = gdal.InvGeoTransform(in_gt)
offsets = gdal.ApplyGeoTransform(inv_gt, 465200, 5296000)
xoff, yoff = map(int, offsets)
value = in_band.ReadAsArray(xoff, yoff, 1, 1)[0,0]
value = in_band.ReadAsArray(xoff, yoff, 1, 1)

# 3

data = in_band.ReadAsArray()
x, y = map(int, gdal.ApplyGeoTransform(inv_gt, 465200, 5296000))
value = data[yoff, xoff]


