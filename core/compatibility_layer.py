#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Platform Compatibility Layer

Supports:
  - Windows, macOS, Linux
  - Language detection: Python, JavaScript, Java, Go, Rust, etc.
  - Runtime detection and bridging
  - OS-specific command execution
  - Environment detection
"""

import os
import platform
import subprocess
import sys
from typing import Optional, Dict, List, Tuple
from pathlib import Path
from enum import Enum

class OSType(Enum):
    """Operating system types."""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"

class LanguageRuntime(Enum):
    """Programming language runtimes."""
    PYTHON = "python"
    PYTHON3 = "python3"
    JAVASCRIPT = "node"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    DOTNET = "dotnet"
    RUBY = "ruby"

class CompatibilityLayer:
    """
    Abstraction layer for cross-platform compatibility.
    """
    
    def __init__(self):
        self.os_type = self._detect_os()
        self.available_runtimes = self._detect_runtimes()
        self.environment = self._get_environment()
    
    def _detect_os(self) -> OSType:
        """Detect operating system."""
        system = platform.system()
        if system == "Windows":
            return OSType.WINDOWS
        elif system == "Darwin":
            return OSType.MACOS
        elif system == "Linux":
            return OSType.LINUX
        else:
            return OSType.UNKNOWN
    
    def _detect_runtimes(self) -> Dict[LanguageRuntime, bool]:
        """Detect available language runtimes."""
        runtimes = {}
        
        # Python
        for cmd in ["python", "python3", "py"]:
            if self._command_exists(cmd):
                runtimes[LanguageRuntime.PYTHON] = True
                runtimes[LanguageRuntime.PYTHON3] = True
                break
        else:
            runtimes[LanguageRuntime.PYTHON] = False
            runtimes[LanguageRuntime.PYTHON3] = False
        
        # JavaScript/Node
        runtimes[LanguageRuntime.JAVASCRIPT] = self._command_exists("node")
        
        # Java
        runtimes[LanguageRuntime.JAVA] = self._command_exists("java")
        
        # Go
        runtimes[LanguageRuntime.GO] = self._command_exists("go")
        
        # Rust
        runtimes[LanguageRuntime.RUST] = self._command_exists("rustc")
        
        # .NET
        runtimes[LanguageRuntime.DOTNET] = self._command_exists("dotnet")
        
        # Ruby
        runtimes[LanguageRuntime.RUBY] = self._command_exists("ruby")
        
        return runtimes
    
    def _command_exists(self, command: str) -> bool:
        """Check if command is available."""
        if self.os_type == OSType.WINDOWS:
            cmd = f"where {command}"
        else:
            cmd = f"which {command}"
        
        try:
            subprocess.run(cmd, shell=True, capture_output=True, timeout=2)
            return True
        except Exception:
            return False
    
    def _get_environment(self) -> Dict[str, str]:
        """Get relevant environment variables."""
        return {
            "OS": platform.system(),
            "OS_VERSION": platform.version(),
            "ARCH": platform.machine(),
            "PYTHON_VERSION": platform.python_version(),
            "PATH": os.environ.get("PATH", ""),
        }
    
    def execute_language_file(
        self,
        filepath: str,
        language: LanguageRuntime = None,
        args: List[str] = None
    ) -> Tuple[int, str, str]:
        """
        Execute a file in the appropriate runtime.
        Returns (return_code, stdout, stderr).
        """
        path = Path(filepath)
        if not path.exists():
            return 1, "", f"File not found: {filepath}"
        
        # Auto-detect language if not specified
        if not language:
            language = self._detect_language_from_extension(path.suffix)
        
        # Build command
        cmd = self._build_command(language, filepath, args)
        
        # Execute
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 124, "", "Execution timeout (5 minutes)"
        except Exception as e:
            return 1, "", str(e)
    
    def _detect_language_from_extension(self, extension: str) -> LanguageRuntime:
        """Detect language from file extension."""
        mapping = {
            ".py": LanguageRuntime.PYTHON3,
            ".js": LanguageRuntime.JAVASCRIPT,
            ".java": LanguageRuntime.JAVA,
            ".go": LanguageRuntime.GO,
            ".rs": LanguageRuntime.RUST,
            ".cs": LanguageRuntime.DOTNET,
            ".rb": LanguageRuntime.RUBY,
        }
        return mapping.get(extension, LanguageRuntime.PYTHON3)
    
    def _build_command(self, language: LanguageRuntime, filepath: str, args: List[str] = None) -> str:
        """Build command to execute file."""
        args_str = " ".join(args) if args else ""
        
        if language == LanguageRuntime.PYTHON3:
            if self.os_type == OSType.WINDOWS:
                return f'py "{filepath}" {args_str}'
            else:
                return f'python3 "{filepath}" {args_str}'
        
        elif language == LanguageRuntime.JAVASCRIPT:
            return f'node "{filepath}" {args_str}'
        
        elif language == LanguageRuntime.JAVA:
            # Assume compiled .class file or jar
            return f'java -jar "{filepath}" {args_str}'
        
        elif language == LanguageRuntime.GO:
            return f'go run "{filepath}" {args_str}'
        
        elif language == LanguageRuntime.RUST:
            return f'rustc -o /tmp/rust_out "{filepath}" && /tmp/rust_out {args_str}'
        
        elif language == LanguageRuntime.DOTNET:
            return f'dotnet run "{filepath}" {args_str}'
        
        elif language == LanguageRuntime.RUBY:
            return f'ruby "{filepath}" {args_str}'
        
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def get_status(self) -> Dict[str, any]:
        """Get compatibility status."""
        return {
            "os": self.os_type.value,
            "available_runtimes": {
                name.value: available
                for name, available in self.available_runtimes.items()
            },
            "environment": self.environment,
        }

if __name__ == "__main__":
    compat = CompatibilityLayer()
    
    import json
    print(json.dumps(compat.get_status(), indent=2))
    
    # Example: Run a Python file
    # returncode, stdout, stderr = compat.execute_language_file("test.py", args=["--help"])
    # print(f"Return code: {returncode}")
    # print(f"Output: {stdout}")
    # if stderr:
    #     print(f"Error: {stderr}")
