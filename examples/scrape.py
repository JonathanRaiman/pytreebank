"""
For personal use only. Do not abuse.
"""
import json
import argparse
import pytreebank.box_office

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    reviews = pytreebank.box_office.get_box_office_reviews()
    with open(args.path, "wt") as fout:
        json.dump([{"score": s, "text": text} for s, text in reviews], fout)
