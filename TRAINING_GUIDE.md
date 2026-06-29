# Ashley AI Studio - Training & Data Management Guide

## Overview

This guide explains how Ashley AI's training pipeline works, including:
- Data preparation and indexing
- Vector and weight training
- Model checkpointing and evaluation
- Performance monitoring
- Optimization strategies

---

## Part 1: Neural Network Fundamentals

### How Neural Networks Work

#### Layer Architecture
```
Input Layer (Features)
    ↓
[Hidden Layer 1] → Weights + Bias → Activation → Dropout
    ↓
[Hidden Layer 2] → Weights + Bias → Activation → Dropout
    ↓
[Output Layer] → Weights + Bias → Softmax/Sigmoid
    ↓
Output (Predictions)
```

#### Forward Pass (Inference)
```python
# For each neuron:
output = activation_function(dot_product(input, weights) + bias)

# Example (ReLU):
hidden_layer_output = max(0, input @ weights + bias)
```

#### Backward Pass (Training)
```python
# Calculate loss gradient
loss_gradient = (predictions - targets)

# Backpropagation through layers (chain rule)
for each layer (from output to input):
    weight_gradient = input^T @ loss_gradient
    bias_gradient = sum(loss_gradient)
    input_gradient = loss_gradient @ weights^T
    
    # Update parameters
    weights -= learning_rate * weight_gradient
    bias -= learning_rate * bias_gradient
```

### Weight Initialization

#### Why Initialization Matters
- Poor initialization → Vanishing/exploding gradients
- Random uniform: `U(-√6/(n_in+n_out), √6/(n_in+n_out))`
- Xavier initialization: `σ = √(2/(n_in+n_out))`
- He initialization: `σ = √(2/n_in)` (for ReLU)

```python
# Xavier initialization
weights = np.random.normal(loc=0, scale=np.sqrt(2/(n_in+n_out)), 
                           size=(n_in, n_out))
bias = np.zeros(n_out)
```

### Activation Functions

| Function | Formula | Range | Use Case |
|----------|---------|-------|----------|
| ReLU | max(0, x) | [0, ∞) | Hidden layers (default) |
| Sigmoid | 1/(1+e^(-x)) | (0, 1) | Binary classification output |
| Softmax | e^x / Σ(e^x) | (0, 1) sum=1 | Multi-class output |
| Tanh | (e^x - e^(-x))/(e^x + e^(-x)) | (-1, 1) | LSTM/GRU |
| LeakyReLU | max(αx, x) | (-∞, ∞) | Gradient flow |

---

## Part 2: Training Pipeline

### Phase 1: Data Preparation

#### 1.1 Data Collection
```python
def scan_database(database_path):
    """
    Recursively scan database directory and collect all files.
    """
    files = []
    for root, dirs, filenames in os.walk(database_path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            file_info = {
                'path': filepath,
                'size': os.path.getsize(filepath),
                'type': get_file_type(filepath),
                'modified': os.path.getmtime(filepath)
            }
            files.append(file_info)
    return files
```

#### 1.2 File Type Detection & Processing
```python
def process_file(filepath, file_type):
    """
    Process different file types and extract content.
    """
    if file_type == 'text':
        return read_text_file(filepath)
    elif file_type == 'image':
        return extract_image_features(filepath)
    elif file_type == 'audio':
        return extract_audio_features(filepath)
    elif file_type == 'video':
        return extract_video_frames(filepath)
    elif file_type == 'compressed':
        return extract_compressed_file(filepath)
    # ... more types
```

#### 1.3 Data Cleaning
```python
def clean_text(text):
    """
    Normalize and clean text data.
    """
    # Remove special characters (optional)
    text = re.sub(r'[^a-zA-Z0-9\s\.]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove very short tokens
    tokens = text.split()
    tokens = [t for t in tokens if len(t) > 1]
    
    return ' '.join(tokens)
```

#### 1.4 Dataset Splits
```python
def split_dataset(data, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """
    Split data into train/val/test sets.
    """
    n = len(data)
    indices = np.random.permutation(n)
    
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    train_data = [data[i] for i in indices[:train_end]]
    val_data = [data[i] for i in indices[train_end:val_end]]
    test_data = [data[i] for i in indices[val_end:]]
    
    return train_data, val_data, test_data
```

### Phase 2: Vectorization & Embeddings

#### 2.1 Tokenization
```python
def tokenize(text):
    """
    Convert text into tokens.
    """
    # Character-level
    char_tokens = list(text)
    
    # Word-level
    word_tokens = text.split()
    
    # Subword (BPE - simplified)
    subword_tokens = bpe_encode(text)
    
    return word_tokens  # Use word-level for most tasks

def build_vocabulary(texts, vocab_size=50000):
    """
    Build vocabulary from texts.
    """
    counter = Counter()
    for text in texts:
        tokens = tokenize(text)
        counter.update(tokens)
    
    # Get most common tokens
    vocab = [token for token, _ in counter.most_common(vocab_size)]
    
    # Create token-to-ID mapping
    token_to_id = {token: idx for idx, token in enumerate(vocab)}
    id_to_token = {idx: token for token, idx in token_to_id.items()}
    
    return token_to_id, id_to_token

def text_to_ids(text, token_to_id, max_length=512):
    """
    Convert text to token IDs.
    """
    tokens = tokenize(text)
    ids = [token_to_id.get(token, 0) for token in tokens]  # 0 = unknown
    
    # Pad or truncate
    if len(ids) < max_length:
        ids += [0] * (max_length - len(ids))
    else:
        ids = ids[:max_length]
    
    return np.array(ids)
```

#### 2.2 Word Embeddings
```python
class WordEmbedding:
    """
    Create word embeddings using basic lookup table.
    """
    def __init__(self, vocab_size, embedding_dim):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        # Initialize embedding matrix
        self.embeddings = np.random.normal(
            0, 0.01, (vocab_size, embedding_dim)
        )
    
    def embed(self, token_ids):
        """
        Convert token IDs to embedding vectors.
        """
        return self.embeddings[token_ids]
    
    def embed_text(self, text, token_to_id):
        """
        Embed entire text (average of word embeddings).
        """
        ids = text_to_ids(text, token_to_id)
        embeddings = self.embed(ids)
        return np.mean(embeddings, axis=0)  # Average pooling
```

#### 2.3 Vector Storage
```python
class VectorStore:
    """
    Store and retrieve vectors efficiently.
    """
    def __init__(self, embedding_dim):
        self.embedding_dim = embedding_dim
        self.vectors = []
        self.metadata = []
        self.index = None
    
    def add(self, vector, metadata=None):
        """
        Add vector to store.
        """
        assert len(vector) == self.embedding_dim
        self.vectors.append(vector)
        self.metadata.append(metadata or {})
    
    def build_index(self):
        """
        Build FAISS index for fast similarity search.
        """
        import faiss
        
        vectors = np.array(self.vectors).astype('float32')
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(vectors)
    
    def search(self, query_vector, k=10):
        """
        Find k nearest neighbors to query vector.
        """
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            results.append({
                'index': idx,
                'distance': distance,
                'metadata': self.metadata[idx]
            })
        return results
```

### Phase 3: Training Loop

#### 3.1 Basic Training Loop
```python
def train_epoch(model, train_loader, optimizer, criterion, epoch):
    """
    Train for one epoch.
    """
    model.train()  # Set to training mode
    total_loss = 0
    
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        
        # Backward pass
        optimizer.zero_grad()  # Clear gradients
        loss.backward()  # Calculate gradients
        optimizer.step()  # Update weights
        
        total_loss += loss.item()
        
        if (batch_idx + 1) % 100 == 0:
            print(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}")
    
    avg_loss = total_loss / len(train_loader)
    return avg_loss

def validate(model, val_loader, criterion):
    """
    Validate model performance.
    """
    model.eval()  # Set to evaluation mode
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():  # Don't calculate gradients
        for inputs, targets in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            
            # Calculate accuracy
            _, predicted = torch.max(outputs.data, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()
    
    avg_loss = total_loss / len(val_loader)
    accuracy = 100 * correct / total
    
    return avg_loss, accuracy

def train_model(model, train_loader, val_loader, num_epochs, learning_rate):
    """
    Full training procedure.
    """
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    best_val_loss = float('inf')
    patience = 5
    patience_counter = 0
    
    for epoch in range(num_epochs):
        # Train
        train_loss = train_epoch(model, train_loader, optimizer, criterion, epoch)
        
        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion)
        
        print(f"Epoch {epoch}: Train Loss={train_loss:.4f}, "
              f"Val Loss={val_loss:.4f}, Val Acc={val_acc:.2f}%")
        
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            # Save best model
            torch.save(model.state_dict(), 'best_model.pth')
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping after {epoch} epochs")
                break
```

#### 3.2 Optimizers

| Optimizer | Update Rule | Pros | Cons |
|-----------|-------------|------|------|
| SGD | w -= lr * ∇L | Simple, stable | Slow convergence |
| Momentum | Uses velocity | Faster convergence | More hyperparameters |
| Adam | Adaptive learning rate | Fast, adaptive | Memory intensive |
| RMSprop | Root mean square | Good for RNNs | Less stable |

```python
# SGD with Momentum
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam (recommended)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))

# RMSprop
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01)
```

#### 3.3 Learning Rate Scheduling
```python
def learning_rate_schedule(epoch, initial_lr=0.001):
    """
    Decay learning rate over time.
    """
    # Step decay
    if epoch < 10:
        return initial_lr
    elif epoch < 20:
        return initial_lr * 0.5
    else:
        return initial_lr * 0.1

# Cosine annealing
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=num_epochs
)

# Step decay
scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer, step_size=10, gamma=0.1
)
```

### Phase 4: Weight & Bias Optimization

#### 4.1 Gradient Descent Variants
```python
def gradient_descent_step(weights, bias, gradient_w, gradient_b, learning_rate):
    """
    Standard gradient descent update.
    """
    weights -= learning_rate * gradient_w
    bias -= learning_rate * gradient_b
    return weights, bias

def momentum_update(weights, bias, gradient_w, gradient_b, 
                    velocity_w, velocity_b, learning_rate, momentum=0.9):
    """
    Update with momentum (faster convergence).
    """
    velocity_w = momentum * velocity_w - learning_rate * gradient_w
    velocity_b = momentum * velocity_b - learning_rate * gradient_b
    
    weights += velocity_w
    bias += velocity_b
    
    return weights, bias, velocity_w, velocity_b

def adam_update(weights, bias, gradient_w, gradient_b,
                m_w, m_b, v_w, v_b, learning_rate=0.001, 
                beta1=0.9, beta2=0.999, epsilon=1e-8, t=1):
    """
    Adaptive Moment Estimation (Adam) - combines momentum and adaptive learning rate.
    """
    # Update biased first moment (mean)
    m_w = beta1 * m_w + (1 - beta1) * gradient_w
    m_b = beta1 * m_b + (1 - beta1) * gradient_b
    
    # Update biased second moment (variance)
    v_w = beta2 * v_w + (1 - beta2) * (gradient_w ** 2)
    v_b = beta2 * v_b + (1 - beta2) * (gradient_b ** 2)
    
    # Bias correction
    m_w_hat = m_w / (1 - beta1 ** t)
    m_b_hat = m_b / (1 - beta1 ** t)
    v_w_hat = v_w / (1 - beta2 ** t)
    v_b_hat = v_b / (1 - beta2 ** t)
    
    # Update parameters
    weights -= learning_rate * m_w_hat / (np.sqrt(v_w_hat) + epsilon)
    bias -= learning_rate * m_b_hat / (np.sqrt(v_b_hat) + epsilon)
    
    return weights, bias, m_w, m_b, v_w, v_b
```

#### 4.2 Regularization
```python
def l1_regularization(weights, lambda_l1):
    """
    L1 regularization (sparsity).
    """
    return lambda_l1 * np.sum(np.abs(weights))

def l2_regularization(weights, lambda_l2):
    """
    L2 regularization (weight decay).
    """
    return lambda_l2 * np.sum(weights ** 2)

def dropout(activations, dropout_rate=0.5):
    """
    Dropout during training (random neuron deactivation).
    """
    mask = np.random.binomial(1, 1 - dropout_rate, activations.shape)
    return activations * mask / (1 - dropout_rate)

def batch_normalization(activations, epsilon=1e-5):
    """
    Normalize activations for faster training.
    """
    mean = np.mean(activations, axis=0)
    variance = np.var(activations, axis=0)
    normalized = (activations - mean) / np.sqrt(variance + epsilon)
    return normalized
```

### Phase 5: Model Checkpointing

```python
def save_checkpoint(model, optimizer, epoch, loss, filepath):
    """
    Save model checkpoint.
    """
    checkpoint = {
        'epoch': epoch,
        'model_state': model.state_dict(),
        'optimizer_state': optimizer.state_dict(),
        'loss': loss,
        'timestamp': time.time()
    }
    torch.save(checkpoint, filepath)
    print(f"Checkpoint saved to {filepath}")

def load_checkpoint(model, optimizer, filepath):
    """
    Load model checkpoint.
    """
    checkpoint = torch.load(filepath)
    model.load_state_dict(checkpoint['model_state'])
    optimizer.load_state_dict(checkpoint['optimizer_state'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']
    return model, optimizer, epoch, loss
```

---

## Part 3: Search-Based Training

### 3.1 Vector Search for Training
```python
def mining_hard_negatives(query_embedding, all_embeddings, all_labels, 
                          query_label, num_negatives=10):
    """
    Find hard negative examples using vector search.
    Useful for metric learning and triplet loss.
    """
    # Calculate distances
    distances = cosine_distance(query_embedding, all_embeddings)
    
    # Get negatives (different label, sorted by distance)
    negatives = []
    for idx, distance in enumerate(sorted(range(len(distances)), 
                                          key=lambda i: distances[i])):
        if all_labels[idx] != query_label:
            negatives.append((idx, distance))
        if len(negatives) >= num_negatives:
            break
    
    return negatives

def create_triplets(embeddings, labels):
    """
    Create triplets (anchor, positive, negative) for triplet loss training.
    """
    triplets = []
    
    for anchor_idx, anchor_label in enumerate(labels):
        # Find positive (same label)
        positives = [i for i, l in enumerate(labels) if l == anchor_label and i != anchor_idx]
        
        if positives:
            positive_idx = random.choice(positives)
            
            # Find hard negative using vector search
            hard_negatives = mining_hard_negatives(
                embeddings[anchor_idx], embeddings, labels, anchor_label
            )
            
            if hard_negatives:
                negative_idx = hard_negatives[0][0]
                triplets.append((anchor_idx, positive_idx, negative_idx))
    
    return triplets
```

---

## Part 4: Performance Monitoring

### 4.1 Training Metrics
```python
class TrainingMetrics:
    def __init__(self):
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        self.learning_rates = []
    
    def record(self, train_loss, val_loss, train_acc, val_acc, lr):
        self.train_losses.append(train_loss)
        self.val_losses.append(val_loss)
        self.train_accuracies.append(train_acc)
        self.val_accuracies.append(val_acc)
        self.learning_rates.append(lr)
    
    def plot(self):
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Loss
        axes[0, 0].plot(self.train_losses, label='Train')
        axes[0, 0].plot(self.val_losses, label='Validation')
        axes[0, 0].set_title('Loss')
        axes[0, 0].legend()
        
        # Accuracy
        axes[0, 1].plot(self.train_accuracies, label='Train')
        axes[0, 1].plot(self.val_accuracies, label='Validation')
        axes[0, 1].set_title('Accuracy')
        axes[0, 1].legend()
        
        # Learning Rate
        axes[1, 0].plot(self.learning_rates)
        axes[1, 0].set_title('Learning Rate')
        
        plt.tight_layout()
        plt.show()
```

### 4.2 Vector Weight Analysis
```python
def analyze_weights(model):
    """
    Analyze weight statistics.
    """
    stats = {}
    
    for name, param in model.named_parameters():
        if 'weight' in name:
            w = param.data.numpy()
            stats[name] = {
                'mean': np.mean(w),
                'std': np.std(w),
                'min': np.min(w),
                'max': np.max(w),
                'sparsity': np.sum(w == 0) / w.size
            }
    
    return stats

def check_gradients(model):
    """
    Detect vanishing/exploding gradients.
    """
    max_grad = 0
    
    for param in model.parameters():
        if param.grad is not None:
            grad_norm = param.grad.data.norm(2).item()
            max_grad = max(max_grad, grad_norm)
    
    if max_grad > 10:
        print(f"WARNING: Large gradient detected: {max_grad}")
    elif max_grad < 1e-7:
        print(f"WARNING: Small gradient detected: {max_grad} (vanishing gradients)")
    
    return max_grad
```

---

## Part 5: Optimization & Efficiency

### 5.1 Speed Optimization
```python
# Use batch processing
batch_size = 64  # Process 64 samples at once

# Use GPU acceleration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Use mixed precision (faster computation)
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    outputs = model(inputs)  # Faster computation in float16
    loss = criterion(outputs, targets)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 5.2 Memory Optimization
```python
# Gradient accumulation (simulate larger batches)
accumulation_steps = 4

for i, (inputs, targets) in enumerate(train_loader):
    outputs = model(inputs)
    loss = criterion(outputs, targets) / accumulation_steps
    loss.backward()  # Accumulate gradients
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# Model pruning (remove small weights)
def prune_weights(model, threshold=0.001):
    for param in model.parameters():
        param.data[torch.abs(param.data) < threshold] = 0

# Quantization (reduce precision)
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

---

## Part 6: Prompt Engineering & Token Management

### 6.1 Token Generation
```python
def generate_tokens(prompt, num_tokens=100, temperature=1.0):
    """
    Generate tokens using language model.
    """
    tokens = []
    input_tokens = tokenize(prompt)
    
    for _ in range(num_tokens):
        # Get model prediction
        next_token_logits = model.predict(input_tokens)
        
        # Apply temperature (control randomness)
        next_token_logits /= temperature
        
        # Convert to probabilities
        probabilities = softmax(next_token_logits)
        
        # Sample next token
        next_token = np.random.choice(vocab_size, p=probabilities)
        tokens.append(next_token)
        input_tokens.append(next_token)
    
    return tokens

def beam_search(prompt, num_beams=5, max_length=100):
    """
    Generate sequences using beam search (better quality).
    """
    beams = [[tokenize(prompt), 0.0]]  # [tokens, score]
    
    for _ in range(max_length):
        new_beams = []
        
        for tokens, score in beams:
            # Get predictions for next token
            logits = model.predict(tokens)
            top_k = np.argsort(logits)[-num_beams:]
            
            for token_id in top_k:
                new_tokens = tokens + [token_id]
                new_score = score + logits[token_id]
                new_beams.append([new_tokens, new_score])
        
        # Keep top num_beams sequences
        beams = sorted(new_beams, key=lambda x: x[1], reverse=True)[:num_beams]
    
    return beams[0][0]  # Return best sequence
```

### 6.2 Prompt Templates
```python
# Few-shot learning
few_shot_prompt = """
Examples:
Input: "How are you?"
Output: "I am doing well, thank you for asking."

Input: "What is 2+2?"
Output: "2+2 equals 4."

Now answer:
Input: "{user_input}"
Output:
"""

# Chain-of-thought
cot_prompt = """
Let me solve this step by step:
1. First, I will identify the key information
2. Then, I will think about the approach
3. Finally, I will provide the answer

Question: {question}
Thinking: ...
Answer:
"""
```

---

## Quick Reference: Training Commands

```bash
# Scan database and prepare data
python -m ashley.tools.data_scanner --database /path/to/database --output data.json

# Preprocess and vectorize
python -m ashley.tools.preprocessor --input data.json --output vectors.npy --vocab vocab.json

# Train model
python -m ashley.train --config config.yaml --epochs 100 --batch-size 64

# Monitor training
python -m ashley.tools.monitor --log-dir ./logs --tensorboard

# Evaluate model
python -m ashley.evaluate --model checkpoints/best_model.pth --test-data test.json

# Generate predictions
python -m ashley.generate --model checkpoints/best_model.pth --prompt "Hello" --num-tokens 50
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Loss not decreasing | Learning rate too high | Reduce learning rate |
| Training too slow | Batch size too small | Increase batch size |
| Out of memory | Model too large | Reduce batch size or model size |
| Overfitting | Training too long | Use early stopping or dropout |
| Underfitting | Model too small | Increase model capacity |
| NaN loss | Exploding gradients | Use gradient clipping |
| Stuck in local minimum | Poor initialization | Try different random seed |

---

*Last Updated: 2026-06-29*
