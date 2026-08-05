import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path("../code").resolve()))
from config import SAMPLE_CLAIMS_CSV

def generate_mock_data():
    mock_data = {}
    with open(SAMPLE_CLAIMS_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row["user_id"]
            
            # Ground truth values
            gt_status = row["claim_status"]
            gt_evidence = row["evidence_standard_met"]
            gt_risk = row["risk_flags"].split(";") if row["risk_flags"] != "none" else []
            gt_issue = row["issue_type"]
            gt_part = row["object_part"]
            gt_valid = row["valid_image"]
            gt_sev = row["severity"]
            gt_supp = row["supporting_image_ids"].split(";") if row["supporting_image_ids"] != "none" else []
            
            # Text Extraction Mock
            text_mock = {
                "claimed_object_part": gt_part if gt_part != "unknown" else "unknown",
                "claimed_issue_type": gt_issue if gt_issue != "unknown" else "unknown",
                "claimed_severity_hint": gt_sev if gt_sev != "unknown" else "medium",
                "is_multi_part": False,
                "has_prompt_injection": False
            }
            
            # Vision Mock (Base)
            vision_mock = {
                "visible_object_type": row["claim_object"],
                "visible_object_part": gt_part if gt_part != "unknown" else "unknown",
                "visible_issue_type": gt_issue if gt_issue != "unknown" else "unknown",
                "visible_severity": gt_sev if gt_sev != "unknown" else "medium",
                "is_blurry": "blurry_image" in gt_risk,
                "is_low_light": "low_light_or_glare" in gt_risk,
                "has_watermark": "non_original_image" in gt_risk,
                "has_text_instruction": "text_instruction_present" in gt_risk,
            }

            # Adjustments for Fraud Flags
            if "wrong_object" in gt_risk:
                vision_mock["visible_object_type"] = "unknown"
            if "claim_mismatch" in gt_risk:
                vision_mock["visible_issue_type"] = "scratch" if gt_issue != "scratch" else "dent"
            if "wrong_angle" in gt_risk:
                vision_mock["visible_object_part"] = "unknown"
            if "damage_not_visible" in gt_risk:
                vision_mock["visible_issue_type"] = "none"
            if "wrong_object_part" in gt_risk:
                vision_mock["visible_object_part"] = "wrong_part"
                
            mock_data[uid] = {
                "text": text_mock,
                "vision": vision_mock
            }
            
    with open("mock_data.json", "w") as f:
        json.dump(mock_data, f, indent=2)

if __name__ == "__main__":
    generate_mock_data()
