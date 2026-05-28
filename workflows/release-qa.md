# Release QA

1. Validate JSON and reports.
2. Repack the patch/archive.
3. Re-extract the output and inspect changed scripts.
4. Launch the patched game from the intended directory.
5. Test:
   - first launch;
   - title;
   - start;
   - load;
   - save/load pages;
   - history/log;
   - options/config;
   - fast skip;
   - extra/gallery/music when present.
6. Capture screenshots into `work/runtime_screens`.
7. Build a clean release folder.
8. Build archive outputs only after QA passes.
