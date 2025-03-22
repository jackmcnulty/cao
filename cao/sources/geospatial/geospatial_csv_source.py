from cao.sources.base import BaseSource
from cao.registry import ConverterRegistry
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

class GeoCSVSource(BaseSource):
    def extract(self, path, options=None):
        options = options or {}
        print("[DEBUG] Options received in GeoCSVSource:", options)
        df = pd.read_csv(path)

        lat_col = options.get('lat_col')
        lon_col = options.get('lon_col')

        if not lat_col or not lon_col:
            raise ValueError("You must specify 'lat_col' and 'lon_col' options using -o lat_col=<latitude> -o lon_col=<longitude>.")
        
        if lat_col not in df.columns:
            raise ValueError(f"Column '{lat_col}' not found in CSV file.")
        if lon_col not in df.columns:
            raise ValueError(f"Column '{lon_col}' not found in CSV file.")

        geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        return {"type": "geodataframe", "data": gdf}

    @classmethod
    def supported_extensions(cls):
        return ["csv"]
    
    @classmethod
    def data_type(cls):
        return "geodataframe"

ConverterRegistry.register_source("csv", GeoCSVSource)
