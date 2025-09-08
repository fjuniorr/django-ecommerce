# ADR-0001: Adapter Key and Ingest Envelope

## Context

Different storefronts emit payloads via webhooks, APIs, or flat files. We need a way to map these payloads onto canonical order models while keeping transport concerns separate.

## Decision

* Adapter selection uses a strict key grammar:
  `<provider>.<api_version>.<kind>[.<channel>][.<program>][@<ingest>][#<schema_version>][:<format>][+<flags>...]`.
* Resolution searches from most specific to least: `+flags → :format → #schema → @ingest → .program → .channel → provider.api_version.kind → provider.api_version.* → provider.* → *`.
* Transport and trigger metadata live in an **ingestion envelope** instead of the adapter key. This keeps adapter code focused on semantics, while envelopes capture how/why a payload arrived.

## Consequences

* Adding a new storefront adapter only requires implementing a class and registering keys.
* Raw payloads and envelopes can be stored for auditing and replay.
* Transport or scheduling changes do not require adapter changes.
