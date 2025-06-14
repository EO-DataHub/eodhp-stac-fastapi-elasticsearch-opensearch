"""API configuration."""

import os
import ssl
from typing import Any, Dict, Set

import certifi

from elasticsearch import AsyncElasticsearch, Elasticsearch  # type: ignore
from stac_fastapi.types.config import ApiSettings


def _es_config() -> Dict[str, Any]:
    # Determine the scheme (http or https)
    use_ssl = os.getenv("ES_USE_SSL", "true").lower() == "true"
    scheme = "https" if use_ssl else "http"

    # Configure the hosts parameter with the correct scheme
    hosts = [f"{scheme}://{os.getenv('ES_HOST')}:{os.getenv('ES_PORT')}"]

    # Initialize the configuration dictionary
    config = {
        "hosts": hosts,
        "headers": {"accept": "application/vnd.elasticsearch+json; compatible-with=7"},
    }

    # Handle API key
    if api_key := os.getenv("ES_API_KEY"):
        if isinstance(config["headers"], dict):
            headers = {**config["headers"], "x-api-key": api_key}

        else:
            config["headers"] = {"x-api-key": api_key}

        config["headers"] = headers

    # Explicitly exclude SSL settings when not using SSL
    if not use_ssl:
        return config

    # Include SSL settings if using https
    config["ssl_version"] = ssl.TLSVersion.TLSv1_3  # type: ignore
    config["verify_certs"] = os.getenv("ES_VERIFY_CERTS", "true").lower() != "false"  # type: ignore

    # Include CA Certificates if verifying certs
    if config["verify_certs"]:
        config["ca_certs"] = os.getenv("CURL_CA_BUNDLE", certifi.where())

    # Handle authentication
    if (u := os.getenv("ES_USER")) and (p := os.getenv("ES_PASS")):
        config["http_auth"] = (u, p)

    config["timeout"] = int(os.getenv("ES_TIMEOUT", "60"))

    return config


_forbidden_fields: Set[str] = {"type"}


class ElasticsearchSettings(ApiSettings):
    """API settings."""

    # Fields which are defined by STAC but not included in the database model
    forbidden_fields: Set[str] = _forbidden_fields
    indexed_fields: Set[str] = {"datetime"}

    @property
    def create_client(self):
        """Create es client."""
        return Elasticsearch(**_es_config())


class AsyncElasticsearchSettings(ApiSettings):
    """API settings."""

    # Fields which are defined by STAC but not included in the database model
    forbidden_fields: Set[str] = _forbidden_fields
    indexed_fields: Set[str] = {"datetime"}

    @property
    def create_client(self):
        """Create async elasticsearch client."""
        return AsyncElasticsearch(**_es_config())
