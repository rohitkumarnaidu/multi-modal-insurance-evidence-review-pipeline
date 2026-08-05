# Product Requirements Document: Multi-Modal Evidence Review

## Objective
Build a system that verifies damage claims using images, a short claim conversation, user history, and minimum evidence requirements.

Each claim is about one of three object types:
- `car`
- `laptop`
- `package`

The system must decide whether the submitted images support the user's claim, contradict it, or do not provide enough information.

The images are the primary source of truth. The user conversation defines what needs to be checked. User history can add risk context, but should not override clear visual evidence by itself.

## System Capabilities

For each claim, the system must:
- Extract the actual damage claim from the conversation
- Inspect one or more submitted images
- Decide whether the image evidence is sufficient
- Identify the visible issue type
- Identify the relevant object part
- Decide whether the claim is supported, contradicted, or lacks enough information
- Select the image IDs that support the decision
- Flag image quality, mismatch, authenticity, or user-history risks
- Estimate severity
- Produce short justifications grounded in the images

## Input Schema
The system reads from `claims.csv`, where each row represents one damage claim.

Input fields:
- `user_id`: user submitting the claim; use this to look up `user_history.csv`
- `image_paths`: one or more submitted image paths
- `user_claim`: chat transcript about the issue
- `claim_object`: `car`, `laptop`, or `package`

## Evidence Requirements Schema
The system must validate evidence against `evidence_requirements.csv`:
- `requirement_id`: identifier for the rule
- `claim_object`: `car`, `laptop`, `package`, or `all`
- `applies_to`: issue family, such as `dent or scratch`
- `minimum_image_evidence`: minimum visual evidence needed to evaluate that kind of claim

## User History Schema
The system integrates risk context from `user_history.csv`:
- `user_id`
- `past_claim_count`
- `accept_claim`
- `manual_review_claim`
- `rejected_claim`
- `last_90_days_claim_count`
- `history_flags`
- `history_summary`

## Output Schema
The system must produce a CSV output (`output.csv`) with the following columns in order:
- `user_id`
- `image_paths`
- `user_claim`
- `claim_object`
- `evidence_standard_met`: `true` if the image set is sufficient to evaluate the claim; otherwise `false`
- `evidence_standard_met_reason`: short reason for the evidence decision
- `risk_flags`: semicolon-separated risk flags, or `none`
- `issue_type`: visible issue type
- `object_part`: relevant object part
- `claim_status`: final decision: `supported`, `contradicted`, or `not_enough_information`
- `claim_status_justification`: concise image-grounded explanation; mention relevant image IDs when helpful
- `supporting_image_ids`: image IDs supporting the decision, separated by semicolons; use `none` if no image is sufficient
- `valid_image`: `true` if the image set is usable for automated review; otherwise `false`
- `severity`: `none`, `low`, `medium`, `high`, or `unknown`

## Allowed Taxonomy
The system must enforce the following value enumerations:

**`claim_status`**: `supported`, `contradicted`, `not_enough_information`

**`issue_type`**: `dent`, `scratch`, `crack`, `glass_shatter`, `broken_part`, `missing_part`, `torn_packaging`, `crushed_packaging`, `water_damage`, `stain`, `none`, `unknown`

**Car `object_part`**: `front_bumper`, `rear_bumper`, `door`, `hood`, `windshield`, `side_mirror`, `headlight`, `taillight`, `fender`, `quarter_panel`, `body`, `unknown`

**Laptop `object_part`**: `screen`, `keyboard`, `trackpad`, `hinge`, `lid`, `corner`, `port`, `base`, `body`, `unknown`

**Package `object_part`**: `box`, `package_corner`, `package_side`, `seal`, `label`, `contents`, `item`, `unknown`

**`risk_flags`**: `none`, `blurry_image`, `cropped_or_obstructed`, `low_light_or_glare`, `wrong_angle`, `wrong_object`, `wrong_object_part`, `damage_not_visible`, `claim_mismatch`, `possible_manipulation`, `non_original_image`, `text_instruction_present`, `user_history_risk`, `manual_review_required`

*Note: Use `issue_type=none` when the relevant part is visible and no issue is present. Use `unknown` when the issue or part cannot be determined.*
