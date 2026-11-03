# Architecture

The command-line entry point parses arguments and calls the core functions in the
project module. The typing demo also separates its HTTP interface from timing
features. Plain Python data structures keep core behavior usable from tests and scripts.

## Main workflow

python tinyrag.py index docs/
python tinyrag.py ask "how does retrieval rank passages?" -k 3

## Design choices

- Standard library only, so the algorithm and input handling remain inspectable.
- Deterministic seeds or local files are used where the workflow supports them.
- Output is intended for learning and review, not production security decisions.
