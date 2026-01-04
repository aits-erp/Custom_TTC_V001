import frappe
from frappe.utils import flt
from erpnext.manufacturing.doctype.job_card.job_card import JobCard
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry


class CustomJobCard(JobCard):

    # --------------------------------------------------
    # VALIDATE
    # --------------------------------------------------
    def validate(self):
        self.calculate_raw_material_total_qty()
        if self.status == "Complete":
            self.status = "Completed"

    # --------------------------------------------------
    # RAW MATERIAL TOTAL (PER JOB CARD)
    # --------------------------------------------------
    def calculate_raw_material_total_qty(self):
        self.custom_raw_material_total_quantity = sum(
            flt(row.required_qty) for row in (self.items or [])
        )

    # --------------------------------------------------
    # DISABLE ERPNext VALIDATIONS
    # --------------------------------------------------
    def validate_previous_operation_completed_qty(self): pass
    def validate_completed_qty(self): pass
    def validate_qty(self): pass

    # --------------------------------------------------
    # ON SUBMIT
    # --------------------------------------------------
    def on_submit(self):
        self.db_set("status", "Completed", update_modified=False)

        self.calculate_raw_material_total_qty()
        self.db_set(
            "custom_raw_material_total_quantity",
            self.custom_raw_material_total_quantity,
            update_modified=False
        )

        # 🔥 FIXED cumulative logic
        self.update_total_stage_completed_qty()

        self.auto_update_work_order_stock()
        self.update_work_order_status()

    # --------------------------------------------------
    # 🔥 FIXED CUMULATIVE CALCULATION
    # --------------------------------------------------
    def update_total_stage_completed_qty(self):
        """
        Cumulative RM Qty =
        SUM(previous submitted Job Cards) + current Job Card RM
        """

        if not self.work_order or not self.sequence_id:
            return

        # Sum only PREVIOUS job cards
        previous_total = frappe.db.sql(
            """
            SELECT
                COALESCE(SUM(custom_raw_material_total_quantity), 0)
            FROM
                `tabJob Card`
            WHERE
                work_order = %s
                AND docstatus = 1
                AND sequence_id < %s
            """,
            (self.work_order, self.sequence_id),
        )[0][0]

        final_total = flt(previous_total) + flt(self.custom_raw_material_total_quantity)

        self.db_set(
            "custom_total_stage_completed_qty",
            final_total,
            update_modified=False
        )

    # --------------------------------------------------
    # STOCK ENTRY (LAST OPERATION ONLY)
    # --------------------------------------------------
    def auto_update_work_order_stock(self):

        if not self.work_order or self.get("custom_auto_processed"):
            return

        wo = frappe.get_doc("Work Order", self.work_order)

        if not wo.operations or self.operation != wo.operations[-1].operation:
            return

        qty = flt(self.total_completed_qty)
        if qty <= 0:
            return

        if flt(wo.material_transferred_for_manufacturing) == 0:
            se_mt = make_stock_entry(
                work_order=wo.name,
                purpose="Material Transfer for Manufacturing",
                qty=qty
            )
            se_mt.set_missing_values()
            se_mt.insert(ignore_permissions=True)
            se_mt.submit()

        se_fg = make_stock_entry(
            work_order=wo.name,
            purpose="Manufacture",
            qty=qty
        )
        se_fg.consume_materials = 1
        se_fg.fg_completed_qty = qty
        se_fg.set_missing_values()
        se_fg.insert(ignore_permissions=True)
        se_fg.submit()

        self.db_set("custom_auto_processed", 1, update_modified=False)

    # --------------------------------------------------
    # WORK ORDER STATUS
    # --------------------------------------------------
    def update_work_order_status(self):
        wo = frappe.get_doc("Work Order", self.work_order)

        all_completed = all(flt(op.completed_qty) > 0 for op in wo.operations)

        wo.db_set(
            "status",
            "Completed" if all_completed else "In Progress",
            update_modified=False
        )
