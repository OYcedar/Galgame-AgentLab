# Bruns / EENC / EENZ Patch Workflow

Agents:

1. engine-detector
2. text-extractor
3. translator
4. reinsertor
5. font-fixer
6. packager
7. runtime-tester
8. release-builder

Core rules:

- detect `EENC` / `EENZ` wrappers before editing;
- decrypt `ams.cfg` and `scene/*.bso` into the game work directory;
- export external text as SExtractor JSON and keep reinsertion metadata separate;
- reinsert Chinese as GB18030 unless runtime evidence requires another encoding;
- flatten Bruns ruby markers such as `&RA...&RS...&RT` unless Chinese ruby rendering is proven safe;
- keep `voice` config and playback calls intact;
- if `[WARN] VOICE制御は未対応です(%d)` blocks startup, suppress the modal warning with a minimal exe log-level patch, not by disabling voice;
- avoid shipping external font launchers unless formal dialogue screenshots prove they work;
- release only patched exe/config/scripts plus README.

Validation gates:

- translated JSON parses and count/order match the source;
- changed `*.bso` files re-decrypt and contain expected Chinese;
- `ams.cfg` re-decrypts and has valid config syntax;
- first launch reaches the title menu without modal debug warnings;
- start enters formal dialogue;
- voice playback is not intentionally disabled;
- release folder contains no `_work`, save data, screenshots, decrypted scripts, or unmodified large media archives.
