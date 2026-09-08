from .models import Customer
from ninja import NinjaAPI
from .schemas import CustomerSchemaIn, CustomerSchemaOut
from typing import List


api = NinjaAPI()

@api.post("/customers/", response=CustomerSchemaOut)
def create_task(request, payload: CustomerSchemaIn):
    task = Customer.objects.create(**payload.dict())
    return task

@api.get("/customers/", response=List[CustomerSchemaOut])
def list_tasks(request):
    return Customer.objects.all()

@api.get("/customers/{task_id}/", response=CustomerSchemaOut)
def get_task(request, task_id: int):
    task = Customer.objects.get(id=task_id)
    return task

@api.put("/customers/{task_id}/", response=CustomerSchemaOut)
def update_task(request, task_id: int, payload: CustomerSchemaIn):
    task = Customer.objects.get(id=task_id)
    for attr, value in payload.dict().items():
        setattr(task, attr, value)
    task.save()
    return task

@api.delete("/customers/{task_id}/")
def delete_task(request, task_id: int):
    task = Customer.objects.get(id=task_id)
    task.delete()
    return {"success": True}
