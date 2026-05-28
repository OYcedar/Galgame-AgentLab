# Text Format

External translation files use SExtractor JSON.

```json
[
  {
    "message": "Text0"
  },
  {
    "name": "Name1",
    "message": "Text1。"
  }
]
```

Rules:

- UTF-8 JSON.
- Top-level value is an array.
- Every item has `message`.
- `name` is optional and only used when a speaker exists.
- Order must match source script order.
- Reinsertion metadata goes in a separate map file.

Do not expose internal fields such as file path, line number, offset, archive name, or command context to external translators unless explicitly needed.
