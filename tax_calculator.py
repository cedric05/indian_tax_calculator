BASIC_PAY_PER = 0.4
EPF_PER = 0.12
ESPP = 0.15

# Define tax slabs as a configuration
TAX_SLABS = [
    (3, 7, 0.05),
    (7, 10, 0.1),
    (10, 12, 0.15),
    (12, 15, 0.2),
    (15, float('inf'), 0.3)  # Last slab with no upper limit
]

TAX_SLAB_2025_2026 = [
    (4, 8, 0.05),
    (8, 12, 0.1),
    (12, 16, 0.15),
    (16, 20, 0.2),
    (20, 24, 0.25),
    (24, float('inf'), 0.3)  # Last slab with no upper limit
]

class TaxCalculator:
    def __init__(self, income, slab):
        self.income = income
        self.deductions = []
        self.tax_breakdown = []
        self.non_tax_deductable = []
        self.tax_slabs = slab
        self.min = slab[0][0]

    def add_deduction(self, amount, reason):
        self.deductions.append({"amount": amount, "reason": reason})

    def calculate_deductions(self):
        return sum(d["amount"] for d in self.deductions)

    def calculate_tax(self):
        if self.income < self.min:
            return 0
        taxable_income = self.income - self.calculate_deductions()
        self.tax_breakdown.append(
            {"category": f"Taxable Income: {taxable_income}", "amount": taxable_income}
        )
        tax_collected = 0
        for lower, upper, rate in self.tax_slabs:
            if taxable_income <= lower:
                break  # Stop if the income is below the current slab

            effective_upper = min(upper, taxable_income)  # Don't exceed taxable income
            tax_collected += self._add_tax(lower, effective_upper, rate)

        self.tax_breakdown.append(
            {"category": f"Net tax: {tax_collected}", "amount": tax_collected}
        )
        cess = self._calculate_cess(tax_collected)
        self.tax_breakdown.append(
            {"category": f"Education Cess(0.04) of {tax_collected}", "amount": cess}
        )

        surcharge = self._calculate_surcharge(taxable_income, tax_collected)
        tax_collected += cess + surcharge

        return tax_collected

    def _calculate_cess(self, tax_collected):
        cess = tax_collected * 0.04
        return cess

    def _add_tax(self, start, end, percentage):
        taxable = max(0, min(self.income, end) - start)
        tax = taxable * percentage
        self.tax_breakdown.append(
            {"category": f"{start} to {end} @ {percentage * 100}%", "amount": tax}
        )
        return tax

    def _calculate_surcharge(self, income, tax_collected):
        surcharge_rate = 0
        if 50 < income <= 100:
            surcharge_rate = 0.1
        elif 100 < income <= 200:
            surcharge_rate = 0.15
        elif income > 200:
            surcharge_rate = 0.25

        surcharge = surcharge_rate * tax_collected
        self.tax_breakdown.append(
            {
                "category": f"Surcharge ({surcharge_rate}) of {tax_collected}",
                "amount": surcharge,
            }
        )
        return surcharge

    def effective_tax_rate(self):
        total_tax = self.calculate_tax()
        return (total_tax / self.income) * 100

    def add_non_tax_deductable(self, amount, reason):
        self.non_tax_deductable.append(
            {"amount": amount, "monthly": amount / 12, "reason": reason}
        )

    def total_non_tax_deducatble(self):
        return sum(i["amount"] for i in self.non_tax_deductable)

    def pretty_print(self):
        tax_deductables = self.calculate_deductions()
        total_tax = self.calculate_tax()
        effective_income = self.income - total_tax
        non_tax_deducatbles = self.total_non_tax_deducatble()
        net_effective_income = effective_income - non_tax_deducatbles
        print(f"Total Income: ₹{self.income:.2f}")
        print("\n--- Deductions ---")
        for deduction in self.deductions:
            print(f"{deduction['reason']}: ₹{deduction['amount']:.2f}")
        print("\n--- Tax Breakdown ---")
        for entry in self.tax_breakdown:
            print(f"{entry['category']}: ₹{entry['amount']:.2f}")
        print("\n--- Summary ---")
        print(f"Total Deductions: ₹{tax_deductables:.2f}")
        print(f"Net Income After Deductions: ₹{self.income - tax_deductables:.2f}")
        print(f"Total Tax: ₹{total_tax:.2f}")
        print(f"Net Income after Deductions: ₹{effective_income}")
        for non_tax_deduction in self.non_tax_deductable:
            print(
                f"{non_tax_deduction['reason']}: ₹{non_tax_deduction['amount']:.2f}, monthly {non_tax_deduction['monthly']:.2f}"
            )
        print(f"Effective Tax Rate: {self.effective_tax_rate():.2f}%")
        print(f"Monthly pay is : {net_effective_income/12}")

        return {
            "gross_income": self.income,
            "income_after_tax": effective_income,
            "total_tax": total_tax,
            "deductions": non_tax_deducatbles,
            "net_income": net_effective_income,
            "tax_percentage": self.effective_tax_rate(),
            "monthly_pay": net_effective_income/12,
        }

    def add_common_deductions(self):
        basic_pay = self.income * BASIC_PAY_PER
        epf = basic_pay * EPF_PER
        espp = (self.income - epf) * ESPP
        self.add_deduction(0.75, "Standard deduction") # just for tax calculation
        self.add_deduction(epf, "Company EPF deduction") # just for calculation
        self.add_non_tax_deductable(epf, "Employee EPF deduction") # deducted monthly
        self.add_non_tax_deductable(epf, "Company EPF deduction") # deducted monthly
        self.add_non_tax_deductable(espp, "ESPP") # deducted monthly


if __name__ == "__main__":
    import sys
    INCOME  = int(sys.argv[1])
    tax_calculator = TaxCalculator(INCOME, TAX_SLAB_2025_2026)
    tax_calculator.add_common_deductions()
    tax_calculator.pretty_print()