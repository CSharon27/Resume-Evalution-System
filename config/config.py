"""
HireLens Configuration
System-wide configuration settings for the resume evaluation system
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent.parent

# Data Storage Paths
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PARSED_RESUMES_PATH = DATA_DIR / "parsed_resumes.json"
JOB_DESCRIPTIONS_PATH = DATA_DIR / "job_descriptions.json"
EVALUATIONS_PATH = DATA_DIR / "evaluations.json"
SKILL_GAPS_PATH = DATA_DIR / "skill_gaps.json"
RECOMMENDATIONS_PATH = DATA_DIR / "recommendations.json"
FEEDBACK_PATH = DATA_DIR / "feedback.json"
COURSES_DATASET_PATH = DATA_DIR / "courses_dataset.json"

# Upload Directory
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# NLP Model Settings
SPACY_MODEL = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

# Evaluation Scoring Weights (must sum to 1.0)
TFIDF_WEIGHT = 0.3
FUZZY_WEIGHT = 0.3
EMBEDDING_WEIGHT = 0.4

# Classification Thresholds
HIGH_RELEVANCE_THRESHOLD = 75
MEDIUM_RELEVANCE_THRESHOLD = 50

# Fuzzy Matching Settings
FUZZY_MATCH_THRESHOLD = 70  # 0-100, minimum score for skill match

# Course Recommendation Settings
MAX_COURSES_PER_SKILL = 3
MIN_COURSE_RATING = 4.0

# Batch Processing Settings
MAX_BATCH_SIZE = 100

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "logs" / "hirelens.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True

# Streamlit Settings
STREAMLIT_PORT = 8501

# Skill Taxonomy - Comprehensive technical skills list (expandable)
TECHNICAL_SKILLS = [
    # Programming Languages (with variations)
    "Python", "Java", "JavaScript", "JS", "TypeScript", "TS", "C++", "C#", "C Sharp", "Go", "Golang", "Rust", 
    "Ruby", "Ruby on Rails", "RoR", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl",
    "Objective-C", "Dart", "Elixir", "Clojure", "Haskell", "Erlang", "Julia", "VB.NET",
    "Visual Basic", "COBOL", "Fortran", "Assembly", "Shell Scripting", "Bash", "PowerShell",
    
    # Web Development (Frontend)
    "React", "React.js", "ReactJS", "Angular", "AngularJS", "Vue", "Vue.js", "VueJS",
    "Svelte", "Next.js", "Nuxt.js", "Gatsby", "HTML", "HTML5", "CSS", "CSS3", 
    "SASS", "SCSS", "LESS", "Bootstrap", "Tailwind", "Tailwind CSS", "Material-UI",
    "Chakra UI", "Ant Design", "Semantic UI", "jQuery", "Webpack", "Vite", "Parcel",
    "Redux", "MobX", "Vuex", "Context API", "Styled Components", "Emotion",
    
    # Web Development (Backend)
    "Node.js", "Node", "Express", "Express.js", "Django", "Flask", "FastAPI",
    "Spring", "Spring Boot", "ASP.NET", ".NET", ".NET Core", "Laravel", "Symfony",
    "Rails", "Sinatra", "Koa", "Hapi", "Nest.js", "REST API", "RESTful", "GraphQL",
    "gRPC", "WebSocket", "Socket.io", "SOAP", "Microservices",
    
    # Databases (SQL)
    "SQL", "PostgreSQL", "Postgres", "MySQL", "MariaDB", "Oracle", "Oracle DB",
    "SQL Server", "MS SQL", "Microsoft SQL Server", "SQLite", "DB2", "T-SQL", "PL/SQL",
    
    # Databases (NoSQL)
    "MongoDB", "Mongo", "Redis", "Cassandra", "Couchbase", "DynamoDB", "Amazon DynamoDB",
    "Neo4j", "ArangoDB", "RethinkDB", "CouchDB", "Firebase", "Firestore", "Realm",
    "Elasticsearch", "OpenSearch", "Solr", "Memcached",
    
    # Cloud Platforms (AWS)
    "AWS", "Amazon Web Services", "EC2", "S3", "Lambda", "RDS", "DynamoDB",
    "CloudFront", "Route 53", "ECS", "EKS", "Elastic Beanstalk", "CloudFormation",
    "CloudWatch", "IAM", "VPC", "SNS", "SQS", "API Gateway", "Amplify",
    "ElastiCache", "Redshift", "Athena", "Glue", "EMR", "SageMaker",
    
    # Cloud Platforms (Azure)
    "Azure", "Microsoft Azure", "Azure Functions", "Azure DevOps", "Azure AD",
    "Azure SQL", "Cosmos DB", "Azure Storage", "Azure ML", "Azure Kubernetes",
    
    # Cloud Platforms (GCP)
    "GCP", "Google Cloud", "Google Cloud Platform", "BigQuery", "Cloud Functions",
    "Cloud Run", "GKE", "Google Kubernetes Engine", "Cloud Storage", "Pub/Sub",
    "Dataflow", "Cloud SQL", "Firestore", "App Engine", "Compute Engine",
    
    # Cloud Platforms (Other)
    "Heroku", "DigitalOcean", "Linode", "Vercel", "Netlify", "Cloudflare",
    "Railway", "Render", "Fly.io",
    
    # DevOps & CI/CD
    "Docker", "Kubernetes", "K8s", "Helm", "Jenkins", "GitLab CI", "GitLab CI/CD",
    "GitHub Actions", "CircleCI", "Travis CI", "Bamboo", "TeamCity", "ArgoCD",
    "Terraform", "Ansible", "Chef", "Puppet", "SaltStack", "Vagrant", "Packer",
    "CI/CD", "Continuous Integration", "Continuous Deployment", "DevOps",
    
    # Version Control
    "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Subversion", "Mercurial",
    "Git Flow", "GitHub Flow",
    
    # Containerization & Orchestration
    "Container", "Containerization", "Docker Compose", "Docker Swarm",
    "Podman", "containerd", "CRI-O", "Service Mesh", "Istio", "Linkerd", "Consul",
    
    # Monitoring & Logging
    "Prometheus", "Grafana", "DataDog", "New Relic", "Splunk", "ELK Stack",
    "Elasticsearch", "Logstash", "Kibana", "Fluentd", "Jaeger", "Zipkin",
    "CloudWatch", "Azure Monitor", "Stackdriver", "Sentry", "Rollbar",
    
    # Data Science & ML
    "Machine Learning", "ML", "Deep Learning", "AI", "Artificial Intelligence",
    "TensorFlow", "PyTorch", "Scikit-learn", "sklearn", "Keras", "Pandas",
    "NumPy", "Matplotlib", "Seaborn", "Plotly", "Jupyter", "Jupyter Notebook",
    "JupyterLab", "NLP", "Natural Language Processing", "Computer Vision", "CV",
    "Neural Networks", "CNN", "RNN", "LSTM", "GAN", "Transformer", "BERT",
    "GPT", "LLM", "Large Language Models", "XGBoost", "LightGBM", "CatBoost",
    "Hugging Face", "spaCy", "NLTK", "OpenCV", "YOLO", "ResNet",
    
    # Big Data
    "Big Data", "Apache Spark", "Spark", "PySpark", "Hadoop", "HDFS", "MapReduce",
    "Kafka", "Apache Kafka", "Airflow", "Apache Airflow", "Hive", "Presto",
    "Flink", "Storm", "NiFi", "Beam", "Databricks", "Snowflake", "dbt",
    
    # Mobile Development
    "React Native", "Flutter", "Android", "iOS", "SwiftUI", "UIKit",
    "Jetpack Compose", "Xamarin", "Ionic", "Cordova", "PhoneGap",
    "Mobile Development", "App Development", "Xcode", "Android Studio",
    
    # Testing & Quality Assurance
    "Jest", "Mocha", "Chai", "Jasmine", "PyTest", "pytest", "Unittest",
    "JUnit", "TestNG", "Selenium", "Cypress", "Playwright", "Puppeteer",
    "Unit Testing", "Integration Testing", "E2E Testing", "Test Automation",
    "TDD", "Test Driven Development", "BDD", "Behavior Driven Development",
    "QA", "Quality Assurance", "Testing", "Postman", "JMeter", "LoadRunner",
    
    # Security
    "Security", "Cybersecurity", "Information Security", "Penetration Testing",
    "OWASP", "OAuth", "JWT", "SSL", "TLS", "Encryption", "Authentication",
    "Authorization", "SAML", "SSO", "Single Sign-On", "Firewall", "VPN",
    "WAF", "Web Application Firewall",
    
    # API & Integration
    "API", "REST", "RESTful API", "GraphQL API", "SOAP API", "Webhook",
    "API Gateway", "API Design", "Swagger", "OpenAPI", "Postman", "Insomnia",
    "API Integration", "Third-party Integration", "Zapier", "IFTTT",
    
    # Message Queues & Streaming
    "RabbitMQ", "ActiveMQ", "ZeroMQ", "NATS", "Pulsar", "Event Driven Architecture",
    "Message Queue", "Event Streaming", "Pub/Sub",
    
    # Frontend Tools & Build Systems
    "Webpack", "Vite", "Rollup", "esbuild", "Babel", "ESLint", "Prettier",
    "npm", "yarn", "pnpm", "Lerna", "Turborepo", "Nx",
    
    # CMS & E-commerce
    "WordPress", "Drupal", "Joomla", "Contentful", "Strapi", "Sanity",
    "Shopify", "WooCommerce", "Magento", "BigCommerce",
    
    # Design & UI/UX
    "Figma", "Sketch", "Adobe XD", "Photoshop", "Illustrator", "InVision",
    "UI Design", "UX Design", "User Experience", "User Interface", "Prototyping",
    "Wireframing", "Responsive Design", "Mobile First", "Accessibility", "WCAG",
    
    # Other Technologies
    "Linux", "Unix", "Ubuntu", "CentOS", "Red Hat", "RHEL", "Windows Server",
    "Nginx", "Apache", "Tomcat", "IIS", "Load Balancing", "CDN", "DNS",
    "Serverless", "Edge Computing", "Blockchain", "Cryptocurrency", "Web3",
    "Solidity", "Smart Contracts", "Ethereum", "AR", "VR", "IoT",
    "Internet of Things", "Raspberry Pi", "Arduino",
    
    # Methodologies & Practices
    "Agile", "Scrum", "Kanban", "Lean", "SAFe", "Waterfall", "XP", "Extreme Programming",
    "Sprint Planning", "Retrospective", "Daily Standup", "JIRA", "Confluence",
    "Trello", "Asana", "Monday.com", "Notion", "Code Review", "Pair Programming",
    "Design Patterns", "SOLID Principles", "Clean Code", "Refactoring",
    "System Design", "Microservices Architecture", "Monolithic Architecture",
    "Scalability", "High Availability", "Load Balancing", "Caching",
    "Performance Optimization", "SEO", "Search Engine Optimization",
    
    # Data Formats & Protocols
    "JSON", "XML", "YAML", "CSV", "Protobuf", "Avro", "Parquet", "ORC",
    "HTTP", "HTTPS", "TCP/IP", "UDP", "MQTT", "AMQP", "WebRTC",
    
    # Business Intelligence & Analytics
    "Tableau", "Power BI", "Looker", "Metabase", "Superset", "Data Visualization",
    "Business Intelligence", "BI", "ETL", "Data Warehousing", "Data Pipeline",
    "Data Engineering", "Analytics",
    
    # Programming Concepts
    "OOP", "Object Oriented Programming", "Functional Programming", "Async/Await",
    "Promises", "Callbacks", "Multithreading", "Concurrency", "Parallelism",
    "Data Structures", "Algorithms", "Recursion", "Dynamic Programming",
    "Binary Search", "Sorting", "Hashing", "Trees", "Graphs", "Linked Lists",
    
    # Soft Skills & Management
    "Leadership", "Team Lead", "Tech Lead", "Engineering Manager", "Project Management",
    "Communication", "Problem Solving", "Critical Thinking", "Team Collaboration",
    "Mentoring", "Code Review", "Technical Writing", "Documentation", "Presentation",
    "Stakeholder Management", "Time Management", "Conflict Resolution"
]

# Education Keywords
EDUCATION_KEYWORDS = [
    "Bachelor", "Master", "PhD", "B.Tech", "M.Tech", "B.S.", "M.S.",
    "B.E.", "M.E.", "MBA", "B.A.", "M.A.", "Diploma", "Degree",
    "University", "College", "Institute", "School"
]

# Experience Keywords
EXPERIENCE_KEYWORDS = [
    "Software Engineer", "Developer", "Programmer", "Architect", "Lead",
    "Senior", "Junior", "Intern", "Analyst", "Consultant", "Manager",
    "Director", "VP", "CTO", "CEO", "Designer", "Specialist"
]
