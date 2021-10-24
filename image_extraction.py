import ee;

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()


def exportImages(lon, lat, buffer):
    landset8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    landset8.filterDate('2021-08-01', '2021-10-12')

    pt = ee.Geometry.Point([lon, lat])
    buff = pt.buffer(buffer)

    landset8_comb = landset8.median()
    landset8_img = landset8_comb.updateMask(landset8_comb.gt(0))

    task = ee.batch.Export.image.toDrive(
        image=landset8_comb,
        description="test_image",
        folder='example_folder',
        fileNamePrefix="image0",
        scale=30,
        region=buff,
        crs='EPSG:4326',
        fileFormat='GeoTIFF')

    task.start();


lon = 1.4811
lat = 6.0954
buffer = 3000
exportImages(lon, lat, buffer)