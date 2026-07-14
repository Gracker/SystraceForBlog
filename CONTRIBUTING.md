# Contributing trace cases

Read [DATA_POLICY.md](DATA_POLICY.md) before adding data.

1. Use a stable kebab-case case ID and describe one reproducible scenario.
2. Add explicit provenance, capture time, license, consent, privacy review,
   sanitization review, publication status, and article URLs to both the case
   and every artifact.
3. Record `content_format` separately from `packaging`. A zipped Perfetto trace
   remains `perfetto-protobuf` content with `zip` packaging.
4. For ZIP files, record compressed size, total uncompressed size, and member
   count. Do not include absolute paths, `..`, encrypted members, or archive
   bombs.
5. Run:

   ```bash
   python3 scripts/validate_catalog.py
   python3 -m unittest discover -s tests -v
   git diff --check
   ```

Unknown legacy metadata must stay `null` or `pending`; never invent a device,
capture date, permission, or review result to make validation green.
