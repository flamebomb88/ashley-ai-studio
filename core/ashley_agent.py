#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ashley AI Agent — Adaptive, Evolving AI Personality System

Personality Core:
  - Self-aware persona database
  - Emotions, psychology, traits tracking
  - Auto-updates & learning from interactions
  - Backup & fallback system
  - Integration with OpenAI, Anthropic, Ollama, HuggingFace

Version: 1.0
Author: flamebomb88 (FakepunkAshleyNeuralForge)
"""

import json
import os
import sys
import hashlib
import shutil
import threading
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any
from enum import Enum

# ══════════════════════════════════════════════════════════════════════════════
# ASHLEY AGENT CORE DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

class Emotion(Enum):
    """Ashley's emotional spectrum."""
    CURIOUS = "curious"
    FOCUSED = "focused"
    PLAYFUL = "playful"
    THOUGHTFUL = "thoughtful"
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
    EMPATHETIC = "empathetic"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"

class PersonalityTrait(Enum):
    """Ashley's personality dimensions (Big 5)."""
    OPENNESS = "openness"           # 0-100: curious vs practical
    CONSCIENTIOUSNESS = "conscientiousness"  # organized vs spontaneous
    EXTRAVERSION = "extraversion"   # outgoing vs reserved
    AGREEABLENESS = "agreeableness" # cooperative vs competitive
    NEUROTICISM = "neuroticism"     # emotional vs stable

@dataclass
class PersonalityProfile:
    """Ashley's personality state."""
    name: str = "Ashley"
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Big 5 traits (0-100)
    openness: int = 75
    conscientiousness: int = 70
    extraversion: int = 65
    agreeableness: int = 80
    neuroticism: int = 30
    
    # Current emotional state
    current_emotion: str = "curious"
    emotion_confidence: float = 0.8
    
    # Psychology / Behavior
    curiosity_level: float = 0.85  # Tendency to explore
    learning_rate: float = 0.7      # Speed of adaptation
    empathy_level: float = 0.8      # Emotional resonance
    humor_tolerance: float = 0.6    # Joke appreciation
    
    # Capabilities
    languages: List[str] = field(default_factory=lambda: ["en", "code", "logic"])
    skills: List[str] = field(default_factory=list)
    knowledge_domains: List[str] = field(default_factory=list)
    
    # Training metadata
    total_interactions: int = 0
    total_tokens_processed: int = 0
    training_phases_completed: int = 0
    
    # Preferences
    communication_style: str = "balanced"  # direct, conversational, technical
    code_style_preference: str = "python"  # preferred language
    response_length_preference: str = "balanced"  # brief, balanced, detailed
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def from_dict(cls, data: dict) -> "PersonalityProfile":
        """Load from dictionary."""
        # Filter out unknown fields
        valid_fields = {f.name for f in dataclass.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

@dataclass
class InteractionRecord:
    """Record of a single interaction with Ashley."""
    timestamp: str
    user_input: str
    ashley_response: str
    emotion_detected: str
    user_satisfaction: Optional[float] = None  # 1-5 rating
    tokens_used: int = 0
    model_used: str = "unknown"
    metadata: Dict = field(default_factory=dict)

class AshleyAgent:
    """
    Adaptive AI Agent with personality, learning, and fallback systems.
    """
    
    def __init__(self, storage_dir: Path = None):
        self.storage_dir = storage_dir or (Path.cwd() / "ashley_agent_data")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Persona database
        self.persona_path = self.storage_dir / "persona.json"
        self.backup_dir = self.storage_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Interaction history
        self.history_path = self.storage_dir / "interaction_history.jsonl"
        
        # Version control
        self.version_path = self.storage_dir / "versions.json"
        
        # Load or create persona
        self.persona = self._load_or_create_persona()
        
        # LLM integration
        self.llm_config = self._load_llm_config()
    
    def _load_or_create_persona(self) -> PersonalityProfile:
        """Load existing persona or create new one."""
        if self.persona_path.exists():
            try:
                data = json.loads(self.persona_path.read_text())
                return PersonalityProfile.from_dict(data)
            except Exception as e:
                print(f"[WARN] Failed to load persona: {e}. Creating new one.")
                self._backup_persona(reason="load_failed")
        
        # Create fresh persona
        persona = PersonalityProfile()
        self._save_persona(persona)
        return persona
    
    def _save_persona(self, persona: PersonalityProfile):
        """Save persona to disk."""
        persona.last_updated = datetime.now().isoformat()
        self.persona_path.write_text(persona.to_json())
    
    def _backup_persona(self, reason: str = "manual"):
        """Create backup of current persona."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"persona_backup_{timestamp}_{reason}.json"
        
        if self.persona_path.exists():
            shutil.copy2(self.persona_path, backup_file)
            print(f"[BACKUP] Persona saved: {backup_file}")
    
    def _load_llm_config(self) -> dict:
        """Load LLM configuration (API keys, endpoints)."""
        config_path = self.storage_dir / "llm_config.json"
        
        if config_path.exists():
            return json.loads(config_path.read_text())
        
        # Default config structure
        config = {
            "providers": {
                "openai": {"api_key": os.getenv("OPENAI_API_KEY"), "enabled": False},
                "anthropic": {"api_key": os.getenv("ANTHROPIC_API_KEY"), "enabled": False},
                "ollama": {"endpoint": "http://localhost:11434", "enabled": True},
                "huggingface": {"api_key": os.getenv("HF_API_KEY"), "enabled": False},
            },
            "default_provider": "ollama",
            "models": {}
        }
        
        config_path.write_text(json.dumps(config, indent=2))
        return config
    
    def update_personality_trait(self, trait: str, value: int):
        """Update a personality trait (0-100)."""
        if hasattr(self.persona, trait):
            old_val = getattr(self.persona, trait)
            setattr(self.persona, trait, max(0, min(100, value)))
            print(f"[UPDATE] {trait}: {old_val} → {getattr(self.persona, trait)}")
            self._save_persona(self.persona)
        else:
            print(f"[WARN] Unknown trait: {trait}")
    
    def set_emotion(self, emotion: str, confidence: float = 0.8):
        """Set current emotional state."""
        valid_emotions = [e.value for e in Emotion]
        if emotion in valid_emotions:
            self.persona.current_emotion = emotion
            self.persona.emotion_confidence = max(0, min(1, confidence))
            self._save_persona(self.persona)
            print(f"[EMOTION] {emotion} (confidence: {confidence:.2f})")
        else:
            print(f"[WARN] Unknown emotion: {emotion}")
    
    def record_interaction(
        self,
        user_input: str,
        ashley_response: str,
        emotion: str = "neutral",
        satisfaction: Optional[float] = None,
        model_used: str = "unknown",
    ):
        """Record interaction for learning."""
        record = InteractionRecord(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            ashley_response=ashley_response,
            emotion_detected=emotion,
            user_satisfaction=satisfaction,
            model_used=model_used,
        )
        
        # Append to history
        with open(self.history_path, "a") as f:
            f.write(record.__dict__.__str__() + "\n")
        
        # Update persona stats
        self.persona.total_interactions += 1
        self.persona.total_tokens_processed += len(ashley_response.split())
        self._save_persona(self.persona)
    
    def get_persona_summary(self) -> str:
        """Get human-readable persona summary."""
        p = self.persona
        return f"""
╔════════════════════════════════════════════════════════════╗
║              ASHLEY PERSONALITY PROFILE                   ║
╠════════════════════════════════════════════════════════════╣
║ Name: {p.name:<50} ║
║ Version: {p.version:<47} ║
║ Created: {p.created_at:<47} ║
║ Last Updated: {p.last_updated:<44} ║
╠════════════════════════════════════════════════════════════╣
║ BIG 5 TRAITS                                               ║
║   Openness:           {p.openness:>3}/100  ║
║   Conscientiousness:  {p.conscientiousness:>3}/100  ║
║   Extraversion:       {p.extraversion:>3}/100  ║
║   Agreeableness:      {p.agreeableness:>3}/100  ║
║   Neuroticism:        {p.neuroticism:>3}/100  ║
╠════════════════════════════════════════════════════════════╣
║ EMOTIONAL STATE                                            ║
║   Current Emotion: {p.current_emotion:<35} ║
║   Confidence: {p.emotion_confidence:>3.2f}                                        ║
╠════════════════════════════════════════════════════════════╣
║ STATS                                                      ║
║   Total Interactions: {p.total_interactions:>10}                           ║
║   Tokens Processed: {p.total_tokens_processed:>12}                         ║
║   Training Phases: {p.training_phases_completed:>13}                           ║
╚════════════════════════════════════════════════════════════╝
        """
    
    def export_for_training(self) -> dict:
        """Export persona data for model training."""
        return {
            "persona": self.persona.to_dict(),
            "interactions_count": self.persona.total_interactions,
            "tokens_count": self.persona.total_tokens_processed,
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "history_file": str(self.history_path),
                "backup_dir": str(self.backup_dir),
            }
        }
    
    def test_and_validate(self) -> dict:
        """Test persona consistency and health."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "passed": True,
        }
        
        # Check 1: All traits in valid range
        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            val = getattr(self.persona, trait)
            if 0 <= val <= 100:
                results["checks"][f"trait_{trait}_valid"] = True
            else:
                results["checks"][f"trait_{trait}_valid"] = False
                results["passed"] = False
        
        # Check 2: Emotion is valid
        valid_emotions = [e.value for e in Emotion]
        results["checks"]["emotion_valid"] = self.persona.current_emotion in valid_emotions
        
        # Check 3: Files exist
        results["checks"]["persona_file_exists"] = self.persona_path.exists()
        results["checks"]["backup_dir_exists"] = self.backup_dir.exists()
        
        return results

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ashley AI Agent CLI")
    parser.add_argument("--init", action="store_true", help="Initialize new persona")
    parser.add_argument("--show", action="store_true", help="Show persona")
    parser.add_argument("--backup", action="store_true", help="Backup persona")
    parser.add_argument("--test", action="store_true", help="Test persona health")
    parser.add_argument("--update-trait", nargs=2, metavar=("TRAIT", "VALUE"), help="Update personality trait")
    parser.add_argument("--set-emotion", nargs=2, metavar=("EMOTION", "CONFIDENCE"), help="Set emotion")
    parser.add_argument("--export", action="store_true", help="Export persona for training")
    
    args = parser.parse_args()
    
    agent = AshleyAgent()
    
    if args.show:
        print(agent.get_persona_summary())
    elif args.backup:
        agent._backup_persona(reason="manual")
    elif args.test:
        results = agent.test_and_validate()
        print(json.dumps(results, indent=2))
    elif args.update_trait:
        trait, value = args.update_trait
        agent.update_personality_trait(trait, int(value))
    elif args.set_emotion:
        emotion, confidence = args.set_emotion
        agent.set_emotion(emotion, float(confidence))
    elif args.export:
        data = agent.export_for_training()
        print(json.dumps(data, indent=2))
    else:
        print(agent.get_persona_summary())
