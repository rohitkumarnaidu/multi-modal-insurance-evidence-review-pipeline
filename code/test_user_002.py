# ruff: noqa: E402
import logging
from pathlib import Path

# Turn on debug logging
logging.getLogger().setLevel(logging.DEBUG)

from main import run_pipeline

print("STARTING TEST")
try:
    run_pipeline(
        claims_csv=Path("../dataset/sample_claims.csv"),
        output_csv=Path("test_output.csv"),
        mode="sample",
        provider="mock",
        parallel=False
    )
except Exception:

    import traceback
    traceback.print_exc()
print("FINISHED TEST")
