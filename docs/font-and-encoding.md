# Font And Encoding Notes

## Encoding

- Japanese VN scripts often use CP932 / Shift-JIS.
- Chinese old-engine patches often need GBK or GB18030.
- UTF-8 is the default for project docs, JSON, reports, and config files.

Always test target encoding before repacking.

## Font Strategy

Font file name and font family name are different.

Example:

- file: `WenQuanYi-Regular.ttf`
- family: `WenQuanYi Micro Hei`

Some engines require:

- external font registration before launch;
- static real family names in scripts;
- menu/history/dialog patches in separate TJS/KAG files.

Always test:

- formal dialogue;
- log/history;
- save/load;
- option dialogs;
- title and menu text.
