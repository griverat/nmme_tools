"""
Postprocessing module that morphs the data structures in convenient ways
"""

import datetime

import dask
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
    with dask.config.set({"array.slicing.split_large_chunks": False}):
        _res = hindcast.combine_first(forecast).where(nan_mask)
    return _res


def mask_data(ds, mask_mapping):
    """
    Mask data values according to the mask_mapping parameter
    """
    for var, missing_value in mask_mapping.items():
        ds[var] = ds[var].where(ds[var] != missing_value)
    return ds


def shift_leads(ds):
    """
    Shift the time dimension according to the lead values
    """
    new_ds = []
    for lead in ds.lead:
        _ds = ds.sel(lead=lead)
        _ds["time"] = _ds["time"] + datetime.timedelta(days=int(30 * _ds.lead.data))
        new_ds.append(_ds)
    return xr.concat(new_ds, dim="lead")
