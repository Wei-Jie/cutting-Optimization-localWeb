import asyncio
import uuid
import time
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from src.engine import Optimizer, Product, Rect

app = FastAPI(title="Cutting Optimizer API")

# --- Models ---
class ProductItem(BaseModel):
    id: str
    w: int
    h: int
    min_qty: int = 1

class DefectItem(BaseModel):
    x: int
    y: int
    w: int
    h: int

class OptimizeRequest(BaseModel):
    bin_width: int
    bin_height: int
    products: List[ProductItem]
    defects: List[DefectItem] = []
    timeout: float = 5.0
    allow_infinite: bool = False

class PlacementItem(BaseModel):
    product_id: str
    x: int
    y: int
    w: int
    h: int

class TaskResult(BaseModel):
    status: str  # "pending", "processing", "completed", "failed"
    best_area: Optional[int] = None
    placements: Optional[List[PlacementItem]] = None
    error: Optional[str] = None
    created_at: float
    completed_at: Optional[float] = None

# --- Task Manager ---
class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, TaskResult] = {}
        # 單一 Worker 保證循序執行，避免 CPU 資源耗盡
        self.executor = ThreadPoolExecutor(max_workers=1)

    def submit_task(self, req: OptimizeRequest) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = TaskResult(status="pending", created_at=time.time())
        # 在背景執行
        self.executor.submit(self._run_task, task_id, req)
        return task_id

    def get_task(self, task_id: str) -> Optional[TaskResult]:
        return self.tasks.get(task_id)

    def _run_task(self, task_id: str, req: OptimizeRequest):
        task = self.tasks[task_id]
        task.status = "processing"
        
        try:
            opt = Optimizer(req.bin_width, req.bin_height, timeout=req.timeout)
            products = [Product(p.id, p.w, p.h, p.min_qty) for p in req.products]
            defects = [Rect(d.x, d.y, d.w, d.h) for d in req.defects]
            
            best_area, placements = opt.optimize(products, defects, allow_infinite=req.allow_infinite)
            
            task.best_area = best_area
            task.placements = [
                PlacementItem(
                    product_id=p.product_id,
                    x=p.rect.x,
                    y=p.rect.y,
                    w=p.rect.w,
                    h=p.rect.h
                ) for p in placements
            ]
            task.status = "completed"
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
        finally:
            task.completed_at = time.time()

task_manager = TaskManager()

# --- API Endpoints ---
@app.post("/api/optimize")
def submit_optimization(req: OptimizeRequest):
    task_id = task_manager.submit_task(req)
    return {"task_id": task_id}

@app.get("/api/tasks/{task_id}")
def get_task_status(task_id: str):
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
