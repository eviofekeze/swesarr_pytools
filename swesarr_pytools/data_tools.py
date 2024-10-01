"""
This main class has the following functionality
1. Data retrieval for SWESARR flight from https://glihtdata.gsfc.nasa.gov/files/radar/SWESARR/prerelease
2. Metadata retrieval for SWESARR flight path
3. Singular Flight path download for one flight line but six frequencies
4. Singular frequency download for a given flight line
5. Flight path search using date
"""

__author__ = "Evi Ofekeze"
__authors__ = ["HP Marshal"]
__contact__ = "eviofekeze@u.boisestate.edu"
__copyright__ = "Copyright 2024, Boise State University, Boise ID"
__group__ = "Cryosphere GeoPhysics and Remote Sensing Laboratory"
__credits__ = ["Evi Ofekeze", "HP Marshal"]
__email__ = "eviofekeze@u.boisestate.edu"
__maintainer__ = "developer"
__status__ = "Research"

import os
from pathlib import Path

from dataclasses import dataclass
from typing import List, Any

import numpy as np
import pandas as pd
import rioxarray

from .utils.helper import join_files, gdal_corners
from .utils.swesarr_utils import get_logger
logger = get_logger(__file__)

@dataclass
class ReadSwesarr:
    flight_path: str
    version: str = "v1"
    band: str = "all"
    season: str = "Fall"
    dataframe: bool = True
    raster: bool = True
    drop_na: bool = True


    def get_data_files(self) -> List:


        if Path(self.flight_path).is_dir():
            temp_list = [file for file in os.listdir(self.flight_path) if file.endswith(".tif")]

            if self.band.lower() == "x":
                data_files_list = [item for item in temp_list if "09225" in item]
            elif self.band.lower() == "kulo":
                data_files_list = [item for item in temp_list if "13225" in item]
            elif self.band.lower() == "kuhi":
                data_files_list = [item for item in temp_list if "17225" in item]
            else:
                data_files_list = temp_list
        else:
            data_files_list = None
            logger.info(f"Single band case")

        del temp_list
        return data_files_list


    def get_swesarr_raster(self):

        if Path(self.flight_path).is_dir():
            data_file_list = self.get_data_files()
            path_list = [f"{self.flight_path}/{file}" for file in data_file_list]
            current_swesarr = join_files(file_list=path_list, version=self.version)
        elif Path(self.flight_path).is_file():
            current_swesarr = join_files(file_list=[self.flight_path], version=self.version)
        return current_swesarr

    @staticmethod
    def single_band_to_dataframe(swesarr_raster,band):
        current_swesarr_band = swesarr_raster.sel(band=band)
        current_swesarr_band_df = current_swesarr_band.squeeze().drop_vars(["spatial_ref", "band"])
        current_swesarr_band_dataframe = current_swesarr_band_df.to_dataframe(name=f"C{band}").reset_index()
        del current_swesarr_band_df, current_swesarr_band
        return current_swesarr_band_dataframe

    def get_swesarr_df(self) -> pd.DataFrame:
        current_swesarr = self.get_swesarr_raster()

        current_swesarr_09vv_dataframe = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="09VV")
        current_swesarr_09vh_dataframe = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="09VH")
        current_swesarr_13vh_dataframe = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="13VH")
        current_swesarr_13vv_dataframe = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="13VV")
        current_swesarr_17vv_dataframe = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="17VV")
        current_swesarr_17vh_dataframe = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="17VH")

        del current_swesarr

        df = current_swesarr_09vv_dataframe
        df = df.assign(C09VH=current_swesarr_09vh_dataframe['C09VH'])
        df = df.assign(C13VV=current_swesarr_13vv_dataframe['C13VV'])
        df = df.assign(C13VH=current_swesarr_13vh_dataframe['C13VH'])
        df = df.assign(C17VV=current_swesarr_17vv_dataframe['C17VV'])
        df = df.assign(C17VH=current_swesarr_17vh_dataframe['C17VH'])

        del current_swesarr_09vv_dataframe, current_swesarr_09vh_dataframe, current_swesarr_13vv_dataframe
        del current_swesarr_13vh_dataframe, current_swesarr_17vv_dataframe, current_swesarr_17vh_dataframe

        if self.season == 'Fall':
            df.columns = ['y', 'x', 'F09VV', 'F09VH', 'F13VV', 'F13VH', 'F17VV', 'F17VH']
        elif self.season == 'Winter':
            df.columns = ['y', 'x', 'W09VV', 'W09VH', 'W13VV', 'W13VH', 'W17VV', 'W17VH']

        df = df.dropna() if self.drop_na else df

        return df


@dataclass()
class ReadLidar:
    lidar_path: str
    swesarr_flight_path: str = None
    drop_na: bool = False
    lidar_name: str = "Depth"
    crs = 4326


    def get_lidar_raster(self):

        data_array_3m = rioxarray.open_rasterio(self.lidar_path)
        if self.swesarr_flight_path is not None:
            minx, miny, maxx, maxy = gdal_corners(Path(self.swesarr_flight_path))
            clipping_geometry = [{
                'type': 'Polygon',
                'coordinates': [
                    [[minx, maxy],
                     [maxx, maxy],
                     [maxx, miny],
                     [minx, miny]]
                ]}]
            try:
                data_array_3m = data_array_3m.rio.clip(clipping_geometry, crs=self.crs)
            except Exception as e:
                data_array_3m = data_array_3m.rio.clip(clipping_geometry)


        return data_array_3m

    def get_lidar_df(self) -> pd.DataFrame:
        data_array_3m = self.get_lidar_raster()
        lidar_df = data_array_3m.squeeze().drop_vars(["spatial_ref", "band"])
        lidar_df.name = self.lidar_name
        lidar_dataframe = lidar_df.to_dataframe().reset_index()

        if self.lidar_name.lower() == "depth":
            lidar_dataframe.loc[lidar_dataframe['Depth'] >= 2, 'Depth'] = np.nan
            lidar_dataframe.loc[lidar_dataframe['Depth'] == 0, 'Depth'] = np.nan

        lidar_dataframe = lidar_dataframe.dropna() if self.drop_na else lidar_dataframe
        return lidar_dataframe

@dataclass
class SwesarrLidarProjection:
    swesarr_raster: Any
    lidar_raster: Any
    season: str

    def single_band_to_dataframe(self, band_name: str , df_col_name: str) -> pd.DataFrame:
        swesarr_raster_data = self.swesarr_raster.sel(band=band_name)
        lidar_swesarr_data = swesarr_raster_data.rio.reproject_match(self.lidar_raster)
        lidar_swesarr_data_df = lidar_swesarr_data.squeeze().drop_vars(["spatial_ref", "band"])
        lidar_swesarr_data_dataframe = lidar_swesarr_data_df.to_dataframe(
            name=f"{self.season[0]}{df_col_name}").reset_index()
        lidar_swesarr_data_dataframe.replace(-np.inf, np.nan, inplace=True)
        return lidar_swesarr_data_dataframe

    def __post_init__(self):

        # Check Version
        try:
            self.swesarr_raster.sel(band='XVVINC')
            self.flag = True
        except KeyError:
            self.flag = False

        try:
            self.lidar_swesarr_data_09vv_dataFrame = self.single_band_to_dataframe(band_name='XVV', df_col_name="09VV")
            self.lidar_swesarr_data_09vh_dataFrame = self.single_band_to_dataframe(band_name='XVH', df_col_name="09VH")
            self.lidar_swesarr_data_13vv_dataFrame = self.single_band_to_dataframe(band_name='KlVV', df_col_name="13VV")
            self.lidar_swesarr_data_13vh_dataFrame = self.single_band_to_dataframe(band_name='KlVH', df_col_name="13VH")
            self.lidar_swesarr_data_17vv_dataFrame = self.single_band_to_dataframe(band_name='KhVV', df_col_name="17VV")
            self.lidar_swesarr_data_17vh_dataFrame = self.single_band_to_dataframe(band_name='KhVH', df_col_name="17VH")

            if self.flag:
                self.lidar_swesarr_data_inc_dataFrame = self.single_band_to_dataframe(band_name='XVVINC', df_col_name="INC")
                self.lidar_swesarr_data_ofna_dataFrame = self.single_band_to_dataframe(band_name='XVVOFNA', df_col_name="OFNA")
        except KeyError:
            self.lidar_swesarr_data_09vv_dataFrame = self.single_band_to_dataframe(band_name='09VV', df_col_name="09VV")
            self.lidar_swesarr_data_09vh_dataFrame = self.single_band_to_dataframe(band_name='09VH', df_col_name="09VH")
            self.lidar_swesarr_data_13vv_dataFrame = self.single_band_to_dataframe(band_name='13VV', df_col_name="13VV")
            self.lidar_swesarr_data_13vh_dataFrame = self.single_band_to_dataframe(band_name='13VH', df_col_name="13VH")
            self.lidar_swesarr_data_17vv_dataFrame = self.single_band_to_dataframe(band_name='17VV', df_col_name="17VV")
            self.lidar_swesarr_data_17vh_dataFrame = self.single_band_to_dataframe(band_name='17VH', df_col_name="17VH")



def combine_swesarr_lidar(fall_flight_directory: str,
                          winter_flight_directory: str,
                          lidar_flight_path: str,
                          drop_na: bool = True,
                          version:str  = "v1") -> pd.DataFrame:


    fall_swesarr_object = ReadSwesarr(flight_path=fall_flight_directory,
                                      season="Fall", drop_na=False, version=version)
    fall_swesarr = fall_swesarr_object.get_swesarr_raster()

    winter_swesarr_object = ReadSwesarr(flight_path=winter_flight_directory,
                                        season="Winter", drop_na=False, version=version)
    winter_swesarr = winter_swesarr_object.get_swesarr_raster()

    f_name = winter_swesarr_object.get_data_files()[0]
    lidar_object = ReadLidar(lidar_path=lidar_flight_path, swesarr_flight_path=f"{winter_flight_directory}/{f_name}")
    this_lidar_raster = lidar_object.get_lidar_raster()
    lidar_object_df = lidar_object.get_lidar_df()

    fall_projected_object = SwesarrLidarProjection(swesarr_raster=fall_swesarr,
                                                   lidar_raster=this_lidar_raster,
                                                   season="Fall")

    winter_projected_object = SwesarrLidarProjection(swesarr_raster=winter_swesarr,
                                                   lidar_raster=this_lidar_raster,
                                                   season="Winter")

    fall_lidar_swesarr_data_09vv_dataframe = fall_projected_object.lidar_swesarr_data_09vv_dataFrame
    fall_lidar_swesarr_data_09vh_dataframe = fall_projected_object.lidar_swesarr_data_09vh_dataFrame
    fall_lidar_swesarr_data_13vv_dataframe = fall_projected_object.lidar_swesarr_data_13vv_dataFrame
    fall_lidar_swesarr_data_13vh_dataframe = fall_projected_object.lidar_swesarr_data_13vh_dataFrame
    fall_lidar_swesarr_data_17vv_dataframe = fall_projected_object.lidar_swesarr_data_17vv_dataFrame
    fall_lidar_swesarr_data_17vh_dataframe = fall_projected_object.lidar_swesarr_data_17vh_dataFrame
    if fall_projected_object.flag:
        fall_lidar_swesarr_data_inc_dataframe = fall_projected_object.lidar_swesarr_data_inc_dataFrame
        fall_lidar_swesarr_data_ofna_dataframe = fall_projected_object.lidar_swesarr_data_ofna_dataFrame

    winter_lidar_swesarr_data_09vv_dataframe = winter_projected_object.lidar_swesarr_data_09vv_dataFrame
    winter_lidar_swesarr_data_09vh_dataframe = winter_projected_object.lidar_swesarr_data_09vh_dataFrame
    winter_lidar_swesarr_data_13vv_dataframe = winter_projected_object.lidar_swesarr_data_13vv_dataFrame
    winter_lidar_swesarr_data_13vh_dataframe = winter_projected_object.lidar_swesarr_data_13vh_dataFrame
    winter_lidar_swesarr_data_17vv_dataframe = winter_projected_object.lidar_swesarr_data_17vv_dataFrame
    winter_lidar_swesarr_data_17vh_dataframe = winter_projected_object.lidar_swesarr_data_17vh_dataFrame
    if winter_projected_object.flag:
        winter_lidar_swesarr_data_inc_dataframe = winter_projected_object.lidar_swesarr_data_inc_dataFrame
        winter_lidar_swesarr_data_ofna_dataframe = winter_projected_object.lidar_swesarr_data_ofna_dataFrame

    df = fall_lidar_swesarr_data_09vv_dataframe

    df = df.assign(F09VH=fall_lidar_swesarr_data_09vh_dataframe['F09VH'])
    df = df.assign(F13VV=fall_lidar_swesarr_data_13vv_dataframe['F13VV'])
    df = df.assign(F13VH=fall_lidar_swesarr_data_13vh_dataframe['F13VH'])
    df = df.assign(F17VV=fall_lidar_swesarr_data_17vv_dataframe['F17VV'])
    df = df.assign(F17VH=fall_lidar_swesarr_data_17vh_dataframe['F17VH'])
    if fall_projected_object.flag:
        df = df.assign(FINC=fall_lidar_swesarr_data_inc_dataframe['FINC'])
        df = df.assign(FOFNA=fall_lidar_swesarr_data_ofna_dataframe['FOFNA'])

    df = df.assign(W09VV=winter_lidar_swesarr_data_09vv_dataframe['W09VV'])
    df = df.assign(W09VH=winter_lidar_swesarr_data_09vh_dataframe['W09VH'])
    df = df.assign(W13VV=winter_lidar_swesarr_data_13vv_dataframe['W13VV'])
    df = df.assign(W13VH=winter_lidar_swesarr_data_13vh_dataframe['W13VH'])
    df = df.assign(W17VV=winter_lidar_swesarr_data_17vv_dataframe['W17VV'])
    df = df.assign(W17VH=winter_lidar_swesarr_data_17vh_dataframe['W17VH'])
    if winter_projected_object.flag:
        df = df.assign(WINC=winter_lidar_swesarr_data_inc_dataframe['WINC'])
        df = df.assign(WOFNA=winter_lidar_swesarr_data_ofna_dataframe['WOFNA'])

    df = df.assign(Depth=lidar_object_df['Depth'])

    df = df.dropna() if drop_na else df
    return df


if __name__ == "__main__":
    logger.info(f"Nothing to report... Moving on")
