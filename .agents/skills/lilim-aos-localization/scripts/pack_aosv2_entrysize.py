#!/usr/bin/env python3
from __future__ import annotations

import argparse
import heapq
import json
import struct
from collections import Counter
from pathlib import Path


INDEX_OFFSET = 0x111
ENTRY_SIZE = 0x28


class BitWriter:
    def __init__(self) -> None:
        self.buf = bytearray()
        self.acc = 0
        self.count = 0

    def bit(self, value: int) -> None:
        self.acc = (self.acc << 1) | (value & 1)
        self.count += 1
        if self.count == 8:
            self.buf.append(self.acc)
            self.acc = 0
            self.count = 0

    def bits(self, value: int, count: int) -> None:
        for shift in range(count - 1, -1, -1):
            self.bit((value >> shift) & 1)

    def finish(self) -> bytes:
        if self.count:
            self.buf.append(self.acc << (8 - self.count))
            self.acc = 0
            self.count = 0
        return bytes(self.buf)


def make_tree(data: bytes):
    freq = Counter(data)
    heap = []
    seq = 0
    for sym, count in sorted(freq.items()):
        heap.append((count, seq, sym))
        seq += 1
    heapq.heapify(heap)
    if not heap:
        return 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, (a[0] + b[0], seq, (a[2], b[2])))
        seq += 1
    return heap[0][2]


def write_tree(writer: BitWriter, node, codes: dict[int, list[int]], prefix: list[int]) -> None:
    if isinstance(node, int):
        writer.bit(0)
        writer.bits(node, 8)
        codes[node] = prefix[:] or [0]
        return
    writer.bit(1)
    left, right = node
    write_tree(writer, left, codes, prefix + [0])
    write_tree(writer, right, codes, prefix + [1])


def huffman_pack(data: bytes) -> bytes:
    writer = BitWriter()
    if not data:
        return b""
    tree = make_tree(data)
    codes: dict[int, list[int]] = {}
    write_tree(writer, tree, codes, [])
    if isinstance(tree, int):
        return writer.finish()
    for byte in data:
        for bit in codes[byte]:
            writer.bit(bit)
    return writer.finish()


def read_template_order(template: Path) -> list[str]:
    data = template.read_bytes()
    if struct.unpack_from("<I", data, 0)[0] != 0:
        raise ValueError(f"not an AOSv2 archive: {template}")
    index_size = struct.unpack_from("<I", data, 8)[0]
    count = index_size // ENTRY_SIZE
    names: list[str] = []
    for i in range(count):
        index_pos = INDEX_OFFSET + i * ENTRY_SIZE
        raw_name = data[index_pos:index_pos + 0x20].split(b"\0", 1)[0]
        names.append(raw_name.decode("cp932"))
    return names


def validate_aos(data: bytes) -> dict[str, int]:
    base_offset = struct.unpack_from("<I", data, 4)[0]
    index_size = struct.unpack_from("<I", data, 8)[0]
    count = index_size // ENTRY_SIZE
    bad_entries = 0
    previous_end = base_offset
    for i in range(count):
        index_pos = INDEX_OFFSET + i * ENTRY_SIZE
        rel = struct.unpack_from("<I", data, index_pos + 0x20)[0]
        size = struct.unpack_from("<I", data, index_pos + 0x24)[0]
        absolute = base_offset + rel
        if absolute != previous_end:
            bad_entries += 1
        previous_end = absolute + size
    if previous_end != len(data):
        bad_entries += 1
    return {"count": count, "bad_entries": bad_entries, "last_end": previous_end}


def pack_aos(scr_dir: Path, output: Path, template: Path) -> dict[str, int | str]:
    order = read_template_order(template)
    files = [scr_dir / name for name in order]
    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise ValueError(f"template references missing files: {missing[:5]}")

    index_size = len(files) * ENTRY_SIZE
    base_offset = INDEX_OFFSET + index_size
    header = bytearray(base_offset)
    struct.pack_into("<III", header, 0, 0, base_offset, index_size)

    payload = bytearray()
    total_unpacked = 0
    total_entry_bytes = 0

    for i, path in enumerate(files):
        name = path.name.encode("cp932")
        if len(name) > 0x1F:
            raise ValueError(f"file name too long for AOS index: {path.name}")
        data = path.read_bytes()
        packed_body = huffman_pack(data)
        entry_data = struct.pack("<I", len(data)) + packed_body

        index_pos = INDEX_OFFSET + i * ENTRY_SIZE
        header[index_pos:index_pos + len(name)] = name
        struct.pack_into("<II", header, index_pos + 0x20, len(payload), len(entry_data))

        payload.extend(entry_data)
        total_unpacked += len(data)
        total_entry_bytes += len(entry_data)

    output.parent.mkdir(parents=True, exist_ok=True)
    archive = bytes(header + payload)
    validation = validate_aos(archive)
    if validation["bad_entries"]:
        raise ValueError(f"AOS validation failed: {validation}")
    output.write_bytes(archive)

    return {
        "output": str(output),
        "files": len(files),
        "index_size": index_size,
        "base_offset": base_offset,
        "unpacked_bytes": total_unpacked,
        "entry_bytes": total_entry_bytes,
        "archive_size": len(archive),
        **validation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pack LiLiM AOSv2 archives with full entry sizes.")
    parser.add_argument("--scr-dir", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = pack_aos(args.scr_dir, args.output, args.template)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
