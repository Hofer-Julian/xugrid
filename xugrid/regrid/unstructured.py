import numpy as np

import xugrid as xu
from xugrid.constants import FloatDType
from xugrid.ugrid import voronoi
from xugrid.ugrid.ugrid2d import Ugrid2d


class UnstructuredGrid2d:
    """
    e.g. face -> face

    Parameters
    ----------
    grid: Ugrid2d
    """

    def __init__(self, obj):
        if isinstance(obj, (xu.UgridDataArray, xu.UgridDataset)):
            self.ugrid_topology = obj.grid
        elif isinstance(obj, Ugrid2d):
            self.ugrid_topology = obj
        else:
            options = {"Ugrid2d", "UgridDataArray", "UgridDataset"}
            raise TypeError(
                f"Expected one of {options}, received: {type(obj).__name__}"
            )

    @property
    def dims(self):
        return (self.ugrid_topology.face_dimension,)

    @property
    def shape(self):
        return (self.ugrid_topology.n_face,)

    @property
    def size(self):
        return self.ugrid_topology.n_face

    @property
    def area(self):
        return self.ugrid_topology.area

    def overlap(self, other, relative: bool):
        """
        Parameters
        ----------
        other: UnstructuredGrid2d
        """
        (
            target_index,
            source_index,
            weights,
        ) = self.ugrid_topology.celltree.intersect_faces(
            vertices=other.ugrid_topology.node_coordinates,
            faces=other.ugrid_topology.face_node_connectivity,
            fill_value=other.ugrid_topology.fill_value,
        )
        if relative:
            weights /= self.area[source_index]
        return source_index, target_index, weights

    def locate_centroids(self, other):
        tree = self.ugrid_topology.celltree
        source_index = tree.locate_points(other.ugrid_topology.centroids)
        inside = source_index != -1
        source_index = source_index[inside]
        target_index = np.arange(other.size, dtype=source_index.dtype)[inside]
        weight_values = np.ones_like(source_index, dtype=FloatDType)
        return source_index, target_index, weight_values

    def barycentric(self, other):
        points = other.ugrid_topology.centroids
        grid = self.ugrid_topology

        # Create a voronoi grid to get surrounding nodes as vertices
        vertices, faces, node_to_face_index = voronoi.voronoi_topology(
            grid.node_face_connectivity,
            grid.node_coordinates,
            grid.centroids,
            #    edge_face_connectivity=grid.edge_face_connectivity,
            #    edge_node_connectivity=grid.edge_node_connectivity,
            #    fill_value=grid.fill_value,
            #    add_exterior=True,
            #    add_vertices=False,
        )

        voronoi_grid = Ugrid2d(
            vertices[:, 0],
            vertices[:, 1],
            -1,
            faces,
        )

        face_index, weights = voronoi_grid.compute_barycentric_weights(points)
        n_points, n_max_node = weights.shape
        keep = weights.ravel() > 0
        source_index = node_to_face_index[
            voronoi_grid.face_node_connectivity[face_index]
        ].ravel()[keep]
        target_index = np.repeat(np.arange(n_points), n_max_node)[keep]
        weights = weights.ravel()[keep]

        # Look for points falling outside.
        outside = face_index == -1
        other_points = points[outside]
        sampled_index = grid.locate_points(other_points)
        sampled_inside = sampled_index != grid.fill_value
        other_source = sampled_index[sampled_inside]
        other_target = np.arange(n_points)[outside][sampled_inside]

        # Combine first and second
        source_index = np.concatenate((source_index, other_source))
        target_index = np.concatenate((target_index, other_target))
        weights = np.concatenate((weights, np.ones(other_target.size, dtype=float)))

        order = np.argsort(target_index)
        return source_index[order], target_index[order], weights[order]
