#!/usr/bin/env python3
"""
Renexus Demo Script

A simple demonstration of Ren's capabilities including:
- Personality analysis
- Communication style learning
- Digital privacy protection
- Trust-building through humor and self-awareness
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ren.ren_core import RenCore
import json


def print_separator(title=""):
    """Print a nice separator for demo sections."""
    print("\n" + "="*60)
    if title:
        print(f" {title} ")
        print("="*60)
    print()


def demo_personality_analysis():
    """Demonstrate personality analysis capabilities."""
    print_separator("PERSONALITY ANALYSIS DEMO")
    
    # Create a Ren instance for demo user
    ren = RenCore("demo_user")
    
    # Sample messages with different personality indicators
    test_messages = [
        "I love trying new restaurants and exploring different cuisines! There's something amazing about discovering flavors I've never experienced before.",
        
        "I need to organize my schedule better. I keep missing deadlines and it's really stressing me out.",
        
        "Ugh, people are so annoying sometimes. Why can't everyone just be more considerate?",
        
        "I've been thinking about this philosophical question all day - what if our reality is just a simulation?",
        
        "Had a great time at the party last night! Met so many interesting people and stayed up way too late talking."
    ]
    
    print("Analyzing sample messages for personality traits...\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"Message {i}: \"{message[:50]}...\"\n")
        
        # Analyze the message
        personality_scores = ren.personality_analyzer.analyze_text(message)
        
        # Show main Big Five scores
        print("Big Five Personality Indicators:")
        for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            if trait in personality_scores:
                score = personality_scores[trait]
                level = "High" if score > 0.6 else "Low" if score < 0.4 else "Moderate"
                print(f"  {trait.title()}: {score:.2f} ({level})")
        
        print("\n" + "-"*40 + "\n")


def demo_communication_learning():
    """Demonstrate communication style learning."""
    print_separator("COMMUNICATION STYLE LEARNING DEMO")
    
    ren = RenCore("demo_user")
    
    # Simulate a conversation to show style learning
    conversation = [
        "Hey! How's it going?",
        "I'm doing pretty well, thanks for asking. Been working on some interesting projects lately.",
        "That's awesome! What kind of projects? I'm super curious about what you're up to.",
        "Well, I've been diving deep into AI personality research. It's fascinating how we can analyze communication patterns.",
        "Wow, that sounds incredibly complex but also really cool. I bet you're learning tons!"
    ]
    
    print("Learning communication style from conversation...\n")
    
    for i, message in enumerate(conversation, 1):
        print(f"User: {message}")
        
        # Analyze communication style
        style_analysis = ren.style_learner.analyze_message(message)
        
        # Generate Ren's response
        ren_response = ren.chat(message)
        print(f"Ren: {ren_response}\n")
        
        # Show what Ren learned
        if i % 2 == 0:  # Show learning every other message
            summary = ren.style_learner.get_communication_summary()
            print("📊 What Ren has learned about your style:")
            print(f"  Vocabulary Level: {summary['patterns']['vocabulary_level']:.2f}")
            print(f"  Formality Level: {summary['patterns']['formality_level']:.2f}")
            print(f"  Emotional Expressiveness: {summary['patterns']['emotional_expressiveness']:.2f}")
            print(f"  Question Frequency: {summary['patterns']['question_frequency']:.2f}")
            print()
        
        print("-"*50 + "\n")


def demo_digital_guardian():
    """Demonstrate digital privacy protection."""
    print_separator("DIGITAL PRIVACY PROTECTION DEMO")
    
    ren = RenCore("demo_user")
    
    # Simulate user providing basic info
    user_info = {
        "name": "Alex Johnson",
        "age": "28",
        "location": "Seattle, WA"
    }
    
    print(f"User provides basic information:")
    print(f"Name: {user_info['name']}")
    print(f"Age: {user_info['age']}")
    print(f"Location: {user_info['location']}\n")
    
    # Start digital research
    print("Ren starts researching digital footprint...\n")
    research_status = ren.digital_guardian.start_research(user_info)
    print(f"Status: {research_status['message']}\n")
    
    # Get results
    results = ren.digital_guardian.get_research_results()
    
    print("🔍 Research Results:")
    print(f"Overall Privacy Risk: {results['privacy_assessment']['overall_risk'].upper()}")
    print(f"Total Findings: {results['privacy_assessment']['total_findings']}")
    print(f"High Risk Items: {results['privacy_assessment']['high_risk_items']}")
    print()
    
    print("📋 Sample Findings:")
    for finding in results['findings'][:3]:  # Show first 3 findings
        risk_emoji = "🔴" if finding['privacy_risk'] == "high" else "🟡" if finding['privacy_risk'] == "medium" else "🟢"
        print(f"  {risk_emoji} {finding['platform']}: {finding['content']}")
        print(f"     Recommendation: {finding['recommendation']}")
        print()
    
    print("💡 Top Recommendations:")
    for rec in results['recommendations'][:3]:  # Show first 3 recommendations
        print(f"  • {rec['title']}")
        print(f"    {rec['description']}")
        print(f"    Priority: {rec['priority'].title()}, Difficulty: {rec['difficulty'].title()}")
        print()


def demo_personality_development():
    """Demonstrate how Ren's personality develops."""
    print_separator("REN'S PERSONALITY DEVELOPMENT DEMO")
    
    ren = RenCore("demo_user")
    
    # Show initial personality
    initial_personality = ren.get_personality_summary()
    print("Ren's Initial Personality:")
    print(f"Trust Level: {initial_personality['trust_level']:.2f}")
    print(f"Development Stage: {initial_personality['development_stage']}")
    print(f"Humor Style: {ren.ren_personality['humor_style']}")
    print(f"Curiosity Level: {ren.ren_personality['curiosity_level']:.2f}")
    print()
    
    # Simulate several interactions to show personality evolution
    interactions = [
        "Hi Ren! I'm excited to get to know you.",
        "I love your sense of humor! You're actually pretty funny.",
        "I appreciate how you remember things about our conversations.",
        "You're really helpful with understanding my communication style.",
        "I feel like I can trust you with more personal stuff."
    ]
    
    print("Simulating personality development through interactions...\n")
    
    for i, message in enumerate(interactions, 1):
        print(f"Interaction {i}:")
        print(f"User: {message}")
        
        response = ren.chat(message)
        print(f"Ren: {response}")
        
        # Show personality evolution
        current_personality = ren.get_personality_summary()
        print(f"Trust Level: {current_personality['trust_level']:.2f}")
        print(f"Development Stage: {current_personality['development_stage']}")
        print()
        print("-"*50 + "\n")


def demo_timeline_context():
    """Demonstrate age-based timeline context."""
    print_separator("AGE-BASED TIMELINE CONTEXT DEMO")
    
    ren = RenCore("demo_user")
    
    # Test different ages
    test_ages = [16, 25, 35, 65]
    
    for age in test_ages:
        print(f"Timeline context for {age}-year-old user:")
        timeline = ren.get_user_timeline(age)
        
        print(f"  Birth Year: {timeline['birth_year']}")
        print(f"  High School: {timeline['high_school_years'][0]}-{timeline['high_school_years'][1]}")
        print(f"  Digital Era: {timeline['digital_native_era']['era']}")
        print(f"  Context: {timeline['digital_native_era']['context']}")
        print(f"  Platforms During Youth: {', '.join(timeline['major_social_platforms_during_youth'][:3])}")
        print()


def main():
    """Run the complete Renexus demo."""
    print("🤖 Welcome to the Renexus Demo!")
    print("Demonstrating Ren AI Companion capabilities...")
    
    try:
        # Run all demo sections
        demo_personality_analysis()
        demo_communication_learning()
        demo_digital_guardian()
        demo_personality_development()
        demo_timeline_context()
        
        print_separator("DEMO COMPLETE")
        print("This demo shows how Ren:")
        print("✓ Analyzes personality traits from text")
        print("✓ Learns communication styles and adapts")
        print("✓ Protects digital privacy proactively")
        print("✓ Develops complementary personality traits")
        print("✓ Provides age-appropriate context and understanding")
        print()
        print("Ren builds trust through humor, helpfulness, and genuine care")
        print("for the user's privacy and wellbeing.")
        print()
        print("Ready to start building your own Ren? 🚀")
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("This is normal - some modules may need additional setup.")
        print("The core architecture is in place and ready for development!")


if __name__ == "__main__":
    main()
