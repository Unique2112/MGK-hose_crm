from import_export import resources
from .models import HoseRecord
class HoseRecordResource(resources.ModelResource):
    class Meta:
        model = HoseRecord
        # እዚህ ጋር 'colored_status' መኖር የለበትም
        fields = (
            'id', 'date', 'company_name', 'tin_number', 'contact_phone',
            'machine_make', 'machine_model', 'psi', 'product_description',
            'part_number', 'hose_designation', 'hose_length', 'hose_size',
            'coupling_a', 'coupling_b', 'unit_price', 'demand_cycle',
            'status', 'lost_reason', 'remark'
        )
        export_order = fields