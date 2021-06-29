"""
Postprocessing module that morphs the data structures in convenient ways
"""

import xarray as xr


def combine_hindcast_forecast(hindcast, forecast, propagate_nans=True):
    """
    Combine the hindcast and forecast datasets into a single xarray.Dataset
    """
    nan_mask = 1
    if propagate_nans:
        hindcast_mask = hindcast.isel(time=0, drop=True).notnull()
        forecast_mask = forecast.isel(time=0, drop=True).notnull()
        nan_mask = hindcast_mask * forecast_mask
    merged = xr.concat([hindcast, forecast], dim="time", join="left").where(nan_mask)
    return merged


def mask_data(ds, mask_mapping):
    """
    Mask data values according to the mask_mapping parameter
    """
    for var, missing_value in mask_mapping.items():
        ds[var] = ds[var].where(ds[var] != missing_value)
    return ds
