import time
import unittest
from fastapi.testclient import TestClient
from src.server import app, task_manager

class TestStress(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_stress_and_queue(self):
        # 準備複雜產品組合 (8 種)
        products = [
            {"id": "P1", "w": 100, "h": 200},
            {"id": "P2", "w": 150, "h": 150},
            {"id": "P3", "w": 200, "h": 100},
            {"id": "P4", "w": 80, "h": 80},
            {"id": "P5", "w": 120, "h": 120},
            {"id": "P6", "w": 50, "h": 50},
            {"id": "P7", "w": 60, "h": 90},
            {"id": "P8", "w": 110, "h": 70},
        ]
        
        req = {
            "bin_width": 500,
            "bin_height": 500,
            "products": products,
            "defects": [],
            "timeout": 2.0
        }

        task_ids = []
        for _ in range(3):
            response = self.client.post("/api/optimize", json=req)
            self.assertEqual(response.status_code, 200)
            task_ids.append(response.json()["task_id"])

        time.sleep(0.1) 
        statuses = []
        for t_id in task_ids:
            res = self.client.get(f"/api/tasks/{t_id}")
            statuses.append(res.json()["status"])
            
        print("Initial statuses:", statuses)
        
        all_completed = False
        start_wait = time.time()
        while time.time() - start_wait < 10.0:
            all_completed = True
            for t_id in task_ids:
                res = self.client.get(f"/api/tasks/{t_id}")
                if res.json()["status"] not in ["completed", "failed"]:
                    all_completed = False
            if all_completed:
                break
            time.sleep(0.5)
            
        self.assertTrue(all_completed)
        
        for t_id in task_ids:
            res = self.client.get(f"/api/tasks/{t_id}")
            data = res.json()
            self.assertEqual(data["status"], "completed")
            self.assertIsNotNone(data["best_area"])

if __name__ == "__main__":
    unittest.main()
