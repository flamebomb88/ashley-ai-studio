#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odysseus Bridge — Integration with Odysseus AI Workspace

Provides:
  - Connection to Odysseus server
  - Model discovery
  - Chat integration
  - Document sharing
  - Tool registration
"""

import requests
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class OdysseusConfig:
    """Odysseus server configuration."""
    host: str = "localhost"
    port: int = 7000
    username: str = ""
    password: str = ""
    api_token: Optional[str] = None
    use_https: bool = False
    verify_ssl: bool = True

class OdysseusBridge:
    """
    Bridge to Odysseus AI workspace.
    Enables two-way integration and model discovery.
    """
    
    def __init__(self, config: OdysseusConfig = None):
        self.config = config or OdysseusConfig()
        self.base_url = self._build_url()
        self.session = requests.Session()
        self.authenticated = False
    
    def _build_url(self) -> str:
        """Build base URL."""
        protocol = "https" if self.config.use_https else "http"
        return f"{protocol}://{self.config.host}:{self.config.port}"
    
    def authenticate(self, token: str = None) -> bool:
        """Authenticate with Odysseus server."""
        token = token or self.config.api_token
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            self.authenticated = True
            return True
        return False
    
    def ping(self) -> bool:
        """Check connection to Odysseus."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/companion/ping",
                timeout=5,
                verify=self.config.verify_ssl
            )
            return response.status_code == 200
        except Exception as e:
            print(f"[WARN] Odysseus ping failed: {e}")
            return False
    
    def get_server_info(self) -> Optional[Dict[str, Any]]:
        """Get Odysseus server information."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/companion/info",
                timeout=5,
                verify=self.config.verify_ssl
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[WARN] Failed to get server info: {e}")
        return None
    
    def discover_models(self) -> List[Dict[str, Any]]:
        """Discover available models on Odysseus."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/companion/models",
                timeout=10,
                verify=self.config.verify_ssl
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[WARN] Failed to discover models: {e}")
        return []
    
    def send_message(
        self,
        chat_id: str,
        content: str,
        model: str = None
    ) -> Optional[str]:
        """Send message to Odysseus chat."""
        payload = {
            "content": content,
            "model": model,
        }
        try:
            response = self.session.post(
                f"{self.base_url}/api/chats/{chat_id}/messages",
                json=payload,
                timeout=30,
                verify=self.config.verify_ssl
            )
            if response.status_code == 200:
                return response.json().get("response")
        except Exception as e:
            print(f"[WARN] Failed to send message: {e}")
        return None
    
    def register_tool(
        self,
        name: str,
        description: str,
        endpoint: str,
        schema: Dict[str, Any]
    ) -> bool:
        """Register a tool in Odysseus."""
        payload = {
            "name": name,
            "description": description,
            "endpoint": endpoint,
            "schema": schema,
        }
        try:
            response = self.session.post(
                f"{self.base_url}/api/tools",
                json=payload,
                timeout=10,
                verify=self.config.verify_ssl
            )
            return response.status_code == 201
        except Exception as e:
            print(f"[WARN] Failed to register tool: {e}")
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall bridge status."""
        return {
            "connected": self.ping(),
            "authenticated": self.authenticated,
            "server_info": self.get_server_info(),
            "models_available": len(self.discover_models()),
        }

if __name__ == "__main__":
    # Example usage
    bridge = OdysseusBridge()
    
    print("Connecting to Odysseus...")
    if bridge.ping():
        print("✓ Connected!")
        info = bridge.get_server_info()
        print(f"Server: {info}")
        
        models = bridge.discover_models()
        print(f"Available models: {len(models)}")
    else:
        print("✗ Could not connect to Odysseus")
        print("  Make sure Odysseus is running: docker compose up -d")
