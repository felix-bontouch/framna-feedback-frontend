"""Persona system for generating consistent user profiles"""

import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from .data_providers import DataProvider
from .sentiment_engine import Sentiment


class AgeGroup(Enum):
    """Age group categories"""
    TEEN = "teen"           # 13-19
    YOUNG_ADULT = "young"   # 20-29
    ADULT = "adult"         # 30-49
    MIDDLE_AGE = "middle"   # 50-64
    SENIOR = "senior"       # 65+


class Profession(Enum):
    """Professional categories"""
    STUDENT = "student"
    TECH = "tech"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    BUSINESS = "business"
    CREATIVE = "creative"
    SERVICE = "service"
    RETIRED = "retired"
    UNEMPLOYED = "unemployed"


class TechSavvy(Enum):
    """Technology proficiency levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Persona:
    """Individual persona with consistent characteristics"""
    
    # Basic demographics
    first_name: str
    last_name: str
    email: str
    phone: str
    age: int
    age_group: AgeGroup
    gender: str
    locale: str
    
    # Professional info
    profession: Profession
    company: str
    job_title: str
    income_level: str
    
    # Location
    address: Dict[str, str]
    timezone: str
    
    # Behavioral traits
    tech_savvy: TechSavvy
    response_style: str  # verbose, concise, moderate
    typing_speed: str    # slow, medium, fast
    error_rate: float    # Probability of typos
    
    # Sentiment tendencies
    base_sentiment: Sentiment
    sentiment_stability: float  # How consistent their sentiment is
    complainer_score: float     # Tendency to complain
    enthusiast_score: float     # Tendency to be enthusiastic
    
    # Device and platform
    device_type: str  # mobile, desktop, tablet
    browser: str
    os: str
    
    # Additional metadata
    created_at: str
    persona_id: str
    tags: List[str] = field(default_factory=list)
    
    def get_sentiment(self) -> Sentiment:
        """Get sentiment for this persona, with some variation"""
        if random.random() < self.sentiment_stability:
            return self.base_sentiment
        else:
            # Occasionally vary from base sentiment
            if self.base_sentiment == Sentiment.POSITIVE:
                return random.choice([Sentiment.NEUTRAL, Sentiment.POSITIVE])
            elif self.base_sentiment == Sentiment.NEGATIVE:
                return random.choice([Sentiment.NEUTRAL, Sentiment.NEGATIVE])
            else:
                return random.choice(list(Sentiment))
    
    def should_make_typo(self) -> bool:
        """Determine if persona should make a typo"""
        return random.random() < self.error_rate
    
    def get_response_length_factor(self) -> float:
        """Get factor for adjusting response length"""
        if self.response_style == 'verbose':
            return random.uniform(1.2, 1.5)
        elif self.response_style == 'concise':
            return random.uniform(0.5, 0.8)
        else:
            return random.uniform(0.9, 1.1)
    
    def get_completion_time(self, num_fields: int) -> int:
        """Estimate completion time in seconds"""
        base_time = num_fields * 15  # 15 seconds per field average
        
        # Adjust for typing speed
        if self.typing_speed == 'fast':
            base_time *= 0.7
        elif self.typing_speed == 'slow':
            base_time *= 1.5
        
        # Adjust for tech savvy
        if self.tech_savvy == TechSavvy.HIGH:
            base_time *= 0.8
        elif self.tech_savvy == TechSavvy.LOW:
            base_time *= 1.3
        
        # Add randomness
        variation = random.uniform(0.8, 1.2)
        return int(base_time * variation)


class PersonaGenerator:
    """Generator for creating diverse personas"""
    
    # Job titles by profession
    JOB_TITLES = {
        Profession.STUDENT: [
            'Undergraduate Student', 'Graduate Student', 'PhD Candidate',
            'Research Assistant', 'Teaching Assistant', 'Intern'
        ],
        Profession.TECH: [
            'Software Engineer', 'Data Scientist', 'Product Manager',
            'DevOps Engineer', 'UX Designer', 'System Administrator',
            'Full Stack Developer', 'Mobile Developer', 'QA Engineer'
        ],
        Profession.HEALTHCARE: [
            'Nurse', 'Doctor', 'Medical Assistant', 'Therapist',
            'Pharmacist', 'Lab Technician', 'Healthcare Administrator'
        ],
        Profession.EDUCATION: [
            'Teacher', 'Professor', 'Instructor', 'Tutor',
            'School Administrator', 'Counselor', 'Librarian'
        ],
        Profession.BUSINESS: [
            'Manager', 'Analyst', 'Consultant', 'Executive',
            'Accountant', 'Sales Representative', 'Marketing Specialist'
        ],
        Profession.CREATIVE: [
            'Designer', 'Writer', 'Artist', 'Photographer',
            'Video Editor', 'Content Creator', 'Musician'
        ],
        Profession.SERVICE: [
            'Customer Service Rep', 'Retail Associate', 'Server',
            'Delivery Driver', 'Technician', 'Support Specialist'
        ],
        Profession.RETIRED: [
            'Retired', 'Former Executive', 'Retired Teacher',
            'Retired Engineer', 'Retired Manager'
        ],
        Profession.UNEMPLOYED: [
            'Job Seeker', 'Between Jobs', 'Freelancer',
            'Self-Employed', 'Contractor'
        ]
    }
    
    # Income levels by profession
    INCOME_LEVELS = {
        Profession.STUDENT: ['low', 'low', 'medium'],
        Profession.TECH: ['medium', 'high', 'high'],
        Profession.HEALTHCARE: ['medium', 'high', 'medium'],
        Profession.EDUCATION: ['low', 'medium', 'medium'],
        Profession.BUSINESS: ['medium', 'high', 'high'],
        Profession.CREATIVE: ['low', 'medium', 'medium'],
        Profession.SERVICE: ['low', 'low', 'medium'],
        Profession.RETIRED: ['medium', 'medium', 'high'],
        Profession.UNEMPLOYED: ['low', 'low', 'medium']
    }
    
    # Browsers
    BROWSERS = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera']
    
    # Operating systems by device
    OS_BY_DEVICE = {
        'desktop': ['Windows 10', 'Windows 11', 'macOS', 'Ubuntu', 'Linux'],
        'mobile': ['iOS', 'Android'],
        'tablet': ['iPadOS', 'Android']
    }
    
    # Timezones
    TIMEZONES = [
        'America/New_York', 'America/Chicago', 'America/Denver',
        'America/Los_Angeles', 'Europe/London', 'Europe/Paris',
        'Europe/Berlin', 'Asia/Tokyo', 'Asia/Shanghai', 'Australia/Sydney'
    ]
    
    def __init__(self, locale: str = 'en_US'):
        self.locale = locale
        self.data_provider = DataProvider(locale)
        self.persona_counter = 0
    
    def generate(self, 
                age_group: Optional[AgeGroup] = None,
                profession: Optional[Profession] = None,
                sentiment: Optional[Sentiment] = None) -> Persona:
        """Generate a new persona"""
        
        # Demographics
        if not age_group:
            age_group = random.choice(list(AgeGroup))
        
        age = self._get_age_from_group(age_group)
        
        # Profession based on age
        if not profession:
            profession = self._get_profession_for_age(age_group)
        
        # Names and contact
        first_name, last_name = self.data_provider.get_full_name()
        email = self.data_provider.get_email(first_name, last_name)
        phone = self.data_provider.get_phone()
        
        # Professional info
        company = self.data_provider.get_company_name()
        job_title = random.choice(self.JOB_TITLES[profession])
        income_level = random.choice(self.INCOME_LEVELS[profession])
        
        # Address
        address = self.data_provider.get_address()
        
        # Tech savvy based on age and profession
        tech_savvy = self._get_tech_savvy(age_group, profession)
        
        # Response style
        response_styles = ['verbose', 'concise', 'moderate']
        response_style = random.choice(response_styles)
        
        # Typing speed correlates with age and tech savvy
        typing_speed = self._get_typing_speed(age_group, tech_savvy)
        
        # Error rate based on typing speed and tech savvy
        error_rate = self._get_error_rate(typing_speed, tech_savvy)
        
        # Sentiment configuration
        if not sentiment:
            # Random with realistic distribution
            sentiment_weights = {
                Sentiment.POSITIVE: 0.4,
                Sentiment.NEUTRAL: 0.45,
                Sentiment.NEGATIVE: 0.15
            }
            sentiment = random.choices(
                list(sentiment_weights.keys()),
                weights=list(sentiment_weights.values())
            )[0]
        
        sentiment_stability = random.uniform(0.7, 0.95)
        
        # Complainer/enthusiast scores based on sentiment
        if sentiment == Sentiment.POSITIVE:
            complainer_score = random.uniform(0.0, 0.3)
            enthusiast_score = random.uniform(0.6, 1.0)
        elif sentiment == Sentiment.NEGATIVE:
            complainer_score = random.uniform(0.6, 1.0)
            enthusiast_score = random.uniform(0.0, 0.3)
        else:
            complainer_score = random.uniform(0.3, 0.6)
            enthusiast_score = random.uniform(0.3, 0.6)
        
        # Device and platform
        device_type = random.choices(
            ['mobile', 'desktop', 'tablet'],
            weights=[0.5, 0.4, 0.1]
        )[0]
        
        browser = random.choice(self.BROWSERS)
        os = random.choice(self.OS_BY_DEVICE[device_type])
        
        # Create persona
        self.persona_counter += 1
        persona_id = f"persona_{self.persona_counter:04d}"
        
        return Persona(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            age=age,
            age_group=age_group,
            gender=random.choice(['male', 'female', 'other']),
            locale=self.locale,
            profession=profession,
            company=company,
            job_title=job_title,
            income_level=income_level,
            address=address,
            timezone=random.choice(self.TIMEZONES),
            tech_savvy=tech_savvy,
            response_style=response_style,
            typing_speed=typing_speed,
            error_rate=error_rate,
            base_sentiment=sentiment,
            sentiment_stability=sentiment_stability,
            complainer_score=complainer_score,
            enthusiast_score=enthusiast_score,
            device_type=device_type,
            browser=browser,
            os=os,
            created_at=self.data_provider.get_date(past_days=0),
            persona_id=persona_id,
            tags=self._generate_tags(age_group, profession, sentiment)
        )
    
    def _get_age_from_group(self, age_group: AgeGroup) -> int:
        """Get specific age from age group"""
        ranges = {
            AgeGroup.TEEN: (13, 19),
            AgeGroup.YOUNG_ADULT: (20, 29),
            AgeGroup.ADULT: (30, 49),
            AgeGroup.MIDDLE_AGE: (50, 64),
            AgeGroup.SENIOR: (65, 85)
        }
        min_age, max_age = ranges[age_group]
        return random.randint(min_age, max_age)
    
    def _get_profession_for_age(self, age_group: AgeGroup) -> Profession:
        """Get appropriate profession for age group"""
        if age_group == AgeGroup.TEEN:
            return Profession.STUDENT
        elif age_group == AgeGroup.SENIOR:
            return random.choice([Profession.RETIRED, Profession.BUSINESS])
        else:
            # Exclude student and retired for other age groups
            professions = [p for p in Profession 
                          if p not in [Profession.STUDENT, Profession.RETIRED]]
            return random.choice(professions)
    
    def _get_tech_savvy(self, age_group: AgeGroup, profession: Profession) -> TechSavvy:
        """Determine tech savvy based on age and profession"""
        if profession == Profession.TECH:
            return TechSavvy.HIGH
        
        if age_group in [AgeGroup.TEEN, AgeGroup.YOUNG_ADULT]:
            return random.choices(
                [TechSavvy.LOW, TechSavvy.MEDIUM, TechSavvy.HIGH],
                weights=[0.1, 0.3, 0.6]
            )[0]
        elif age_group == AgeGroup.SENIOR:
            return random.choices(
                [TechSavvy.LOW, TechSavvy.MEDIUM, TechSavvy.HIGH],
                weights=[0.5, 0.4, 0.1]
            )[0]
        else:
            return random.choices(
                [TechSavvy.LOW, TechSavvy.MEDIUM, TechSavvy.HIGH],
                weights=[0.2, 0.5, 0.3]
            )[0]
    
    def _get_typing_speed(self, age_group: AgeGroup, tech_savvy: TechSavvy) -> str:
        """Determine typing speed"""
        if tech_savvy == TechSavvy.HIGH:
            return random.choices(['medium', 'fast'], weights=[0.3, 0.7])[0]
        elif tech_savvy == TechSavvy.LOW:
            return random.choices(['slow', 'medium'], weights=[0.7, 0.3])[0]
        else:
            return random.choices(['slow', 'medium', 'fast'], weights=[0.2, 0.6, 0.2])[0]
    
    def _get_error_rate(self, typing_speed: str, tech_savvy: TechSavvy) -> float:
        """Calculate error rate for typos"""
        base_rate = {
            'slow': 0.02,
            'medium': 0.03,
            'fast': 0.05
        }[typing_speed]
        
        # Adjust for tech savvy
        if tech_savvy == TechSavvy.HIGH:
            base_rate *= 0.5
        elif tech_savvy == TechSavvy.LOW:
            base_rate *= 1.5
        
        return min(0.1, base_rate)
    
    def _generate_tags(self, age_group: AgeGroup, profession: Profession, 
                      sentiment: Sentiment) -> List[str]:
        """Generate descriptive tags for persona"""
        tags = [
            age_group.value,
            profession.value,
            sentiment.value
        ]
        
        # Add additional descriptive tags
        if age_group == AgeGroup.TEEN:
            tags.append('digital_native')
        if profession == Profession.TECH:
            tags.append('tech_worker')
        if sentiment == Sentiment.POSITIVE:
            tags.append('satisfied_customer')
        elif sentiment == Sentiment.NEGATIVE:
            tags.append('dissatisfied_customer')
        
        return tags


class PersonaPool:
    """Pool of personas for batch generation"""
    
    def __init__(self, size: int = 100, diversity: str = 'high', locale: str = 'en_US'):
        """
        Initialize persona pool
        
        Args:
            size: Number of personas to generate
            diversity: Level of diversity (low, medium, high)
            locale: Locale for data generation
        """
        self.size = size
        self.diversity = diversity
        self.locale = locale
        self.generator = PersonaGenerator(locale)
        self.personas: List[Persona] = []
        self._generate_pool()
    
    def _generate_pool(self):
        """Generate the pool of personas"""
        if self.diversity == 'high':
            # Maximum diversity - random everything
            for _ in range(self.size):
                self.personas.append(self.generator.generate())
        
        elif self.diversity == 'medium':
            # Moderate diversity - some patterns
            age_groups = list(AgeGroup)
            professions = list(Profession)
            sentiments = [Sentiment.POSITIVE, Sentiment.NEGATIVE, Sentiment.NEUTRAL]
            
            for i in range(self.size):
                # Cycle through combinations with some randomness
                age = age_groups[i % len(age_groups)]
                prof = random.choice(professions)
                sent = random.choices(
                    sentiments,
                    weights=[0.4, 0.15, 0.45]  # pos, neg, neutral
                )[0]
                self.personas.append(self.generator.generate(age, prof, sent))
        
        else:  # low diversity
            # Limited variation - create archetypes
            archetypes = [
                (AgeGroup.YOUNG_ADULT, Profession.TECH, Sentiment.POSITIVE),
                (AgeGroup.ADULT, Profession.BUSINESS, Sentiment.NEUTRAL),
                (AgeGroup.MIDDLE_AGE, Profession.SERVICE, Sentiment.NEGATIVE),
                (AgeGroup.SENIOR, Profession.RETIRED, Sentiment.NEUTRAL)
            ]
            
            for i in range(self.size):
                archetype = archetypes[i % len(archetypes)]
                self.personas.append(self.generator.generate(*archetype))
    
    def get_persona(self, index: int = None) -> Persona:
        """Get a specific persona or random one"""
        if index is not None:
            return self.personas[index % len(self.personas)]
        return random.choice(self.personas)
    
    def get_batch(self, count: int) -> List[Persona]:
        """Get a batch of personas"""
        if count <= self.size:
            return random.sample(self.personas, count)
        else:
            # Need to repeat some personas
            batch = []
            for i in range(count):
                batch.append(self.personas[i % self.size])
            random.shuffle(batch)
            return batch
    
    def filter_by_sentiment(self, sentiment: Sentiment) -> List[Persona]:
        """Get personas with specific sentiment"""
        return [p for p in self.personas if p.base_sentiment == sentiment]
    
    def filter_by_age_group(self, age_group: AgeGroup) -> List[Persona]:
        """Get personas in specific age group"""
        return [p for p in self.personas if p.age_group == age_group]
    
    def filter_by_profession(self, profession: Profession) -> List[Persona]:
        """Get personas with specific profession"""
        return [p for p in self.personas if p.profession == profession]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the persona pool"""
        stats = {
            'total': len(self.personas),
            'age_groups': {},
            'professions': {},
            'sentiments': {},
            'device_types': {},
            'avg_age': sum(p.age for p in self.personas) / len(self.personas)
        }
        
        for persona in self.personas:
            # Age groups
            ag = persona.age_group.value
            stats['age_groups'][ag] = stats['age_groups'].get(ag, 0) + 1
            
            # Professions
            prof = persona.profession.value
            stats['professions'][prof] = stats['professions'].get(prof, 0) + 1
            
            # Sentiments
            sent = persona.base_sentiment.value
            stats['sentiments'][sent] = stats['sentiments'].get(sent, 0) + 1
            
            # Device types
            dev = persona.device_type
            stats['device_types'][dev] = stats['device_types'].get(dev, 0) + 1
        
        return stats
    
    def __iter__(self):
        """Make pool iterable"""
        return iter(self.personas)
    
    def __len__(self):
        """Get pool size"""
        return len(self.personas)
    
    def __getitem__(self, index):
        """Get persona by index"""
        return self.personas[index]