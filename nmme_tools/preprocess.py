"""
Preprocess module with utilities that aim to uniformize the
naming convention and some other dimension/coordinate operations.

Does not modify the underlying data
"""
import numpy as np
import xarray as xr


def rename_dims(ds):
    """
    Rename dataset dimensions with a more explicit naming scheme
    """
    dims_mapping = {"L": "lead", "Y": "lat", "X": "lon", "M": "member", "S": "time"}
    return ds.rename({k: v for k, v in dims_mapping.items() if k in ds.variables})


def fix_time(ds):
    """
    Fix non-standard calendar to work with cftime
    """
    ds["time"].attrs["calendar"] = "360_day"
    return xr.decode_cf(ds)


def coords_to_int(ds, coords):
    """
    Cast the coordinates to integer values
    """
    coords = [coords] if not isinstance(coords, list) else coords
    for coord in coords:
        _coord_attrs = ds[coord].attrs
        ds[coord] = np.int32(ds[coord])
        ds[coord].attrs = _coord_attrs
    return ds


def capitalize_names(ds):
    """
    Capitalize the 'long_name' attribute for plotting purposes
    """
    for var in ds.variables.values():
        if "long_name" in var.attrs:
            var.attrs["long_name"] = var.attrs["long_name"].capitalize()
    return ds


def preprocess_nmme(ds):
    """
    Core preprocessing function. It combines most of the standalone functions
    defined in nmme_tools.preprocess to provide a unified tool.
    """
    ds = rename_dims(ds)
    ds = fix_time(ds)
    coords = [coord for coord in ["lead", "member"] if coord in ds.variables]
    if coords:
        ds = coords_to_int(ds, coords)
    ds = capitalize_names(ds)
    return ds.sortby("time")
