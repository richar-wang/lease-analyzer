"""
Ontario Standard Lease (Form 2229E) — Key Provisions

The Ontario Standard Lease is the mandatory lease form for most residential
tenancies in Ontario. These are the standard terms that should appear in
any compliant lease. Deviations from these terms are flagged for comparison.
"""

STANDARD_LEASE_SECTIONS: dict[str, dict[str, str]] = {
    "rent_and_deposits": {
        "title": "Rent and Deposits",
        "standard": (
            "The standard lease permits only:\n"
            "- Monthly rent amount clearly stated\n"
            "- A rent deposit (last month's rent) of no more than one month's rent\n"
            "- The rent deposit must be applied to the last month's rent\n"
            "- Interest must be paid on the rent deposit annually at the guideline rate\n"
            "- No other deposits, fees, premiums, or charges are permitted\n"
            "- No key deposits (or if charged, must be refundable and no more than replacement cost)\n"
            "- The tenant can pay rent by any method they choose"
        ),
    },
    "services_and_utilities": {
        "title": "Services and Utilities",
        "standard": (
            "The standard lease requires:\n"
            "- Clear indication of which utilities/services are included in rent\n"
            "- Clear indication of which utilities/services the tenant pays separately\n"
            "- Gas, AC, kitchen/laundry appliances, parking, cable/internet explicitly listed\n"
            "- Landlord cannot cut off or withhold vital services"
        ),
    },
    "maintenance_and_repairs": {
        "title": "Maintenance and Repairs",
        "standard": (
            "The standard lease states:\n"
            "- The landlord must keep the unit and building in good repair\n"
            "- The landlord must comply with health, safety, and maintenance standards\n"
            "- The tenant is responsible for ordinary cleanliness\n"
            "- The tenant must repair or pay for any damage caused by the tenant, "
            "guests, or another occupant (not including normal wear and tear)\n"
            "- The landlord cannot shift repair obligations to the tenant"
        ),
    },
    "entry_rules": {
        "title": "Entry by Landlord",
        "standard": (
            "The standard lease states:\n"
            "- 24 hours written notice required for entry\n"
            "- Entry only between 8 a.m. and 8 p.m.\n"
            "- Notice must state the reason for entry\n"
            "- Entry without notice only in emergencies or with tenant consent at the time\n"
            "- Entry to show the unit to prospective tenants allowed only after notice of "
            "termination given, with reasonable efforts to inform tenant, between 8am-8pm"
        ),
    },
    "assignment_subletting": {
        "title": "Assignment and Subletting",
        "standard": (
            "The standard lease states:\n"
            "- The tenant may ask the landlord to assign or sublet the unit\n"
            "- The landlord cannot arbitrarily or unreasonably refuse\n"
            "- The landlord may charge only reasonable out-of-pocket expenses for processing\n"
            "- If the landlord refuses consent to assign, the tenant can give 30 days notice "
            "to terminate"
        ),
    },
    "pets": {
        "title": "Pets",
        "standard": (
            "The standard lease includes:\n"
            "- A section to indicate if the tenant has pets and what kind\n"
            "- A note that a no-pet clause in the lease is void\n"
            "- However, the tenant can be evicted if the pet causes serious problems "
            "(damage, allergies, danger, noise)"
        ),
    },
    "rent_increases": {
        "title": "Rent Increases",
        "standard": (
            "The standard lease states:\n"
            "- Rent can only be increased once every 12 months\n"
            "- 90 days written notice required (on the proper LTB form)\n"
            "- Increase cannot exceed the annual guideline (2.5% for 2024) without LTB approval\n"
            "- New construction occupied after Nov 15, 2018 is exempt from the guideline"
        ),
    },
    "termination": {
        "title": "Ending the Tenancy",
        "standard": (
            "The standard lease states:\n"
            "- A tenancy can only be ended in accordance with the RTA\n"
            "- The landlord cannot terminate without proper grounds and proper notice\n"
            "- Only the Landlord and Tenant Board can order an eviction\n"
            "- For a fixed-term lease, the tenancy automatically becomes month-to-month "
            "at the end of the term unless the tenant gives proper notice\n"
            "- The standard lease does not include early termination penalties"
        ),
    },
    "additional_terms": {
        "title": "Additional Terms",
        "standard": (
            "The standard lease allows additional terms ONLY if they:\n"
            "- Do not conflict with the RTA or any other laws\n"
            "- Do not conflict with the standard terms of the lease\n"
            "- Are not unconscionable\n"
            "Common illegal additional terms include: no-pet clauses, guest restrictions, "
            "mandatory cleaning fees, specific payment methods, and landlord entry beyond "
            "what the RTA allows"
        ),
    },
}
