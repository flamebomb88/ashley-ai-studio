# Ashley AI Studio - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  ┌──────────────┬──────────────┬──────────────────────────┐  │
│  │ Text Editor  │ Chat Panel   │ Content Viewer (2D/3D)   │  │
│  │              │              │                          │  │
│  │ - File I/O   │ - Messaging  │ - Diffusion Waves        │  │
│  │ - Predictor  │ - Chatbot    │ - Physics Simulation     │  │
│  │ - Virtual KB │ - Commands   │ - 3D Rendering          │  │
│  └──────────────┴──────────────┴──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               Application Logic Layer                        │
│  ┌──────────────┬──────────────┬──────────────────────────┐  │
│  │  Text Proc   │  AI/ML Core  │  Media Processing        │  │
│  │              │              │                          │  │
│  │ - Tokenizer  │ - Embeddings │ - Audio (STT/TTS)        │  │
│  │ - Predictor  │ - Neural Net │ - Video Processing       │  │
│  │ - Grammar    │ - Transformers│- Image Generation      │  │
│  │ - Dictionary │ - Legacy AI  │ - Format Detection      │  │
│  └──────────────┴──────────────┴──────────────────────────┘  │
│                                                              │
│  ┌──────────────┬──────────────┬──────────────────────────┐  │
│  │ Diffusion    │  Game Engine │  Ashley AI Agent         │  │
│  │ Rendering    │              │                          │  │
│  │              │ - Physics    │ - Chatbot Logic         │  │
│  │ - Wave Sim   │ - Scene Mgmt │ - Code Generation       │  │
│  │ - 3D Mesh    │ - Animation  │ - Model Improvement     │  │
│  │ - Shaders    │ - Camera     │ - Error Detection       │  │
│  └──────────────┴──────────────┴──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Storage & Management Layer                      │
│  ┌──────────────┬──────────────┬──────────────────────────┐  │
│  │ Database     │ Vector Store │ File System              │  │
│  │              │              │                          │  │
│  │ - Metadata   │ - Embeddings │ - File Indexing         │  │
│  │ - Models     │ - Search     │ - Directory Management   │  │
│  │ - Vectors    │ - Weights    │ - Compression Handling  │  │
│  │ - Cache      │ - FAISS      │ - Content Analysis      │  │
│  └──────────────┴──────────────┴──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│  ┌──────────────┬──────────────┬──────────────────────────┐  │
│  │ GPU/CPU      │ Memory Mgmt  │ I/O & Networking        │  │
│  │              │              │                          │  │
│  │ - CUDA/ROCm  │ - Caching    │ - File I/O             │  │
│  │ - Threading  │ - Allocation │ - Network Bridge        │  │
│  │ - Optimization│ - Garbage   │ - Web Scraping         │  │
│  │ - Profiling  │   Collection │ - Local Browser        │  │
│  └──────────────┴──────────────┴──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Dependencies

```
UI Layer
   ↓
 Text Editor ← → Predictor ← → Tokenizer
   ↓              ↓              ↓
File I/O    Embeddings    Dictionary
   ↓              ↓              ↓
Database   Vector Store   Grammar Rules
   ↓              ↓              ↓
File System ← Search ← → Neural Network
   ↓              ↓              ↓
Metadata    Vectors      Transformers
   ↓              ↓              ↓
Backup  ← → Weights ← → Training Loop
```

## Data Flow

### Text Prediction Pipeline
```
User Input
    ↓
Text Cleaning & Normalization
    ↓
Tokenization (char/word/subword)
    ↓
Vocabulary Lookup
    ↓
Embedding Lookup (Vector)
    ↓
Neural Network Forward Pass
    ↓
Prediction Probabilities
    ↓
Top-K Sampling/Beam Search
    ↓
Display Suggestions
```

### Training Pipeline
```
Data Collection
    ↓
Content Scanning & Indexing
    ↓
Data Cleaning & Preprocessing
    ↓
Tokenization & Vectorization
    ↓
Batch Creation (Train/Val/Test)
    ↓
Training Loop
    ├─ Forward Pass
    ├─ Loss Calculation
    ├─ Backward Pass (Backpropagation)
    ├─ Weight Updates
    └─ Validation
    ↓
Model Checkpointing
    ↓
Evaluation Metrics
    ↓
Optimization & Fine-tuning
```

### Media Processing Pipeline
```
Audio/Video/Image Input
    ↓
Format Detection
    ↓
Codec/Decompression
    ↓
Feature Extraction
    ├─ Audio: MFCC, Spectral Features
    ├─ Video: Frame Detection, Motion
    └─ Image: Edge Detection, Segmentation
    ↓
Embedding Generation
    ↓
Vector Storage
    ↓
Search/Retrieval
```

## Database Schema

### Core Tables

```sql
-- Models and Checkpoints
CREATE TABLE models (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,  -- 'transformer', 'lstm', 'cnn', etc.
    version TEXT,
    created_at TIMESTAMP,
    parameters INTEGER,  -- Total params
    checkpoint_path TEXT,
    metadata JSON
);

-- Training Runs
CREATE TABLE training_runs (
    id INTEGER PRIMARY KEY,
    model_id INTEGER,
    dataset_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    epochs INTEGER,
    batch_size INTEGER,
    learning_rate REAL,
    final_loss REAL,
    final_accuracy REAL,
    FOREIGN KEY(model_id) REFERENCES models(id)
);

-- Embeddings/Vectors
CREATE TABLE vectors (
    id INTEGER PRIMARY KEY,
    content_id INTEGER,  -- Reference to content
    embedding BLOB,  -- Serialized numpy array
    dimension INTEGER,
    norm REAL,  -- L2 norm
    created_at TIMESTAMP
);

-- Weights and Biases
CREATE TABLE network_weights (
    id INTEGER PRIMARY KEY,
    model_id INTEGER,
    layer_id INTEGER,
    name TEXT,
    shape TEXT,  -- JSON array
    data BLOB,
    updated_at TIMESTAMP,
    FOREIGN KEY(model_id) REFERENCES models(id)
);

-- File Index
CREATE TABLE file_index (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE,
    file_type TEXT,
    size INTEGER,
    content_hash TEXT,
    indexed_at TIMESTAMP,
    metadata JSON
);

-- Content (text, code, etc.)
CREATE TABLE content (
    id INTEGER PRIMARY KEY,
    file_id INTEGER,
    type TEXT,  -- 'text', 'code', 'image', 'audio', 'video'
    data BLOB,
    tokens INTEGER,
    vector_id INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY(file_id) REFERENCES file_index(id),
    FOREIGN KEY(vector_id) REFERENCES vectors(id)
);

-- Vocabulary
CREATE TABLE vocabulary (
    id INTEGER PRIMARY KEY,
    token TEXT UNIQUE,
    token_id INTEGER UNIQUE,
    frequency INTEGER,
    embedding_id INTEGER,
    FOREIGN KEY(embedding_id) REFERENCES vectors(id)
);

-- Training Metrics
CREATE TABLE training_metrics (
    id INTEGER PRIMARY KEY,
    training_run_id INTEGER,
    epoch INTEGER,
    batch_idx INTEGER,
    train_loss REAL,
    val_loss REAL,
    train_accuracy REAL,
    val_accuracy REAL,
    learning_rate REAL,
    timestamp TIMESTAMP,
    FOREIGN KEY(training_run_id) REFERENCES training_runs(id)
);
```

## Module Structure

```
ashley_ai_studio/
├── core/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── logger.py           # Logging system
│   ├── errors.py           # Custom exceptions
│   └── utils.py            # Utility functions
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Main application window
│   ├── editor.py           # Text editor widget
│   ├── chat_panel.py       # Chat/messaging panel
│   ├── viewer_3d.py        # 3D content viewer
│   ├── virtual_keyboard.py # Virtual keyboard
│   └── themes/
│       └── default.css
│
├── text_processing/
│   ├── __init__.py
│   ├── tokenizer.py        # Tokenization
│   ├── predictor.py        # Text/word prediction
│   ├── grammar.py          # Grammar analysis
│   └── dictionary.py       # Dictionary management
│
├── ai_ml/
│   ├── __init__.py
│   ├── neural_network.py   # Neural network framework
│   ├── embeddings.py       # Word/sentence embeddings
│   ├── transformers.py     # Transformer components
│   ├── legacy_ai.py        # Deep Blue, ELIZA, etc.
│   ├── trainer.py          # Training loop
│   └── inference.py        # Model inference
│
├── media/
│   ├── __init__.py
│   ├── audio.py            # Audio I/O and processing
│   ├── video.py            # Video processing
│   ├── image.py            # Image processing
│   ├── tts.py              # Text-to-speech
│   └── stt.py              # Speech-to-text
│
├── diffusion/
│   ├── __init__.py
│   ├── physics.py          # Wave/fluid physics
│   ├── renderer.py         # Graphics rendering
│   ├── shaders/
│   │   ├── vertex.glsl
│   │   └── fragment.glsl
│   └── 3d_mesh.py          # 3D mesh generation
│
├── game_engine/
│   ├── __init__.py
│   ├── physics.py          # Physics simulation
│   ├── scene.py            # Scene management
│   ├── animation.py        # Animation system
│   └── camera.py           # Camera controls
│
├── database/
│   ├── __init__.py
│   ├── connection.py       # Database connection
│   ├── schema.py           # Schema management
│   ├── models.py           # ORM models
│   └── vector_store.py     # Vector storage (FAISS)
│
├── file_management/
│   ├── __init__.py
│   ├── scanner.py          # File scanning
│   ├── indexer.py          # File indexing
│   ├── compression.py      # Compression handling
│   └── cache.py            # Caching system
│
├── ashley/
│   ├── __init__.py
│   ├── agent.py            # Ashley AI agent
│   ├── chatbot.py          # Chatbot logic
│   ├── code_gen.py         # Code generation
│   └── model_improver.py   # Model improvement
│
├── tools/
│   ├── __init__.py
│   ├── data_scanner.py     # Command-line data scanner
│   ├── preprocessor.py     # Data preprocessing
│   ├── monitor.py          # Training monitor
│   └── evaluator.py        # Model evaluation
│
└── launcher.py             # Application entry point
```

## Configuration

```yaml
# config.yaml

app:
  name: Ashley AI Studio
  version: 0.1.0
  debug: false
  log_level: INFO

ui:
  theme: dark
  default_font_size: 12
  editor_line_numbers: true
  syntax_highlighting: true

database:
  type: sqlite  # sqlite, postgresql
  path: ./data/ashley.db
  vector_store: faiss  # faiss, pinecone, milvus
  vector_dim: 768

model:
  type: transformer
  vocab_size: 50000
  embedding_dim: 768
  num_layers: 12
  num_heads: 12
  hidden_dim: 3072
  dropout: 0.1
  max_seq_length: 512

training:
  batch_size: 64
  learning_rate: 0.001
  optimizer: adam
  num_epochs: 100
  early_stopping_patience: 5
  checkpoint_dir: ./checkpoints

media:
  tts_voice: zira
  audio_sample_rate: 16000
  audio_channels: 1

performance:
  use_gpu: true
  gpu_id: 0
  mixed_precision: true
  num_workers: 4
  cache_size_mb: 1024
```

---

## Key Integration Points

1. **Text Editor ↔ Predictor**: Real-time predictions as user types
2. **Predictor ↔ Neural Network**: Forward pass for predictions
3. **Training Loop ↔ Vector Store**: Store and retrieve embeddings
4. **File Scanner ↔ Database**: Index files and content
5. **Ashley Agent ↔ All Components**: Orchestrate functionality
6. **UI ↔ 3D Viewer**: Real-time diffusion visualization

---

*Last Updated: 2026-06-29*
