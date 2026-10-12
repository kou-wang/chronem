"""Deterministic, conservative entity-resolution behavior."""

from chronem.entities.normalization import normalize_entity_name
from chronem.entities.resolver import DeterministicEntityResolver

__all__ = ["DeterministicEntityResolver", "normalize_entity_name"]
