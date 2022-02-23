import frappe


@frappe.whitelist()
def update_sn_all():
    sn_list = frappe.get_all("Serial No",filters=[["purchase_document_no","is","not set"]],fields=["name"])
    for row in sn_list:
        sl_entry = frappe.get_all("Stock Ledger Entry",filters=[["serial_no","like",f"%{row.name}%"],["voucher_type","in",["Purchase Receipt","Stock Entry"]]],fields=["*"],order_by="posting_date asc")
        if len(sl_entry) >= 1:
            print(sl_entry[0].name)
            frappe.db.sql("""UPDATE `tabSerial No`
SET purchase_document_type=%s,
purchase_document_no=%s,
purchase_date=%s,
purchase_time=%s,
purchase_rate=%s
WHERE name=%s""", (sl_entry[0].voucher_type, sl_entry[0].voucher_no, sl_entry[0].posting_date, sl_entry[0].posting_time, sl_entry[0].incoming_rate, row.name))
