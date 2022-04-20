



    def calc_fair_value(self):
        #eps5y = 0.1543
        #model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)        
        '''
        calculate the fair_value using DCF model as follows
        1. calculate a yearly discount factor using the WACC
        2. Get the Free Cash flow
        3. Sum the discounted value of the FCC for the 20 years using similar approach as presented in class
        4. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        5. Return the stock fair value of the stock
        '''
        results = None
        FreeCashFlow = self.stock.get_free_cashflow()
        CurrentCash = self.stock.get_cash_and_cash_equivalent()
        WACC = self.stock.lookup_wacc_by_beta(self.stock.get_beta())
        TotalDebt = self.stock.get_total_debt()
        Shares = self.stock.get_num_shares_outstanding()
        DiscountFactor = 1 / (1 + WACC)
        EPS5Y = self.short_term_growth_rate
        EPS6To10Y = self.medium_term_growth_rate
        EPS10To20Y = self.long_term_growth_rate
        DCF = 0
        for i in range(1, 6):
            DCF += FreeCashFlow * (1 + EPS5Y) ** i * DiscountFactor ** i

        CF5 = FreeCashFlow * (1 + EPS5Y) ** 5
        for i in range(1, 6):
            DCF += CF5 * (1 + EPS6To10Y) ** i * DiscountFactor ** (i + 5)

        CF10 = CF5 * (1 + EPS6To10Y) ** 5
        for i in range(1, 11):
            DCF += CF10 * (1 + EPS10To20Y) ** i * DiscountFactor ** (i + 10)

        PresentValue = CurrentCash - TotalDebt + DCF
        results = PresentValue / Shares
        return(results)