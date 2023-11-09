from importlib.metadata import version as _version

from xugrid import data
from xugrid.core.common import (
    concat,
    full_like,
    merge,
    ones_like,
    open_dataarray,
    open_dataset,
    open_mfdataset,
    open_zarr,
    zeros_like,
)
from xugrid.core.dataarray_accessor import UgridDataArrayAccessor
from xugrid.core.dataset_accessor import UgridDatasetAccessor
from xugrid.core.wrap import UgridDataArray, UgridDataset
from xugrid.plot import plot
from xugrid.regrid.regridder import (
    BarycentricInterpolator,
    CentroidLocatorRegridder,
    OverlapRegridder,
    RelativeOverlapRegridder,
)
from xugrid.ugrid.burn import burn_vector_geometry
from xugrid.ugrid.conventions import UgridRolesAccessor
from xugrid.ugrid.partitioning import merge_partitions
from xugrid.ugrid.polygonize import polygonize
from xugrid.ugrid.snapping import snap_to_grid
from xugrid.ugrid.ugrid1d import Ugrid1d
from xugrid.ugrid.ugrid2d import Ugrid2d

try:
    __version__ = _version("xugrid")
except Exception:
    # Disable minimum version checks on downstream libraries.
    __version__ = "9999"

__all__ = (
    "data",
    "concat",
    "full_like",
    "merge",
    "ones_like",
    "open_dataarray",
    "open_dataset",
    "open_mfdataset",
    "open_zarr",
    "zeros_like",
    "UgridDataArrayAccessor",
    "UgridDatasetAccessor",
    "UgridDataArray",
    "UgridDataset",
    "plot",
    "BarycentricInterpolator",
    "CentroidLocatorRegridder",
    "OverlapRegridder",
    "RelativeOverlapRegridder",
    "burn_vector_geometry",
    "UgridRolesAccessor",
    "merge_partitions",
    "polygonize",
    "snap_to_grid",
    "Ugrid1d",
    "Ugrid2d",
)
