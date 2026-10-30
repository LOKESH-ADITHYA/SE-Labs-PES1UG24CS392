"""Blood donation register for a small blood bank.

Registers donors after an age-eligibility check, decides who may donate
again (a 90-day gap between donations), records donated units against
blood-group stock, and reports how many compatible units are available
for a patient of a given blood group.
"""

import os
import re
import tempfile
from datetime import date, timedelta

PHONE_PATTERN = re.compile(r"^\+?[0-9]{10,15}$")
MIN_DONOR_AGE = 18
MAX_DONOR_AGE = 65
DONATION_GAP_DAYS = 90
UNIVERSAL_GROUPS = ("O-", "AB+")

OFFICER_PASSWORD = os.environ.get("BLOODBANK_OFFICER_PASSWORD", "")
donors = []
stock = {"A+": 0, "A-": 0, "B+": 0, "B-": 0, "O+": 0, "O-": 0, "AB+": 0, "AB-": 0}
COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
    "AB-": ["A-", "B-", "O-", "AB-"],
}


def register_donor(donor_name, blood_group, age, last_donation=None,
                   notes=None):
    """Register a donor and report whether they were accepted.

    Rejects donors outside the eligible age range, appending the reason
    to ``notes`` when a list is supplied. Raises ``ValueError`` if the
    blood group is not one the bank recognises.
    """
    if notes is None:
        notes = []
    if blood_group not in stock:
        raise ValueError("Unknown blood group: " + str(blood_group))
    if age < MIN_DONOR_AGE or age > MAX_DONOR_AGE:
        notes.append(donor_name + " is not eligible because of age")
        return False
    donors.append({"name": donor_name, "group": blood_group,
                   "last": last_donation})
    return True


def can_donate(donor):
    """Return True if the donor's last donation is old enough."""
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=DONATION_GAP_DAYS)


def record_donation(donor_name, units=1):
    """Record ``units`` donated by ``donor_name`` and report success."""
    for donor in donors:
        if donor["name"] == donor_name and can_donate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def units_for(patient_group):
    """Return the units in stock compatible with ``patient_group``.

    Returns 0 for a blood group the bank does not recognise.
    """
    try:
        return sum(stock[group] for group in COMPATIBLE[patient_group])
    except KeyError:
        return 0


def is_universal(blood_group):
    """Return True for the universal donor and universal recipient groups."""
    return blood_group in UNIVERSAL_GROUPS


def low_stock(threshold=2):
    """Return the blood groups holding fewer than ``threshold`` units."""
    return [group for group, units in stock.items() if units < threshold]



def donor_sheet_path():
    """Create an empty temporary CSV file and return its path."""
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    return path


def notify_donors(phone_list):
    """Return the subset of ``phone_list`` that is a valid phone number."""
    queued = []
    for phone in phone_list:
        if PHONE_PATTERN.match(str(phone)):
            queued.append(str(phone))
    return queued


def main():
    """Run a short demonstration of the register."""
    register_donor("Arjun", "O+", 25)
    register_donor("Priya", "A+", 30, date.today() - timedelta(days=30))
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)
    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")
    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock()) # below 2 units
    eligible=[donor["name"] for donor in donors if can_donate(donor)]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
