#!/usr/bin/env python3
"""Validate a research_data_spec.json.

  python validate_spec.py spec.json [--schema ../references/research_data_spec.schema.json]

Two layers:
  ERRORS   - the file does not follow the schema (missing field, bad enum value, wrong type),
             or references a variable/construct id that does not exist.
  WARNINGS - the content is formally valid but internally inconsistent with the logic of
             pre-specification (e.g. a 'pre_locked' decision recorded after E4 exposure,
             a confirmatory primary analysis marked 'data_driven').
Warnings are prompts to look again; they are not verdicts.
Exit code: 0 = no errors (warnings allowed), 1 = errors.
Uses only the standard library (a small built-in checker covers the schema features used here).
"""
import argparse, json, os, re, sys


def check(value, schema, root, path, errs):
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        schema = root["definitions"][ref]
    t = schema.get("type")
    pytypes = {"object": dict, "array": list, "string": str, "boolean": bool, "number": (int, float), "integer": int}
    if t and not isinstance(value, pytypes[t]):
        errs.append(f"{path}: expected {t}, got {type(value).__name__}")
        return
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: '{value}' not in {schema['enum']}")
    if t == "string" and "pattern" in schema and not re.search(schema["pattern"], value):
        errs.append(f"{path}: '{value}' does not match {schema['pattern']}")
    if t == "object":
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path}: missing required field '{k}'")
        for k, sub in schema.get("properties", {}).items():
            if k in value:
                check(value[k], sub, root, f"{path}.{k}", errs)
    if t == "array":
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path}: needs at least {schema['minItems']} item(s)")
        if "items" in schema:
            for i, v in enumerate(value):
                check(v, schema["items"], root, f"{path}[{i}]", errs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--schema", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      "..", "references", "research_data_spec.schema.json"))
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    schema = json.load(open(a.schema, encoding="utf-8"))

    errs, warns = [], []
    check(spec, schema, schema, "$", errs)

    if not errs:
        var_ids = {v["id"] for v in spec["variables"]}
        if len(var_ids) != len(spec["variables"]):
            errs.append("variables: duplicate ids")
        for c in spec.get("constructs", []):
            for ind in c["indicators"]:
                if ind not in var_ids:
                    errs.append(f"construct '{c['id']}': indicator '{ind}' is not a variable id")
        roles = {v["role"] for v in spec["variables"]}
        if "outcome" not in roles and spec["study"]["data_path"] in ("primary_quant", "secondary_structured") \
                and spec["study"]["design_purpose"] in ("confirmatory", "prediction"):
            warns.append("confirmatory/prediction study without any variable of role 'outcome'")

        level = spec["data_exposure"]["level"]
        purpose = spec["study"]["design_purpose"]
        exposed_hi = level in ("E3", "E4")
        if level == "E4":
            locked = [v["id"] for v in spec["variables"] if v["decision_status"] == "pre_locked"]
            if locked:
                warns.append(f"exposure is E4 but these variables are marked 'pre_locked': {locked}. Confirm each was fixed "
                             f"before any hypothesis-related analysis, or downgrade to 'locked_after_exposure'/'data_driven'")
        for p in spec["analysis_plan"]:
            if purpose == "confirmatory" and p["primary"] and p["decision_status"] == "data_driven":
                warns.append(f"analysis '{p['id']}': a PRIMARY analysis of a confirmatory study is 'data_driven' "
                             f"- label it exploratory or re-plan")
            if purpose == "confirmatory" and p["primary"] and p["decision_status"] == "open":
                warns.append(f"analysis '{p['id']}': primary analysis still 'open' - freeze before data collection/analysis")
        for e in spec["sample_rules"]["exclusion"]:
            if not e["decided_before_outcome"]:
                warns.append(f"exclusion rule '{e['rule']}' was decided after seeing outcome data: report it as data-driven "
                             f"and show results with and without it")
        strategy = spec.get("holdout_or_blinding", {}).get("strategy")
        if exposed_hi and strategy == "blinded_summary":
            warns.append("strategy is 'blinded_summary' but exposure is E3/E4: blinding may already be compromised")
        if spec["study"]["data_path"] in ("secondary_structured", "secondary_digital_trace") and level == "E0":
            warns.append("secondary data with exposure E0: confirm the researcher has truly not seen the data or its summaries")
        if spec["readiness"]["status"] == "ready":
            open_items = [v["id"] for v in spec["variables"] if v["decision_status"] == "open"]
            if open_items:
                warns.append(f"readiness is 'ready' but variables are still 'open': {open_items}")
            unver = [v["id"] for v in spec["variables"] if v["evidence_status"] == "needs_verification"]
            if unver:
                warns.append(f"readiness is 'ready' but these variables are 'needs_verification': {unver}")
        if spec["governance"]["personal_data"] in ("identifiable", "unknown") and \
                spec["governance"]["ethics_approval_status"] in ("unknown", "pending"):
            warns.append("personal data may be involved but ethics approval is unknown/pending")
        if not spec["governance"]["items_needing_human_verification"]:
            warns.append("governance.items_needing_human_verification is empty: legal/ethics/data-use points "
                         "should at least be listed for human confirmation")

    for e in errs:
        print("ERROR  ", e)
    for w in warns:
        print("WARNING", w)
    if not errs and not warns:
        print("OK: no errors, no warnings")
    elif not errs:
        print(f"Valid ({len(warns)} warning(s)).")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
