from erpnext.manufacturing.doctype.job_card.job_card import JobCard
from frappe.utils import flt


class CustomJobCard(JobCard):

    def validate(self):
        self.calculate_raw_material_total_qty()

        # Fix wrong status string if user sets it manually
        if self.status == "Complete":
            self.status = "Completed"

    def calculate_raw_material_total_qty(self):
        """
        Calculate total required_qty from Job Card Raw Materials
        """
        total_qty = 0

        for row in self.items:
            total_qty += flt(row.required_qty)

        self.custom_raw_material_total_quantity = total_qty

    # ❌ Disable all standard validations
    def validate_previous_operation_completed_qty(self):
        pass

    def validate_completed_qty(self):
        pass

    def validate_qty(self):
        pass

    def on_submit(self):
        """
        Submit without any manufacturing validations
        """
        self.calculate_raw_material_total_qty()
        self.db_set(
            "custom_raw_material_total_quantity",
            self.custom_raw_material_total_quantity,
            update_modified=False
        )

        self.db_set("status", "Completed", update_modified=False)
