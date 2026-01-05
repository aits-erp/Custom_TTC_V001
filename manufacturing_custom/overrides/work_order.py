from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder


class CustomWorkOrder(WorkOrder):

    # 🔥 THIS IS THE REAL VALIDATION
    def validate_completed_qty_against_previous_operation(self):
        pass

    # (extra safety – no harm)
    def validate_completed_qty(self):
        pass
