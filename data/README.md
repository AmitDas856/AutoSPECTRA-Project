# Data Directory

Large datasets must not be committed.

Place local files under:

```text
data/raw/
```

Generated datasets and caches belong under:

```text
data/processed/
```

Both locations are ignored by Git. Commit only:

- this README;
- example manifests;
- download instructions;
- checksum scripts;
- small synthetic test fixtures when legally and ethically appropriate.
