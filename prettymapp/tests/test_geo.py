from unittest.mock import patch

import geopandas as gpd
import osmnx as ox
import pandas as pd
import pytest
from shapely.geometry import MultiPolygon, Polygon

from prettymapp.geo import (
    GeoCodingError,
    explode_multigeometries,
    get_aoi,
    validate_coordinates,
)


def test_validate_coordinates():
    validate_coordinates(lat=-89.3, lon=178.2)
    validate_coordinates(lat=89.3, lon=-178.2)
    with pytest.raises(ValueError):
        validate_coordinates(lat=-92.3, lon=237.2)
    with pytest.raises(ValueError):
        validate_coordinates(lat=92.3, lon=-237.2)


TOLERANCE = 0.0001  # test tolerance to compare values


def _is_in_tol(values: list, answers: tuple):
    for val, ans in zip(values, answers, strict=True):
        assert abs(val - ans) < TOLERANCE


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_address(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)

    _is_in_tol(
        poly.bounds,
        (
            13.373621926483281,
            52.507705884952586,
            13.403083847278062,
            52.52567909987013,
        ),
    )

    assert abs(poly.area - 0.00041542753985753124) < TOLERANCE


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_coordinates(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)

    _is_in_tol(
        poly.bounds,
        (
            13.38526793559592,
            52.51101333875345,
            13.414732236942758,
            52.52898664609028,
        ),
    )

    assert abs(poly.area - 0.00041546027853784154) < TOLERANCE


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_rectangle(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi("Unter den Linden 37, 10117 Berlin", rectangular=True)
    assert isinstance(poly, Polygon)

    _is_in_tol(
        poly.bounds,
        (
            13.373621926483281,
            52.507705884952586,
            13.403083847278062,
            52.52567909987013,
        ),
    )

    assert abs(poly.area - 0.0005295254343283185) < TOLERANCE


@pytest.mark.live
def test_get_aoi_from_user_input_address_live():
    poly = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)

    _is_in_tol(
        poly.bounds,
        (
            13.373621926483281,
            52.507705884952586,
            13.403083847278062,
            52.52567909987013,
        ),
    )


@pytest.mark.live
def test_get_aoi_from_user_input_coordinates_live():
    poly = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    _is_in_tol(
        poly.bounds,
        (
            13.38526793559592,
            52.51101333875345,
            13.414732236942758,
            52.52898664609028,
        ),
    )


@pytest.mark.live
def test_get_aoi_invalid_address_raises():
    with pytest.raises(GeoCodingError):
        get_aoi("not_an_address")


def test_explode_multigeoemtries():
    poly1 = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    poly2 = Polygon([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]])
    multipoly = MultiPolygon([poly1, poly2])
    df = gpd.GeoDataFrame(
        pd.DataFrame([0, 1], columns=["id"]),
        crs="EPSG:4326",
        geometry=[poly1, multipoly],
    )
    df_result = explode_multigeometries(df)

    assert df.shape[0] != df_result.shape[0]
    assert df_result.shape[0] == 3
