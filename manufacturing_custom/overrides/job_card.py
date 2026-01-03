from erpnext.manufacturing.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):

    def validate(self):
        # Fix wrong status string if user sets it
        if self.status == "Complete":
            self.status = "Completed"

    # ❌ Disable ALL quantity validations
    def validate_previous_operation_completed_qty(self):
        pass

    def validate_completed_qty(self):
        pass

    def validate_qty(self):
        pass

    # ❌ Disable final submit validation
    def on_submit(self):
        """
        Completely override standard on_submit
        and skip:
        - total_completed_qty == for_quantity
        - previous operation checks
        """
        # Just set status safely
        self.status = "Completed"
        self.db_set("status", "Completed", update_modified=False)
