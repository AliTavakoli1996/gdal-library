from osgeo import gdal
import glob, os, math

def get_extent(fn):
    '''Returns min_x, max_y, max_x, min_y'''
    ds = gdal.Open(fn)
    gt = ds.GetGeoTransform()
    return (gt[0], gt[3], gt[0] + gt[1] * ds.RasterXSize, gt[3] + gt[5] * ds.RasterYSize)

os.chdir(r'C:\Users\Ali\Desktop\khn-ut\raster\data\Massachusetts')
# read all files in one list
in_files = glob.glob('O*.tif')

# calculate output extent from all inputs

min_x, max_y, max_x, min_y = get_extent(in_files[0])
for fn in in_files[1:]:
    minx, maxy, maxx, miny = get_extent(fn)
    min_x = min(min_x, minx)
    max_y = max(max_y, maxy)
    max_x = max(max_x, maxx)
    min_y = min(min_y, miny)

# calculate of dimension output image

in_ds = gdal.Open(in_files[0])
gt = in_ds.GetGeoTransform()
rows = math.ceil((max_y - min_y) / -gt[5])
columns = math.ceil((max_x - min_x) / gt[1])

# Create output

driver = gdal.GetDriverByName('gtiff')
out_ds = driver.Create('mosaic1.tif', columns, rows)
out_ds.SetProjection(in_ds.GetProjection())
out_band = out_ds.GetRasterBand(1)


# calculate new geo-transform

gt = list(in_ds.GetGeoTransform())
gt[0], gt[3] = min_x, max_y
out_ds.SetGeoTransform(gt)

for fn in in_files:
    in_ds = gdal.Open(fn)
    trans = gdal.Transformer(in_ds, out_ds, [])
    success, xyz = trans.TransformPoint(False, 0, 0)
    '''
    TransformPoint(bDstToSrc, x, y, [z])
    ■ bDstToSrc is a flag specifying if you want to compute offsets from the destination raster 
    to the source raster or vice versa. Use True to go from the destination to the source and False 
    to go the other way.
    ■ x, y, and z are the coordinates or offsets that you want to transform. z is optional and
    defaults to 0.
    '''

    x, y, z = map(int, xyz)
    data = in_ds.GetRasterBand(1).ReadAsArray()
    out_band.WriteArray(data, x, y)

del in_ds, out_band, out_ds
