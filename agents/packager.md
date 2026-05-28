# Packager Agent

Goal: rebuild patch archives safely.

Responsibilities:

- use the correct current-version archive base;
- preserve archive scheme/encryption/compression settings when legally permitted;
- rebuild only the needed files;
- re-extract the output archive and verify modified scripts are present;
- never include unrelated original assets in a release package.
