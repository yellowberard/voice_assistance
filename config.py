"""
Configuration file for the Voice Interview Bot
Simple, readable configuration that's easy to explain to interviewers
"""

import os
from dataclasses import dataclass
from typing import List

@dataclass
class PersonalInfo:
    """
    Data class to store personal information
    Easy to modify and explain the structure
    """
    name: str
    role: str
    experience: str
    life_story: str
    superpower: str
    growth_areas: List[str]
    misconception: str
    pushing_boundaries: str

# Personal Information - Customize this section with your details
PERSONAL_INFO = PersonalInfo(
    name="Mayank Goel",
    role="Software Developer",
    experience="2+ years",
    
    life_story="""I'm a passionate software developer with 2+ years of experience building 
    web applications. I started coding in college and fell in love with creating solutions 
    that make people's lives easier. I've worked on various projects from e-commerce 
    platforms to data visualization tools.""",
    
    superpower="""My #1 superpower is problem-solving and breaking down complex technical 
    challenges into manageable pieces. I have a knack for debugging and finding creative 
    solutions when others get stuck.""",
    
    growth_areas=[
        "System design and architecture for large-scale applications",
        "Machine learning and AI integration in web applications", 
        "Leadership and mentoring junior developers"
    ],
    
    misconception="""My coworkers sometimes think I'm overly focused on perfection, 
    but actually I believe in iterative improvement. I prefer shipping working code 
    and then refining it rather than getting stuck in analysis paralysis.""",
    
    pushing_boundaries="""I push my boundaries by taking on projects slightly outside 
    my comfort zone, contributing to open source, and staying updated with new technologies. 
    I also participate in hackathons and coding challenges to test my skills."""
)

# Application Configuration
class Config:
    """Simple configuration class"""
    
    # Flask settings
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o-mini'
    
    # Voice settings
    VOICE_LANGUAGE = 'en'
    SPEECH_TIMEOUT = 10  # seconds
    
    # Response settings
    MAX_RESPONSE_TOKENS = 15000
    RESPONSE_TEMPERATURE = 0.7