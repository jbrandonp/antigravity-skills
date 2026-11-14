# 04 — Institutional Financial Modeling Matrix (Oria One)

## 🎯 Objective
Provide ready-to-run generators and mathematical architectures for institutional-grade financial models, complete with dynamic multi-statement linkages, scenario switches, and automated balance checks.

---

## 🎨 The Wall Street Typography Standard

| Category | Hex Code | Visual Meaning | Example Syntax |
| :--- | :--- | :--- | :--- |
| **Inputs** | `#0000FF` | Hardcoded assumptions, drivers, user inputs | `10000.00`, `15.0%` |
| **Formulas** | `#000000` | Native calculations internal to the sheet | `=SUM(B6:B7)`, `=B5*(1+$B$20)` |
| **Cross-Links** | `#008000` | References pointing to another tab | `='P&L Inputs'!$B$10` |
| **External** | `#FF0000` | Links to external files / data sources | `='[Budget.xlsx]Sheet1'!$C$4` |
| **Alerts / Checks** | `#DCFCE7` / `#FEE2E2` | Balanced OK (Green) vs Error (Red) | `=IF(Check=0, "OK", "ERROR")` |

---

## 🏛️ The 7 Core Institutional Models

### 1. Three-Statement Integrated Model (`three_statement`)
- **P&L (Income Statement):** Revenue -> Gross Profit -> EBITDA -> EBIT -> EBT -> Net Income.
- **Balance Sheet:** Assets (Cash, AR, Net PP&E) vs Liabilities & Equity (AP, Retained Earnings).
- **Cash Flow:** Operating Cash Flow (Net Income + D&A - Delta NWC) + Investing Cash Flow (CapEx).
- **Mandatory Balance Check:** Programmed cell `=Total_Assets - (Total_Liabilities + Equity)` formatted with a green/red conditional check.

### 2. Discounted Cash Flow Valuation (`dcf`)
- Unlevered Free Cash Flow (UFCF) projection over a 5-year forecast horizon.
- WACC discounting schedule with mid-year convention capability.
- Dual Terminal Value engines: Gordon Growth Model vs Exit EBITDA Multiple.
- Enterprise Value (EV) to Equity Value bridge (less Net Debt).

### 3. Leveraged Buyout Model (`lbo`)
- Sources & Uses of Funds table with Debt % and Equity % validation.
- Senior Bank Debt (Term Loan A) and Subordinated / Mezzanine tranches.
- Exit Waterfall with implied 5-year IRR (`=IRR(...)`) and Multiple on Invested Capital (MoIC).

### 4. SaaS Cash Runway & Unit Economics (`saas_runway`)
- 12-month cohort projection of MRR, ARR, and gross margins.
- Net Monthly Burn rate and Ending Cash Balance trajectory.
- Automated Zero-Cash Date warning formula alerting if liquidity drops below zero.

### 5. Debt Amortization Cascade (`debt_schedule`)
- Tranche-level Beginning Balance, Scheduled Mandatory Amortization, and Voluntary Cash Sweep.
- Average balance interest calculations and Ending Balance roll-forwards.

### 6. Startup Capitalization Table (`cap_table`)
- Common stock, Option Pool (ESOP), Seed and Series A preferred share tranches.
- Pre-Money Valuation, Investment Capital, Post-Money Share Price, and Dilution percentages.

### 7. Working Capital & Operating Cycle (`working_capital`)
- Detailed breakdown of Accounts Receivable, Inventory, and Accounts Payable.
- Days Sales Outstanding (DSO), Days Inventory Outstanding (DIO), and Days Payable Outstanding (DPO).
- Net Working Capital (NWC) and Cash Conversion Cycle (CCC = DSO + DIO - DPO) in days.
