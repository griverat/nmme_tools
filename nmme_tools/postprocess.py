import xarray as xr


def combine_hindcast_forecast(hindcast, forecast, propagate_nans=True):
    nan_mask = 1
    if propagate_nans:
        hindcast_mask = hindcast.isel(time=0, drop=True).isnull()
        forecast_mask = forecast.isel(time=0, drop=True).isnull()
        nan_mask = hindcast_mask * forecast_mask
    merged = xr.concat([hindcast, forecast], dim="time", join="left").where(~nan_mask)
    return merged