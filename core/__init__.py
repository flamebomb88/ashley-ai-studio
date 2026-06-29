#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core module — Ashley AI Studio foundation
"""

from .ashley_agent import AshleyAgent, PersonalityProfile, Emotion
from .code_generator import CodeGenerator, PythonGenerator
from .llm_bridge import LLMBridge, LLMProvider
from .odysseus_bridge import OdysseusBridge, OdysseusConfig
from .compatibility_layer import CompatibilityLayer, OSType, LanguageRuntime

__all__ = [
    "AshleyAgent",
    "PersonalityProfile",
    "Emotion",
    "CodeGenerator",
    "PythonGenerator",
    "LLMBridge",
    "LLMProvider",
    "OdysseusBridge",
    "OdysseusConfig",
    "CompatibilityLayer",
    "OSType",
    "LanguageRuntime",
]
