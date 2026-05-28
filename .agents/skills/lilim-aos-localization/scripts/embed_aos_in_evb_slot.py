#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
from datetime import datetime
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch_exe(
    exe: Path,
    new_aos: bytes,
    backup_dir: Path,
    slot_offset: int | None,
    slot_size: int | None,
    old_aos: bytes | None,
    stamp: str,
) -> dict[str, object]:
    data = bytearray(exe.read_bytes())

    if old_aos is not None:
        found = bytes(data).find(old_aos)
        if found < 0:
            raise ValueError(f"old AOS bytes not found in {exe}")
        offset = found
        size = len(old_aos)
    else:
        if slot_offset is None or slot_size is None:
            raise ValueError("slot_offset and slot_size are required when old_aos is not provided")
        offset = slot_offset
        size = slot_size

    if len(new_aos) > size:
        raise ValueError(f"new AOS is larger than slot for {exe}: {len(new_aos)} > {size}")

    if data[offset:offset + 4] != b"\0\0\0\0":
        raise ValueError(f"slot at {offset} in {exe} does not look like AOSv2")

    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{exe.name}.before_aos_embed_{stamp}.{exe.parent.name}.bak"
    shutil.copy2(exe, backup)

    data[offset:offset + len(new_aos)] = new_aos
    data[offset + len(new_aos):offset + size] = b"\0" * (size - len(new_aos))
    exe.write_bytes(data)

    written = exe.read_bytes()
    return {
        "exe": str(exe),
        "backup": str(backup),
        "slot_offset": offset,
        "slot_size": size,
        "new_aos_size": len(new_aos),
        "exe_sha256": sha256(written),
        "new_aos_full_offset": written.find(new_aos),
        "old_aos_full_offset": -1 if old_aos is None else written.find(old_aos),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Embed a rebuilt LiLiM AOS archive into an existing EVB-packed executable slot.")
    parser.add_argument("--new-aos", required=True, type=Path)
    parser.add_argument("--old-aos", type=Path, help="Old embedded AOS used to locate the slot by exact byte match.")
    parser.add_argument("--slot-offset", type=lambda x: int(x, 0))
    parser.add_argument("--slot-size", type=lambda x: int(x, 0))
    parser.add_argument("--exe", action="append", required=True, type=Path)
    parser.add_argument("--backup-dir", required=True, type=Path)
    args = parser.parse_args()

    new_aos = args.new_aos.read_bytes()
    old_aos = args.old_aos.read_bytes() if args.old_aos else None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []
    for exe in args.exe:
        results.append(
            patch_exe(
                exe=exe,
                new_aos=new_aos,
                backup_dir=args.backup_dir,
                slot_offset=args.slot_offset,
                slot_size=args.slot_size,
                old_aos=old_aos,
                stamp=stamp,
            )
        )

    print("new_aos_sha256=" + sha256(new_aos))
    for item in results:
        print(
            "patched={exe} backup={backup} offset={slot_offset} size={slot_size} "
            "new_full={new_aos_full_offset} old_full={old_aos_full_offset} sha256={exe_sha256}".format(**item)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
