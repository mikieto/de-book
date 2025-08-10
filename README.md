# DE Book (draft)
- 入力: build/context_packs/ 以下の context_pack.json
- ガイド: charter/, legislation/ (style, workflow, personas), knowledge/


## How to update context pack
1. In context-ops: `python3 tools/ci/build_context_pack.py --unit ch01`
2. Copy: `cp ../context-ops/packs/ch01/<DATE>/context_pack.json build/context_packs/ch01/`
3. Commit & push. CI (debook-validate) will verify.
