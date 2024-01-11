import os
from osgeo import gdal

vashon_ulx, vashon_uly = 532000, 5262600
vashon_lrx, vashon_lry = 548500, 5241500

os.chdir(r'C:\Users\Ali\Desktop\khn-ut\raster\data\nat')
in_ds = gdal.Open('nat_color.tif')
in_gt = in_ds.GetGeoTransform()
inv_gt = gdal.InvGeoTransform(in_gt)

# calculate upper-left and lower right offset in two next line:

offsets_ul = gdal.ApplyGeoTransform(inv_gt, vashon_ulx, vashon_uly)
offsets_lr = gdal.ApplyGeoTransform(inv_gt, vashon_lrx, vashon_lry)
off_ulx, off_uly = map(int, offsets_ul)
off_lrx, off_lry = map(int, offsets_lr)

# compute number of rows and columns to extract:
rows = off_lry - off_uly
columns = off_lrx - off_ulx

gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('vashon2.tif', columns, rows, 3)
out_ds.SetProjection(in_ds.GetProjection())

# Put new origin coordinates in geo-transform

subset_ulx, subset_uly = gdal.ApplyGeoTransform(in_gt, off_ulx, off_uly)
out_gt = list(in_gt)
out_gt[0] = subset_ulx
out_gt[3] = subset_uly
out_ds.SetGeoTransform(out_gt)

# read in data using computed values

for i in range(1, 4):
    in_band = in_ds.GetRasterBand(i)
    out_band = out_ds.GetRasterBand(i)
    data = in_band.ReadAsArray(off_ulx, off_uly, columns, rows)
    out_band.WriteArray(data)

del out_ds

