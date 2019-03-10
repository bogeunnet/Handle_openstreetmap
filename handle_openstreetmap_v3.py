import os
import math
from PIL import Image
import urllib.request
from io import BytesIO

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def get_map(east, west, north, south, zoom):
    # Equations References
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    source_for_colap = "http://a.tile.openstreetmap.org/"
    source_colap = "https://maps.wikimedia.org/osm-intl/{0}/{1}/{2}.png"  ## 이 스타일이 가장 네이버지도와 흡사

    tilestore = os.getcwd() + '/cachemap'


    if not os.path.exists(tilestore):
        os.makedirs(tilestore)

    top_left = deg2num(north, west, zoom)
    bottom_right = deg2num(south, east, zoom)

    source_for_colap = "http://c.tile.openstreetmap.org/" + str(zoom) + "/" + str(top_left[0]) + "/" + str(
        top_left[1]) + ".png"

    y_zero_ul = num2deg(top_left[0], top_left[1], zoom)[0]
    x_zero_ul = num2deg(top_left[0], top_left[1], zoom)[1]
    y_zero_br = num2deg(bottom_right[0], bottom_right[1], zoom)[0]
    x_zero_br = num2deg(bottom_right[0], bottom_right[1], zoom)[1]

    # create tile list
    tiles = []

    # 원래 소스에는 top_left[0] ~ bottom_right[0] 인데
    # 실제 range 함수의 특성상, bottom_right 에 1을 더해서 range를 활용해야한다.
    for x in range(top_left[0], bottom_right[0] + 1):
        for y in range(top_left[1], bottom_right[1] + 1):
            tiles.append((zoom, x, y))

    # download tiles and make map

    height = (bottom_right[1] - top_left[1]) * 256
    width = (bottom_right[0] - top_left[0]) * 256
    img = Image.new("RGB", (width, height))

    for idx, tile in enumerate(tiles):

        zoom, x, y = tile
        fName = '_'.join([str(f) for f in tile]) + '.png'
        fName = os.path.join(tilestore, fName)

        f = urllib.request.urlopen(source_for_colap)
        im = Image.open(BytesIO(f.read()))

        print
        '[%i/%i] %s' % (idx + 1, len(tiles), fName),
        if not os.path.exists(fName):
            url = source_colap.format(*tile)
            urllib.request.urlretrieve(url, fName)
            print(' ok')
        else:
            print(' cached')
        print(fName)

        # paste
        tmp = Image.open(fName)
        img.paste(tmp, (256 * (x - top_left[0]), 256 * (y - top_left[1])))

    try:
        img.save("img" + "ABC" + ".jpg")
    except:
        print("Cached. So, No operations happened")

    return x_zero_ul, y_zero_ul,x_zero_br, y_zero_br

east = 126.954
west = 127.105
north = 37.505
south = 37.406

xyzero = get_map(west,east,north,south, 13)

x_zero_ul = xyzero[0]
y_zero_ul = xyzero[1]
x_zero_br = xyzero[2]
y_zero_br = xyzero[3]

print(str(x_zero_ul), str(y_zero_ul))
print(str(x_zero_ul-west), str(y_zero_ul-north))

print(str(x_zero_br), str(y_zero_br))
print(str(x_zero_ul-east), str(y_zero_ul-south))
