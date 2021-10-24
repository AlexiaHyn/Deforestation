import ee
# Trigger the authentication flow.
ee.Authenticate()
ee.Initialize()
pt = ee.Geometry.Point([-2.40986111110000012, 26.76033333330000019])
region = pt.buffer(10)

col = ee.ImageCollection('LANDSAT/LC08/C01/T1')\
        .filterDate('2015-01-01','2015-04-30')\
        .filterBounds(region)

bands = ['B4','B5'] #Change it!

def accumulate(image,img):
    name_image = image.get('system:index')
    image = image.select([0],[name_image])
    cumm = ee.Image(img).addBands(image)
    return cumm

for band in bands:
    col_band = col.map(lambda img: img.select(band)\
                               .set('system:time_start', img.get('system:time_start'))\
                               .set('system:index', img.get('system:index')))
    #  ImageCollection to List
    col_list = col_band.toList(col_band.size())

    #  Define the initial value for iterate.
    base = ee.Image(col_list.get(0))
    base_name = base.get('system:index')
    base = base.select([0], [base_name])

    #  Eliminate the image 'base'.
    new_col = ee.ImageCollection(col_list.splice(0,1))

    img_cummulative = ee.Image(new_col.iterate(accumulate,base))

    task = ee.batch.Export.image.toDrive(
        image = img_cummulative.clip(region),
        folder = 'landsat',
        fileNamePrefix = band,
        scale = 30).start()

    print('Export Image '+ band+ ' was submitted, please wait ...')

img_cummulative.bandNames().getInfo()
