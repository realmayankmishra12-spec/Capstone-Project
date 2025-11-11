# Capstone-Project

# SDG16 Evidence Judgment System

A sophisticated Django-based application for submitting, processing, and AI-analyzing evidence related to Sustainable Development Goal 16 (Peace, Justice and Strong Institutions). The system integrates OCR technology, AI analysis, and image processing to validate evidence submissions.

## Project Overview

This application enables organizations and individuals to submit evidence of corruption, justice violations, and institutional accountability. Each submission undergoes multi-stage processing including OCR extraction, AI judgment, and confidence scoring.

## System Architecture

```mermaid
graph TB
    subgraph Input["Evidence Input Layer"]
        U1[User Submission]
        U2[Multiple Images]
        U3[Text Description]
    end
    
    subgraph Processing["Processing Pipeline"]
        P1[Image Upload Handler]
        P2[OCR Extraction]
        P3[Text Analysis]
        P4[AI Judgment]
    end
    
    subgraph Storage["Data Storage"]
        S1[(Database)]
        S2[Media Files]
        S3[Metadata]
    end
    
    subgraph Output["Results & Insights"]
        O1[Judgment Report]
        O2[Confidence Scores]
        O3[Pattern Analysis]
    end
    
    Input --> Processing
    Processing --> Storage
    Storage --> Output
    
    classDef inputStyle fill:#3a5f8f,color:#ffffff,stroke:#2c4563,stroke-width:2px
    classDef processStyle fill:#1e5a96,color:#ffffff,stroke:#134a7a,stroke-width:2px
    classDef storageStyle fill:#2d7a4a,color:#ffffff,stroke:#1f5632,stroke-width:2px
    classDef outputStyle fill:#8b4f7c,color:#ffffff,stroke:#6a3a5b,stroke-width:2px
    
    class U1,U2,U3 inputStyle
    class P1,P2,P3,P4 processStyle
    class S1,S2,S3 storageStyle
    class O1,O2,O3 outputStyle
```

## Evidence Processing Flow

```mermaid
flowchart TD
    Start([Evidence Submission]) --> Validate{Format Valid?}
    
    Validate -->|Invalid| ErrorVal[Validation Error]
    Validate -->|Valid| Upload[Upload Images]
    
    Upload --> OCRProcess[Pytesseract OCR]
    OCRProcess --> TextExtract[Extract Text Content]
    
    TextExtract --> ConfCheck{Confidence Above 60%?}
    ConfCheck -->|Low| WarningConf[Flag Low Confidence]
    ConfCheck -->|High| AIAnalysis[AI Judge Analysis]
    
    AIAnalysis --> PatternMatch[Pattern Recognition]
    PatternMatch --> KeywordDetect[Detect Keywords]
    
    KeywordDetect --> GenerateReport[Generate Report]
    GenerateReport --> SaveDB[Save to Database]
    
    SaveDB --> Success([Processing Complete])
    ErrorVal --> Failed([Submission Failed])
    WarningConf --> Success
    
    classDef startEnd fill:#2d5016,color:#ffffff,stroke:#1f3d0f,stroke-width:3px
    classDef validation fill:#d4a574,color:#000000,stroke:#a67c52,stroke-width:2px
    classDef processing fill:#4a7ba7,color:#ffffff,stroke:#365678,stroke-width:2px
    classDef decision fill:#b8860b,color:#000000,stroke:#8b6500,stroke-width:2px
    classDef warning fill:#cd6f5f,color:#ffffff,stroke:#9b4f3f,stroke-width:2px
    
    class Start,Success,Failed startEnd
    class Upload,TextExtract,GenerateReport,SaveDB processing
    class Validate,ConfCheck,KeywordDetect validation
    class ErrorVal,WarningConf warning
    class OCRProcess,AIAnalysis,PatternMatch decision
```

## AI Judgment Decision Tree

```mermaid
graph TB
    Start["Extracted Text Input"] --> CheckEmpty{Text Empty?}
    
    CheckEmpty -->|Yes| EmptyResult["No Text Found"]
    CheckEmpty -->|No| CheckKeywords{Contains Evidence Keywords?}
    
    CheckKeywords -->|No| NoEvidence["Insufficient Evidence"]
    CheckKeywords -->|Yes| CheckPattern{Pattern Match Found?}
    
    CheckPattern -->|No Pattern| PartialMatch["Partial Evidence"]
    CheckPattern -->|Pattern Found| AnalyzeType{Evidence Type?}
    
    AnalyzeType -->|Corruption| CorruptionLevel{Severity?}
    AnalyzeType -->|Justice| JusticeLevel{Violation Level?}
    AnalyzeType -->|Other| OtherType["Categorize as Other"]
    
    CorruptionLevel -->|High| HighCorruption["High Corruption Evidence"]
    CorruptionLevel -->|Medium| MediumCorruption["Medium Corruption Evidence"]
    CorruptionLevel -->|Low| LowCorruption["Low Corruption Evidence"]
    
    JusticeLevel -->|Critical| CriticalJustice["Critical Justice Violation"]
    JusticeLevel -->|Moderate| ModerateJustice["Moderate Justice Violation"]
    JusticeLevel -->|Minor| MinorJustice["Minor Justice Concern"]
    
    EmptyResult --> End["Generate Report"]
    NoEvidence --> End
    PartialMatch --> End
    OtherType --> End
    HighCorruption --> End
    MediumCorruption --> End
    LowCorruption --> End
    CriticalJustice --> End
    ModerateJustice --> End
    MinorJustice --> End
    
    classDef startNode fill:#2d5016,color:#ffffff,stroke:#1f3d0f,stroke-width:3px
    classDef decisionNode fill:#b8860b,color:#000000,stroke:#8b6500,stroke-width:2px
    classDef resultNode fill:#4a6fa5,color:#ffffff,stroke:#2d4563,stroke-width:2px
    classDef endNode fill:#8b4f7c,color:#ffffff,stroke:#6a3a5b,stroke-width:3px
    
    class Start startNode
    class CheckEmpty,CheckKeywords,CheckPattern,AnalyzeType,CorruptionLevel,JusticeLevel decisionNode
    class EmptyResult,NoEvidence,PartialMatch,OtherType,HighCorruption,MediumCorruption,LowCorruption,CriticalJustice,ModerateJustice,MinorJustice resultNode
    class End endNode
```

## Evidence Model Structure

```mermaid
graph TB
    subgraph Core["Core Fields"]
        C1["Title"]
        C2["Description"]
        C3["Submitted By"]
        C4["Date Submitted"]
    end
    
    subgraph ImageData["Image Processing"]
        I1["Image Evidence File"]
        I2["Extracted Text"]
        I3["Confidence Score"]
        I4["Image Analysis"]
    end
    
    subgraph MultiFile["Multi-File Support"]
        M1["Multiple Images Data"]
        M2["Total Files Count"]
        M3["Combined Text"]
        M4["Processing Status"]
    end
    
    subgraph Analysis["AI Analysis"]
        A1["AI Judgment Result"]
        A2["Pattern Detection"]
        A3["Evidence Classification"]
        A4["Confidence Rating"]
    end
    
    Core --> ImageData
    ImageData --> MultiFile
    MultiFile --> Analysis
    
    classDef coreStyle fill:#3a5f8f,color:#ffffff,stroke:#2c4563,stroke-width:2px
    classDef imageStyle fill:#5a6b8f,color:#ffffff,stroke:#3d4d6b,stroke-width:2px
    classDef multiStyle fill:#6b5a8f,color:#ffffff,stroke:#4d3d6b,stroke-width:2px
    classDef analysisStyle fill:#8f5a6b,color:#ffffff,stroke:#6b3d4d,stroke-width:2px
    
    class C1,C2,C3,C4 coreStyle
    class I1,I2,I3,I4 imageStyle
    class M1,M2,M3,M4 multiStyle
    class A1,A2,A3,A4 analysisStyle
```

## User Workflow

```mermaid
graph TB
    User["User Access"] --> Dashboard["Dashboard"]
    
    Dashboard --> CreateEvidence["Create Evidence"]
    Dashboard --> ViewHistory["View Submissions"]
    Dashboard --> CheckStatus["Check Status"]
    
    CreateEvidence --> EnterDetails["Enter Title & Description"]
    EnterDetails --> UploadImages["Upload Evidence Images"]
    UploadImages --> ReviewSubmit["Review & Submit"]
    ReviewSubmit --> Confirmation["Submission Confirmed"]
    
    ViewHistory --> ListEvidence["List All Evidence"]
    ListEvidence --> ViewDetails["View Details"]
    ViewDetails --> DownloadReport["Download Report"]
    
    CheckStatus --> ActiveSubmit["Check Active Submissions"]
    ActiveSubmit --> ViewProgress["View Processing Progress"]
    ViewProgress --> ViewResults["View Final Results"]
    
    Confirmation --> Store["Store in Database"]
    DownloadReport --> Report["Export Results"]
    ViewResults --> Report
    
    classDef userAction fill:#3a5f8f,color:#ffffff,stroke:#2c4563,stroke-width:2px
    classDef workflow fill:#1e5a96,color:#ffffff,stroke:#134a7a,stroke-width:2px
    classDef submission fill:#2d7a4a,color:#ffffff,stroke:#1f5632,stroke-width:2px
    classDef query fill:#8b4f7c,color:#ffffff,stroke:#6a3a5b,stroke-width:2px
    classDef storage fill:#a89033,color:#ffffff,stroke:#7a6b25,stroke-width:2px
    
    class User,Dashboard userAction
    class CreateEvidence,EnterDetails,UploadImages,ReviewSubmit workflow
    class ViewHistory,ListEvidence,ViewDetails submission
    class CheckStatus,ActiveSubmit,ViewProgress,ViewResults query
    class Confirmation,Store,DownloadReport,Report storage
```

## Django Application Structure

```mermaid
graph TB
    subgraph Web["Web Layer"]
        W1["Templates"]
        W2["Static Files"]
        W3["HTML Pages"]
    end
    
    subgraph Views["Views Layer"]
        V1["Evidence Views"]
        V2["Upload Handlers"]
        V3["API Endpoints"]
    end
    
    subgraph Models["Models Layer"]
        M1["Evidence Model"]
        M2["User Model"]
        M3["Metadata Storage"]
    end
    
    subgraph Processing["Processing Layer"]
        P1["OCR Engine"]
        P2["AI Judge"]
        P3["Image Processor"]
    end
    
    subgraph Database["Data Layer"]
        DB1["SQLite Database"]
        DB2["Media Storage"]
        DB3["Cache Layer"]
    end
    
    Web --> Views
    Views --> Models
    Models --> Processing
    Processing --> Database
    
    classDef webStyle fill:#3a5f8f,color:#ffffff,stroke:#2c4563,stroke-width:2px
    classDef viewStyle fill:#1e5a96,color:#ffffff,stroke:#134a7a,stroke-width:2px
    classDef modelStyle fill:#2d7a4a,color:#ffffff,stroke:#1f5632,stroke-width:2px
    classDef processStyle fill:#8b4f7c,color:#ffffff,stroke:#6a3a5b,stroke-width:2px
    classDef dbStyle fill:#a89033,color:#ffffff,stroke:#7a6b25,stroke-width:2px
    
    class W1,W2,W3 webStyle
    class V1,V2,V3 viewStyle
    class M1,M2,M3 modelStyle
    class P1,P2,P3 processStyle
    class DB1,DB2,DB3 dbStyle
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- Pillow for image processing
- pip for package management

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-repo/sdg16-evidence-system.git
cd sdg16
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## Core Features

### Evidence Submission
- Multi-image upload with support for multiple formats
- Real-time OCR text extraction
- Confidence scoring for extracted text
- Full metadata capture and storage

### AI Analysis
- Keyword-based evidence classification
- Pattern recognition for corruption indicators
- Justice violation detection
- Automatic severity assessment

### Processing Pipeline
- Asynchronous multi-file processing
- Error handling and recovery mechanisms
- Progress tracking for long submissions
- Detailed processing status reports

### Data Management
- Secure evidence storage
- Complete audit trail
- Export capabilities
- Search and filter functionality

## API Endpoints

### Evidence Management
- `POST /api/evidence/submit/` - Submit new evidence
- `GET /api/evidence/list/` - List all submissions
- `GET /api/evidence/<id>/` - Get evidence details
- `DELETE /api/evidence/<id>/` - Delete evidence

### Processing Status
- `GET /api/status/<submission_id>/` - Get processing status
- `GET /api/results/<submission_id>/` - Get analysis results

### Image Operations
- `POST /api/upload/images/` - Upload multiple images
- `GET /api/extract/text/` - Extract text from image
- `POST /api/analyze/image/` - Run AI analysis on image

## Configuration

### settings.py Key Settings

```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# OCR Configuration
TESSERACT_PATH = '/usr/bin/tesseract'  # Adjust per system
OCR_CONFIDENCE_THRESHOLD = 60.0
```

### Environment Variables

```bash
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=your-secret-key
OLLAMA_API_URL=http://localhost:11434
```

## Testing

Run the test suite:
```bash
python manage.py test
```

Run with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

**SDG16 Evidence System** - Advancing Peace, Justice and Strong Institutions through evidence-based accountability.

Capstone project for the Edunet and is done in collabration with [**Tanishq-JM**](https://github.com/Tanishq-JM) with [**LinkedIn**](https://www.linkedin.com/in/tanishq-jm)
