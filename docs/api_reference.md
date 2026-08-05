# API Reference

The Multi-Modal Evidence Review platform provides a RESTful HTTP API built using FastAPI.

## Base URL
`http://localhost:8000`

---

## `POST /api/v1/claims/submit`

Submits a new claim for evaluation by the AI orchestration pipeline.

### Request Format
This endpoint accepts `multipart/form-data`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | `string` | Yes | The ID of the user submitting the claim. Used to look up risk history. |
| `claim_object` | `string` | Yes | What the claim is regarding (e.g., `car`, `laptop`, `package`). |
| `user_claim` | `string` | Yes | The conversational text description of the damage. |
| `use_mock` | `boolean` | No | If `true`, uses the Mock AI engine for fast, local simulated responses. Default is `false`. |
| `images` | `UploadFile[]`| Yes | An array of image files containing visual evidence of the claim. |

### Response Schema

Returns a `ClaimResponse` object indicating the evaluation outcome.

```json
{
  "user_id": "U1001",
  "claim_status": "supported",
  "issue_type": "scratch",
  "object_part": "door",
  "severity": "low",
  "evidence_standard_met": true,
  "risk_flags": [
    "user_history_high_risk"
  ],
  "claim_status_justification": "The visual evidence matches the user's claim perfectly."
}
```

---

## `GET /health`

Used for uptime monitoring and load-balancer checks.

### Response
```json
{
  "status": "ok"
}
```
