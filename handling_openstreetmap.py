import sys
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


# Equations References
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
# source = "http://www.4umaps.eu/{0}/{1}/{2}.png"
source_for_colap = "http://a.tile.openstreetmap.org/"
# source_colap = "http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
source_colap = "https://maps.wikimedia.org/osm-intl/{0}/{1}/{2}.png"          ## 이 스타일이 가장 네이버지도와 흡사            순위 1
# source_colap = "http://a.tile.openstreetmap.fr/hot/{0}/{1}/{2}.png"             ## 2번째로 흡사한 스타일                   순위 2
# source_colap = "http://a.tile.openstreetmap.fr/osmfr/{0}/{1}/{2}.png"           ## 스타일 별로
# source_colap = "http://toolserver.org/tiles/hikebike/{0}/{1}/{2}.png"             ## 2번째와 흡시하지만 좀 떨어지는 스타일        순위 3
# source_colap = "https://tiles.wmflabs.org/bw-mapnik/{0}/{1}/{2}.png"                 ## 흑백 스타일 (스타일만 흑백)
# source_colap = "https://tiles.wmflabs.org/osm-no-labels/{0}/{1}/{2}.png"                ## 칼라에 라벨없는 스타일
# source_colap = "http://a.tile.stamen.com/toner/{0}/{1}/{2}.png"                         ## 완전 흑백으로,,, 청사진느낌
# source_colap = "http://c.tile.stamen.com/watercolor/{0}/{1}/{2}.png"                         ## 파스텔톤 지도
# source_colap = "http://tile.thunderforest.com/transport/{0}/{1}/{2}.png"               ## 주요 도로를 부각해서 나타냄
# source_colap = "https://cartodb-basemaps-1.global.ssl.fastly.net/light_all/{0}/{1}/{2}.png"               ## 흑백이긴한데, 흐리멍텅한 지도 _ 명도만 낮춘느낌
                                                                                                            ## 주소중에 basemaps-1 은 서버를 말하는건데, 숫자부분에서 바꾸면 될듯
# source_colap = "https://cartodb-basemaps-1.global.ssl.fastly.net/dark_all/{0}/{1}/{2}.png"               ## 완전 흑색 지도

# 다양한 Map Style
# https://wiki.openstreetmap.org/wiki/Tile_servers
# 에서 확인


dest = os.getcwd()+'/cachemap'
tilestore = os.getcwd()+'/cachemap'
zoom = 12

e = 127.255
n = 37.665
s = 37.406
w = 127.014


if not os.path.exists(tilestore):
    os.makedirs(tilestore)

top_left = deg2num(n, w, zoom)
bottom_right = deg2num(s, e, zoom)

source_for_colap = "http://c.tile.openstreetmap.org/"+str(zoom)+"/"+str(top_left[0])+"/"+str(top_left[1])+".png"
print(top_left,bottom_right, zoom, source_colap)

# This is test for find start position(GPS) of each tiles
print(num2deg(top_left[0], top_left[1], zoom))
#  is 37.61423141542417, 127.001953125
# Original is
print(num2deg(bottom_right[0], bottom_right[1], zoom))



# create tile list
tiles = []
min_x_tile = top_left[0]
min_y_tile = top_left[1]
max_x_tile = bottom_right[0]
max_y_tile = bottom_right[1]


# 원래 소스에는 top_left[0] ~ bottom_right[0] 인데
# 실제 range 함수의 특성상, bottom_right 에 1을 더해서 range를 활용해야한다.
for x in range(top_left[0], bottom_right[0]+1):
    for y in range(top_left[1], bottom_right[1]+1):
        tiles.append((zoom, x, y))


print ('Nr tiles: ', len(tiles))
print("---------------")
print(min_x_tile, min_y_tile, max_x_tile,max_y_tile )
print("---------------")



# download tiles and make map

height = (bottom_right[1] - top_left[1]) * 256
width = (bottom_right[0] - top_left[0]) * 256
img = Image.new("RGB", (width, height))

for idx, tile in enumerate(tiles):

    zoom, x, y = tile
    fName = '_'.join([str(f) for f in tile]) + '.png'
    fName = os.path.join(tilestore, fName)

    f = urllib.request.urlopen(source_for_colap)
    # print(f.read())
    im = Image.open(BytesIO(f.read()))


    print
    '[%i/%i] %s' % (idx + 1, len(tiles), fName),
    if not os.path.exists(fName):
        url = source_colap.format(*tile)
        urllib.request.urlretrieve(url, fName)
        print(' ok')
    else:
        print(' cached')

    # paste
    tmp = Image.open(fName)
    img.paste(tmp, (256 * (x - top_left[0]), 256 * (y - top_left[1])))


try:
    img.save("img" + "ABC" + ".jpg")
except:
    print("Cached. So, No operations happened")
