# intake.json schema

```json
{
  "client_id": "EVG1xxx",
  "tax_year": 2025,
  "profile": {
    "taxpayer": {"name": "", "dob": "YYYY-MM-DD", "age_12_31_2025": 0, "occupation": ""},
    "spouse":   {"name": "", "dob": "", "age_12_31_2025": 0, "deceased_date": null},
    "marital_status_12_31_2025": "married | single | divorced | widowed | separated (still married)",
    "marital_events": ["e.g. married 12/20/2025", "separated 03/01/2025; divorce final 02/10/2026"],
    "prior_year_filing_status": "MFJ",
    "dependents": [{"name": "", "dob": "", "relationship": "", "months_in_home": 12, "ssn": "on file | pending",
                    "notes": "e.g. released to other parent via 8332 for 2025"}],
    "residency": [{"state": "IL", "city": "Chicago", "from": "2025-01-01", "to": "2025-12-31", "status": "resident"}],
    "contact": {"preferred": "email", "who": ""}
  },
  "documents": [
    {"file": "PBC/02_W-2_Employer.pdf", "type": "W-2", "owner": "T", "issuer": "Employer LLC", "issuer_id": "00-1234567",
     "status": "use | duplicate_of:<file> | superseded_by:<file> | informational | not_this_client | needs_manual_entry",
     "flags": ["CORRECTED", "DRAFT", "FINAL", "photo", "handwritten"],
     "data": {"box1": 0, "box2": 0, "box12": [["D", 0]], "box14": [["OVERTIME", 0]]},
     "notes": "anything unusual on the form"}
  ],
  "prior_year": {
    "items": [{"item": "Interest - Bank A", "py_amount": 980, "cy_status": "found | missing | ended (client confirmed) | resolved later in PBC",
               "cy_source": "PBC/13_...pdf"}],
    "carryovers": [{"item": "Capital loss carryover", "amount": 0, "character": "ST/LT", "source": "PERM/2024_..."}]
  },
  "conflicts": [{"topic": "", "organizer_says": "", "documents_show": "", "source": ""}],
  "filing_requirements": [{"filing": "IL-1040 resident", "trigger": "", "certainty": "required | likely | check"}],
  "issues_for_preparer": [{"area": "Schedule E", "issue": "", "evidence": "file + page/box"}],
  "open_items": [{"item": "", "why_it_matters": "", "blocking": true, "resolved_in_pbc": false}],
  "engagement": {"engagement_letter_signed": null, "extension_filed": null, "docs_received_within_15_days_of_deadline": false}
}
```
Keep `data` keys close to the form's box labels so the preparer can trace them.
