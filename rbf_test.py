def test_interpolate_data_rbf():
    # Define test data
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 2, 3])
    values = np.array([1, 2, 3, 4])
    xi, yi = np.meshgrid(np.linspace(0, 3, 10), np.linspace(0, 3, 10))
    
    # Perform RBF interpolation
    result = interpolate_data(x, y, values, xi, yi, method='rbf')
    
    # Check that the result is not None and has expected shape
    assert result is not None
    assert result.shape == xi.shape
    assert np.all(np.isfinite(result)), "RBF interpolation failed with NaN or Inf values"
