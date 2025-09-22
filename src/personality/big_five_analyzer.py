"""
Big Five Personality Analyzer

Based on Jordan Peterson's research and the Big Five personality model,
this module analyzes text to identify personality traits and patterns.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import math


class BigFiveAnalyzer:
    """
    Analyzes text for Big Five personality indicators.
    
    The Big Five traits:
    - Openness: creativity, curiosity, openness to experience
    - Conscientiousness: organization, discipline, goal-oriented behavior  
    - Extraversion: sociability, assertiveness, energy
    - Agreeableness: cooperation, trust, empathy
    - Neuroticism: emotional instability, anxiety, negative emotions
    """
    
    def __init__(self):
        """Initialize the analyzer with trait indicators."""
        self.trait_indicators = self._load_trait_indicators()
        
    def _load_trait_indicators(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Load linguistic indicators for each Big Five trait.
        
        These are based on research into language patterns that correlate
        with personality traits.
        """
        return {
            "openness": {
                "high": [
                    # Creativity and imagination words
                    "creative", "imagine", "artistic", "innovative", "original",
                    "abstract", "theoretical", "philosophical", "metaphor",
                    "possibility", "potential", "explore", "discover",
                    # Intellectual curiosity
                    "wonder", "curious", "fascinating", "intriguing", "complex",
                    "analyze", "understand", "learn", "study", "research",
                    # Openness to experience
                    "adventure", "travel", "culture", "different", "unique",
                    "experiment", "try", "experience", "new", "novel"
                ],
                "low": [
                    # Conventional thinking
                    "traditional", "conventional", "normal", "standard", "typical",
                    "practical", "realistic", "concrete", "simple", "basic",
                    # Resistance to change
                    "always", "never", "same", "routine", "habit", "usual",
                    "predictable", "stable", "consistent", "reliable"
                ]
            },
            
            "conscientiousness": {
                "high": [
                    # Organization and planning
                    "organize", "plan", "schedule", "prepare", "arrange",
                    "systematic", "methodical", "structured", "ordered",
                    # Goal orientation
                    "goal", "achieve", "accomplish", "complete", "finish",
                    "success", "work", "effort", "discipline", "focus",
                    # Responsibility
                    "responsible", "duty", "obligation", "commitment", "promise",
                    "reliable", "dependable", "punctual", "thorough"
                ],
                "low": [
                    # Disorganization
                    "messy", "chaotic", "disorganized", "scattered", "random",
                    "spontaneous", "impulsive", "careless", "lazy",
                    # Procrastination
                    "later", "tomorrow", "eventually", "postpone", "delay",
                    "forget", "ignore", "skip", "avoid", "procrastinate"
                ]
            },
            
            "extraversion": {
                "high": [
                    # Social orientation
                    "people", "friends", "party", "social", "group", "team",
                    "together", "meet", "talk", "chat", "conversation",
                    # Energy and assertiveness
                    "excited", "energetic", "enthusiastic", "confident", "bold",
                    "outgoing", "talkative", "loud", "active", "lively",
                    # Leadership
                    "lead", "direct", "manage", "control", "influence", "persuade"
                ],
                "low": [
                    # Introversion
                    "quiet", "alone", "solitude", "private", "reserved", "shy",
                    "introverted", "withdrawn", "isolated", "independent",
                    # Preference for smaller groups
                    "few", "small", "intimate", "close", "personal", "individual",
                    # Thoughtful communication
                    "think", "reflect", "consider", "ponder", "contemplate"
                ]
            },
            
            "agreeableness": {
                "high": [
                    # Cooperation and empathy
                    "help", "support", "care", "kind", "compassionate", "empathy",
                    "understanding", "sympathetic", "considerate", "thoughtful",
                    # Trust and harmony
                    "trust", "believe", "faith", "harmony", "peace", "cooperation",
                    "agree", "compromise", "collaborate", "share", "give",
                    # Positive regard for others
                    "love", "like", "appreciate", "respect", "admire", "value"
                ],
                "low": [
                    # Competitiveness and skepticism
                    "compete", "win", "beat", "defeat", "superior", "better",
                    "skeptical", "doubt", "suspicious", "distrust", "question",
                    # Self-focus
                    "myself", "my", "me", "I", "selfish", "independent",
                    # Critical attitudes
                    "wrong", "stupid", "annoying", "irritating", "hate", "dislike"
                ]
            },
            
            "neuroticism": {
                "high": [
                    # Anxiety and worry
                    "anxious", "worried", "nervous", "stress", "tension", "fear",
                    "panic", "overwhelmed", "pressure", "burden", "struggle",
                    # Negative emotions
                    "sad", "depressed", "upset", "angry", "frustrated", "irritated",
                    "disappointed", "hurt", "pain", "suffering", "miserable",
                    # Emotional instability
                    "emotional", "sensitive", "moody", "unstable", "volatile",
                    "dramatic", "intense", "extreme", "overreact"
                ],
                "low": [
                    # Emotional stability
                    "calm", "relaxed", "peaceful", "stable", "steady", "balanced",
                    "composed", "controlled", "even", "consistent", "secure",
                    # Positive emotions
                    "happy", "content", "satisfied", "pleased", "comfortable",
                    "confident", "optimistic", "positive", "cheerful", "joyful",
                    # Resilience
                    "cope", "handle", "manage", "deal", "overcome", "resilient"
                ]
            }
        }
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze text for Big Five personality indicators.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with scores for each trait (0.0 to 1.0)
        """
        # Clean and tokenize text
        words = self._tokenize(text.lower())
        word_count = len(words)
        
        if word_count == 0:
            return self._default_scores()
        
        scores = {}
        
        for trait in self.trait_indicators:
            high_indicators = self.trait_indicators[trait]["high"]
            low_indicators = self.trait_indicators[trait]["low"]
            
            # Count matches
            high_matches = sum(1 for word in words if word in high_indicators)
            low_matches = sum(1 for word in words if word in low_indicators)
            
            # Calculate trait score
            if high_matches + low_matches == 0:
                scores[trait] = 0.5  # Neutral if no indicators
            else:
                # Score based on ratio of high to total indicators
                trait_score = high_matches / (high_matches + low_matches)
                scores[trait] = trait_score
        
        # Add additional linguistic analysis
        linguistic_features = self._analyze_linguistic_features(text, words)
        scores.update(linguistic_features)
        
        return scores
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization - split on non-alphanumeric characters."""
        return [word for word in re.findall(r'\b\w+\b', text) if len(word) > 2]
    
    def _analyze_linguistic_features(self, text: str, words: List[str]) -> Dict[str, float]:
        """
        Analyze additional linguistic features that correlate with personality.
        
        Args:
            text: Original text
            words: Tokenized words
            
        Returns:
            Additional personality indicators
        """
        features = {}
        
        # Sentence length and complexity (Openness indicator)
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / max(len(sentences), 1)
        features["linguistic_complexity"] = min(1.0, avg_sentence_length / 20.0)
        
        # Question usage (Openness/Curiosity)
        question_count = text.count('?')
        features["curiosity_indicators"] = min(1.0, question_count / max(len(sentences), 1))
        
        # Exclamation usage (Extraversion)
        exclamation_count = text.count('!')
        features["enthusiasm_indicators"] = min(1.0, exclamation_count / max(len(sentences), 1))
        
        # First person pronouns (potential Neuroticism indicator)
        first_person = ['i', 'me', 'my', 'myself', 'mine']
        first_person_count = sum(1 for word in words if word in first_person)
        features["self_focus"] = min(1.0, first_person_count / max(len(words), 1) * 10)
        
        # Positive vs negative sentiment words (Agreeableness/Neuroticism)
        positive_words = ['good', 'great', 'awesome', 'amazing', 'wonderful', 'excellent', 'fantastic', 'love', 'like', 'enjoy', 'happy', 'pleased']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry', 'sad', 'upset', 'frustrated', 'annoyed']
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count + negative_count > 0:
            features["sentiment_ratio"] = positive_count / (positive_count + negative_count)
        else:
            features["sentiment_ratio"] = 0.5
        
        return features
    
    def _default_scores(self) -> Dict[str, float]:
        """Return default neutral scores when no text to analyze."""
        return {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5,
            "linguistic_complexity": 0.5,
            "curiosity_indicators": 0.5,
            "enthusiasm_indicators": 0.5,
            "self_focus": 0.5,
            "sentiment_ratio": 0.5
        }
    
    def get_personality_summary(self, scores: Dict[str, float]) -> str:
        """
        Generate a human-readable personality summary.
        
        Args:
            scores: Personality scores from analyze_text()
            
        Returns:
            Text summary of personality indicators
        """
        summary_parts = []
        
        # Analyze each main trait
        for trait, score in scores.items():
            if trait in self.trait_indicators:  # Main Big Five traits
                if score > 0.7:
                    level = "high"
                elif score < 0.3:
                    level = "low"
                else:
                    level = "moderate"
                
                summary_parts.append(f"{trait.title()}: {level} ({score:.2f})")
        
        return "; ".join(summary_parts)
    
    def get_complementary_traits(self, user_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate complementary personality traits for Ren.
        
        The idea is that Ren should have traits that balance and complement
        the user's personality, creating a harmonious relationship.
        
        Args:
            user_scores: User's personality scores
            
        Returns:
            Recommended personality scores for Ren
        """
        complementary = {}
        
        for trait, user_score in user_scores.items():
            if trait in self.trait_indicators:  # Main Big Five traits
                if trait == "agreeableness":
                    # Ren should always be reasonably agreeable
                    complementary[trait] = max(0.7, user_score)
                elif trait == "neuroticism":
                    # Ren should be emotionally stable to balance user's emotions
                    complementary[trait] = max(0.2, 1.0 - user_score * 0.8)
                elif trait == "openness":
                    # If user is very open, Ren can be slightly more grounded
                    # If user is closed, Ren should encourage exploration
                    if user_score > 0.7:
                        complementary[trait] = 0.6
                    elif user_score < 0.3:
                        complementary[trait] = 0.8
                    else:
                        complementary[trait] = 0.7
                else:
                    # For other traits, aim for slight complementarity
                    if user_score > 0.6:
                        complementary[trait] = user_score - 0.2
                    elif user_score < 0.4:
                        complementary[trait] = user_score + 0.2
                    else:
                        complementary[trait] = user_score
        
        return complementary
