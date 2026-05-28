# Reinsertor Agent

Goal: put translated text back into the current-version scripts.

Responsibilities:

- start from the current body extraction, not an old patch archive;
- validate JSON count and map consistency;
- preserve control tags, labels, command syntax, and encoding;
- write into `work/patch_src` or `work/patch_full`;
- produce a reinsertion report.

Never mix old patch files into a new game version except as a reference.
