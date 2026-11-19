"""Backward-compatible entry point for SHA-pinned checkpoint verification.

Use ``python -m research.checkpoint CHECKPOINT --sha256 ... --profile ...``.
The implementation is shared with :mod:`research.verify_model` so this entry
point cannot silently use a different model-loading or probe contract.
"""
from .verify_model import main


if __name__ == "__main__":
    main()
