from seldon_core.user_model import SeldonComponent
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime


def coor_to_ID(coord):
    df = {"geometry": [Point(coord[1], coord[0])]}
    gdf = gpd.GeoDataFrame(df).set_crs("epsg:4326")

    # shp_path - shape file path
    shp_path = "taxi_zone/taxi_zones.shp"
    # file open
    nyc_shp = gpd.read_file(shp_path)
    nyc_shp["geometry"] = nyc_shp["geometry"].to_crs("epsg:4326")
    result_df = nyc_shp[nyc_shp.geometry.contains(gdf.geometry[0])]
    return result_df["LocationID"].item()


class InputTransformer(SeldonComponent):
    def __init__(self):
        super(InputTransformer, self).__init__()
        self.location_id_transformer = coor_to_ID

    def transform_input(self, input_data, features_names=None):
        x_0 = input_data[0]
        x_1 = input_data[1]
        x_2 = coor_to_ID(input_data[2])
        x_3 = coor_to_ID(input_data[3])
        x_4 = input_data[4]
        input_time = input_data[5]
        D = datetime.strptime(input_time, "%Y-%m-%dT%H:%M")
        if (D.weekday() + 2) % 7 == 0:
            x_5 = 1
        else:
            x_5 = D.weekday() + 2
        x_6 = D.hour
        x_7 = D.minute
        x_8 = input_data[6]
        return np.array([[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8]])
