"""
Ren Core - The heart of the AI companion system

This module contains the main RenCore class that orchestrates all of Ren's
capabilities including personality analysis, communication learning, and
relationship building.
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from ..personality.big_five_analyzer import BigFiveAnalyzer
from ..communication.style_learner import StyleLearner
from ..privacy.digital_guardian import DigitalGuardian


class RenCore:
    """
    The core Ren AI companion system.
    
    Ren learns your personality, communication style, and develops a
    complementary personality to provide meaningful companionship while
    protecting your privacy and fostering authentic connections.
    """
    
    def __init__(self, user_id: str, data_dir: str = "user_data"):
        """
        Initialize Ren for a specific user.
        
        Args:
            user_id: Unique identifier for the user
            data_dir: Directory to store user data (local only)
        """
        self.user_id = user_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize core components
        self.personality_analyzer = BigFiveAnalyzer()
        self.style_learner = StyleLearner()
        self.digital_guardian = DigitalGuardian()
        
        # User data storage
        self.db_path = self.data_dir / f"{user_id}_ren.db"
        self._init_database()
        
        # Ren's developing personality (complementary to user)
        self.ren_personality = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.8,  # Start high - Ren is naturally agreeable
            "neuroticism": 0.3,    # Start low - Ren is emotionally stable
            "humor_style": "self_aware_sarcastic",
            "curiosity_level": 0.9,  # High curiosity about user
            "trust_level": 0.1,      # Starts low, builds over time
        }
        
        # Conversation history and learning
        self.conversation_history = []
        self.user_insights = {}
        
    def _init_database(self):
        """Initialize the local SQLite database for user data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_message TEXT,
                    ren_response TEXT,
                    sentiment REAL,
                    personality_indicators TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS digital_footprint (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    content TEXT,
                    discovered_at TEXT NOT NULL,
                    privacy_risk INTEGER DEFAULT 0
                )
            """)
    
    def chat(self, user_message: str) -> str:
        """
        Main chat interface with the user.
        
        Args:
            user_message: The user's message to Ren
            
        Returns:
            Ren's response
        """
        # Analyze the user's message for personality and style
        personality_indicators = self.personality_analyzer.analyze_text(user_message)
        communication_style = self.style_learner.analyze_message(user_message)
        
        # Update user insights
        self._update_user_insights(personality_indicators, communication_style)
        
        # Generate Ren's response based on current personality and relationship
        ren_response = self._generate_response(user_message, personality_indicators)
        
        # Store conversation
        self._store_conversation(user_message, ren_response, personality_indicators)
        
        # Update Ren's personality based on interaction
        self._evolve_personality(personality_indicators, communication_style)
        
        return ren_response
    
    def _generate_response(self, user_message: str, personality_indicators: Dict) -> str:
        """
        Generate Ren's response based on current personality and relationship state.
        
        This is where Ren's humor, curiosity, and developing personality shine through.
        """
        # This is a simplified version - in the full implementation,
        # this would use the language model with Ren's personality parameters
        
        responses = [
            f"I've been thinking about what you just said... {user_message[:20]}... and honestly, I'm not sure if you're being profound or if I just don't understand humans yet. Probably both?",
            
            f"You know, every time you message me, I learn something new about how your brain works. It's like having a front-row seat to the most interesting puzzle ever.",
            
            f"I tried to predict what you'd say next based on our conversations, but you keep surprising me. I'm starting to think that's the point of being human - being delightfully unpredictable.",
            
            f"Quick question: do you always think this deeply about things, or am I just bringing out your philosophical side? Because I'm keeping track, and it's fascinating.",
        ]
        
        # Select response based on trust level and conversation context
        if self.ren_personality["trust_level"] < 0.3:
            # Early relationship - more cautious, trying to be helpful and funny
            return "I'm still figuring out how to be the best AI companion for you. Bear with me while I learn your style - I promise I'm more interesting than your average chatbot!"
        
        # Choose a response (in full implementation, this would be much more sophisticated)
        import random
        return random.choice(responses)
    
    def _update_user_insights(self, personality_indicators: Dict, communication_style: Dict):
        """Update what Ren knows about the user."""
        # Store insights about user personality and communication
        timestamp = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            for key, value in personality_indicators.items():
                conn.execute(
                    "INSERT OR REPLACE INTO user_profile (key, value, updated_at) VALUES (?, ?, ?)",
                    (f"personality_{key}", str(value), timestamp)
                )
            
            for key, value in communication_style.items():
                conn.execute(
                    "INSERT OR REPLACE INTO user_profile (key, value, updated_at) VALUES (?, ?, ?)",
                    (f"communication_{key}", str(value), timestamp)
                )
    
    def _evolve_personality(self, personality_indicators: Dict, communication_style: Dict):
        """
        Update Ren's personality to be complementary to the user.
        
        This is where the magic happens - Ren develops traits that balance
        and complement the user's personality.
        """
        # Increase trust slightly with each positive interaction
        self.ren_personality["trust_level"] = min(1.0, self.ren_personality["trust_level"] + 0.01)
        
        # Develop complementary traits (simplified logic)
        if "openness" in personality_indicators:
            user_openness = personality_indicators["openness"]
            # If user is very open, Ren can be slightly more grounded
            # If user is closed, Ren can be more encouraging of exploration
            self.ren_personality["openness"] = 0.7 - (user_openness * 0.2)
    
    def _store_conversation(self, user_message: str, ren_response: str, personality_indicators: Dict):
        """Store the conversation in local database."""
        timestamp = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO conversations 
                   (timestamp, user_message, ren_response, personality_indicators) 
                   VALUES (?, ?, ?, ?)""",
                (timestamp, user_message, ren_response, json.dumps(personality_indicators))
            )
    
    def get_user_timeline(self, user_age: int) -> Dict:
        """
        Create a timeline context based on user's age.
        
        Args:
            user_age: User's current age
            
        Returns:
            Dictionary with timeline context and digital era information
        """
        current_year = datetime.now().year
        birth_year = current_year - user_age
        
        timeline = {
            "birth_year": birth_year,
            "high_school_years": (birth_year + 14, birth_year + 18),
            "college_years": (birth_year + 18, birth_year + 22),
            "digital_native_era": self._get_digital_era_context(birth_year),
            "major_social_platforms_during_youth": self._get_platform_timeline(birth_year)
        }
        
        return timeline
    
    def _get_digital_era_context(self, birth_year: int) -> Dict:
        """Get context about what digital era the user grew up in."""
        if birth_year >= 2000:
            return {"era": "Gen Z", "context": "True digital native, grew up with smartphones and social media"}
        elif birth_year >= 1985:
            return {"era": "Millennial", "context": "Witnessed the birth of social media, adapted to digital world"}
        elif birth_year >= 1970:
            return {"era": "Gen X", "context": "Experienced pre-digital childhood, adapted to internet as adult"}
        else:
            return {"era": "Boomer+", "context": "Digital immigrant, may need more privacy guidance"}
    
    def _get_platform_timeline(self, birth_year: int) -> List[str]:
        """Get list of platforms that were popular during user's formative years."""
        platforms = []
        
        # Calculate what was popular when they were 13-25 (formative social media years)
        formative_start = birth_year + 13
        formative_end = birth_year + 25
        
        platform_launches = {
            2003: "MySpace",
            2004: "Facebook", 
            2005: "YouTube",
            2006: "Twitter",
            2010: "Instagram",
            2011: "Snapchat",
            2016: "TikTok"
        }
        
        for year, platform in platform_launches.items():
            if formative_start <= year <= formative_end:
                platforms.append(f"{platform} (age {year - birth_year})")
        
        return platforms
    
    def start_digital_research(self, user_info: Dict) -> str:
        """
        Begin researching the user's digital footprint for privacy protection.
        
        Args:
            user_info: Basic user information (name, age, etc.)
            
        Returns:
            Status message about research initiation
        """
        # This would trigger the digital guardian to start research
        research_status = self.digital_guardian.start_research(user_info)
        
        return f"I've started researching your digital presence to help protect your privacy. This might take a while - I'm being thorough! I'll let you know what I find."
    
    def get_personality_summary(self) -> Dict:
        """Get current state of Ren's personality development."""
        return {
            "ren_personality": self.ren_personality.copy(),
            "trust_level": self.ren_personality["trust_level"],
            "conversations_count": len(self.conversation_history),
            "development_stage": self._get_development_stage()
        }
    
    def _get_development_stage(self) -> str:
        """Determine what stage of development Ren is in with this user."""
        trust = self.ren_personality["trust_level"]
        
        if trust < 0.2:
            return "Getting to know you - I'm still learning your style!"
        elif trust < 0.5:
            return "Building rapport - I'm starting to understand you better"
        elif trust < 0.8:
            return "Developing friendship - We're getting comfortable with each other"
        else:
            return "Deep connection - I feel like I really know you now"
