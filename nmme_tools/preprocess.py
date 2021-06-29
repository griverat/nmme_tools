import numpy as np
import xarray as xr


def rename_dims(ds):
    dims_mapping = {"L": "lead", "Y": "lat", "X": "lon", "M": "member", "S": "time"}
    return ds.rename({k: v for k, v in dims_mapping.items() if k in ds.variables})


def fix_time(ds):
    ds["time"].attrs["calendar"] = "360_day"
    return xr.decode_cf(ds)


def coords_to_int(ds, coords):
    coords = [coords] if not isinstance(coords, list) else coords
    for coord in coords:
        _coord_attrs = ds[coord].attrs
        ds[coord] = np.int32(ds[coord])
        ds[coord].attrs = _coord_attrs
    return ds


def capitalize_names(ds):
    for var in ds.variables.values():
        if "long_name" in var.attrs:
            var.attrs["long_name"] = var.attrs["long_name"].capitalize()
    return ds


def preprocess_nmme(ds):
    ds = rename_dims(ds)
    ds = fix_time(ds)
    coords = [coord for coord in ["lead", "member"] if coord in ds.variables]
    if coords:
        ds = coords_to_int(ds, coords)
    ds = capitalize_names(ds)
    return ds.sortby("time")
