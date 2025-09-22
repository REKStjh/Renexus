"""
Ren AI Companion - Core Module

An AI that serves people instead of profits, focused on connection and healing.
"""

__version__ = "0.1.0"
__author__ = "Renexus Development Team"

from .ren_core import RenCore
from .personality_engine import PersonalityEngine
from .communication_analyzer import CommunicationAnalyzer

__all__ = ["RenCore", "PersonalityEngine", "CommunicationAnalyzer"]
