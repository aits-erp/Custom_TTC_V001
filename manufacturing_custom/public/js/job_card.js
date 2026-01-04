frappe.ui.form.on("Job Card", {
	refresh(frm) {
		update_raw_material_total(frm);

		// 🔥 Delay override so ERPNext cannot re-override it
		setTimeout(() => {
			override_complete_job(frm);
		}, 300);
	},

	validate(frm) {
		update_raw_material_total(frm);
	}
});

// 🔥 RAW MATERIAL TOTAL
function update_raw_material_total(frm) {
	let total = 0;
	(frm.doc.items || []).forEach(row => {
		total += flt(row.required_qty);
	});
	frm.set_value("custom_raw_material_total_quantity", total);
}

// 🔥 FORCE COMPLETE JOB FOR ALL STAGES
function override_complete_job(frm) {

	// REMOVE ERPNext BUTTON
	frm.page.clear_primary_action();

	// APPLY FOR ALL DRAFT JOB CARDS
	if (frm.doc.docstatus !== 0) return;

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

				// 🔥 SAVE ONLY → NO OPERATION VALIDATION
				frm.save();
			},
			__("Enter Completed Quantity"),
			__("Complete")
		);
	});
}
