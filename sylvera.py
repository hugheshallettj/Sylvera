
import fiona
import rasterio
import rasterio.mask
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject, Resampling

import geopandas as gpd
import matplotlib


shape_file = "data/AOI/AOI.shp"

def save_and_clip_raster(year, shape_file):

    unclipped_filename = "data/{}.tif".format(year)

    # Read Shape file
    with fiona.open(shape_file, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    # read imagery file
    with rasterio.open(unclipped_filename) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    # Save clipped imagery
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open("clipped_rasters/{}.tif".format(year), "w", **out_meta) as dest:
        dest.write(out_image)
    pass
    


for year in range(2015,2021):
    
    imagery = rasterio.open("data/{}.tif".format(year))
    # show(imagery)
    save_and_clip_raster(year, shape_file)


# I only had time to do the first part of this question!