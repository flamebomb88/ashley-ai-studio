#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Bridge — Multi-Provider LLM Integration

Supported Providers:
  - OpenAI (GPT-3.5, GPT-4)
  - Anthropic (Claude)
  - Ollama (Local)
  - HuggingFace Inference
  - Together.ai
  - Groq
"""

import os
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class LLMProvider(Enum):
    """Available LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    TOGETHER = "together"
    GROQ = "groq"

@dataclass
class LLMConfig:
    """LLM configuration."""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout: int = 30

class LLMBridge:
    """Unified interface for multiple LLM providers."""
    
    def __init__(self):
        self.configs: Dict[str, LLMConfig] = {}
        self.active_config: Optional[LLMConfig] = None
        self._load_configs()
    
    def _load_configs(self):
        """Load LLM configurations from environment."""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            self.register_provider(
                LLMProvider.OPENAI,
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4"
            )
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            self.register_provider(
                LLMProvider.ANTHROPIC,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model="claude-3-opus"
            )
        
        # Ollama (local)
        self.register_provider(
            LLMProvider.OLLAMA,
            endpoint="http://localhost:11434",
            model="mistral"
        )
        
        # Set default to first available
        if self.configs:
            self.active_config = next(iter(self.configs.values()))
    
    def register_provider(
        self,
        provider: LLMProvider,
        model: str = None,
        api_key: str = None,
        endpoint: str = None,
        **kwargs
    ):
        """Register an LLM provider."""
        config = LLMConfig(
            provider=provider,
            model=model or self._get_default_model(provider),
            api_key=api_key,
            endpoint=endpoint,
            **kwargs
        )
        self.configs[provider.value] = config
    
    def _get_default_model(self, provider: LLMProvider) -> str:
        """Get default model for provider."""
        defaults = {
            LLMProvider.OPENAI: "gpt-4",
            LLMProvider.ANTHROPIC: "claude-3-opus",
            LLMProvider.OLLAMA: "mistral",
            LLMProvider.HUGGINGFACE: "meta-llama/Llama-2-70b-hf",
            LLMProvider.TOGETHER: "meta-llama/Llama-2-70b-chat",
            LLMProvider.GROQ: "mixtral-8x7b-32768",
        }
        return defaults.get(provider, "unknown")
    
    def set_active_provider(self, provider: LLMProvider):
        """Set active LLM provider."""
        if provider.value in self.configs:
            self.active_config = self.configs[provider.value]
            print(f"[LLM] Active provider: {provider.value}")
        else:
            print(f"[WARN] Provider not configured: {provider.value}")
    
    def select_best_provider(self, criteria: Dict[str, Any]) -> LLMProvider:
        """
        Select best provider based on criteria:
          - speed: prefer local (Ollama) > API
          - cost: prefer free/cheap options
          - quality: prefer advanced models (GPT-4, Claude-3)
          - latency: local < API
        """
        priority = criteria.get("priority", "balanced")  # balanced, speed, quality, cost
        
        if priority == "speed":
            return LLMProvider.OLLAMA  # Local is fastest
        elif priority == "quality":
            if LLMProvider.OPENAI.value in self.configs:
                return LLMProvider.OPENAI
            elif LLMProvider.ANTHROPIC.value in self.configs:
                return LLMProvider.ANTHROPIC
        elif priority == "cost":
            return LLMProvider.OLLAMA  # Local is free
        
        # Default: use active provider
        return self.active_config.provider if self.active_config else LLMProvider.OLLAMA
    
    async def generate(
        self,
        prompt: str,
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> str:
        """
        Generate text using LLM.
        Async-ready for future integration.
        """
        if not provider and not self.active_config:
            raise ValueError("No LLM provider configured")
        
        config = self.configs.get((provider or self.active_config.provider).value)
        
        if config.provider == LLMProvider.OPENAI:
            return await self._call_openai(prompt, config, **kwargs)
        elif config.provider == LLMProvider.ANTHROPIC:
            return await self._call_anthropic(prompt, config, **kwargs)
        elif config.provider == LLMProvider.OLLAMA:
            return await self._call_ollama(prompt, config, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
    
    async def _call_openai(self, prompt: str, config: LLMConfig, **kwargs) -> str:
        """Call OpenAI API (stub)."""
        try:
            import openai
            openai.api_key = config.api_key
            # response = openai.ChatCompletion.create(...)
            # return response["choices"][0]["message"]["content"]
        except ImportError:
            print("[WARN] openai package not installed")
        return "[OpenAI call stub]"
    
    async def _call_anthropic(self, prompt: str, config: LLMConfig, **kwargs) -> str:
        """Call Anthropic API (stub)."""
        return "[Anthropic call stub]"
    
    async def _call_ollama(self, prompt: str, config: LLMConfig, **kwargs) -> str:
        """Call Ollama local model (stub)."""
        return "[Ollama call stub]"
    
    def get_available_providers(self) -> List[str]:
        """Get list of configured providers."""
        return list(self.configs.keys())
    
    def get_provider_info(self, provider: LLMProvider) -> Dict[str, Any]:
        """Get info about a provider."""
        if provider.value not in self.configs:
            return {"status": "not_configured"}
        
        config = self.configs[provider.value]
        return {
            "status": "configured",
            "provider": provider.value,
            "model": config.model,
            "has_api_key": bool(config.api_key),
            "endpoint": config.endpoint,
        }

if __name__ == "__main__":
    bridge = LLMBridge()
    print("Available providers:", bridge.get_available_providers())
    
    for provider_name in bridge.get_available_providers():
        provider = LLMProvider(provider_name)
        info = bridge.get_provider_info(provider)
        print(json.dumps(info, indent=2))
