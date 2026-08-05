# Multi-Modal Evidence Review Pipeline

## Overview
An automated AI pipeline for insurance and customer support teams. It uses Vision-Language Models (VLMs), object detection (YOLOv8), and deterministic rule engines to verify damage claims for cars, laptops, and packages while automatically flagging fraudulent or mismatched images.

## Architecture

```mermaid
graph TD
    A[User Claim & Images] --> B(E1: Text Extraction - LLM)
    A --> C(E2: Vision Analysis - VLM x N images)
    
    B --> D{E3: Evidence Sufficiency}
    C --> D
    
    D --> E(E4: Image Quality)
    E --> F(E5: Fraud Detection)
    F --> G(E6: User Risk History)
    G --> H(E7: Decision Engine)
    H --> I(E8: Explainability)
    
    I --> J[[Final Claim Status & Output]]
    
    classDef llm fill:#f9d0c4,stroke:#333,stroke-width:2px;
    classDef rule fill:#d4e157,stroke:#333,stroke-width:2px;
    classDef decision fill:#81c784,stroke:#333,stroke-width:2px;
    
    class B,C llm;
    class D,E,F,G rule;
    class H,I decision;
```

- **8 Deterministic Engines**: Claim extraction, Vision analysis, Evidence checking, Quality assessment, Fraud detection, Risk evaluation, Decision making, Explanation
- **4 LLM Providers**: Gemini 2.5 Flash → Groq (Llama 4 Scout) → OpenRouter → NVIDIA (Llama 4 Maverick) with automatic fallback
- **Per-key Rate Limiting**: Sliding-window RPM/RPD tracking with proactive key rotation
- **Multi-Model Comparison**: Independent runs per provider with majority-vote consensus

## Setup
```bash
pip install -r requirements.txt
# Add API keys to .env file
```

## .env Configuration
```
GEMINI_API_KEYS=key1,key2,key3
GROQ_API_KEY=your_key
OPENROUTER_API_KEY=your_key
NVIDIA_API_KEY=your_key
```

## Usage

### Quick Start
To get up and running quickly:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API keys
echo "GEMINI_API_KEY=your_key_here" > code/.env

# 3. Run the mock pipeline to verify functionality
cd code
python main.py --mode sample --provider mock --output ../dataset/sample_output.csv

# 4. Run the evaluation script
python evaluation/main.py --no-run
```

### Command Line Options
```bash
python main.py                          # Standard run (auto fallback)
python main.py --mode sample            # Run on sample claims
python main.py --provider nvidia        # Use specific provider
python main.py --parallel --workers 10  # High-throughput parallel execution
python main.py --retry-failed           # Re-process only failed claims
python compare_models.py --report-only  # Cross-model comparison
```

## Production Deployment
For high-volume production use cases (e.g., thousands of claims per day):
1. **Parallelization**: Set `MAX_WORKERS` in your `.env` or use the `--parallel` CLI flag. The system uses a ThreadPoolExecutor to handle concurrent API calls efficiently.
2. **Robust Hashing**: The `perceptual_hash.py` engine supports local image hashing. In production, connect this to your cloud blob storage (e.g., S3 or GCS) for deduplication.
3. **Orchestration**: See [Cloud Orchestration](docs/cloud_orchestration.md) for how to wrap this pipeline in Apache Airflow or Dagster.

## Pipeline Flow
1. Load claims from CSV + user history + evidence requirements
2. For each claim:
   - **E1 Claim Engine**: Extract claimed part/issue from conversation text (1 LLM call)
   - **E2 Vision Engine**: Analyze each image independently (N VLM calls)
   - **E3 Evidence Engine**: Check if evidence meets requirements (deterministic)
   - **E4 Quality Engine**: Assess image quality — blur, watermarks (deterministic)
   - **E5 Fraud Engine**: 8 fraud signal checks — wrong object, injection, manipulation (deterministic)
   - **E6 Risk Engine**: User history risk propagation (deterministic)
   - **E7 Decision Engine**: Final status determination (deterministic)
   - **E8 Explain Engine**: Consistency polish (deterministic)
3. Write output CSV with 14 columns

## Key Design Decisions
- **Two-call design**: Each image analyzed independently (prevents cross-contamination)
- **File-based caching**: SHA-256 keyed JSON cache, re-runs skip processed claims
- **Enum enforcement**: All output fields validated against allowed values
- **Graceful degradation**: API failures → "unknown" fallback, never crashes

## Documentation

| Document | Description |
|----------|-------------|
| [**PROJECT_DESIGN.md**](docs/PROJECT_DESIGN.md) | Master design document — architecture, tech stack, limitations, enterprise roadmap, Mermaid diagrams |
| [architecture.md](docs/architecture.md) | 10-engine pipeline deep dive |
| [cloud_orchestration.md](docs/cloud_orchestration.md) | Apache Airflow DAG integration guide |
| [IMPLEMENTATION_OVERVIEW.md](code/IMPLEMENTATION_OVERVIEW.md) | File-by-file code breakdown with honest assessments |
| [problem_statement.md](problem_statement.md) | Original product requirements |

