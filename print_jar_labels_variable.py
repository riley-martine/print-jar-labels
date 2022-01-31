#!/usr/bin/env python3
"""Program to print a variable number of jar side labels, scaled by use frequency."""

import csv
from dataclasses import dataclass
from pathlib import Path
from enum import IntEnum
import logging

JAR_QUANTITIES = "jar_target_quantities.csv"
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
        logging.info(f"I am printing {num} of {self.path()}")


def load_jars() -> list[SmallJar]:
    """Load jar info from the CSV."""
    jars = []
    with open(JAR_QUANTITIES, "r", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            jars.append(SmallJar(row["sku"], row["description"], row["target"]))

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
    missing_paths = [jar for jar in jars if not jar in extant_jars]
    for jar in missing_paths:
        logging.warning(
            f"I was unable to locate the file for {jar.sku} ({jar.english_name}) where I expected it: {jar.path()}"
        )

    if len(extant_jars)/len(jars) < 0.5:
        raise Exception("Too many jars not found.")

    # Check for other paths that are present
    all_printing_paths = (jar.path() for jar in extant_jars)
    extra_files = [
        x for x in Path(LABELS_FOLDER).glob("*1.spub") if x not in all_printing_paths
    ]
    for label in extra_files:
        logging.warning(f"Found unexpected file: {label}")

    return extant_jars


if __name__ == "__main__":
    jars = run_checks_and_load()
    for jar in jars:
        jar.print()
