# Copyright (c) 2025, afseena and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 200},
        {"label": "PO Amount", "fieldname": "po_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Invoice Amount", "fieldname": "invoice_amount", "fieldtype": "Currency", "width": 150},
        {"label": "SO Amount", "fieldname": "so_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Invoice % to SO", "fieldname": "invoice_percentage", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    project_filter = filters.get("project")

    conditions = ""
    if project_filter:
        conditions += f" AND project = '{project_filter}'"
    if from_date and to_date:
        date_filter = f" BETWEEN '{from_date}' AND '{to_date}'"
    else:
        date_filter = ""

    po_data = frappe.db.sql(f"""
        SELECT project, SUM(base_grand_total) as po_amount
        FROM `tabPurchase Order`
        WHERE docstatus = 1 {conditions} AND transaction_date {date_filter}
        GROUP BY project
    """, as_dict=1)

    pi_data = frappe.db.sql(f"""
        SELECT project, SUM(base_grand_total) as invoice_amount
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1 {conditions} AND posting_date {date_filter}
        GROUP BY project
    """, as_dict=1)

    so_data = frappe.db.sql(f"""
        SELECT project, SUM(base_grand_total) as so_amount
        FROM `tabSales Order`
        WHERE docstatus = 1 {conditions} AND transaction_date {date_filter}
        GROUP BY project
    """, as_dict=1)

    project_set = set()
    for d in (po_data + pi_data + so_data):
        if d.project:
            project_set.add(d.project)

    result = []
    for project in project_set:
        po = next((d.po_amount for d in po_data if d.project == project), 0)
        invoice = next((d.invoice_amount for d in pi_data if d.project == project), 0)
        so = next((d.so_amount for d in so_data if d.project == project), 0)

        percentage = "0%"
        if so:
            percentage = f"{round((invoice / so) * 100, 2)}%"

        result.append({
            "project": project,
            "po_amount": flt(po, 2),
            "invoice_amount": flt(invoice, 2),
            "so_amount": flt(so, 2),
            "invoice_percentage": percentage
        })

    return result
