
class Voucher:

    def __init__(self, cheque_date, posting_date, title):

        self.dict_voucher = {}
        self.cuentas = []
        self.dict_voucher['cheque_date'] = cheque_date
        self.dict_voucher['posting_date'] = posting_date
        self.dict_voucher['title'] = title
        self.dict_voucher['accounts'] = self.cuentas
        self.dict_voucher['total_credit'] = 0
        self.dict_voucher['total_debit'] = 0
        self.dict_voucher['company'] = 'Constructora Tecton SpA'
        self.dict_voucher['naming_series'] = "JV-"
        self.dict_voucher['doctype'] = "Journal Entry"

    def agregarCuenta(self, cuenta):

        debit = cuenta.dict_cuenta['debit']
        credit = cuenta.dict_cuenta['credit']

        if debit > 0 and credit > 0:
            nuevo_dict = cuenta.dict_cuenta.copy()
            nuevo_dict['credit'] = cuenta.dict_cuenta['debit'] = 0.0
            nuevo_dict['credit_in_account_currency'] = cuenta.dict_cuenta['debit_in_account_currency'] = 0.0
            self.cuentas.append(nuevo_dict)
            self.cuentas.append(cuenta.dict_cuenta)
        else:
            self.cuentas.append(cuenta.dict_cuenta)

        self.recalcular_totales()

    def recalcular_totales(self):

        total_credit = 0
        total_debit = 0

        for cuenta in self.cuentas:
            total_credit += cuenta['credit']
            total_debit += cuenta['debit']

        self.dict_voucher['total_credit'] = total_credit
        self.dict_voucher['total_debit'] = total_debit

    def insert_erp(self):
        return 0

class JournalEntryAccount:

    def __init__(self, debit, credit, account, cost_center):

        self.dict_cuenta = {}

        self.dict_cuenta['doctype'] = "Journal Entry Account"
        self.dict_cuenta['cost_center'] = cost_center
        self.dict_cuenta['debit'] = debit
        self.dict_cuenta['debit_in_account_currency'] = debit
        self.dict_cuenta['account'] = account
        self.dict_cuenta['credit'] = credit
        self.dict_cuenta['credit_in_account_currency'] = credit
