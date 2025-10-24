# Regulatory Knowledge Base - QCB Articles
REGULATORY_ARTICLES = {
    "1.1.1": {
        "article": "Article 1.1.1: Mandatory Verification",
        "category": "AML",
        "requirement": "Enhanced Customer Due Diligence (CDD) for users transacting more than QAR 10,000 per calendar month",
        "keywords": ["CDD", "due diligence", "verification", "QAR 10000", "monthly transactions"]
    },
    "1.1.2": {
        "article": "Article 1.1.2: Source of Funds",
        "category": "AML",
        "requirement": "For high-risk customers or transactions exceeding QAR 50,000, must obtain and maintain verified source of funds and wealth",
        "keywords": ["source of funds", "source of wealth", "QAR 50000", "high-risk", "verification"]
    },
    "1.1.3": {
        "article": "Article 1.1.3: KYC Documentation",
        "category": "AML",
        "requirement": "Minimum two forms of government-issued ID verified digitally. Proof of residency required for international users",
        "keywords": ["KYC", "identification", "government ID", "proof of residency", "international users"]
    },
    "1.1.4": {
        "article": "Article 1.1.4: Policy Document",
        "category": "AML",
        "requirement": "Board-approved Anti-Money Laundering (AML) and Counter-Financing of Terrorism (CFT) Policy with transaction monitoring rules",
        "keywords": ["AML policy", "CFT policy", "board-approved", "transaction monitoring", "policy document"]
    },
    "1.2.1": {
        "article": "Article 1.2.1: Transaction Monitoring",
        "category": "AML",
        "requirement": "Automated transaction monitoring system to identify and flag suspicious activity based on patterns, velocity, and deviation",
        "keywords": ["transaction monitoring", "automated system", "suspicious activity", "patterns", "velocity"]
    },
    "1.2.2": {
        "article": "Article 1.2.2: Reporting",
        "category": "AML",
        "requirement": "All Suspicious Transaction Reports (STRs) must be filed within 48 hours of detection",
        "keywords": ["STR", "suspicious transaction", "reporting", "48 hours", "filing"]
    },
    "2.1.1": {
        "article": "Article 2.1.1: Data Residency",
        "category": "Data Protection",
        "requirement": "All customer PII and transactional data related to Qatari citizens and residents MUST be stored on servers physically located within the State of Qatar",
        "keywords": ["data residency", "Qatar", "local storage", "PII", "transactional data", "server location"]
    },
    "2.1.2": {
        "article": "Article 2.1.2: Consent",
        "category": "Data Protection",
        "requirement": "Explicit, informed consent must be obtained for sharing any data with third-party service providers including cloud providers",
        "keywords": ["consent", "explicit consent", "third-party", "data sharing", "cloud providers"]
    },
    "2.2.1": {
        "article": "Article 2.2.1: Compliance Officer",
        "category": "Governance",
        "requirement": "Must appoint designated, independent Compliance Officer whose CV and credentials must be QCB-approved prior to licensing",
        "keywords": ["compliance officer", "designated officer", "independent", "QCB approval", "credentials"]
    },
    "2.2.2": {
        "article": "Article 2.2.2: Annual Audit",
        "category": "Governance",
        "requirement": "Annual external audit of all technology systems and compliance policies is mandatory",
        "keywords": ["annual audit", "external audit", "technology systems", "compliance policies", "mandatory"]
    }
}

# Capital Requirements by Category
CAPITAL_REQUIREMENTS = {
    "Category 1": {
        "name": "Payment Service Provider (PSP)",
        "minimum_capital": 5000000,  # QAR 5,000,000
        "description": "Entities providing domestic or cross-border payment processing or electronic money issuance"
    },
    "Category 2": {
        "name": "Marketplace Lending (P2P/Crowdfunding)",
        "minimum_capital": 7500000,  # QAR 7,500,000
        "description": "Platforms facilitating direct lending or capital raising between investors and businesses/consumers"
    },
    "Category 3": {
        "name": "Digital Wealth Management",
        "minimum_capital": 4000000,  # QAR 4,000,000
        "description": "Entities offering automated investment advice (Robo-advisory) or portfolio management"
    }
}

# Resource Mapping - Experts and Programs
RESOURCE_MAPPING = {
    "experts": {
        "EXPERT_C101": {
            "name": "Dr. Aisha Al-Mansoori",
            "specialization": "Data Residency and Cloud Compliance",
            "article_mapping": ["2.1.1"],
            "contact": "aisha.almansoori@qdb.qa"
        },
        "EXPERT_C102": {
            "name": "Mr. Karim Hassan",
            "specialization": "AML/CFT Policy Drafting and Training",
            "article_mapping": ["1.1.4", "1.2.1"],
            "contact": "karim.hassan@qdb.qa"
        }
    },
    "programs": {
        "QDB_INCUBATOR_001": {
            "name": "Fintech Regulatory Accelerator",
            "focus_areas": ["Licensing Strategy", "Corporate Structure", "QCB Engagement"],
            "description": "Comprehensive program for fintech licensing preparation",
            "duration": "12 weeks",
            "website": "https://qdb.qa/fintech-accelerator"
        },
        "QDB_EXPERT_002": {
            "name": "AML Compliance Workshop Series",
            "focus_areas": ["AML Policy Drafting", "Transaction Monitoring", "FATF Compliance"],
            "description": "Expert-led workshops on AML/CFT compliance",
            "duration": "6 weeks",
            "website": "https://qdb.qa/aml-workshop"
        }
    }
}
