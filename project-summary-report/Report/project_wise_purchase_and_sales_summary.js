// Copyright (c) 2025, afseena and contributors
// For license information, please see license.txt

frappe.query_reports["Project-wise Purchase and Sales Summary"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "project",
            label: "Project",
            fieldtype: "Link",
            options: "Project"
        }
    ],

    after_datatable_render: function() {
        setTimeout(() => {
            const data = frappe.query_report.data;

            const labels = [];
            const values = [];

            for (const row of data) {
                if (row.project && row.invoice_percentage) {
                    const percent = parseFloat(row.invoice_percentage.replace('%', '').trim());
                    if (!isNaN(percent)) {
                        labels.push(row.project);
                        values.push(percent);
                    }
                }
            }

            const old_chart = document.getElementById("custom-invoice-chart");
            if (old_chart) old_chart.remove();

            if (labels.length && values.length) {
                const container = document.querySelector(".layout-main-section");
                if (!container) return;

                const chart_div = document.createElement("div");
                chart_div.id = "custom-invoice-chart";
                chart_div.style.marginTop = "30px";

                container.appendChild(chart_div);

                new frappe.Chart("#custom-invoice-chart", {
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                name: "Invoice % to SO",
                                values: values
                            }
                        ]
                    },
                    type: 'bar',
                    height: 300,
                    colors: ['#007bff']
                });
            }
        }, 300);
    }
};
