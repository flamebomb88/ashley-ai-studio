# Ashley AI Studio — Phase 1-3 Implementation Guide

## 🎯 Overview

**Target**: Foundation, Shell/GUI, Text Processing  
**Duration**: 4-12 weeks  
**Completion**: 35%  

This document details the step-by-step implementation of Phases 1-3, with focus on:
- Core architecture & scaffolding
- Shell (CLI) & GUI (Tkinter)
- File I/O & text editor
- Tokenizer & embeddings foundation
- Hardware optimization
- Checkpoint/savepoint system

---

## Phase 1: Foundation & Setup (Weeks 1-4)

### 1.1 Project Structure (COMPLETE)

```
ashley-ai-studio/
├── launcher.py              # Entry point
├── ashley_ai_studio.py      # Main orchestrator
├── README.md
├── PHASE_1_3_IMPLEMENTATION.md
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging system
│   ├── errors.py            # Custom exceptions
│   ├── utils.py             # Utility functions
│   └── hardware.py          # Hardware monitoring
├── ui/
│   ├── __init__.py
│   ├── shell.py             # Terminal shell
│   ├── gui.py               # Tkinter GUI
│   ├── editor.py            # Text editor widget
│   └── themes/
│       └── default.css
├── text_processing/
│   ├── __init__.py
│   ├── tokenizer.py         # Tokenization
│   ├── embeddings.py        # Word embeddings
│   ├── predictor.py         # Text prediction
│   └── grammar.py           # Grammar analysis
├── database/
│   ├── __init__.py
│   ├── sqlite_schema.sql    # Database schema
│   ├── connection.py        # DB connection
│   └── migrations/
│       └── 001_init.sql
├── models/
│   ├── checkpoints/
│   ├── manifest.json
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── data/
│   ├── datasets/
│   ├── vectors/
│   └── cache/
└── tests/
    ├── __init__.py
    ├── test_tokenizer.py
    ├── test_database.py
    └── test_ui.py
```

### 1.2 Core Modules to Implement

#### A. `core/config.py` — Configuration Management

```python
# Manages runtime configuration, environment variables, defaults
import json
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class Config:
    # UI
    ui_mode: str = "gui"  # "gui", "shell", "web"
    theme: str = "dark"
    font_size: int = 11
    
    # Database
    db_path: Path = None
    db_auto_backup: bool = True
    
    # Training
    batch_size: int = 32
    learning_rate: float = 0.001
    num_epochs: int = 100
    
    # Hardware
    use_gpu: bool = True
    max_threads: int = 4
    cache_mb: int = 512
    
    # Paths
    data_dir: Path = None
    models_dir: Path = None
    logs_dir: Path = None
    
    def save(self, path: Path):
        path.write_text(json.dumps(asdict(self), default=str))
    
    @classmethod
    def load(cls, path: Path):
        data = json.loads(path.read_text())
        # Convert string paths back to Path objects
        for k in ["db_path", "data_dir", "models_dir", "logs_dir"]:
            if k in data and data[k]:
                data[k] = Path(data[k])
        return cls(**data)
```

#### B. `core/logger.py` — Logging System

```python
# Multi-level logging with file & console output
import logging
from pathlib import Path
from datetime import datetime

class AshleyLogger:
    def __init__(self, name: str, log_dir: Path):
        self.logger = logging.getLogger(name)
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        # File handler
        log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        ))
        self.logger.addHandler(fh)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s', 
            datefmt='%H:%M:%S'
        ))
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)
    
    def info(self, msg): self.logger.info(msg)
    def debug(self, msg): self.logger.debug(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)
```

#### C. `core/errors.py` — Custom Exceptions

```python
# Custom exception hierarchy

class AshleyException(Exception):
    """Base exception."""
    pass

class ConfigError(AshleyException):
    """Configuration error."""
    pass

class DatabaseError(AshleyException):
    """Database operation error."""
    pass

class TokenizerError(AshleyException):
    """Tokenization error."""
    pass

class ModelError(AshleyException):
    """Model loading/training error."""
    pass

class HardwareError(AshleyException):
    """Hardware detection error."""
    pass
```

### 1.3 Database Schema

#### `database/sqlite_schema.sql`

```sql
-- Core schema for Ashley AI memory & training

CREATE TABLE IF NOT EXISTS metadata (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE,
    value TEXT,
    timestamp TEXT,
    version TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE,
    started_at TEXT,
    ended_at TEXT,
    mode TEXT,  -- 'shell', 'gui', 'web'
    metadata TEXT  -- JSON
);

CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    timestamp TEXT,
    level TEXT,  -- 'short_term', 'session', 'project', 'long_term'
    content TEXT,
    tags TEXT,  -- JSON array
    emotion TEXT,
    logic_score REAL,
    dream_score REAL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    role TEXT,  -- 'core', 'processing', 'memory', 'output'
    name TEXT,
    activation REAL DEFAULT 0.0,
    state TEXT DEFAULT 'idle',
    created_at TEXT,
    last_active TEXT
);

CREATE TABLE IF NOT EXISTS training_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    timestamp TEXT,
    phase INTEGER,
    stage TEXT,
    metric_name TEXT,
    metric_value REAL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY,
    token TEXT UNIQUE,
    token_id INTEGER UNIQUE,
    frequency INTEGER,
    embedding_id INTEGER
);

CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY,
    token_id INTEGER,
    vector BLOB,  -- Serialized numpy array
    dimension INTEGER,
    created_at TEXT,
    FOREIGN KEY(token_id) REFERENCES vocabulary(token_id)
);

CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_memory_session_id ON memory(session_id);
CREATE INDEX IF NOT EXISTS idx_memory_timestamp ON memory(timestamp);
CREATE INDEX IF NOT EXISTS idx_vocabulary_token ON vocabulary(token);
CREATE INDEX IF NOT EXISTS idx_embeddings_token_id ON embeddings(token_id);
```

### 1.4 Requirements & Dependencies

#### `requirements.txt`

```
# Core
numpy>=1.21.0
Pillow>=8.3.0
requests>=2.26.0

# UI
tkinter  # Built-in Python

# Optional GPU/ML
torch>=1.9.0  # CPU-only by default
scikit-learn>=0.24.0

# Optional: LLM integration
chromadb>=0.3.0
sentence-transformers>=2.2.0

# Optional: TTS/STT/Voice
pyttsx3>=2.90
SpeechRecognition>=3.8.1
PyAudio>=0.2.11  # Requires PortAudio dev libs

# Optional: Web
flask>=2.0.0
flask-socketio>=5.0.0

# Optional: System monitoring
psutil>=5.8.0
GPUtil>=1.4.0

# Testing
pytest>=6.2.0
pytest-cov>=2.12.0

# Development
black>=21.5b0
pylint>=2.8.0
mypy>=0.910
```

### 1.5 Setup Automation

#### `setup.py` — Installation script

```python
import subprocess
import sys
from pathlib import Path

def install_deps():
    """Install all dependencies."""
    req_file = Path(__file__).parent / "requirements.txt"
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", str(req_file)
    ])

if __name__ == "__main__":
    print("Installing Ashley AI Studio dependencies...")
    install_deps()
    print("✓ Complete!")
```

---

## Phase 2: Text Editor & UI (Weeks 4-12)

### 2.1 Text Editor Widget

#### `ui/editor.py`

```python
# Tkinter-based text editor with syntax highlighting & prediction

import tkinter as tk
from tkinter import scrolledtext
import re

class TextEditor(scrolledtext.ScrolledText):
    """Enhanced text editor with syntax highlighting."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tag_config("keyword", foreground="#7c3aed")
        self.tag_config("string", foreground="#22c55e")
        self.tag_config("comment", foreground="#6b7280")
        self.tag_config("error", foreground="#ef4444", underline=True)
        self.tag_config("prediction", foreground="#06b6d4", overstrike=False)
        
        self.bind("<KeyRelease>", self._on_key)
        self.predictor = None
    
    def set_predictor(self, predictor):
        self.predictor = predictor
    
    def _on_key(self, event):
        self._highlight_syntax()
        if self.predictor:
            self._show_predictions()
    
    def _highlight_syntax(self):
        # Remove previous tags
        for tag in ["keyword", "string", "comment"]:
            self.tag_remove(tag, "1.0", "end")
        
        # Highlight keywords
        keywords = r'\b(def|class|import|from|return|if|else|for|while|break|continue)\b'
        for match in re.finditer(keywords, self.get("1.0", "end")):
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.tag_add("keyword", start_idx, end_idx)
    
    def _show_predictions(self):
        # Show next-word predictions (placeholder)
        pass
```

### 2.2 Terminal Shell

#### `ui/shell.py`

```python
# Rich terminal interface

import cmd
import sys
from datetime import datetime

class AshleyShell(cmd.Cmd):
    """Interactive terminal shell."""
    
    intro = """╔══════════════════════════════════════════╗
║  Ashley AI Studio — Terminal Shell     ║
║  Type 'help' for commands              ║
╚══════════════════════════════════════════╝"""
    
    prompt = "ashley> "
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.history = []
    
    def do_help(self, arg):
        """Show help."""
        print("""Commands:
  help         — This menu
  status       — System status
  scan PATH    — Scan project
  train        — Start training
  predict TEXT — Get text prediction
  quit         — Exit
        """)
    
    def do_status(self, arg):
        """Show system status."""
        print("✓ Online")
        print(f"  Session: {self.session_id}")
        print(f"  Mode: shell")
    
    def do_scan(self, arg):
        """Scan project."""
        if not arg:
            print("Usage: scan <path>")
            return
        print(f"Scanning: {arg}")
        # Placeholder
    
    def do_predict(self, arg):
        """Predict next words."""
        if not arg:
            print("Usage: predict <text>")
            return
        print(f"Predictions for: {arg}")
        # Placeholder
    
    def do_quit(self, arg):
        """Exit."""
        print("Goodbye!")
        return True
    
    def do_EOF(self, arg):
        return self.do_quit(arg)
```

---

## Phase 3: Text Processing & Training Foundation (Weeks 12-24)

### 3.1 Tokenizer

#### `text_processing/tokenizer.py`

```python
# Multi-level tokenization: character, word, subword

import re
from typing import List, Dict

class Tokenizer:
    """Tokenize text at character, word, and subword levels."""
    
    def __init__(self, vocab_size: int = 50000):
        self.vocab = {}
        self.token_to_id = {}
        self.id_to_token = {}
        self.vocab_size = vocab_size
    
    def tokenize_word(self, text: str) -> List[str]:
        """Word-level tokenization."""
        return text.lower().split()
    
    def tokenize_char(self, text: str) -> List[str]:
        """Character-level tokenization."""
        return list(text.lower())
    
    def build_vocab(self, texts: List[str]):
        """Build vocabulary from texts."""
        from collections import Counter
        counter = Counter()
        for text in texts:
            tokens = self.tokenize_word(text)
            counter.update(tokens)
        
        # Get most common tokens
        for idx, (token, _) in enumerate(counter.most_common(self.vocab_size)):
            self.token_to_id[token] = idx
            self.id_to_token[idx] = token
    
    def encode(self, text: str) -> List[int]:
        """Convert text to token IDs."""
        tokens = self.tokenize_word(text)
        return [self.token_to_id.get(t, 0) for t in tokens]  # 0 = unknown
    
    def decode(self, ids: List[int]) -> str:
        """Convert token IDs back to text."""
        return " ".join([self.id_to_token.get(i, "<UNK>") for i in ids])
```

### 3.2 Embeddings

#### `text_processing/embeddings.py`

```python
# Word embeddings (Word2Vec-style)

import numpy as np
from typing import List, Tuple

class WordEmbedding:
    """Simple word embedding layer."""
    
    def __init__(self, vocab_size: int, embedding_dim: int = 300):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embeddings = np.random.normal(
            0, 0.01, (vocab_size, embedding_dim)
        ).astype(np.float32)
    
    def embed(self, token_ids: List[int]) -> np.ndarray:
        """Get embeddings for token IDs."""
        return self.embeddings[token_ids]
    
    def embed_text(self, text_ids: List[int]) -> np.ndarray:
        """Average embedding for entire text."""
        embeds = self.embed(text_ids)
        return np.mean(embeds, axis=0)
    
    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Cosine similarity between two vectors."""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot / (norm1 * norm2 + 1e-8)
```

### 3.3 Training Foundation

#### `core/trainer.py` (stub)

```python
# Training loop scaffolding

class Trainer:
    """Base trainer class."""
    
    def __init__(self, model, optimizer, loss_fn):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.history = {"loss": [], "val_loss": []}
    
    def train_epoch(self, train_loader, epoch: int):
        """Train one epoch."""
        total_loss = 0
        for batch_idx, (x, y) in enumerate(train_loader):
            # Forward pass
            outputs = self.model(x)
            loss = self.loss_fn(outputs, y)
            
            # Backward pass
            self.optimizer.zero_grad()
            # loss.backward()  # When using PyTorch
            self.optimizer.step()
            
            total_loss += loss
        
        avg_loss = total_loss / len(train_loader)
        self.history["loss"].append(avg_loss)
        return avg_loss
```

---

## Hardware Optimization (NEW)

### 4.1 Detection & Profiling

```python
# Detect PC specs and optimize training parameters
# Already in ashley_ai_studio.py: HardwareMonitor class

# Usage:
hm = HardwareMonitor()
print(hm.get_report())  # CPU, GPU, RAM info
print(hm.optimize_for_training())  # Recommended params
```

### 4.2 Checkpoint System

```python
# Already in ashley_ai_studio.py: CheckpointManager class

# Usage:
ckpt_mgr = CheckpointManager()
ckpt_mgr.save("model_v1", model_data, {"epoch": 5})
latest = ckpt_mgr.load_latest("model_v1")
print(ckpt_mgr.get_summary())
```

---

## Quick Start

### Installation

```bash
# Clone
git clone https://github.com/flamebomb88/ashley-ai-studio.git
cd ashley-ai-studio

# Setup
python launcher.py --setup

# Or manually:
pip install -r requirements.txt
```

### Launch

```bash
# GUI (default)
python launcher.py

# Shell
python launcher.py --shell

# Hardware info
python launcher.py --hardware

# Optimize training
python launcher.py --optimize
```

---

## Next Steps (Phase 4+)

1. **Neural Network Core** — Implement basic feedforward network
2. **Training Pipeline** — Full training loop with loss/accuracy tracking
3. **Vector Search** — FAISS/ChromaDB integration
4. **Advanced Scanner** — Recursive project analysis
5. **RAG System** — Retrieval-augmented generation

---

*Last Updated: 2026-06-29*  
*Target Completion: 12 weeks*
