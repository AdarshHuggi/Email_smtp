

import pytest
import pandas as pd
import numpy as np
from scipy.interpolate import Rbf

# Sample Data
@pytest.fixture
def sample_data():
    data = {
        'x': [0, 0, 1, 1],
        'y': [0, 1, 0, 1],
        'value': [0, 1, 1, 0]
    }
    return pd.DataFrame(data)

def test_interpolated_data_cubic(sample_data):
    grid_x = np.linspace(0, 1, 10)
    grid_y = np.linspace(0, 1, 10)
    
    # Testing cubic interpolation
    interpolated = interpolated_data(sample_data, 'x', 'y', 'value', grid_x, grid_y, method='cubic')
    assert interpolated is not None, "Cubic interpolation returned None"
    assert not np.any(np.isnan(interpolated)), "Cubic interpolation has NaN values"

def test_interpolated_data_rbf(sample_data):
    grid_x = np.linspace(0, 1, 10)
    grid_y = np.linspace(0, 1, 10)
    grid_xx, grid_yy = np.meshgrid(grid_x, grid_y)
    
    # Using RBF for interpolation
    rbf_interpolator = Rbf(sample_data['x'], sample_data['y'], sample_data['value'], function='linear')
    interpolated_values = rbf_interpolator(grid_xx, grid_yy)
    
    assert interpolated_values is not None, "RBF interpolation returned None"
    assert not np.any(np.isnan(interpolated_values)), "RBF interpolation has NaN values"
