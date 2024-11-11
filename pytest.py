
import numpy as np
from scipy.interpolate import griddata

def interpolated_data(df, x_col, y_col, value_col, grid_x, grid_y, method='linear'):
    """
    Interpolates data based on given x, y, and value columns.
    
    Parameters:
    df (DataFrame): Data containing x, y, and value columns.
    x_col (str): Name of the column representing x coordinates.
    y_col (str): Name of the column representing y coordinates.
    value_col (str): Name of the column representing values to be interpolated.
    grid_x (array-like): 1D array representing the x-coordinates of the grid.
    grid_y (array-like): 1D array representing the y-coordinates of the grid.
    method (str): Interpolation method, e.g., 'linear', 'nearest', or 'cubic'.
    
    Returns:
    np.ndarray: 2D array of interpolated values over the specified grid.
    """
    points = df[[x_col, y_col]].values  # Extract x, y coordinates
    values = df[value_col].values       # Extract values to interpolate

    # Create a mesh grid for interpolation
    grid_xx, grid_yy = np.meshgrid(grid_x, grid_y)
    
    # Interpolate values over the grid
    interpolated_values = griddata(points, values, (grid_xx, grid_yy), method=method)
    
    return interpolated_values

def interpolation(df, grid_x=None, grid_y=None, method='linear'):
    """
    Wrapper function to set up grid and call interpolated_data.

    Parameters:
    df (DataFrame): DataFrame containing data for interpolation.
    grid_x (array-like, optional): Grid values for x-axis; defaults to linspace if None.
    grid_y (array-like, optional): Grid values for y-axis; defaults to linspace if None.
    method (str): Interpolation method; defaults to 'linear'.

    Returns:
    np.ndarray: 2D array of interpolated values.
    """
    # Set default grid if not provided
    if grid_x is None:
        grid_x = np.linspace(0, 1, 100)
    if grid_y is None:
        grid_y = np.linspace(0, 1, 100)


    # Call the interpolation function with specified method
    return interpolated_data(df, 'x', 'y', 'value', grid_x, grid_y, method)


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import pytest
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

# Assume the functions are in a module named interpolation_module
from test import interpolated_data, interpolation

@pytest.fixture
def sample_data():
    """Fixture for a simple DataFrame with x, y, and value columns."""
    data = {
        'x': [0, 1, 0, 1],
        'y': [0, 0, 1, 1],
        'value': [0, 1, 1, 0]
    }
    df = pd.DataFrame(data)
    return df

@pytest.fixture
def default_grid():
    """Fixture for default grid values."""
    grid_x = np.linspace(0, 1, 5)
    grid_y = np.linspace(0, 1, 5)
    return grid_x, grid_y

def test_interpolated_data_linear(sample_data, default_grid):
    """Test interpolated_data with linear interpolation."""
    grid_x, grid_y = default_grid
    result = interpolated_data(sample_data, 'x', 'y', 'value', grid_x, grid_y, method='linear')
    
    # Check if the result is a 2D array with expected shape
    assert result.shape == (len(grid_y), len(grid_x))
    # Verify known points
    assert result[0, 0] == pytest.approx(0, abs=1e-5)  # Top-left corner
    assert result[-1, -1] == pytest.approx(0, abs=1e-5)  # Bottom-right corner
    assert result[0, -1] == pytest.approx(1, abs=1e-5)  # Top-right corner
    assert result[-1, 0] == pytest.approx(1, abs=1e-5)  # Bottom-left corner

def test_interpolated_data_nearest(sample_data, default_grid):
    """Test interpolated_data with nearest interpolation."""
    grid_x, grid_y = default_grid
    result = interpolated_data(sample_data, 'x', 'y', 'value', grid_x, grid_y, method='nearest')
    
    # Check if the result is a 2D array with expected shape
    assert result.shape == (len(grid_y), len(grid_x))
    # Verify known points match nearest neighbor values
    assert result[0, 0] == 0  # Top-left corner
    assert result[-1, -1] == 0  # Bottom-right corner
    assert result[0, -1] == 1  # Top-right corner
    assert result[-1, 0] == 1  # Bottom-left corner

def test_interpolation_with_defaults(sample_data):
    """Test the interpolation wrapper function with default grids."""
    result = interpolation(sample_data)
    # Check if the result is a 2D array with default shape (100x100)
    assert result.shape == (100, 100)

def test_interpolation_custom_grid(sample_data):
    """Test the interpolation wrapper function with a custom grid."""
    grid_x = np.linspace(0, 1, 10)
    grid_y = np.linspace(0, 1, 10)
    result = interpolation(sample_data, grid_x, grid_y)
    # Check if the result is a 2D array with shape (10x10)
    assert result.shape == (10, 10)

def test_interpolated_data_invalid_method(sample_data, default_grid):
    """Test interpolated_data with an invalid interpolation method."""
    grid_x, grid_y = default_grid
    with pytest.raises(ValueError):
        interpolated_data(sample_data, 'x', 'y', 'value', grid_x, grid_y, method='unsupported_method')



===============================================================================================================
import pytest
from unittest.mock import patch, MagicMock
from mail_server import send_email

def test_send_email_success():
    # Test sending a basic email successfully
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email(to="recipient@example.com", subject="Test Email", body="This is a test email.")

        mock_server.send_message.assert_called_once()

def test_send_email_with_cc_bcc():
    # Test sending email with CC and BCC fields
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email(
            to="recipient@example.com",
            subject="Test Email with CC and BCC",
            body="This email has CC and BCC fields.",
            cc=["cc1@example.com", "cc2@example.com"],
            bcc=["bcc1@example.com"]
        )

        msg = mock_server.send_message.call_args[0][0]
        assert "cc1@example.com" in msg["Cc"]
        assert "cc2@example.com" in msg["Cc"]
        assert "bcc1@example.com" in msg["Bcc"]

def test_send_email_attachment_not_found():
    # Test sending email with an attachment that doesn't exist
    with pytest.raises(FileNotFoundError, match="Attachment .* not found"):
        send_email(
            to="recipient@example.com",
            subject="Test Email with Missing Attachment",
            body="This email should raise a FileNotFoundError.",
            attachments=["non_existent_file.txt"]
        )

def test_send_email_with_attachment():
    # Test sending email with an existing attachment
    with patch("smtplib.SMTP") as mock_smtp, patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_open.return_value.__enter__.return_value.read.return_value = b"file content"

        send_email(
            to="recipient@example.com",
            subject="Test Email with Attachment",
            body="This email has an attachment.",
            attachments=["existing_file.txt"]
        )

        mock_server.send_message.assert_called_once()
        # Check that file was attempted to be opened
        mock_open.assert_called_once_with("existing_file.txt", 'rb')





