from erpnext.manufacturing.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):

    def validate_previous_operation_completed_qty(self):
        pass

    def validate_completed_qty(self):
        pass

    def validate_qty(self):
        pass
