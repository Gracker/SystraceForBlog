# Trace data policy

This repository contains historical Perfetto, Systrace HTML, and ART method
trace attachments used by Android Performance articles. Trace data can contain
package names, process/thread names, file paths, build fingerprints, account
identifiers, or other device/user context.

## Existing artifacts

`catalog.json` records the known state of every artifact. `license: null`,
`consent: null`, or a `pending` review means that the historical record is
unknown; it does not grant additional permission to copy, redistribute, or use
third-party data. Repository visibility is not a blanket data license.

The existing binary artifacts are intentionally unchanged by the cataloging
work. Their hashes make later review auditable. If provenance or authorization
cannot be established, update the catalog before changing publication status.

## New artifacts

A new contribution must document:

- who captured or supplied it and when;
- the capture owner or permission basis;
- the data license or explicit redistribution terms;
- privacy and sanitization review results;
- all related article URLs;
- content format, packaging, byte sizes, archive members, and SHA-256.

Do not contribute credentials, tokens, account identifiers, personal messages,
private file paths, proprietary app data, or traces you are not authorized to
publish. Prefer a minimal Perfetto protobuf capture over legacy self-contained
HTML, and capture a purpose-built demo when possible.

## Code and documentation

`LICENSE-CODE` applies only to the repository's original documentation,
catalog schema, validation code, tests, and workflow. It does not relicense any
trace/archive artifact or linked article.
