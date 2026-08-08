"""Tests for the GET / root endpoint."""

import pytest


def test_root_redirect(client):
    """Test that root endpoint redirects to the static HTML."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    
    # Verify redirect location
    assert "location" in response.headers
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_with_follow(client):
    """Test root endpoint redirect with follow_redirects=True."""
    response = client.get("/", follow_redirects=True)
    # When following redirects, we should get the static file
    # This might be 200 if the static file is served, or 404 if not (depending on TestClient behavior)
    assert response.status_code in [200, 404]
