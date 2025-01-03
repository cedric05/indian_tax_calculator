class TaxCalculator:
    def __init__(self, income):
        self.income = income
        self.deductions = []
        self.tax_breakdown = []
        self.non_tax_deductable = []

    def add_deduction(self, amount, reason):
        self.deductions.append({"amount": amount, "reason": reason})

    def calculate_deductions(self):
        return sum(d["amount"] for d in self.deductions)

    def calculate_tax(self):
        taxable_income = self.income - self.calculate_deductions()
        self.tax_breakdown.append({"category": f"Taxable Income: {taxable_income}", "amount": taxable_income})
        tax_collected = 0
        if taxable_income <= 3:
            tax_collected = 0
        elif 3 < taxable_income <= 7:
            tax_collected += self._add_tax(3, taxable_income, 0.05)
        elif 7 < taxable_income <= 10:
            tax_collected += self._add_tax(7, taxable_income, 0.1)
            tax_collected += self._add_tax(3, 7, 0.05)
        elif 10 < taxable_income <= 12:
            tax_collected += self._add_tax(10, taxable_income, 0.15)
            tax_collected += self._add_tax(7, 10, 0.1)
            tax_collected += self._add_tax(3, 7, 0.05)
        elif 12 < taxable_income <= 15:
            tax_collected += self._add_tax(12, taxable_income, 0.2)
            tax_collected += self._add_tax(10, 12, 0.15)
            tax_collected += self._add_tax(7, 10, 0.1)
            tax_collected += self._add_tax(3, 7, 0.05)
        elif 15 < taxable_income:
            tax_collected += self._add_tax(15, taxable_income, 0.3)
            tax_collected += self._add_tax(12, 15, 0.2)
            tax_collected += self._add_tax(10, 12, 0.15)
            tax_collected += self._add_tax(7, 10, 0.1)
            tax_collected += self._add_tax(3, 7, 0.05)
        self.tax_breakdown.append({"category": f"Net tax: {tax_collected}", "amount": tax_collected})
        cess = tax_collected * 0.04
        self.tax_breakdown.append({"category": f"Education Cess(0.04) of {tax_collected}", "amount": cess})

        surcharge = self._calculate_surcharge(taxable_income, tax_collected)
        tax_collected += cess + surcharge

        return tax_collected

    def _add_tax(self, start, end, percentage):
        taxable = max(0, min(self.income, end) - start)
        tax = taxable * percentage
        self.tax_breakdown.append({"category": f"{start} to {end} @ {percentage * 100}%", "amount": tax})
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
        self.tax_breakdown.append({"category": f"Surcharge ({surcharge_rate}) of {tax_collected}", "amount": surcharge})
        return surcharge

    def effective_tax_rate(self):
        total_tax = self.calculate_tax()
        return (total_tax / self.income) * 100

    def add_non_tax_deductable(self, amount, reason):
        self.non_tax_deductable.append({"amount": amount, "reason": reason})
    
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
        print(f"Effective Tax Rate: {self.effective_tax_rate():.2f}%")
        print(f"Monthly pay is : {net_effective_income/12}")
