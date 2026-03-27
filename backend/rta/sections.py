"""
Ontario Residential Tenancies Act, 2006 (RTA) — Key Statutory Text

These are verbatim excerpts from the RTA used as reference context
in the Claude API prompt for lease analysis.
"""

RTA_SECTIONS: dict[str, dict[str, str]] = {
    "illegal_deposits": {
        "title": "Illegal Charges and Deposits",
        "sections": "s.105-106, s.134",
        "text": (
            "Section 105 — Security deposits, limitation\n"
            "(1) The only security deposit that a landlord may collect is a rent deposit "
            "collected in accordance with section 106.\n"
            "(2) A landlord shall not require or attempt to require a tenant or prospective "
            "tenant to pay any consideration, fee, deposit, premium or other like amount "
            "in addition to the rent for a rental unit, other than a rent deposit as provided "
            "for in section 106.\n\n"
            "Section 106 — Rent deposit\n"
            "(1) A landlord may require a tenant to pay a rent deposit with respect to a "
            "tenancy if the landlord does so on or before entering into the tenancy agreement.\n"
            "(2) The amount of a rent deposit shall not be more than the lesser of the amount "
            "of rent for one rent period and the amount of rent for one month.\n"
            "(3) If the lawful rent increases after a tenant has paid a rent deposit, the "
            "landlord may require the tenant to pay an additional amount to increase the "
            "rent deposit up to the amount permitted by subsection (2). However, the "
            "landlord shall do so no earlier than one year after the date of the last "
            "rent deposit increase.\n"
            "(4) A landlord of a rental unit shall pay interest to the tenant annually on "
            "the amount of the rent deposit at a rate equal to the guideline determined "
            "under section 120 that is in effect at the time payment becomes due.\n"
            "(5) The obligation under subsection (4) to pay interest applies from the day "
            "the landlord receives the rent deposit to the day the landlord last used the "
            "rent deposit to pay the rent for the last rent period before the tenancy "
            "terminates.\n"
            "(6) A landlord shall apply a rent deposit that a tenant has paid to the rent "
            "for the last rent period before the tenancy terminates.\n\n"
            "Section 134 — Additional charges prohibited\n"
            "(1) Unless otherwise prescribed, no landlord shall, directly or indirectly, "
            "with respect to any rental unit, collect or require or attempt to collect or "
            "require from a tenant, prospective tenant or former tenant any fee, premium, "
            "commission, bonus, penalty, key deposit or other like amount of money whether "
            "or not the money is refundable.\n"
            "(3) Unless otherwise prescribed, no landlord shall, directly or indirectly, "
            "with respect to any rental unit, require or attempt to require a tenant or "
            "prospective tenant to pay any consideration for goods or services as a condition "
            "for granting the tenancy or continuing to permit occupancy of a rental unit."
        ),
    },
    "no_pet_clauses": {
        "title": "No-Pet Clauses",
        "sections": "s.14",
        "text": (
            "Section 14 — No pet provisions void\n"
            "A provision in a tenancy agreement prohibiting the presence of animals in or "
            "about the residential complex is void.\n\n"
            "Note: While landlords cannot include enforceable no-pet clauses, a tenant can "
            "still be evicted under s.76 if an animal causes serious problems such as "
            "substantial damage, allergic reactions to other tenants, or poses a danger. "
            "The no-pet clause itself, however, is void and unenforceable."
        ),
    },
    "maintenance_obligations": {
        "title": "Maintenance and Repair Obligations",
        "sections": "s.20-26",
        "text": (
            "Section 20 — Landlord's responsibility to repair\n"
            "(1) A landlord is responsible for providing and maintaining a residential "
            "complex, including the rental units in it, in a good state of repair and fit "
            "for habitation and for complying with health, safety, housing and maintenance "
            "standards.\n"
            "(2) Subsection (1) applies even if the tenant was aware of a state of "
            "non-repair or a contravention of a standard before entering into the tenancy "
            "agreement.\n\n"
            "Section 21 — Landlord's responsibility re services\n"
            "(1) A landlord shall not at any time during a tenant's occupancy of a rental "
            "unit and before the day on which an order evicting the tenant is executed "
            "withhold the reasonable supply of any vital service, care service or food "
            "that it is the landlord's obligation to supply under the tenancy agreement "
            "or deliberately interfere with the reasonable supply of any vital service, "
            "care service or food.\n\n"
            "Section 22 — Landlord not to interfere with reasonable enjoyment\n"
            "A landlord shall not at any time during a tenant's occupancy of a rental unit "
            "and before the day on which an order evicting the tenant is executed "
            "substantially interfere with the reasonable enjoyment of the rental unit or "
            "the residential complex in which it is located for all usual purposes by a "
            "tenant or members of his or her household.\n\n"
            "Section 23 — Landlord not to harass, etc.\n"
            "A landlord shall not harass, obstruct, coerce, threaten or interfere with a "
            "tenant.\n\n"
            "Section 26 — Tenant's responsibility for cleanliness\n"
            "The tenant is responsible for ordinary cleanliness of the rental unit, except "
            "to the extent that the tenancy agreement requires the landlord to clean it."
        ),
    },
    "landlord_entry": {
        "title": "Landlord Entry Rules",
        "sections": "s.25-27",
        "text": (
            "Section 25 — Entry without notice\n"
            "A landlord may enter a rental unit at any time without written notice in the "
            "following cases:\n"
            "(a) in cases of emergency;\n"
            "(b) if the tenant consents to the entry at the time of entry.\n\n"
            "Section 26 — Notice of entry\n"
            "(1) A landlord may enter a rental unit in accordance with written notice "
            "given to the tenant at least 24 hours before the time of entry under the "
            "following circumstances:\n"
            "1. To carry out a repair or replacement or do work in the rental unit.\n"
            "2. To allow a potential mortgagee or insurer of the residential complex to "
            "view the rental unit.\n"
            "3. To allow a person who holds a certificate of authorization within the "
            "meaning of the Professional Engineers Act, 1990 or a certificate of practice "
            "within the meaning of the Architects Act to make a physical inspection of "
            "the rental unit to satisfy a requirement imposed under subsection 9(4) of "
            "the Condominium Act, 1998.\n"
            "4. For any other reasonable reason for entry specified in the tenancy "
            "agreement.\n"
            "(2) The written notice under subsection (1) shall specify the reason for "
            "entry, the day of entry and a time of entry between the hours of 8 a.m. and "
            "8 p.m.\n"
            "(3) The landlord may enter the rental unit within the time period specified "
            "in the notice.\n\n"
            "Section 27 — Entry to show rental unit\n"
            "(1) A landlord may enter the rental unit without written notice to show the "
            "unit to prospective tenants if the tenancy agreement has been terminated or "
            "the landlord and tenant have agreed that the tenancy will be terminated.\n"
            "(2) The landlord shall make a reasonable effort to inform the tenant before "
            "entering for a showing.\n"
            "(3) The entry under subsection (1) shall be between the hours of 8 a.m. and "
            "8 p.m."
        ),
    },
    "rent_increases": {
        "title": "Rent Increase Limits",
        "sections": "s.116-120",
        "text": (
            "Section 116 — Landlord's notice of rent increase\n"
            "(1) A landlord shall not increase the rent charged to a tenant for a rental "
            "unit without first giving the tenant at least 90 days written notice of the "
            "landlord's intention to increase the rent.\n"
            "(2) The notice shall be in a form approved by the Board and shall set out the "
            "landlord's intention to increase the rent and the new rent.\n"
            "(3) An increase in rent is void if the landlord has not given the notice "
            "required by this section.\n\n"
            "Section 119 — Guideline\n"
            "(1) The Minister shall, each calendar year, determine a guideline in effect "
            "for the following calendar year.\n"
            "(2) The guideline for a calendar year shall be the percentage change from "
            "year to year in the Consumer Price Index for Ontario, as reported monthly by "
            "Statistics Canada, averaged over the 12-month period that ends in the June "
            "before that calendar year, rounded to the first decimal point.\n\n"
            "Section 120 — Rent increase — Limitation\n"
            "(1) No landlord may increase the rent charged to a tenant, or to an assignee "
            "under section 95, during the term of their tenancy by more than the guideline, "
            "except in accordance with:\n"
            "(a) an agreement under section 121 [above guideline by agreement];\n"
            "(b) an order under section 126 [above guideline increase order from LTB].\n"
            "(2) Subsection (1) does not apply with respect to a rental unit if:\n"
            "(a) it was not occupied for any purpose before June 17, 1998;\n"
            "(b) no part of the building was occupied for residential purposes before "
            "November 15, 2018 [new construction exemption].\n\n"
            "Note: For 2024, the rent increase guideline is 2.5%. The guideline is capped "
            "at 2.5% under the Protecting Tenants and Strengthening Community Housing Act, "
            "2020. Landlords cannot increase rent more than once every 12 months."
        ),
    },
    "assignment_subletting": {
        "title": "Assignment and Subletting",
        "sections": "s.95-98",
        "text": (
            "Section 95 — Assignment of tenancy\n"
            "(1) Subject to subsections (2), (3) and (6), and section 96, a tenant may "
            "not assign a rental unit to another person without the consent of the "
            "landlord.\n"
            "(2) A landlord shall not arbitrarily or unreasonably refuse consent to an "
            "assignment of a rental unit to a potential assignee under this section.\n"
            "(3) Upon receiving a request from a tenant to assign the rental unit, the "
            "landlord may:\n"
            "(a) consent to the assignment;\n"
            "(b) refuse consent to the assignment; or\n"
            "(c) refuse consent to the assignment and give the tenant a notice of "
            "termination under section 96.\n"
            "(6) A landlord who refuses to consent to an assignment under subclause "
            "(3)(b) shall set out the reasons for the refusal in writing within seven "
            "days after receiving the request.\n\n"
            "Section 97 — Subletting rental unit\n"
            "(1) A tenant may sublet a rental unit to another person with the consent of "
            "the landlord.\n"
            "(2) A landlord shall not arbitrarily or unreasonably withhold consent to the "
            "sublet of a rental unit to a potential subtenant.\n\n"
            "Section 98 — Charges related to assignment or subletting\n"
            "(1) A tenant shall not charge an amount that is more than what the tenant is "
            "required to pay under the tenancy agreement, unless the amount is for "
            "additional services, facilities, or goods provided by the tenant.\n"
            "(4) A landlord may charge a tenant only for the landlord's reasonable "
            "out-of-pocket expenses incurred in giving consent to an assignment or "
            "sublet."
        ),
    },
    "eviction_restrictions": {
        "title": "Eviction Restrictions",
        "sections": "s.37, s.48, s.77, s.83",
        "text": (
            "Section 37 — Termination by agreement or notice\n"
            "(1) A tenancy may be terminated only in accordance with this Act.\n"
            "(2) For greater certainty, a notice of termination need not be given if a "
            "landlord and a tenant have agreed to terminate a tenancy.\n\n"
            "Section 48 — Notice, landlord personally requires unit\n"
            "(1) A landlord may, by notice, terminate a tenancy if the landlord in good "
            "faith requires possession of the rental unit for the purpose of residential "
            "occupation by:\n"
            "(a) the landlord;\n"
            "(b) the landlord's spouse;\n"
            "(c) a child or parent of the landlord or the landlord's spouse.\n"
            "(2) The date for termination specified in the notice shall be at least 60 "
            "days after the notice is given and shall be the day a period of the tenancy "
            "ends or, where the tenancy is for a fixed term, the end of the term.\n\n"
            "Section 48.1 — Compensation, landlord's own use\n"
            "A landlord shall compensate a tenant in an amount equal to one month's rent "
            "or offer the tenant another rental unit acceptable to the tenant if the "
            "landlord gives a notice of termination under section 48.\n\n"
            "Section 77 — Agreement to terminate, tenant's notice\n"
            "A landlord and a tenant may agree to terminate a tenancy. The agreement "
            "shall be in a form approved by the Board.\n\n"
            "Section 83 — Power of Board, eviction\n"
            "(1) Upon an application for an order evicting a tenant, the Board may, "
            "despite any other provision of this Act or the tenancy agreement:\n"
            "(a) refuse to grant the application unless satisfied, having regard to all "
            "the circumstances, that it would be unfair to refuse; or\n"
            "(b) order that the enforcement of the eviction order be postponed for a "
            "period of time.\n\n"
            "Key principle: A landlord CANNOT evict a tenant on their own. Only the "
            "Landlord and Tenant Board (LTB) can order an eviction. Any lease clause "
            "purporting to allow the landlord to terminate the tenancy at will, without "
            "cause, or outside the procedures in the RTA is void."
        ),
    },
    "guest_restrictions": {
        "title": "Guest Restrictions",
        "sections": "s.22, s.23",
        "text": (
            "Under Ontario law, a tenant has the right to have guests in their rental "
            "unit. This right flows from the tenant's right to reasonable enjoyment of "
            "the unit under s.22 of the RTA.\n\n"
            "Section 22 — A landlord shall not substantially interfere with the "
            "reasonable enjoyment of the rental unit or the residential complex for all "
            "usual purposes by a tenant or members of his or her household.\n\n"
            "Section 23 — A landlord shall not harass, obstruct, coerce, threaten or "
            "interfere with a tenant.\n\n"
            "Any clause that unreasonably restricts guests — such as imposing guest "
            "registration requirements, limiting overnight guests, charging fees for "
            "guests, or requiring landlord approval for visitors — is generally "
            "considered an interference with reasonable enjoyment under s.22. While a "
            "tenant must not permit guests to cause damage or disturb other tenants, "
            "blanket restrictions on guests are unenforceable."
        ),
    },
    "wear_and_tear": {
        "title": "Standard Wear and Tear",
        "sections": "s.20, s.89",
        "text": (
            "Section 20 — Landlord's responsibility to repair\n"
            "(1) A landlord is responsible for providing and maintaining a residential "
            "complex, including the rental units in it, in a good state of repair and "
            "fit for habitation and for complying with health, safety, housing and "
            "maintenance standards.\n\n"
            "Section 89 — Compensation for damage\n"
            "(1) A landlord may apply to the Board for an order requiring a tenant to "
            "pay reasonable costs that the landlord has incurred or will incur for the "
            "repair of or, where repairing is not reasonable, the replacement of damaged "
            "property, if the tenant, another occupant of the rental unit or a person "
            "whom the tenant permits in the residential complex wilfully or negligently "
            "causes undue damage to the rental unit or the residential complex.\n\n"
            "Key distinction: 'Undue damage' is damage beyond normal wear and tear "
            "caused by wilful or negligent conduct. Normal wear and tear includes things "
            "like paint fading, carpet wearing thin from normal use, minor scuffs on "
            "walls, nail holes from hanging pictures, and minor floor scratches. A "
            "landlord CANNOT charge a tenant for normal wear and tear. Any lease clause "
            "requiring a tenant to restore the unit to its original condition, "
            "professionally clean carpets, repaint walls, or pay for normal wear and "
            "tear upon moving out is unenforceable."
        ),
    },
    "post_dated_cheques": {
        "title": "Post-Dated Cheques and Payment Methods",
        "sections": "s.108",
        "text": (
            "Section 108 — Rent payment methods\n"
            "(1) A tenant has the right to pay rent by any method that allows the "
            "tenant to make a payment.\n"
            "(2) A provision in a tenancy agreement that requires the tenant to pay rent "
            "by a specific method, including but not limited to post-dated cheques or "
            "automatic debits, is void.\n\n"
            "Note: A landlord cannot require post-dated cheques or any single specific "
            "payment method. While a tenant may voluntarily provide post-dated cheques, "
            "a lease clause that mandates them is void and unenforceable under s.108."
        ),
    },
}
