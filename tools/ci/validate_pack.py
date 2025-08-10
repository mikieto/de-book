#!/usr/bin/env python3
import json, sys, hashlib, os

DEFAULT_PATH = "build/context_packs/ch01/context_pack.json"
path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

if not os.path.exists(path):
    print(f"ERROR: pack not found: {path}", file=sys.stderr)
    sys.exit(1)

data = open(path, "rb").read()
try:
    obj = json.loads(data.decode("utf-8"))
except Exception as e:
    print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)

sha = hashlib.sha256(data).hexdigest()
size = len(data)

print(f"OK: {path} ({size} bytes)")
print(f"sha256:{sha}")

# 最低限のフィールドがあればログに出す（無くても失敗させない）
for key in ("context_id","created_at","unit","items","version"):
    if key in obj:
        print(f"- {key}: {obj.get(key)}")

sys.exit(0)
