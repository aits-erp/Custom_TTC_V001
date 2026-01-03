import erpnext.manufacturing.doctype.job_card.job_card as job_card
import erpnext.manufacturing.doctype.work_order.work_order as work_order


def apply_manufacturing_patches():
    def dummy(*args, **kwargs):
        return

    # ================= JOB CARD VALIDATIONS =================
    job_card.JobCard.validate_previous_operation_completed_qty = dummy
    job_card.JobCard.validate_completed_qty = dummy
    job_card.JobCard.validate_qty = dummy
    job_card.JobCard.validate_operation_sequence = dummy

    # ================= WORK ORDER VALIDATIONS =================
    work_order.WorkOrder.validate_total_completed_qty = dummy
    work_order.WorkOrder.validate_production_completed_qty = dummy
    work_order.WorkOrder.validate_completed_qty = dummy
    work_order.WorkOrder.validate_qty = dummy
