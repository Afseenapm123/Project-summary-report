# Project-wise Purchase and Sales Summary Report – ERPNext

This project is a custom Script Report in ERPNext that provides a financial summary for each project, including:

- Total Purchase Order (PO) Amount
- Total Purchase Invoice Amount
- Total Sales Order (SO) Amount
- Percentage of Invoice Amount against Sales Order
- A bar chart visualization of invoice percentage

---

## ✅ Features

- Aggregated data per project
- Filters:
  - From Date
  - To Date
  - Project (optional)
- Handles edge cases:
  - Missing PO, PI, or SO data
  - Sales Order amount = 0 (no division errors)
- Amounts formatted in Indian currency (INR)
- Bar chart using `frappe.Chart`

---

## 📁 Folder Structure

project-summary-report/
├── Report/
│ ├── project_wise_purchase_and_sales_summary.py # Backend data logic
│ └── project_wise_purchase_and_sales_summary.js # Frontend filters and chart
└── README.md # This documentation

---

## 🛠 Setup Instructions

1. **Create a Script Report** in ERPNext UI:
   - Go to: Tools > Report > New
   - Report Name: `Project-wise Purchase and Sales Summary`
   - Ref Doctype: `Project`
   - Report Type: `Script Report`
   - Module: Select your module
   - Is Standard: Unchecked

2. **Place Files:**
   - Copy the `project_wise_purchase_and_sales_summary.py` and `.js` files to:
     ```
     your_app/your_app/report/project_wise_purchase_and_sales_summary/
     ```

3. **Build & Restart Bench:**

   ```bash
   bench build
   bench restart 

4. **Open the Report from UI and test filters and chart:** 

---

## 📊 Example Output

| Project   | PO Amount | Invoice Amount | SO Amount | Invoice % to SO |
|-----------|-----------|----------------|-----------|-----------------|
| Project A | ₹50,000   | ₹40,000        | ₹80,000   | 50%             |
| Project B | ₹0        | ₹30,000        | ₹0        | 0%              |

---

## 📌 Author

- Afseena pm


   

   
