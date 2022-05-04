#!/usr/bin/env python3
"""Program to print a variable number of jar side labels, scaled by use frequency."""

import csv
import functools
import itertools
import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

JAR_QUANTITIES = "jar_median_quantities.csv"
LABELS_FOLDER = "/Users/jeangleason/Desktop/jar_labels/"
MOST_TO_PRINT = (
    18  # Don't print more than 18 because we often have label waste
)


@dataclass
class SmallJar:
    """Keep track of jar info."""

    sku: str
    english_name: str
    target_quantity: int

    def path(self) -> str:
        """Location of file. Not guaranteed to exist."""
        return LABELS_FOLDER + self.sku + ".spub"

    def print(self) -> None:
        num = min(self.target_quantity, MOST_TO_PRINT)
        logging.info(f"I am printing {num} of {self.english_name}")
        with open("printsmall.applescript", "r") as f:
            program = f.read().format(file_path=self.path(), number_print=num)
        subprocess.call(["osascript", "-e", program])

    def __hash__(self) -> int:
        return hash(self.sku)


def load_jars() -> list[SmallJar]:
    """Load jar info from the CSV."""
    jars = []
    with open(JAR_QUANTITIES, "r", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            jars.append(SmallJar(row["sku"], row["description"], int(row["target"])))

    return jars


def run_checks_and_load() -> list[SmallJar]:
    jars = load_jars()

    if len(jars) < 10:
        raise Exception(
            "I was unable to load the jar information from the info file. Check that it is formatted correctly."
        )

    if not Path(LABELS_FOLDER).exists():
        raise Exception(
            f"I was unable to locate the labels folder at {LABELS_FOLDER}. Are you running this on the right computer?"
        )

    # Check all paths exist
    extant_jars = [jar for jar in jars if Path(jar.path()).exists()]
    missing_paths = set(jars) - set(extant_jars)
    for jar in missing_paths:
        logging.warning(
            f"I was unable to locate the file for {jar.sku} ({jar.english_name}) where I expected it: {jar.path()}"
            + f"\n\tConsider fixing this in {Path(JAR_QUANTITIES)}",
        )

    if len(extant_jars) / len(jars) < 0.5:
        raise Exception("Too many jars not found.")

    # Check for other paths that are present
    all_printing_paths = list(jar.path() for jar in extant_jars)
    extra_files = [
        str(x)
        for x in Path(LABELS_FOLDER).glob("*1.spub")
        if str(x) not in all_printing_paths
    ]
    for label in extra_files:
        logging.warning(
            f"Found unexpected file (will not print): {label}"
            + f"\n\tConsider removing the file or adding a line to {Path(JAR_QUANTITIES)}",
        )

    should_be_all = itertools.chain.from_iterable(
        fun(extant_jars) for fun in (herbs, spices, salts, blends)
    )
    should_be_none = set(extant_jars) - set(should_be_all)
    if should_be_none:
        logging.warning(
            "Jar skus that were not categorized (starts with none of H, B, S, NA): %s",
            str(", ".join(jar.sku for jar in should_be_none)),
        )

    return extant_jars


def filter_prefix(jars: list[SmallJar], prefix: str) -> list[SmallJar]:
    """Filter jars by SKU prefix."""
    return [jar for jar in jars if jar.sku.startswith(prefix)]


herbs = functools.partial(filter_prefix, prefix="H")
salts = functools.partial(filter_prefix, prefix="NA")
spices = functools.partial(filter_prefix, prefix="S")
blends = functools.partial(filter_prefix, prefix="B")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    jars = run_checks_and_load()
    logging.info(
        "Loaded jars. Please do a test print to align the label offsets and ensure the 6-label cutoff is correct."
    )
    cont = input("Continue? Y/n: ")
    if cont.lower() not in ["y", "", "yes"]:
        sys.exit()
    what = input("What to print? H(erbs), B(lends), S(pices), NA(Salts), A(ll): ")
    match what.lower():
        case "h":
            logging.info("Selected herbs.")
            jars = herbs(jars)
        case "b":
            logging.info("Selected blends.")
            jars = blends(jars)
        case "s":
            logging.info("Selected spices.")
            jars = spices(jars)
        case "na":
            logging.info("Selected salts.")
            jars = salts(jars)
        case "a":
            logging.info("Selected all.")
        case _:
            logging.warning("Unknown selector; printing all")

    for jar in jars:
        jar.print()
