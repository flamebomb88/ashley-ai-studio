# Ashley AI Studio — System Requirements

## Minimum Specifications

- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **CPU**: 4-core processor (Intel i5/AMD Ryzen 5 or equivalent)
- **RAM**: 8GB (16GB recommended)
- **GPU**: Optional (NVIDIA RTX 2060 or better for acceleration)
- **Storage**: 20GB SSD (for code, models, datasets)
- **Python**: 3.9+ (3.10+ recommended)

## Installation

### Windows

```bash
# Download Python 3.10+ from python.org
# Install with "Add Python to PATH" checked

# Then:
git clone https://github.com/flamebomb88/ashley-ai-studio.git
cd ashley-ai-studio

pip install -r requirements.txt
python launcher.py --setup

python launcher.py  # Launch GUI
```

### macOS

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Clone and install
git clone https://github.com/flamebomb88/ashley-ai-studio.git
cd ashley-ai-studio
pip3 install -r requirements.txt
python3 launcher.py
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-dev

git clone https://github.com/flamebomb88/ashley-ai-studio.git
cd ashley-ai-studio
pip install -r requirements.txt
python launcher.py
```

## GPU Setup (Optional)

### NVIDIA CUDA

```bash
# Install CUDA Toolkit 11.8+
# Download from: https://developer.nvidia.com/cuda-downloads

# Then install PyTorch with CUDA:
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### AMD ROCm

```bash
# Install ROCm
# Download from: https://rocmdocs.amd.com/en/docs-5.4.2/

# Then install PyTorch with ROCm:
pip install torch --index-url https://download.pytorch.org/whl/rocm5.4
```

## Troubleshooting

### Python not found
```bash
# Check installation
python --version  # Should be 3.9+

# Or use python3
python3 --version
python3 launcher.py
```

### Module not found errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Tkinter not available (Linux)
```bash
# Install Tkinter
sudo apt install python3-tk
```

### GPU not detected
```bash
python launcher.py --hardware  # Check if CUDA available

# Install NVIDIA drivers:
# Download from: https://www.nvidia.com/Download/driverDetails.aspx
```

---

*Last Updated: 2026-06-29*
