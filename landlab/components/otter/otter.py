# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:34:38 2019

@author: Sarah
"""

import numpy as np

from landlab import Component
from landlab.utils.return_array import return_array_at_node


class Otter(Component):

    """


    Parameters
    ----------
    grid: ModelGrid
        Landlab ModelGrid object
    soil_production__maximum_rate : float
        Characteristic weathering depth
    soil_production__decay_depth : float
        Maximum weathering rate for bare bedrock

    Examples
    --------
    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import Otter
    """

    _name = "Otter"

    _input_var_names = ("soil__depth",)

    _output_var_names = ("soil_production__rate",)

    _var_units = {"soil__depth": "m", "soil_production__rate": "m/yr"}

    _var_mapping = {"soil__depth": "node", "soil_production__rate": "node"}

    _var_doc = {
        "soil__depth": "depth of soil/weather bedrock",
        "soil_production__rate": "rate of soil production at nodes",
    }

    def __init__(
        self,
        grid,
        discharge_field="surface_water__discharge",
        kw=1e-5,
        manning_n=0.04,
        rhos=2700,
        g=9.8,
        # pass flooded nodes, see example in erosion_deposition component
        **kwds
    ):


    # where does width come from, esp at the beginning, and need a channel threshold to say which nodes to operate width on 
    
    
        # Store grid and parameters
        super(Otter, self).__init__(grid)
        self._grid = grid
        self._rhow = 1000 # kg/m^3
        self._g = g
        self._kw = return_array_at_node(grid, kw)
        self._man_n = return_array_at_node(grid, manning_n)
        self._rhos = return_array_at_node(grid, rhos)
        self._Qw = return_array_at_node(grid, discharge_field)
        self._cthresh = 10
        if "channl__width" not in grid.at_node:
            self._w = grid.add_zeros("channel__width", at="node")
            self._check_widths()
        # Create fields:
        # "channel__depth" is H
        # "channel__width" is W


    def _check_widths(self):
        
        # find where there is channel, but W is zero, then 
        # set that based on scaling.
        
        
        # find wher there is no channel, but W is > 0, set
        # to zero.
        self._w[not self._is_channel] = 0
        

    def run_one_step(self, dt=None, **kwds):
        """

        Parameters
        ----------
        dt: float
            Used only for compatibility with standard run_one_step.
        """
        self._is_channel = self.Qw > self._cthresh

        self._check_widths()
        
        for node in self._stack[::-1]:
            if self._is_channel[node]:
                # update width
                
        self._w[:] = new_width_values