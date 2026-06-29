# Ashley AI Studio — Hardware Optimization & Monitoring

## 🖥️ Hardware Detection

Ashley AI Studio automatically detects and optimizes for your hardware:

### Detected Specs
- **CPU**: Cores, frequency, temperature
- **RAM**: Total, available, usage
- **GPU**: NVIDIA (CUDA), AMD (ROCm), Intel (oneAPI)
- **VRAM**: Total VRAM, memory usage
- **Storage**: Available disk space
- **Motherboard**: BIOS version, chipset
- **OS**: Windows/macOS/Linux specifics

### Check Hardware

```bash
python launcher.py --hardware
```

Output:
```json
{
  "cpu": {
    "cores": 16,
    "freq_ghz": 3.6
  },
  "ram": {
    "total_gb": 32,
    "available_gb": 24
  },
  "gpu": {
    "cuda_available": true,
    "devices": ["NVIDIA GeForce RTX 3080"],
    "vram_total_gb": 10
  },
  "platform": {
    "os": "Windows",
    "release": "10",
    "arch": "AMD64"
  }
}
```

## 🚀 Training Optimization

### Auto-Recommend Parameters

```bash
python launcher.py --optimize
```

Output:
```
Recommended Training Parameters:
  batch_size: 128
  num_workers: 14
  device: cuda
  mixed_precision: true
  gradient_accumulation_steps: 1
  cache_size_mb: 2048
```

### Manual Configuration

```python
from ashley_ai_studio import HardwareMonitor

hm = HardwareMonitor()
recs = hm.optimize_for_training()

# Use in training
trainer = Trainer(
    batch_size=recs["batch_size"],
    num_workers=recs["num_workers"],
    device=recs["device"],
    mixed_precision=recs["mixed_precision"],
)
```

## 🌡️ Temperature & Power Management

### Monitor GPU Temperature

```python
import GPUtil

GPUs = GPUtil.getGPUs()
for gpu in GPUs:
    print(f"GPU {gpu.id}: {gpu.name}")
    print(f"  Temperature: {gpu.temperature}°C")
    print(f"  Load: {gpu.load*100}%")
    print(f"  Memory: {gpu.memoryUsed}/{gpu.memoryTotal} MB")
```

### Reduce Power Consumption

```python
# Reduce batch size if GPU overheats
if gpu.temperature > 80:
    batch_size = batch_size // 2
    print(f"GPU too hot! Reducing batch size to {batch_size}")

# Use mixed precision (FP16)
from torch.cuda.amp import autocast

with autocast():
    output = model(input)
```

### Fan Speed Management

```python
# Windows: Use NVIDIA drivers to manage fan
# nvidia-smi -pm 1  # Enable persistent mode
# nvidia-smi -pl 200  # Power limit (watts)

# Cool down if needed
time.sleep(30)  # Pause training
```

## 💾 Memory Management

### Cache Management

```python
import torch

# Clear GPU cache
torch.cuda.empty_cache()

# Reduce cache size
config.cache_mb = 512  # Default: 2048
```

### RAM Optimization

```python
# Profile memory usage
import psutil

process = psutil.Process()
print(f"RAM: {process.memory_info().rss / (1024**3):.2f} GB")

# Set memory limit
import resource
resource.setrlimit(resource.RLIMIT_AS, (8*1024**3, -1))  # 8GB limit
```

## 🔄 Checkpoint Recovery

### Save Checkpoints

```python
from ashley_ai_studio import CheckpointManager

ckpt = CheckpointManager()

# Save after each epoch
if epoch % 5 == 0:
    ckpt.save(
        "model_phase1",
        model_data={"weights": model.state_dict()},
        metadata={"epoch": epoch, "loss": loss}
    )
```

### Resume Training

```python
# Load latest checkpoint
latest = ckpt.load_latest("model_phase1")
if latest:
    print(f"Resuming from epoch {latest['metadata']['epoch']}")
    model.load_state_dict(latest['data']['weights'])
else:
    print("No checkpoint found, starting from scratch")
```

### Backup Strategy

```python
# Auto-backup important files
import shutil

shutil.copytree(
    "models/checkpoints",
    f"backups/checkpoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
)
```

## 📊 Performance Benchmarks

### CPU Benchmark

```python
import time
import numpy as np

start = time.time()
for _ in range(1000):
    np.dot(np.random.randn(1000), np.random.randn(1000))
elapsed = time.time() - start
print(f"CPU: {elapsed:.3f}s per 1000 dot products")
```

### GPU Benchmark

```python
import torch
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
a = torch.randn(10000, 10000, device=device)
b = torch.randn(10000, 10000, device=device)

torch.cuda.synchronize()
start = time.time()
for _ in range(100):
    c = torch.matmul(a, b)
torch.cuda.synchronize()
elapsed = time.time() - start
print(f"GPU: {elapsed:.3f}s per 100 matmuls")
```

### Training Speed Target

Based on hardware:

| Hardware | Samples/sec |
|----------|-------------|
| CPU (8c) | 50-100 |
| RTX 3060 | 1000-2000 |
| RTX 3080 | 3000-5000 |
| A100 | 10000+ |

---

*Last Updated: 2026-06-29*
