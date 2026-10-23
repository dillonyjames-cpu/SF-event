"""Someday Society year-one financial model. All inputs are assumptions to verify."""

PRICE = {"session": 175, "plan": 450, "come_true": 1200}
DIRECT_COST = {"session": 35, "plan": 65, "come_true": 500}
REFERRAL_PER_COME_TRUE = 150   # 5% of an assumed $3,000 experience booked through partners
CARD_FEE = 0.03                # payment processing on service revenue

# Monthly sales (sessions, plans, come_true) for months 1-12
VOLUME = [(3, 1, 0), (4, 2, 0), (5, 2, 1), (6, 3, 1), (7, 3, 1), (8, 3, 2),
          (8, 4, 2), (9, 4, 2), (10, 4, 2), (10, 5, 3), (11, 5, 3), (12, 5, 3)]

FIXED = {"Owner salary": 1500, "Coworking office": 450, "Marketing": 600,
         "Insurance": 150, "Phone, software, website": 150, "Accounting and legal": 100}

STARTUP = {"LLC filing, Statement of Information, $800 franchise tax": 890,
           "City business license and Seller of Travel registration": 200,
           "Legal review of client contract and waiver": 1000,
           "Website, logo and brand": 2500,
           "Laptop, tablet, portable printer": 2000,
           "Launch marketing (brochures, mailers, launch event)": 3000,
           "Insurance deposit": 600,
           "Office deposit and first month": 900,
           "Background check, CPR and first-aid training": 200,
           "Supplies and keepsake materials": 500,
           "Cash reserve (about 3 months of fixed costs)": 9000}

OWNER_EQUITY = 6000
LOAN = 15000
RATE = 0.09
TERM_MONTHS = 60

def payment(p, r, n):
    i = r / 12
    return p * i / (1 - (1 + i) ** -n)

pay = payment(LOAN, RATE, TERM_MONTHS)
fixed = sum(FIXED.values())
startup = sum(STARTUP.values())
reserve = STARTUP["Cash reserve (about 3 months of fixed costs)"]
cash = OWNER_EQUITY + LOAN - (startup - reserve)
balance = LOAN
rows = []
for m, (s, p, c) in enumerate(VOLUME, 1):
    service = s * PRICE["session"] + p * PRICE["plan"] + c * PRICE["come_true"]
    referral = c * REFERRAL_PER_COME_TRUE
    revenue = service + referral
    cogs = s * DIRECT_COST["session"] + p * DIRECT_COST["plan"] + c * DIRECT_COST["come_true"] + round(service * CARD_FEE)
    interest = balance * RATE / 12
    principal = pay - interest
    balance -= principal
    net = revenue - cogs - fixed - interest
    cash += revenue - cogs - fixed - pay
    rows.append(dict(m=m, s=s, p=p, c=c, revenue=revenue, cogs=cogs, gross=revenue - cogs,
                     interest=interest, net=net, cash=cash))

tot = lambda k: sum(r[k] for r in rows)
print(f"Startup total {startup:,}; loan payment {pay:,.2f}/mo; fixed {fixed:,}/mo")
print("M  S P C  revenue  cogs  gross  net  cash_end")
for r in rows:
    print(f"{r['m']:2} {r['s']:2} {r['p']} {r['c']} {r['revenue']:7,} {r['cogs']:5,} {r['gross']:6,} {r['net']:8,.0f} {r['cash']:8,.0f}")
print(f"Year 1: sales {tot('s')}/{tot('p')}/{tot('c')}, revenue {tot('revenue'):,}, cogs {tot('cogs'):,}, "
      f"gross {tot('gross'):,}, fixed {fixed*12:,}, interest {tot('interest'):,.0f}, net {tot('net'):,.0f}")
print(f"Loan balance end Y1 {balance:,.0f}; principal paid {LOAN-balance:,.0f}")
# contribution margins and break-even using month-12 mix
cm = {k: PRICE[k] - DIRECT_COST[k] - PRICE[k] * CARD_FEE for k in PRICE}
cm["come_true"] += REFERRAL_PER_COME_TRUE
print("Contribution margins", {k: round(v, 2) for k, v in cm.items()})
s, p, c = VOLUME[-1]
bundle_cm = s * cm["session"] + p * cm["plan"] + c * cm["come_true"]
bundle_rev = s * 175 + p * 450 + c * 1350
need = fixed + pay
print(f"M12 mix: bundle CM {bundle_cm:,.2f}, revenue {bundle_rev:,}; monthly costs incl loan payment {need:,.2f}; "
      f"break-even = {need/bundle_cm:.2f} bundles = revenue {need/bundle_cm*bundle_rev:,.0f}/mo")
