"""Data providers for realistic data generation"""

import random
import string
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta, date
import hashlib


class DataProvider:
    """Base class for data providers"""

    # Common first names by region
    FIRST_NAMES = {
        "en_US": [
            "James",
            "John",
            "Robert",
            "Michael",
            "William",
            "David",
            "Richard",
            "Joseph",
            "Thomas",
            "Christopher",
            "Mary",
            "Patricia",
            "Jennifer",
            "Linda",
            "Elizabeth",
            "Barbara",
            "Susan",
            "Jessica",
            "Sarah",
            "Karen",
            "Emma",
            "Olivia",
            "Ava",
            "Isabella",
            "Sophia",
            "Liam",
            "Noah",
            "Oliver",
            "Elijah",
            "Lucas",
        ],
        "en_GB": [
            "Oliver",
            "George",
            "Harry",
            "Jack",
            "Jacob",
            "Charlie",
            "Thomas",
            "Oscar",
            "William",
            "James",
            "Olivia",
            "Amelia",
            "Isla",
            "Ava",
            "Emily",
            "Isabella",
            "Mia",
            "Poppy",
            "Ella",
            "Lily",
            "Sophie",
            "Grace",
            "Alice",
            "Freya",
            "Charlotte",
        ],
        "es_ES": [
            "Antonio",
            "Manuel",
            "Francisco",
            "José",
            "David",
            "Juan",
            "Javier",
            "Daniel",
            "Miguel",
            "Pedro",
            "María",
            "Carmen",
            "Ana",
            "Isabel",
            "Laura",
            "Cristina",
            "Marta",
            "Lucía",
            "Francisca",
            "Elena",
            "Sofia",
            "Paula",
            "Emma",
            "Martina",
            "Alba",
        ],
        "de_DE": [
            "Ben",
            "Paul",
            "Leon",
            "Finn",
            "Noah",
            "Luis",
            "Felix",
            "Luca",
            "Maximilian",
            "Henry",
            "Emma",
            "Mia",
            "Hannah",
            "Emilia",
            "Sofia",
            "Lina",
            "Marie",
            "Lea",
            "Anna",
            "Lena",
            "Clara",
            "Ella",
            "Laura",
            "Maja",
            "Amelie",
        ],
        "fr_FR": [
            "Gabriel",
            "Raphaël",
            "Léo",
            "Louis",
            "Lucas",
            "Adam",
            "Arthur",
            "Hugo",
            "Jules",
            "Maël",
            "Emma",
            "Jade",
            "Louise",
            "Alice",
            "Chloé",
            "Lina",
            "Rose",
            "Léa",
            "Anna",
            "Mila",
            "Camille",
            "Zoé",
            "Manon",
            "Lucie",
            "Juliette",
        ],
    }

    # Common last names by region
    LAST_NAMES = {
        "en_US": [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
            "Ramirez",
            "Lewis",
            "Robinson",
        ],
        "en_GB": [
            "Smith",
            "Jones",
            "Taylor",
            "Brown",
            "Williams",
            "Johnson",
            "Davies",
            "Robinson",
            "Wright",
            "Thompson",
            "Evans",
            "Walker",
            "White",
            "Roberts",
            "Green",
            "Hall",
            "Wood",
            "Jackson",
            "Clarke",
            "Harris",
            "Scott",
            "Turner",
            "Hill",
            "Moore",
            "Clark",
        ],
        "es_ES": [
            "García",
            "Fernández",
            "González",
            "Rodríguez",
            "López",
            "Martínez",
            "Sánchez",
            "Pérez",
            "Martín",
            "Gómez",
            "Ruiz",
            "Hernández",
            "Jiménez",
            "Díaz",
            "Álvarez",
            "Moreno",
            "Muñoz",
            "Alonso",
            "Romero",
            "Navarro",
            "Torres",
            "Domínguez",
            "Ramos",
            "Vázquez",
            "Serrano",
        ],
        "de_DE": [
            "Müller",
            "Schmidt",
            "Schneider",
            "Fischer",
            "Weber",
            "Meyer",
            "Wagner",
            "Becker",
            "Schulz",
            "Hoffmann",
            "Schäfer",
            "Koch",
            "Bauer",
            "Richter",
            "Klein",
            "Wolf",
            "Schröder",
            "Neumann",
            "Schwarz",
            "Zimmermann",
            "Braun",
            "Hofmann",
            "Krüger",
            "Hartmann",
            "Lange",
        ],
        "fr_FR": [
            "Martin",
            "Bernard",
            "Thomas",
            "Petit",
            "Robert",
            "Richard",
            "Durand",
            "Dubois",
            "Moreau",
            "Laurent",
            "Simon",
            "Michel",
            "Lefebvre",
            "Leroy",
            "Roux",
            "David",
            "Bertrand",
            "Morel",
            "Fournier",
            "Girard",
            "Bonnet",
            "Dupont",
            "Lambert",
            "Fontaine",
            "Rousseau",
        ],
    }

    # Email domains
    EMAIL_DOMAINS = {
        "personal": [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "icloud.com",
            "protonmail.com",
            "aol.com",
            "mail.com",
            "yandex.com",
            "zoho.com",
        ],
        "business": [
            "company.com",
            "business.io",
            "work.co",
            "corporate.net",
            "enterprise.org",
            "tech.io",
            "consulting.com",
            "agency.co",
            "studio.design",
            "labs.tech",
        ],
    }

    # Company names components
    COMPANY_PREFIXES = [
        "Global",
        "Premier",
        "Advanced",
        "Dynamic",
        "Strategic",
        "Innovative",
        "Digital",
        "Modern",
        "Future",
        "Smart",
        "Tech",
        "Pro",
        "Elite",
        "Prime",
    ]

    COMPANY_SUFFIXES = [
        "Solutions",
        "Systems",
        "Technologies",
        "Innovations",
        "Services",
        "Group",
        "Industries",
        "Enterprises",
        "Corporation",
        "Partners",
        "Consulting",
        "Labs",
        "Dynamics",
        "Networks",
        "Ventures",
    ]

    # Street names and types
    STREET_NAMES = [
        "Main",
        "High",
        "Park",
        "Oak",
        "Pine",
        "Maple",
        "Cedar",
        "Elm",
        "Washington",
        "Lake",
        "Hill",
        "First",
        "Second",
        "Third",
        "Fourth",
        "Fifth",
        "Spring",
        "Church",
        "Market",
        "Court",
        "North",
        "South",
        "East",
        "West",
        "Central",
    ]

    STREET_TYPES = [
        "Street",
        "Road",
        "Avenue",
        "Boulevard",
        "Lane",
        "Drive",
        "Court",
        "Place",
        "Way",
        "Parkway",
        "Circle",
        "Square",
        "Trail",
        "Pike",
        "Path",
    ]

    # Cities by region
    CITIES = {
        "en_US": [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
            "Austin",
            "Jacksonville",
            "Fort Worth",
            "Columbus",
            "San Francisco",
            "Charlotte",
            "Indianapolis",
            "Seattle",
            "Denver",
            "Washington",
            "Boston",
            "Nashville",
            "Portland",
        ],
        "en_GB": [
            "London",
            "Birmingham",
            "Leeds",
            "Glasgow",
            "Sheffield",
            "Bradford",
            "Manchester",
            "Edinburgh",
            "Liverpool",
            "Bristol",
            "Cardiff",
            "Belfast",
            "Leicester",
            "Nottingham",
            "Newcastle",
            "Coventry",
            "Hull",
            "Stoke",
            "Southampton",
            "Portsmouth",
            "Derby",
            "Reading",
            "Norwich",
            "Plymouth",
        ],
    }

    # States/Regions
    STATES = {
        "en_US": [
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ]
    }

    # Country codes
    COUNTRY_CODES = {
        "en_US": "US",
        "en_GB": "GB",
        "es_ES": "ES",
        "de_DE": "DE",
        "fr_FR": "FR",
        "it_IT": "IT",
        "pt_BR": "BR",
        "ja_JP": "JP",
        "zh_CN": "CN",
        "ko_KR": "KR",
    }

    def __init__(self, locale: str = "en_US"):
        self.locale = locale
        self.random = random.Random()

    def set_seed(self, seed: int):
        """Set random seed for reproducibility"""
        self.random.seed(seed)
        random.seed(seed)

    def get_first_name(self) -> str:
        """Get a random first name"""
        names = self.FIRST_NAMES.get(self.locale, self.FIRST_NAMES["en_US"])
        return self.random.choice(names)

    def get_last_name(self) -> str:
        """Get a random last name"""
        names = self.LAST_NAMES.get(self.locale, self.LAST_NAMES["en_US"])
        return self.random.choice(names)

    def get_full_name(self) -> Tuple[str, str]:
        """Get a random full name (first, last)"""
        return (self.get_first_name(), self.get_last_name())

    def get_email(
        self,
        first_name: str = None,
        last_name: str = None,
        domain_type: str = "personal",
    ) -> str:
        """Generate a realistic email address"""
        if not first_name:
            first_name = self.get_first_name()
        if not last_name:
            last_name = self.get_last_name()

        first = first_name.lower().replace(" ", "")
        last = last_name.lower().replace(" ", "")

        # Different email patterns
        patterns = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first[0]}{last}",
            f"{first}_{last}",
            f"{first}.{last[0]}",
            f"{first}{self.random.randint(1, 999)}",
        ]

        pattern = self.random.choice(patterns)
        domains = self.EMAIL_DOMAINS.get(domain_type, self.EMAIL_DOMAINS["personal"])
        domain = self.random.choice(domains)

        return f"{pattern}@{domain}"

    def get_phone(self, country_code: str = None) -> str:
        """Generate a phone number with country code"""
        if not country_code:
            if self.locale == "en_US":
                country_code = "+1"
            elif self.locale == "en_GB":
                country_code = "+44"
            elif self.locale == "es_ES":
                country_code = "+34"
            elif self.locale == "de_DE":
                country_code = "+49"
            elif self.locale == "fr_FR":
                country_code = "+33"
            else:
                country_code = "+1"

        # Generate number based on country
        if country_code == "+1":
            # US format: +1 (XXX) XXX-XXXX
            # Use only valid US area codes (avoid 355, 555, 700, etc.)
            valid_area_codes = [
                201, 202, 203, 205, 206, 207, 208, 209, 210, 212, 213, 214, 215, 216, 217, 218,
                219, 224, 225, 228, 229, 231, 234, 239, 240, 248, 251, 252, 253, 254, 256, 260,
                262, 267, 269, 270, 276, 281, 301, 302, 303, 304, 305, 307, 308, 309, 310, 312,
                313, 314, 315, 316, 317, 318, 319, 320, 321, 323, 325, 330, 331, 334, 336, 337,
                339, 347, 351, 352, 360, 361, 385, 386, 401, 402, 404, 405, 406, 407, 408, 409,
                410, 412, 413, 414, 415, 417, 419, 423, 424, 425, 430, 432, 434, 435, 440, 442,
                443, 469, 470, 475, 478, 479, 480, 484, 501, 502, 503, 504, 505, 507, 508, 509,
                510, 512, 513, 515, 516, 517, 518, 520, 530, 534, 539, 540, 541, 551, 559, 561,
                562, 563, 567, 570, 571, 573, 574, 575, 580, 585, 586, 601, 602, 603, 605, 606,
                607, 608, 609, 610, 612, 614, 615, 616, 617, 618, 619, 620, 623, 626, 628, 629,
                630, 631, 636, 641, 646, 650, 651, 657, 660, 661, 662, 667, 669, 678, 681, 682,
                701, 702, 703, 704, 706, 707, 708, 712, 713, 714, 715, 716, 717, 718, 719, 720,
                724, 725, 727, 731, 732, 734, 737, 740, 743, 747, 754, 757, 760, 762, 763, 765,
                769, 770, 772, 773, 774, 775, 779, 781, 785, 786, 801, 802, 803, 804, 805, 806,
                808, 810, 812, 813, 814, 815, 816, 817, 818, 828, 830, 831, 832, 843, 845, 847,
                848, 850, 856, 857, 858, 859, 860, 862, 863, 864, 865, 870, 872, 878, 901, 903,
                904, 906, 907, 908, 909, 910, 912, 913, 914, 915, 916, 917, 918, 919, 920, 925,
                928, 929, 930, 931, 936, 937, 938, 940, 941, 947, 949, 951, 952, 954, 956, 959,
                970, 971, 972, 973, 978, 979, 980, 984, 985, 989
            ]
            area = self.random.choice(valid_area_codes)
            prefix = self.random.randint(200, 999)
            suffix = self.random.randint(1000, 9999)
            return f"{country_code}{area}{prefix}{suffix}"
        else:
            # Generic international format
            number = "".join([str(self.random.randint(0, 9)) for _ in range(9)])
            return f"{country_code}{number}"

    def get_address(self) -> Dict[str, str]:
        """Generate a complete address"""
        street_num = self.random.randint(1, 9999)
        street_name = self.random.choice(self.STREET_NAMES)
        street_type = self.random.choice(self.STREET_TYPES)

        address = {
            "address1": f"{street_num} {street_name} {street_type}",
            "city": self.random.choice(
                self.CITIES.get(self.locale, self.CITIES["en_US"])
            ),
            "state": self.random.choice(self.STATES.get("en_US", ["CA"])),
            "zip": str(self.random.randint(10000, 99999)),
            "country": self.COUNTRY_CODES.get(self.locale, "US"),
        }

        # Occasionally add address2
        if self.random.random() < 0.3:
            apt_type = self.random.choice(["Apt", "Suite", "Unit", "Floor"])
            apt_num = self.random.randint(1, 500)
            address["address2"] = f"{apt_type} {apt_num}"

        return address

    def get_date(self, past_days: int = 365, future_days: int = 0, format: str = "US") -> str:
        """Generate a random date
        
        Args:
            past_days: How many days in the past to generate from
            future_days: How many days in the future to generate to
            format: Date format - 'US' for MM/DD/YYYY, 'ISO' for YYYY-MM-DD
        """
        start_date = datetime.now() - timedelta(days=past_days)
        end_date = datetime.now() + timedelta(days=future_days)

        time_between = end_date - start_date
        days_between = time_between.days
        random_days = self.random.randint(0, days_between)

        random_date = start_date + timedelta(days=random_days)
        
        if format == "US":
            # US format: MM/DD/YYYY
            return random_date.strftime("%m/%d/%Y")
        else:
            # ISO format: YYYY-MM-DD
            return random_date.date().isoformat()

    def get_date_range(
        self, past_days: int = 365, max_duration: int = 30, format: str = "US"
    ) -> Dict[str, str]:
        """Generate a date range"""
        start = self.get_date(past_days=past_days, format="ISO")  # Use ISO for parsing
        start_date = datetime.fromisoformat(start)
        duration = self.random.randint(1, max_duration)
        end_date = start_date + timedelta(days=duration)

        if format == "US":
            return {
                "start": start_date.strftime("%m/%d/%Y"),
                "end": end_date.strftime("%m/%d/%Y")
            }
        else:
            return {"start": start, "end": end_date.date().isoformat()}

    def get_time(self) -> str:
        """Generate a random time"""
        hour = self.random.randint(0, 23)
        minute = self.random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"

    def get_website(self, company_name: str = None) -> str:
        """Generate a website URL"""
        if not company_name:
            company_name = self.get_company_name()

        # Clean company name for URL
        clean_name = company_name.lower()
        clean_name = "".join(c for c in clean_name if c.isalnum() or c.isspace())
        clean_name = clean_name.replace(" ", "")

        tlds = ["com", "io", "co", "net", "org", "tech", "app", "dev"]
        tld = self.random.choice(tlds)

        return f"https://www.{clean_name}.{tld}"

    def get_company_name(self) -> str:
        """Generate a company name"""
        if self.random.random() < 0.7:
            # Use prefix + suffix pattern
            prefix = self.random.choice(self.COMPANY_PREFIXES)
            suffix = self.random.choice(self.COMPANY_SUFFIXES)
            return f"{prefix} {suffix}"
        else:
            # Use last name + suffix pattern
            last_name = self.get_last_name()
            suffix = self.random.choice(self.COMPANY_SUFFIXES)
            return f"{last_name} {suffix}"

    def get_country_code(self) -> str:
        """Get country code for current locale"""
        return self.COUNTRY_CODES.get(self.locale, "US")

    def get_file_metadata(self, file_type: str = "document") -> Dict[str, any]:
        """Generate file upload metadata"""
        file_types = {
            "document": [
                ("pdf", "application/pdf", (50000, 5000000)),
                (
                    "docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    (20000, 2000000),
                ),
                ("doc", "application/msword", (20000, 2000000)),
                ("txt", "text/plain", (1000, 100000)),
            ],
            "image": [
                ("jpg", "image/jpeg", (100000, 10000000)),
                ("png", "image/png", (100000, 10000000)),
                ("gif", "image/gif", (50000, 5000000)),
                ("webp", "image/webp", (50000, 5000000)),
            ],
            "spreadsheet": [
                (
                    "xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    (10000, 5000000),
                ),
                ("xls", "application/vnd.ms-excel", (10000, 5000000)),
                ("csv", "text/csv", (1000, 1000000)),
            ],
        }

        options = file_types.get(file_type, file_types["document"])
        ext, mime, (min_size, max_size) = self.random.choice(options)

        # Generate filename
        words = ["report", "document", "file", "data", "export", "summary", "analysis"]
        name = f"{self.random.choice(words)}_{self.random.randint(1000, 9999)}.{ext}"

        return {
            "url": f"https://storage.example.com/uploads/{name}",
            "name": name,
            "size": self.random.randint(min_size, max_size),
            "type": mime,
        }

    def get_signature_data(self) -> str:
        """Generate a mock base64 signature"""
        # Generate a simple SVG signature-like pattern
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="300" height="100">
            <path d="M10,50 Q50,10 90,50 T170,50 Q210,10 250,50" 
                  stroke="black" stroke-width="2" fill="none"/>
        </svg>"""

        # Convert to base64 (mock - in real implementation would be actual image)
        import base64

        svg_bytes = svg.encode("utf-8")
        b64 = base64.b64encode(svg_bytes).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64}"

    def get_lorem_ipsum(self, words: int = 20) -> str:
        """Generate lorem ipsum text"""
        lorem_words = [
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "do",
            "eiusmod",
            "tempor",
            "incididunt",
            "ut",
            "labore",
            "et",
            "dolore",
            "magna",
            "aliqua",
            "enim",
            "ad",
            "minim",
            "veniam",
            "quis",
            "nostrud",
            "exercitation",
            "ullamco",
            "laboris",
            "nisi",
            "aliquip",
            "ex",
            "ea",
            "commodo",
            "consequat",
            "duis",
            "aute",
            "irure",
            "in",
            "reprehenderit",
            "voluptate",
            "velit",
            "esse",
            "cillum",
            "fugiat",
            "nulla",
            "pariatur",
            "excepteur",
            "sint",
            "occaecat",
            "cupidatat",
            "non",
            "proident",
            "sunt",
            "culpa",
            "qui",
            "officia",
            "deserunt",
            "mollit",
            "anim",
            "id",
            "est",
            "laborum",
        ]

        text = []
        for _ in range(words):
            text.append(self.random.choice(lorem_words))

        # Capitalize first word and add period
        result = " ".join(text)
        return result[0].upper() + result[1:] + "."
