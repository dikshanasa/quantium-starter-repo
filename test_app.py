import pytest
from dash.testing.application_runners import import_app

# Import the app to be tested only once
app = import_app('FinalDashApp')

def test_header_is_present(dash_duo):
    """Test that the header is present"""
    dash_duo.start_server(app)
    
    header = dash_duo.find_element("#header")
    assert header is not None, "Header is missing"

def test_visualization_is_present(dash_duo):
    """Test that the visualization is present"""
    dash_duo.start_server(app)

    visualization = dash_duo.find_element("#visualization")
    assert visualization is not None, "Visualization (Graph) is missing"

def test_region_picker_is_present(dash_duo):
    """Test that the region picker is present"""
    dash_duo.start_server(app)

    region_picker = dash_duo.find_element("#region_picker")
    assert region_picker is not None, "Region picker is missing"
