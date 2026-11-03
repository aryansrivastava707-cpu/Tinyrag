#!/usr/bin/env python3
"""tinyrag: retrieval from scratch (BM25) over your own notes. Standard library only.

    python tinyrag.py index docs/
    python tinyrag.py ask "why split documents into chunks?" -k 3

This is the *retrieval* half of RAG with every step visible. It returns the best
passages and best sentences; it does not generate text with an LLM.
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter

INDEX_FILE = "index.json"
STOP = set("a an and are as at be by for from how in is it of on or that the this to was what when where which who why with do does you your i we can".split())
K1, B = 1.5, 0.75


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    out = []
    for w in words:
        if w in STOP:
            continue
        for suffix in ("ing", "ed", "es", "s"):  # deliberately crude stemmer
            if len(w) > len(suffix) + 3 and w.endswith(suffix):
                w = w[: -len(suffix)]
                break
        out.append(w)
    return out


def chunk_text(text, max_words=70):
    """Group paragraphs into chunks of roughly max_words words."""
    chunks, current, count = [], [], 0
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        n = len(para.split())
        if current and count + n > max_words:
            chunks.append("\n".join(current))
            current, count = [], 0
        current.append(para)
        count += n
    if current:
        chunks.append("\n".join(current))
    return chunks


def build_index(folder):
    chunks = []
    for root, _, names in os.walk(folder):
        for name in sorted(names):
            if not name.endswith((".md", ".txt")):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                for i, text in enumerate(chunk_text(f.read())):
                    chunks.append({"source": os.path.relpath(path, folder), "n": i, "text": text})
    if not chunks:
        sys.exit(f"No .md/.txt files found in {folder}")
    for c in chunks:
        c["tokens"] = Counter(tokenize(c["text"]))
        c["len"] = sum(c["tokens"].values())
    df = Counter(t for c in chunks for t in c["tokens"])
    avg = sum(c["len"] for c in chunks) / len(chunks)
    return {"chunks": [{**c, "tokens": dict(c["tokens"])} for c in chunks], "df": dict(df), "avg_len": avg}


def bm25(index, query_terms, tokens, length):
    n = len(index["chunks"])
    score, matched = 0.0, []
    for t in query_terms:
        tf = tokens.get(t, 0)
        if not tf:
            continue
        df = index["df"].get(t, 0)
        idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
        score += idf * tf * (K1 + 1) / (tf + K1 * (1 - B + B * length / index["avg_len"]))
        matched.append(t)
    return score, matched


def search(index, question, k=3):
    terms = tokenize(question)
    results = []
    for c in index["chunks"]:
        s, matched = bm25(index, terms, c["tokens"], c["len"])
        if s > 0:
            results.append({"score": s, "matched": matched, "chunk": c})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:k]


def best_sentence(text, question):
    terms = set(tokenize(question))
    sentences = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return max(sentences, key=lambda s: len(terms & set(tokenize(s))) / (1 + 0.02 * len(s.split())))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("index", help="build an index from a folder of .md/.txt files")
    pi.add_argument("folder")
    pa = sub.add_parser("ask", help="ask a question")
    pa.add_argument("question")
    pa.add_argument("-k", type=int, default=3)
    args = p.parse_args()

    if args.cmd == "index":
        idx = build_index(args.folder)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(idx, f)
        print(f"Indexed {len(idx['chunks'])} chunks, {len(idx['df'])} distinct terms -> {INDEX_FILE}")
        return
    if not os.path.exists(INDEX_FILE):
        sys.exit("No index yet. Run: python tinyrag.py index docs/")
    with open(INDEX_FILE, encoding="utf-8") as f:
        idx = json.load(f)
    hits = search(idx, args.question, args.k)
    if not hits:
        print("No passage shares a meaningful word with that question.")
        return
    print(f"Best sentence: {best_sentence(hits[0]['chunk']['text'], args.question)}\n")
    for i, h in enumerate(hits, 1):
        c = h["chunk"]
        print(f"[{i}] {c['source']} (chunk {c['n']})  score {h['score']:.2f}  matched: {', '.join(h['matched'])}")
        print("    " + c["text"].replace("\n", "\n    ") + "\n")


if __name__ == "__main__":
    main()
