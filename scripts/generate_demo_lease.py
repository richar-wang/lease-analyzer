"""Generate a sample lease PDF with deliberately illegal/problematic clauses for testing."""

import fitz  # PyMuPDF
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "backend" / "sample" / "demo_lease.pdf"

LEASE_TEXT = """
RESIDENTIAL LEASE AGREEMENT

This Residential Lease Agreement ("Agreement") is entered into on January 15, 2025,
by and between:

LANDLORD: John Smith Properties Inc. ("Landlord")
TENANT: Jane Doe ("Tenant")

PROPERTY: Unit 4B, 123 Maple Street, Toronto, Ontario M5V 2T6

TERM: February 1, 2025 to January 31, 2026 (12 months)

MONTHLY RENT: $2,200.00 (Two Thousand Two Hundred Dollars)

1. RENT PAYMENT
The Tenant shall pay rent on the first day of each month. Rent is due in advance.

2. DEPOSITS AND MOVE-IN COSTS
Upon signing this Agreement, the Tenant shall pay:
(a) First month's rent: $2,200.00
(b) Last month's rent deposit: $2,200.00
(c) Security/damage deposit: $500.00
(d) Key deposit: $150.00 (non-refundable)
Total move-in cost: $5,050.00

3. POST-DATED CHEQUES
The Tenant must provide twelve (12) post-dated cheques for the full term of the
lease at the time of signing. No alternative payment methods will be accepted.

4. PET POLICY
No pets of any kind are permitted in the rental unit or anywhere on the premises.
This includes but is not limited to dogs, cats, birds, fish, and reptiles.
Violation of this policy is grounds for immediate eviction.

5. GUESTS AND VISITORS
(a) Overnight guests are limited to a maximum of two (2) nights per calendar month.
(b) All guests must be registered with the building management office upon arrival.
(c) The Tenant shall not permit any person not named on this lease to reside in
    the unit for more than 48 consecutive hours.
(d) A fee of $25.00 per night will be charged for any guest staying beyond the
    permitted two nights.

6. LANDLORD ACCESS AND INSPECTIONS
The Landlord or the Landlord's authorized agent may enter the rental unit at any
time with twelve (12) hours' notice for the purpose of inspections, maintenance,
showing the unit to prospective tenants or buyers, or for any other reason deemed
necessary by the Landlord. The Tenant agrees to provide a key to the Landlord.

7. MAINTENANCE AND REPAIRS
(a) The Tenant is responsible for all minor repairs under $200.00, including but
    not limited to plumbing issues, electrical problems, appliance maintenance,
    and replacement of light fixtures.
(b) The Tenant shall not alter, paint, or make any modifications to the unit
    without prior written consent from the Landlord.

8. MOVE-OUT CONDITIONS
Upon vacating the rental unit, the Tenant agrees to:
(a) Professionally clean all carpets at the Tenant's expense.
(b) Repaint all walls to the original color (Benjamin Moore "Simply White" OC-117).
(c) Fill all nail holes and repair any wall damage.
(d) Have the unit professionally cleaned.
(e) Replace any stained or worn carpet sections.
Failure to comply will result in deductions from the security deposit.

9. RENT INCREASES
The Landlord reserves the right to increase rent by up to 5% annually with sixty
(60) days written notice to the Tenant. The Tenant agrees that this increase
percentage is reasonable and waives any right to dispute rent increases within
this range.

10. ASSIGNMENT AND SUBLETTING
The Tenant may not assign this lease or sublet the rental unit under any
circumstances whatsoever. Any attempt to assign or sublet without the express
written consent of the Landlord shall be deemed a material breach of this
Agreement and grounds for immediate termination.

11. EARLY TERMINATION
(a) The Landlord may terminate this lease with thirty (30) days written notice
    for any reason, including but not limited to the sale of the property.
(b) If the Tenant wishes to terminate the lease early, the Tenant must pay a
    penalty equal to three (3) months' rent.

12. INSURANCE
The Tenant must purchase tenant insurance through LandlordSure Insurance Co.,
the Landlord's affiliated insurance provider, at a cost of $50.00 per month,
payable with the monthly rent.

13. PARKING
One parking spot is included. The Tenant may not allow any other vehicle to use
the assigned parking spot.

14. UTILITIES
The Tenant is responsible for hydro and internet. Water and gas are included.

15. NOISE AND CONDUCT
The Tenant agrees to maintain reasonable noise levels, particularly between
10:00 PM and 8:00 AM.

16. SMOKING
Smoking is not permitted inside the rental unit or on balconies.

17. GOVERNING LAW
This Agreement shall be governed by the laws of the Province of Ontario. In
the event of any conflict between this Agreement and the Residential Tenancies
Act, 2006, this Agreement shall prevail.

SIGNATURES:

_________________________          _________________________
Landlord: John Smith               Tenant: Jane Doe
Date: January 15, 2025             Date: January 15, 2025
"""


def generate_pdf():
    doc = fitz.open()

    # Split text into chunks that fit on pages
    lines = LEASE_TEXT.strip().split("\n")
    lines_per_page = 48
    font_size = 10
    margin_x = 54  # 0.75 inch
    margin_y = 54
    line_height = 13

    for page_start in range(0, len(lines), lines_per_page):
        page = doc.new_page(width=612, height=792)  # Letter size
        page_lines = lines[page_start : page_start + lines_per_page]

        y = margin_y
        for line in page_lines:
            # Title and section headers in bold
            if line.strip().startswith("RESIDENTIAL LEASE AGREEMENT"):
                page.insert_text(
                    (margin_x, y),
                    line.strip(),
                    fontsize=14,
                    fontname="helv",
                )
                y += line_height + 4
            elif line.strip() and line.strip()[0].isdigit() and "." in line.strip()[:3]:
                page.insert_text(
                    (margin_x, y),
                    line.strip(),
                    fontsize=font_size + 1,
                    fontname="helv",
                )
                y += line_height
            else:
                page.insert_text(
                    (margin_x, y),
                    line.rstrip(),
                    fontsize=font_size,
                    fontname="helv",
                )
                y += line_height

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT_PATH))
    doc.close()
    print(f"Demo lease PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_pdf()
