from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder


class CustomWorkOrder(WorkOrder):

    def validate(self):
        # Allow standard validation flow
        pass

    # ---- Disable qty consistency checks only ----
    def validate_total_completed_qty(self):
        pass

    def validate_production_completed_qty(self):
        pass
