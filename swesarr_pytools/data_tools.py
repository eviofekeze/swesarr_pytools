"""
This Data processing module has the following functionality
1. Class to read a swesarr
2. Class to read Lidar
3. Function to reproject Swesarr and lidar
4. Function to combine swesarr fall , swesarr fall winter and lidar into one dataframe
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

try:
    from .utils.helper import join_files, gdal_corners
    from .utils.swesarr_utils import get_logger
except ImportError:
    from utils.helper import join_files, gdal_corners
    from utils.swesarr_utils import get_logger



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

        data_files_list = None
        if Path(self.flight_path).is_dir():
            temp_list = [file for file in os.listdir(self.flight_path) if file.endswith(".tif")]

            if self.band.lower() == "x":
                data_files_list = [item for item in temp_list if ("09225" in item) or
                                   ("XVV" in item) or ("XVH" in item)]
            elif self.band.lower() == "kulo":
                data_files_list = [item for item in temp_list if ("13225" in item) or
                                   ("Kl" in item) or ("XVVI" in item) or ("XVVO" in item)]
            elif self.band.lower() == "kuhi":
                data_files_list = [item for item in temp_list if ("17225" in item) or
                                   ("Kh" in item) or ("XVVI" in item) or ("XVVO" in item)]
            else:
                data_files_list = temp_list
        else:
            logger.info(f"Single band case")

        return data_files_list


    def get_swesarr_raster(self):

        if Path(self.flight_path).is_dir():
            data_file_list = self.get_data_files()
            path_list = [f"{self.flight_path}/{file}" for file in data_file_list]
            current_swesarr = join_files(file_list=path_list, version=self.version)
        elif Path(self.flight_path).is_file():
            current_swesarr = join_files(file_list=[self.flight_path], version=self.version)
        else:
            raise Exception(f"Please specify path to directory or single file")
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

        if self.version == "v1":
            df = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="09VV")
            df = df.assign(C09VH=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="09VH")['C09VH'])
            df = df.assign(C13VV=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="13VV")['C13VV'])
            df = df.assign(C13VH=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="13VH")['C13VH'])
            df = df.assign(C17VV=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="17VV")['C17VV'])
            df = df.assign(C17VH=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="17VH")['C17VH'])
        else:
            df = self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="XVV")
            df = df.rename(columns={"VVV": "CXVV"})
            df = df.assign(C09VH=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="XVH")['C09VH'])
            df = df.assign(C13VV=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="KlVV")['C13VV'])
            df = df.assign(C13VH=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="KlVH")['C13VH'])
            df = df.assign(C17VV=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="KhVV")['C17VV'])
            df = df.assign(C17VH=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="KhVH")['C17VH'])
            df = df.assign(CINC=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="XVVINC")['CINC'])
            df = df.assign(COFNA=self.single_band_to_dataframe(swesarr_raster=current_swesarr, band="XVVOFNA")['COFNA'])


        del current_swesarr

        if self.season.lower() == 'fall':
            df.rename(columns={'C09VV': 'F09VV', 'C09VH': 'F09VH', 'C13VV': 'F13VV', 'C13VH': 'F13VH',
                               'C17VV': 'F17VV', 'C17VH': 'F17VH', 'CXVVINC': 'FINC', 'CXVVOFNA': 'FOFNA'},
                      inplace=True)
        elif self.season.lower() == 'winter':
            df.rename(columns={'CXVV': 'W09VV','C09VH': 'W09VH','C13VV': 'W13VV','C13VH': 'W13VH',
                               'C17VV': 'W17VV', 'C17VH': 'W17VH', 'CXVVINC': 'WINC','CXVVOFNA': 'WOFNA'},
                      inplace=True)
        else:
            raise Exception (f"Invalid Version: Supported Version is either of 'v1' or 'v3'")


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
        """
        retrieves Lidar raster as an Xarray Dataset
        :return:
        """

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
        """
        Convert lidar to dataframe
        :return: pd.DataFrame
        """
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

    def single_band_to_df_reproject(self, band_name: str , df_col_name: str) -> pd.DataFrame:
        """
        :param band_name: band name raster values
        :param df_col_name: names to assign the band in the dataframe
        :return: (pd.DataFrame) A dataframe of the converted frequency
        """
        swesarr_raster_data = self.swesarr_raster.sel(band=band_name)
        lidar_swesarr_data = swesarr_raster_data.rio.reproject_match(self.lidar_raster)
        lidar_swesarr_data_df = lidar_swesarr_data.squeeze().drop_vars(["spatial_ref", "band"])
        lidar_swesarr_data_dataframe = lidar_swesarr_data_df.to_dataframe(
            name=f"{self.season[0].upper()}{df_col_name}").reset_index()
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
            self.lidar_swesarr_data_09vv_dataFrame = self.single_band_to_df_reproject(band_name='XVV', df_col_name="09VV")
            self.lidar_swesarr_data_09vh_dataFrame = self.single_band_to_df_reproject(band_name='XVH', df_col_name="09VH")
            self.lidar_swesarr_data_13vv_dataFrame = self.single_band_to_df_reproject(band_name='KlVV', df_col_name="13VV")
            self.lidar_swesarr_data_13vh_dataFrame = self.single_band_to_df_reproject(band_name='KlVH', df_col_name="13VH")
            self.lidar_swesarr_data_17vv_dataFrame = self.single_band_to_df_reproject(band_name='KhVV', df_col_name="17VV")
            self.lidar_swesarr_data_17vh_dataFrame = self.single_band_to_df_reproject(band_name='KhVH', df_col_name="17VH")

            if self.flag:
                self.lidar_swesarr_data_inc_dataFrame = self.single_band_to_df_reproject(band_name='XVVINC', df_col_name="INC")
                self.lidar_swesarr_data_ofna_dataFrame = self.single_band_to_df_reproject(band_name='XVVOFNA', df_col_name="OFNA")
        except KeyError:
            self.lidar_swesarr_data_09vv_dataFrame = self.single_band_to_df_reproject(band_name='09VV', df_col_name="09VV")
            self.lidar_swesarr_data_09vh_dataFrame = self.single_band_to_df_reproject(band_name='09VH', df_col_name="09VH")
            self.lidar_swesarr_data_13vv_dataFrame = self.single_band_to_df_reproject(band_name='13VV', df_col_name="13VV")
            self.lidar_swesarr_data_13vh_dataFrame = self.single_band_to_df_reproject(band_name='13VH', df_col_name="13VH")
            self.lidar_swesarr_data_17vv_dataFrame = self.single_band_to_df_reproject(band_name='17VV', df_col_name="17VV")
            self.lidar_swesarr_data_17vh_dataFrame = self.single_band_to_df_reproject(band_name='17VH', df_col_name="17VH")



def combine_swesarr_lidar(fall_flight_directory: str,
                          winter_flight_directory: str,
                          lidar_flight_path: str,
                          drop_na: bool = True,
                          version:str  = "v1") -> pd.DataFrame:
    """
    :param fall_flight_directory: (str) Path to the folder containing fall flights to be reprojected and combined.
    :param winter_flight_directory: (str) Path to the folder containing winter flights to be reprojected and combined.
    :param lidar_flight_path: (str) Path to the lidar files to be reprojected and combined.
    :param drop_na: (bool, optional) A flag indicating whether to drop rows containing NaN values after
                    combining rasters (default is True).
    :param version:
    :return: (pd.DataFrame) A DataFrame containing the combined raster data with reprojected coordinates.
            Rows containing NaN values will be dropped if `drop_na` is set to True.
    """

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


    df = fall_projected_object.lidar_swesarr_data_09vv_dataFrame
    df = df.assign(F09VH=fall_projected_object.lidar_swesarr_data_09vh_dataFrame['F09VH'])
    df = df.assign(F13VV=fall_projected_object.lidar_swesarr_data_13vv_dataFrame['F13VV'])
    df = df.assign(F13VH=fall_projected_object.lidar_swesarr_data_13vh_dataFrame['F13VH'])
    df = df.assign(F17VV=fall_projected_object.lidar_swesarr_data_17vv_dataFrame['F17VV'])
    df = df.assign(F17VH=fall_projected_object.lidar_swesarr_data_17vh_dataFrame['F17VH'])
    if fall_projected_object.flag:
        df = df.assign(FINC=fall_projected_object.lidar_swesarr_data_inc_dataFrame['FINC'])
        df = df.assign(FOFNA=fall_projected_object.lidar_swesarr_data_ofna_dataFrame['FOFNA'])

    df = df.assign(W09VV=winter_projected_object.lidar_swesarr_data_09vv_dataFrame['W09VV'])
    df = df.assign(W09VH=winter_projected_object.lidar_swesarr_data_09vh_dataFrame['W09VH'])
    df = df.assign(W13VV=winter_projected_object.lidar_swesarr_data_13vv_dataFrame['W13VV'])
    df = df.assign(W13VH=winter_projected_object.lidar_swesarr_data_13vh_dataFrame['W13VH'])
    df = df.assign(W17VV=winter_projected_object.lidar_swesarr_data_17vv_dataFrame['W17VV'])
    df = df.assign(W17VH=winter_projected_object.lidar_swesarr_data_17vh_dataFrame['W17VH'])
    if winter_projected_object.flag:
        df = df.assign(WINC=winter_projected_object.lidar_swesarr_data_inc_dataFrame['WINC'])
        df = df.assign(WOFNA=winter_projected_object.lidar_swesarr_data_ofna_dataFrame['WOFNA'])


    threshold = 0 if version == "v3" else 2
    df.loc[df['F09VV'] >= threshold, 'F09VV'] = np.nan
    df.loc[df['F09VH'] >= threshold, 'F09VH'] = np.nan
    df.loc[df['F13VV'] >= threshold, 'F13VV'] = np.nan
    df.loc[df['F13VH'] >= threshold, 'F13VH'] = np.nan
    df.loc[df['F17VV'] >= threshold, 'F17VV'] = np.nan
    df.loc[df['F17VH'] >= threshold, 'F17VH'] = np.nan
    df.loc[df['W09VV'] >= threshold, 'W09VV'] = np.nan
    df.loc[df['W09VH'] >= threshold, 'W09VH'] = np.nan
    df.loc[df['W13VV'] >= threshold, 'W13VV'] = np.nan
    df.loc[df['W13VH'] >= threshold, 'W13VH'] = np.nan
    df.loc[df['W17VV'] >= threshold, 'W17VV'] = np.nan
    df.loc[df['W17VH'] >= threshold, 'W17VH'] = np.nan

    df = df.assign(Depth=lidar_object_df['Depth'])

    df = df.dropna() if drop_na else df
    return df


if __name__ == "__main__":
    logger.info(f"Nothing to report... Moving on")
