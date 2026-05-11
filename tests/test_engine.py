import unittest
from src.engine import Rect, Bin, Product, Optimizer

class TestEngine(unittest.TestCase):
    def test_rect_intersects(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(10, 10, 10, 10)
        self.assertTrue(r1.intersects(r2))
        self.assertFalse(r1.intersects(r3))

    def test_bin_add_defect(self):
        b = Bin(100, 100)
        b.add_defect(Rect(40, 40, 20, 20))
        # 瑕疵在中間，分割後應該有多個 free_rects，且都不會與瑕疵重疊
        defect = Rect(40, 40, 20, 20)
        for r in b.free_rects:
            self.assertFalse(r.intersects(defect))

    def test_optimizer_basic(self):
        opt = Optimizer(100, 100, timeout=2.0)
        products = [Product("p1", 30, 30), Product("p2", 40, 40)]
        defects = [Rect(40, 40, 20, 20)]
        
        area, placements = opt.optimize(products, defects)
        
        self.assertEqual(len(placements), 2)
        
        # 檢查所有的 placements 都在 Bin 內，且不與 defects 重疊，且彼此不重疊
        for p in placements:
            self.assertTrue(p.rect.x >= 0 and p.rect.y >= 0)
            self.assertTrue(p.rect.x + p.rect.w <= 100)
            self.assertTrue(p.rect.y + p.rect.h <= 100)
            for d in defects:
                self.assertFalse(p.rect.intersects(d))
                
        self.assertFalse(placements[0].rect.intersects(placements[1].rect))

if __name__ == "__main__":
    unittest.main()
