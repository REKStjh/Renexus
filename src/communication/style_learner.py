"""
Communication Style Learner

This module analyzes how users communicate and learns their unique style,
helping Ren adapt its responses to match the user's preferred communication patterns.
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
import json


class StyleLearner:
    """
    Learns and analyzes user communication patterns.
    
    This includes:
    - Vocabulary preferences and complexity
    - Sentence structure and length
    - Humor style and sarcasm detection
    - Emotional expression patterns
    - Topic preferences and interests
    """
    
    def __init__(self):
        """Initialize the style learner."""
        self.user_patterns = {
            "vocabulary_level": 0.5,  # 0=simple, 1=complex
            "sentence_length_preference": 0.5,  # 0=short, 1=long
            "humor_style": "unknown",  # sarcastic, wholesome, dry, etc.
            "emotional_expressiveness": 0.5,  # 0=reserved, 1=expressive
            "formality_level": 0.5,  # 0=casual, 1=formal
            "question_frequency": 0.5,  # How often they ask questions
            "topic_interests": [],
            "communication_quirks": []
        }
        
        # Track patterns over time
        self.message_history = []
        self.pattern_evolution = []
        
    def analyze_message(self, message: str) -> Dict[str, any]:
        """
        Analyze a single message for communication style indicators.
        
        Args:
            message: The user's message to analyze
            
        Returns:
            Dictionary of style indicators found in this message
        """
        analysis = {}
        
        # Basic text processing
        words = self._tokenize(message.lower())
        sentences = self._split_sentences(message)
        
        # Vocabulary analysis
        analysis["vocabulary_complexity"] = self._analyze_vocabulary_complexity(words)
        analysis["unique_word_ratio"] = len(set(words)) / max(len(words), 1)
        
        # Sentence structure
        analysis["avg_sentence_length"] = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        analysis["sentence_variety"] = self._analyze_sentence_variety(sentences)
        
        # Emotional expression
        analysis["emotional_indicators"] = self._detect_emotional_expression(message, words)
        analysis["punctuation_style"] = self._analyze_punctuation(message)
        
        # Humor and personality
        analysis["humor_indicators"] = self._detect_humor_style(message, words)
        analysis["sarcasm_likelihood"] = self._detect_sarcasm(message, words)
        
        # Formality and tone
        analysis["formality_indicators"] = self._analyze_formality(words, message)
        analysis["question_patterns"] = self._analyze_questions(message)
        
        # Topic and interest extraction
        analysis["topics_mentioned"] = self._extract_topics(words)
        analysis["personal_references"] = self._count_personal_references(words)
        
        # Store for pattern learning
        self.message_history.append({
            "message": message,
            "analysis": analysis,
            "timestamp": len(self.message_history)  # Simple counter for now
        })
        
        # Update learned patterns
        self._update_patterns(analysis)
        
        return analysis
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return [word for word in re.findall(r'\b\w+\b', text) if len(word) > 1]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _analyze_vocabulary_complexity(self, words: List[str]) -> float:
        """
        Analyze vocabulary complexity based on word length and sophistication.
        
        Returns score from 0 (simple) to 1 (complex).
        """
        if not words:
            return 0.5
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Complex word indicators (simplified)
        complex_words = [word for word in words if len(word) > 6]
        complex_ratio = len(complex_words) / len(words)
        
        # Academic/sophisticated vocabulary indicators
        sophisticated_words = [
            "analyze", "synthesize", "conceptualize", "methodology", "paradigm",
            "hypothesis", "empirical", "theoretical", "philosophical", "psychological",
            "furthermore", "consequently", "nevertheless", "moreover", "therefore"
        ]
        
        sophisticated_count = sum(1 for word in words if word in sophisticated_words)
        sophisticated_ratio = sophisticated_count / len(words)
        
        # Combine indicators
        complexity_score = (
            (avg_word_length - 3) / 7 * 0.4 +  # Word length component
            complex_ratio * 0.4 +  # Complex words component
            sophisticated_ratio * 10 * 0.2  # Sophisticated vocabulary component
        )
        
        return min(1.0, max(0.0, complexity_score))
    
    def _analyze_sentence_variety(self, sentences: List[str]) -> float:
        """Analyze variety in sentence structure."""
        if len(sentences) < 2:
            return 0.5
        
        lengths = [len(s.split()) for s in sentences]
        
        # Calculate coefficient of variation (std dev / mean)
        if not lengths or sum(lengths) == 0:
            return 0.5
        
        mean_length = sum(lengths) / len(lengths)
        variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
        std_dev = variance ** 0.5
        
        if mean_length == 0:
            return 0.5
        
        variety_score = std_dev / mean_length
        return min(1.0, variety_score)
    
    def _detect_emotional_expression(self, message: str, words: List[str]) -> Dict[str, float]:
        """Detect emotional expression patterns."""
        emotions = {
            "excitement": 0.0,
            "enthusiasm": 0.0,
            "concern": 0.0,
            "affection": 0.0,
            "frustration": 0.0
        }
        
        # Excitement indicators
        excitement_words = ["amazing", "awesome", "incredible", "fantastic", "wow", "omg"]
        excitement_punctuation = message.count('!') + message.count('!!!')
        emotions["excitement"] = (
            sum(1 for word in words if word in excitement_words) / max(len(words), 1) +
            excitement_punctuation / max(len(message), 1) * 10
        )
        
        # Enthusiasm indicators  
        enthusiasm_words = ["love", "excited", "can't wait", "looking forward", "thrilled"]
        emotions["enthusiasm"] = sum(1 for word in words if word in enthusiasm_words) / max(len(words), 1)
        
        # Concern indicators
        concern_words = ["worried", "concerned", "anxious", "nervous", "unsure", "confused"]
        emotions["concern"] = sum(1 for word in words if word in concern_words) / max(len(words), 1)
        
        # Affection indicators
        affection_words = ["love", "care", "appreciate", "grateful", "thankful", "sweet"]
        emotions["affection"] = sum(1 for word in words if word in affection_words) / max(len(words), 1)
        
        # Frustration indicators
        frustration_words = ["frustrated", "annoying", "irritating", "ugh", "seriously", "ridiculous"]
        emotions["frustration"] = sum(1 for word in words if word in frustration_words) / max(len(words), 1)
        
        return emotions
    
    def _analyze_punctuation(self, message: str) -> Dict[str, int]:
        """Analyze punctuation usage patterns."""
        return {
            "exclamation_marks": message.count('!'),
            "question_marks": message.count('?'),
            "ellipses": message.count('...'),
            "dashes": message.count('--') + message.count('—'),
            "parentheses": message.count('('),
            "quotation_marks": message.count('"') + message.count("'")
        }
    
    def _detect_humor_style(self, message: str, words: List[str]) -> Dict[str, float]:
        """Detect different types of humor."""
        humor_styles = {
            "sarcastic": 0.0,
            "self_deprecating": 0.0,
            "wordplay": 0.0,
            "observational": 0.0,
            "wholesome": 0.0
        }
        
        # Sarcasm indicators
        sarcasm_words = ["obviously", "clearly", "sure", "right", "totally", "absolutely"]
        sarcasm_phrases = ["oh great", "just perfect", "how wonderful", "that's just"]
        
        sarcasm_score = sum(1 for word in words if word in sarcasm_words) / max(len(words), 1)
        for phrase in sarcasm_phrases:
            if phrase in message.lower():
                sarcasm_score += 0.1
        
        humor_styles["sarcastic"] = sarcasm_score
        
        # Self-deprecating humor
        self_deprecating_words = ["stupid", "dumb", "idiot", "fail", "mess", "disaster"]
        first_person = ["i", "me", "my", "myself"]
        
        # Check if self-deprecating words are used with first person
        self_deprecating_score = 0.0
        for i, word in enumerate(words):
            if word in self_deprecating_words:
                # Check surrounding words for first person
                context = words[max(0, i-3):i+4]
                if any(fp in context for fp in first_person):
                    self_deprecating_score += 0.1
        
        humor_styles["self_deprecating"] = self_deprecating_score
        
        # Wordplay detection (simplified)
        if any(char in message for char in ['😄', '😂', '🤣', '😆']) or 'lol' in message.lower() or 'haha' in message.lower():
            humor_styles["wordplay"] = 0.1
        
        return humor_styles
    
    def _detect_sarcasm(self, message: str, words: List[str]) -> float:
        """Detect likelihood of sarcasm in the message."""
        sarcasm_indicators = [
            "obviously", "clearly", "sure", "right", "totally", "absolutely",
            "perfect", "wonderful", "great", "fantastic", "amazing"
        ]
        
        # Context matters for sarcasm
        negative_context = ["not", "never", "can't", "won't", "don't", "isn't", "aren't"]
        
        sarcasm_score = 0.0
        
        # Direct sarcasm words
        sarcasm_score += sum(1 for word in words if word in sarcasm_indicators) / max(len(words), 1)
        
        # Positive words in negative context
        positive_words = ["great", "perfect", "wonderful", "amazing", "fantastic"]
        for i, word in enumerate(words):
            if word in positive_words:
                # Check for negative context nearby
                context = words[max(0, i-2):i+3]
                if any(neg in context for neg in negative_context):
                    sarcasm_score += 0.2
        
        # Excessive punctuation can indicate sarcasm
        if message.count('!') > 2 or '...' in message:
            sarcasm_score += 0.1
        
        return min(1.0, sarcasm_score)
    
    def _analyze_formality(self, words: List[str], message: str) -> Dict[str, float]:
        """Analyze formality level of communication."""
        formal_indicators = [
            "please", "thank you", "would", "could", "should", "might",
            "perhaps", "possibly", "certainly", "indeed", "furthermore",
            "however", "therefore", "consequently"
        ]
        
        informal_indicators = [
            "gonna", "wanna", "gotta", "yeah", "yep", "nope", "ok", "okay",
            "cool", "awesome", "dude", "guys", "stuff", "things", "kinda",
            "sorta", "pretty", "really", "super", "totally"
        ]
        
        contractions = ["don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't"]
        
        formal_count = sum(1 for word in words if word in formal_indicators)
        informal_count = sum(1 for word in words if word in informal_indicators)
        contraction_count = sum(1 for word in words if word in contractions)
        
        # Check for complete sentences and proper capitalization
        proper_capitalization = message[0].isupper() if message else False
        
        formality_score = {
            "formal_words": formal_count / max(len(words), 1),
            "informal_words": informal_count / max(len(words), 1),
            "contractions": contraction_count / max(len(words), 1),
            "proper_capitalization": 1.0 if proper_capitalization else 0.0
        }
        
        return formality_score
    
    def _analyze_questions(self, message: str) -> Dict[str, any]:
        """Analyze question patterns."""
        questions = [s.strip() for s in re.split(r'[.!]', message) if '?' in s]
        
        question_types = {
            "yes_no": 0,
            "open_ended": 0,
            "rhetorical": 0
        }
        
        for question in questions:
            question_lower = question.lower()
            
            # Yes/no questions
            if any(question_lower.startswith(word) for word in ["do", "does", "did", "is", "are", "was", "were", "can", "could", "will", "would", "should"]):
                question_types["yes_no"] += 1
            
            # Open-ended questions
            elif any(word in question_lower for word in ["what", "how", "why", "when", "where", "who"]):
                question_types["open_ended"] += 1
            
            # Rhetorical (harder to detect, simplified)
            elif any(phrase in question_lower for phrase in ["right?", "you know?", "don't you think?"]):
                question_types["rhetorical"] += 1
        
        return {
            "total_questions": len(questions),
            "question_types": question_types,
            "question_ratio": len(questions) / max(len(re.split(r'[.!?]', message)), 1)
        }
    
    def _extract_topics(self, words: List[str]) -> List[str]:
        """Extract potential topics of interest."""
        # Simplified topic extraction
        topic_categories = {
            "technology": ["computer", "software", "app", "tech", "digital", "online", "internet", "ai", "programming"],
            "work": ["job", "work", "career", "office", "business", "meeting", "project", "deadline"],
            "relationships": ["friend", "family", "relationship", "dating", "marriage", "love", "partner"],
            "hobbies": ["music", "movie", "book", "game", "sport", "art", "cooking", "travel"],
            "health": ["health", "exercise", "diet", "sleep", "stress", "mental", "physical"],
            "education": ["school", "college", "university", "study", "learn", "class", "degree"]
        }
        
        detected_topics = []
        for topic, keywords in topic_categories.items():
            if any(keyword in words for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    def _count_personal_references(self, words: List[str]) -> Dict[str, int]:
        """Count personal references in the message."""
        return {
            "first_person": sum(1 for word in words if word in ["i", "me", "my", "myself", "mine"]),
            "second_person": sum(1 for word in words if word in ["you", "your", "yours", "yourself"]),
            "third_person": sum(1 for word in words if word in ["he", "she", "they", "them", "his", "her", "their"])
        }
    
    def _update_patterns(self, analysis: Dict[str, any]):
        """Update learned patterns based on new analysis."""
        # Simple exponential moving average to update patterns
        alpha = 0.1  # Learning rate
        
        # Update vocabulary level
        if "vocabulary_complexity" in analysis:
            self.user_patterns["vocabulary_level"] = (
                (1 - alpha) * self.user_patterns["vocabulary_level"] +
                alpha * analysis["vocabulary_complexity"]
            )
        
        # Update sentence length preference
        if "avg_sentence_length" in analysis:
            # Normalize sentence length to 0-1 scale
            normalized_length = min(1.0, analysis["avg_sentence_length"] / 20.0)
            self.user_patterns["sentence_length_preference"] = (
                (1 - alpha) * self.user_patterns["sentence_length_preference"] +
                alpha * normalized_length
            )
        
        # Update emotional expressiveness
        if "emotional_indicators" in analysis:
            total_emotion = sum(analysis["emotional_indicators"].values())
            self.user_patterns["emotional_expressiveness"] = (
                (1 - alpha) * self.user_patterns["emotional_expressiveness"] +
                alpha * min(1.0, total_emotion)
            )
        
        # Update formality level
        if "formality_indicators" in analysis:
            formal_score = analysis["formality_indicators"]["formal_words"]
            informal_score = analysis["formality_indicators"]["informal_words"]
            
            if formal_score + informal_score > 0:
                formality_ratio = formal_score / (formal_score + informal_score)
                self.user_patterns["formality_level"] = (
                    (1 - alpha) * self.user_patterns["formality_level"] +
                    alpha * formality_ratio
                )
        
        # Update question frequency
        if "question_patterns" in analysis:
            self.user_patterns["question_frequency"] = (
                (1 - alpha) * self.user_patterns["question_frequency"] +
                alpha * analysis["question_patterns"]["question_ratio"]
            )
        
        # Update topic interests
        if "topics_mentioned" in analysis:
            for topic in analysis["topics_mentioned"]:
                if topic not in self.user_patterns["topic_interests"]:
                    self.user_patterns["topic_interests"].append(topic)
    
    def get_communication_summary(self) -> Dict[str, any]:
        """Get a summary of learned communication patterns."""
        return {
            "patterns": self.user_patterns.copy(),
            "messages_analyzed": len(self.message_history),
            "confidence": min(1.0, len(self.message_history) / 20.0),  # Confidence increases with more data
            "recent_trends": self._analyze_recent_trends()
        }
    
    def _analyze_recent_trends(self) -> Dict[str, str]:
        """Analyze recent trends in communication style."""
        if len(self.message_history) < 5:
            return {"trend": "insufficient_data"}
        
        # Compare recent messages to overall patterns
        recent_messages = self.message_history[-5:]
        
        trends = {}
        
        # Analyze if user is becoming more or less formal
        recent_formality = sum(msg["analysis"].get("formality_indicators", {}).get("formal_words", 0) for msg in recent_messages) / len(recent_messages)
        overall_formality = self.user_patterns["formality_level"]
        
        if recent_formality > overall_formality + 0.1:
            trends["formality"] = "increasing"
        elif recent_formality < overall_formality - 0.1:
            trends["formality"] = "decreasing"
        else:
            trends["formality"] = "stable"
        
        return trends
    
    def adapt_response_style(self, base_response: str) -> str:
        """
        Adapt a response to match the user's communication style.
        
        Args:
            base_response: The base response to adapt
            
        Returns:
            Response adapted to user's style
        """
        adapted_response = base_response
        
        # Adjust formality
        if self.user_patterns["formality_level"] < 0.3:
            # Make more casual
            adapted_response = adapted_response.replace("I would", "I'd")
            adapted_response = adapted_response.replace("cannot", "can't")
            adapted_response = adapted_response.replace("do not", "don't")
        
        # Adjust enthusiasm based on user's emotional expressiveness
        if self.user_patterns["emotional_expressiveness"] > 0.7:
            # Add more enthusiasm
            if not adapted_response.endswith('!'):
                adapted_response += "!"
        
        # Adjust complexity based on vocabulary level
        if self.user_patterns["vocabulary_level"] < 0.3:
            # Simplify language (basic implementation)
            complex_words = {
                "utilize": "use",
                "facilitate": "help",
                "demonstrate": "show",
                "approximately": "about",
                "subsequently": "then"
            }
            
            for complex_word, simple_word in complex_words.items():
                adapted_response = adapted_response.replace(complex_word, simple_word)
        
        return adapted_response
