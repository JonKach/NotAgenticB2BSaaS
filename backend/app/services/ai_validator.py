"""AI output validator and sanitizer for HIPAA / EHR compliance.

This module provides `AIValidator` which inspects AI service outputs for
potential Protected Health Information (PHI), performs basic EHR/FHIR
structure checks, and produces a sanitized version of the output.

Notes:
- This is a best-effort heuristic validator and sanitizer. It detects common
  PHI patterns (SSN, phone, email, addresses, DOB, MRN) and redacts them.
- For FHIR/EHR validation this performs lightweight checks (e.g. `resourceType`)
  rather than full schema validation.
"""
from __future__ import annotations

import os
import json
import re
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx


DEFAULT_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b"),
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "mrn": re.compile(r"\b(?:MRN|mrn|Medical Record Number)[:\s-]*\d+\b"),
    "dob": re.compile(r"\b(?:DOB|Date of Birth|Birth Date)[:\s]*\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b", re.IGNORECASE),
    "address": re.compile(r"\d{1,5}\s+\w+(?:\s\w+){0,3}\s+(?:Street|St|Avenue|Ave|Drive|Dr|Road|Rd|Boulevard|Blvd|Lane|Ln)\b", re.IGNORECASE),
}


def _find_phi_in_text(text: str, patterns: Dict[str, re.Pattern]) -> List[Tuple[str, str]]:
    found: List[Tuple[str, str]] = []
    for name, pattern in patterns.items():
        for m in pattern.finditer(text):
            found.append((name, m.group(0)))
    return found


def _redact_text(text: str, patterns: Dict[str, re.Pattern]) -> Tuple[str, List[Tuple[str, str]]]:
    phi = _find_phi_in_text(text, patterns)
    redacted = text
    # Replace longer matches first to avoid overlapping issues
    for _, match in sorted(phi, key=lambda x: -len(x[1])):
        # simple global replace for the match
        redacted = redacted.replace(match, "[REDACTED]")
    return redacted, phi


def _sanitize_json_like(obj: Any, patterns: Dict[str, re.Pattern]) -> Tuple[Any, List[Tuple[str, str]]]:
    phi_found: List[Tuple[str, str]] = []

    if isinstance(obj, str):
        redacted, phi = _redact_text(obj, patterns)
        phi_found.extend(phi)
        return redacted, phi_found

    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            sanitized_v, phi = _sanitize_json_like(v, patterns)
            new[k] = sanitized_v
            phi_found.extend(phi)
        return new, phi_found

    if isinstance(obj, list):
        new_list = []
        for v in obj:
            sanitized_v, phi = _sanitize_json_like(v, patterns)
            new_list.append(sanitized_v)
            phi_found.extend(phi)
        return new_list, phi_found

    # numbers, bools, None
    return obj, phi_found


class AIValidator:
    """Validator that checks AI outputs for PHI and basic EHR structure.

    Usage:
        validator = AIValidator()
        result = validator.validate(ai_output)

    `ai_output` may be a string or a JSON-like dict (the return value from
    `ai_service.generate_response()` is supported as well).
    """

    def __init__(self, patterns: Optional[Dict[str, re.Pattern]] = None, api_key: str = "API_KEY_PLACEHOLDER") -> None:
        """Create an AIValidator.

        Args:
            patterns: Optional custom PHI regex patterns.
            api_key: Optional API key for an external validation/de-identification service.
                     If provided it will be stored as `self.api_key`. If not provided,
                     the environment variable `VALIDATOR_API_KEY` will be used when available.
                     To hard-code a key at initialization, pass it here (e.g.:
                     `AIValidator(api_key="sk-xxxx-your-key")`).
        """
        self.patterns = patterns or DEFAULT_PATTERNS
        # store an API key for potential external validator usage
        # The caller should pass a valid API key when constructing the validator.
        # A placeholder default is provided so code can run locally; replace it
        # with your real key when instantiating in production.
        self.api_key = api_key

    def _check_fhir_like(self, obj: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        # lightweight FHIR-style checks
        if not isinstance(obj, dict):
            return ["FHIR check: resource is not a JSON object"]

        if "resourceType" not in obj:
            errors.append("FHIR check: missing 'resourceType' key")
        # ensure an id exists for identifiable resources
        if "resourceType" in obj and "id" not in obj:
            errors.append("FHIR check: missing 'id' key for resource")
        return errors

    async def validate(self, ai_output: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Validate `ai_output` and return a report.

        Returns a dict with fields:
        - compliant: bool (True if no PHI found and no critical EHR errors)
        - errors: list[str] (critical problems)
        - warnings: list[str] (non-critical issues)
        - phi_found: list[(type, match)]
        - sanitized_output: same type as ai_output with PHI redacted
        """
        errors: List[str] = []
        warnings: List[str] = []
        phi_found: List[Tuple[str, str]] = []

        # If ai_output is a dict that contains a 'response' key (ai_service format),
        # validate both the wrapper and the inner response.
        original_type = type(ai_output)

        # Try to parse string that contains JSON
        parsed_json = None
        if isinstance(ai_output, str):
            text = ai_output
            # check if string is JSON
            try:
                parsed_json = json.loads(ai_output)
            except Exception:
                parsed_json = None

            # find and redact PHI in the raw text
            sanitized_text, phi = _redact_text(text, self.patterns)
            phi_found.extend(phi)
            sanitized_output = sanitized_text

        elif isinstance(ai_output, dict):
            # if there is a 'response' field and it's a string, check it too
            sanitized_copy = {}
            for k, v in ai_output.items():
                if isinstance(v, str):
                    s, phi = _redact_text(v, self.patterns)
                    sanitized_copy[k] = s
                    phi_found.extend(phi)
                else:
                    s, phi = _sanitize_json_like(v, self.patterns)
                    sanitized_copy[k] = s
                    phi_found.extend(phi)

            sanitized_output = sanitized_copy

            # if the dict itself looks like a FHIR resource, run basic checks
            if "resourceType" in ai_output:
                errors.extend(self._check_fhir_like(ai_output))
            # if there is nested JSON inside 'response', try validating it
            if "response" in ai_output and isinstance(ai_output["response"], (str, dict, list)):
                # if string and JSON-like, attempt to parse and validate
                resp = ai_output["response"]
                if isinstance(resp, str):
                    try:
                        parsed = json.loads(resp)
                        if isinstance(parsed, dict) and "resourceType" in parsed:
                            errors.extend(self._check_fhir_like(parsed))
                    except Exception:
                        # not JSON — no FHIR checks
                        pass

        elif isinstance(ai_output, list):
            sanitized_output, phi = _sanitize_json_like(ai_output, self.patterns)
            phi_found.extend(phi)
        else:
            sanitized_output = ai_output

        # By default, external validation wasn't run
        external_run = False
        external_success = False
        external_used_on = None  # what part we sent to external validator

        # After local sanitization, optionally call external validator
        async def try_external_on_text(text: str) -> Optional[str]:
            nonlocal external_run, external_success, external_used_on
            external_run = True
            external_used_on = "response_text"
            try:
                external_result = await self.external_validate(text)
                if external_result is not None:
                    external_success = True
                    return external_result
                return None
            except Exception:
                external_success = False
                return None

        # Build report
        report: Dict[str, Any] = {}
        report["errors"] = errors
        report["warnings"] = warnings
        report["phi_found"] = phi_found

        # If there is an API key, run external validation/de-id and merge results
        final_sanitization = "local"

        try:
            if self.api_key:
                # For strings
                if isinstance(sanitized_output, str):
                    ext = await try_external_on_text(sanitized_output)
                    if ext is not None:
                        sanitized_output = ext
                        final_sanitization = "external"

                # For dicts, prefer to send 'response' field if present
                elif isinstance(sanitized_output, dict):
                    if "response" in sanitized_output and isinstance(sanitized_output["response"], str):
                        ext = await try_external_on_text(sanitized_output["response"])
                        if ext is not None:
                            sanitized_output["response"] = ext
                            final_sanitization = "external"
                    else:
                        # send the JSON string of the whole payload
                        try:
                            payload_text = json.dumps(sanitized_output)
                        except Exception:
                            payload_text = str(sanitized_output)
                        ext = await try_external_on_text(payload_text)
                        if ext is not None:
                            # try to parse external result as JSON
                            try:
                                parsed_ext = json.loads(ext)
                                sanitized_output = parsed_ext
                                final_sanitization = "external"
                            except Exception:
                                # external returned plain text — store it under 'response'
                                sanitized_output["response"] = ext
                                final_sanitization = "external"

                # For lists, send JSON string
                elif isinstance(sanitized_output, list):
                    try:
                        payload_text = json.dumps(sanitized_output)
                    except Exception:
                        payload_text = str(sanitized_output)
                    ext = await try_external_on_text(payload_text)
                    if ext is not None:
                        try:
                            sanitized_output = json.loads(ext)
                            final_sanitization = "external"
                        except Exception:
                            # keep local sanitized list and attach external under a metadata key
                            final_sanitization = "both"
                else:
                    # other types: no external run
                    pass
        except Exception:
            # never crash the validator if external validation fails
            external_success = False

        report["sanitized_output"] = sanitized_output

        # Compliance: no PHI found and no critical errors
        compliant = len(phi_found) == 0 and len(errors) == 0
        report["compliant"] = compliant
        # External validation metadata
        report["external"] = {
            "run": external_run,
            "success": external_success,
            "used_on": external_used_on,
            "final_sanitization": final_sanitization,
        }

        return report

    async def external_validate(self, text: str) -> Optional[str]:
        """Sends the text to an external de-identification or HIPAA validation API.

        Returns the sanitized string on success, or None if the external API
        is unavailable or fails.

        NOTE: This implementation uses a placeholder endpoint and demonstrates
        how to wire the API key. Replace `VALIDATOR_ENDPOINT` with your
        real service URL. The method is synchronous to keep the validator
        interface simple; if you need async behaviour, we can add async
        variants later.
        """
        if not self.api_key:
            return None

        VALIDATOR_ENDPOINT = "https://validator.example.com/deid"  # placeholder
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"text": text}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(VALIDATOR_ENDPOINT, json=payload, headers=headers)
                resp.raise_for_status()
                # Expect the external API to return JSON: {"sanitized": "..."}
                data = resp.json()
                if isinstance(data, dict) and "sanitized" in data:
                    return data["sanitized"]
                # if API returns plain text
                if isinstance(data, str):
                    return data
        except Exception:
            return None



