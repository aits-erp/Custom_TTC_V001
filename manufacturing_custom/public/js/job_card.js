frappe.ui.form.on("Job Card", {
	refresh(frm) {
		update_raw_material_total(frm);

		setTimeout(() => {
			override_complete_job(frm);
		}, 300);
	},

	validate(frm) {
		update_raw_material_total(frm);
	}
});

// ------------------------------
// RAW MATERIAL TOTAL
// ------------------------------
function update_raw_material_total(frm) {
	let total = 0;
	(frm.doc.items || []).forEach(row => {
		total += flt(row.required_qty);
	});
	frm.set_value("custom_raw_material_total_quantity", total);
}

// ------------------------------
// COMPLETE JOB (AUTO SUBMIT)
// ------------------------------
function override_complete_job(frm) {

	if (frm.doc.docstatus !== 0) return;

	frm.page.clear_primary_action();

	frm.page.set_primary_action(__("Complete Job"), () => {

		update_raw_material_total(frm);

		let total_qty = flt(frm.doc.custom_raw_material_total_quantity);

		frappe.prompt(
			[
				{
					fieldname: "completed_qty",
					fieldtype: "Float",
					label: __("Completed Quantity"),
					reqd: 1,
					default: total_qty
				}
			],
			(values) => {

				frm.set_value("total_completed_qty", values.completed_qty);
				frm.set_value("status", "Completed");

				// 🔥 THIS IS THE KEY CHANGE
				frm.submit();   // ✅ triggers on_submit()
			},
			__("Enter Completed Quantity"),
			__("Complete")
		);
	});
}
