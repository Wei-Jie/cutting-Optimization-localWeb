import time
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from functools import lru_cache

@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    @property
    def area(self) -> int:
        return self.w * self.h

    def intersects(self, other: 'Rect') -> bool:
        return not (self.x + self.w <= other.x or
                    other.x + other.w <= self.x or
                    self.y + self.h <= other.y or
                    other.y + other.h <= self.y)

    def contains(self, other: 'Rect') -> bool:
        return (self.x <= other.x and
                self.y <= other.y and
                self.x + self.w >= other.x + other.w and
                self.y + self.h >= other.y + other.h)

class Bin:
    """管理剩餘空間，支援避開瑕疵的空間分割"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # 初始可用空間為整個原物料矩形
        self.free_rects = [Rect(0, 0, width, height)]

    def add_defect(self, defect: Rect):
        """輸入瑕疵點，將重疊的可用空間分割並移除"""
        new_free_rects = []
        for free in self.free_rects:
            if free.intersects(defect):
                # 將空間分割成四個潛在矩形
                # Top
                if defect.y > free.y:
                    new_free_rects.append(Rect(free.x, free.y, free.w, defect.y - free.y))
                # Bottom
                if defect.y + defect.h < free.y + free.h:
                    new_free_rects.append(Rect(free.x, defect.y + defect.h, free.w, (free.y + free.h) - (defect.y + defect.h)))
                # Left
                if defect.x > free.x:
                    new_free_rects.append(Rect(free.x, free.y, defect.x - free.x, free.h))
                # Right
                if defect.x + defect.w < free.x + free.w:
                    new_free_rects.append(Rect(defect.x + defect.w, free.y, (free.x + free.w) - (defect.x + defect.w), free.h))
            else:
                new_free_rects.append(free)
        
        self.free_rects = self._prune_rects(new_free_rects)

    def _prune_rects(self, rects: List[Rect]) -> List[Rect]:
        """移除被其他矩形完全包含的重複空間"""
        unique_rects = []
        for i, r1 in enumerate(rects):
            is_contained = False
            for j, r2 in enumerate(rects):
                if i != j and r2.contains(r1):
                    is_contained = True
                    break
            if not is_contained:
                unique_rects.append(r1)
        return list(set(unique_rects))

@dataclass(frozen=True)
class Product:
    id: str
    w: int
    h: int
    min_qty: int = 1

@dataclass(frozen=True)
class Placement:
    product_id: str
    rect: Rect

def prune_rects(rects: Tuple[Rect, ...]) -> Tuple[Rect, ...]:
    """移除被其他矩形完全包含的重複空間，回傳 tuple 供 hash 使用"""
    unique_rects = []
    for i, r1 in enumerate(rects):
        is_contained = False
        for j, r2 in enumerate(rects):
            if i != j and r2.contains(r1):
                is_contained = True
                break
        if not is_contained:
            unique_rects.append(r1)
    return tuple(sorted(set(unique_rects), key=lambda r: (r.area, r.x, r.y), reverse=True))

class Optimizer:
    def __init__(self, bin_width: int, bin_height: int, timeout: float = 5.0):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.timeout = timeout

    def optimize(self, products: List[Product], defects: List[Rect], allow_infinite: bool = False) -> Tuple[int, List[Placement]]:
        start_time = time.time()
        
        my_bin = Bin(self.bin_width, self.bin_height)
        for d in defects:
            my_bin.add_defect(d)
            
        initial_free = prune_rects(tuple(my_bin.free_rects))
        sorted_prods = tuple(sorted(products, key=lambda p: p.w * p.h, reverse=True))
        
        required_list = []
        for p in sorted_prods:
            required_list.extend([p] * p.min_qty)
        required_tuple = tuple(required_list)
        
        @lru_cache(maxsize=None)
        def dfs(free_rects: Tuple[Rect, ...], remaining_req: Tuple[Product, ...]) -> Tuple[int, int, Tuple[Placement, ...]]:
            if time.time() - start_time > self.timeout:
                return 0, 0, ()
                
            best_req_count = 0
            best_area = 0
            best_placements = ()
            
            if remaining_req:
                prod = remaining_req[0]
                next_req = remaining_req[1:]
                
                # Option 1: Try placing this product FIRST (Greedy depth-first)
                orientations = [(prod.w, prod.h)]
                if prod.w != prod.h:
                    orientations.append((prod.h, prod.w))
                    
                for pw, ph in orientations:
                    for fr in free_rects:
                        if fr.w >= pw and fr.h >= ph:
                            placement_rect = Rect(fr.x, fr.y, pw, ph)
                            current_placement = Placement(prod.id, placement_rect)
                            
                            new_free = []
                            for r in free_rects:
                                if r.intersects(placement_rect):
                                    if placement_rect.y > r.y:
                                        new_free.append(Rect(r.x, r.y, r.w, placement_rect.y - r.y))
                                    if placement_rect.y + placement_rect.h < r.y + r.h:
                                        new_free.append(Rect(r.x, placement_rect.y + placement_rect.h, r.w, (r.y + r.h) - (placement_rect.y + placement_rect.h)))
                                    if placement_rect.x > r.x:
                                        new_free.append(Rect(r.x, r.y, placement_rect.x - r.x, r.h))
                                    if placement_rect.x + pw < r.x + r.w:
                                        new_free.append(Rect(placement_rect.x + pw, r.y, (r.x + r.w) - (placement_rect.x + pw), r.h))
                                else:
                                    new_free.append(r)
                            
                            next_free = prune_rects(tuple(new_free))
                            sub_req, sub_area, sub_placements = dfs(next_free, next_req)
                            
                            if sub_req != -1:
                                total_req = 1 + sub_req
                                total_area = pw * ph + sub_area
                                if (total_req, total_area) > (best_req_count, best_area):
                                    best_req_count = total_req
                                    best_area = total_area
                                    best_placements = (current_placement,) + sub_placements
                                    
                # Option 2: Skip this required product (fallback if it doesn't fit or we have extra time)
                sub_req, sub_area, sub_placements = dfs(free_rects, next_req)
                if sub_req != -1:
                    if (sub_req, sub_area) > (best_req_count, best_area):
                        best_req_count = sub_req
                        best_area = sub_area
                        best_placements = sub_placements
                        
                return best_req_count, best_area, best_placements
                
            else:
                if not allow_infinite:
                    return 0, 0, ()
                    
                best_area = 0
                best_placements = ()
                
                for i, prod in enumerate(sorted_prods):
                    orientations = [(prod.w, prod.h)]
                    if prod.w != prod.h:
                        orientations.append((prod.h, prod.w))
                        
                    for pw, ph in orientations:
                        for fr in free_rects:
                            if fr.w >= pw and fr.h >= ph:
                                placement_rect = Rect(fr.x, fr.y, pw, ph)
                                current_placement = Placement(prod.id, placement_rect)
                                
                                new_free = []
                                for r in free_rects:
                                    if r.intersects(placement_rect):
                                        if placement_rect.y > r.y:
                                            new_free.append(Rect(r.x, r.y, r.w, placement_rect.y - r.y))
                                        if placement_rect.y + placement_rect.h < r.y + r.h:
                                            new_free.append(Rect(r.x, placement_rect.y + placement_rect.h, r.w, (r.y + r.h) - (placement_rect.y + placement_rect.h)))
                                        if placement_rect.x > r.x:
                                            new_free.append(Rect(r.x, r.y, placement_rect.x - r.x, r.h))
                                        if placement_rect.x + pw < r.x + r.w:
                                            new_free.append(Rect(placement_rect.x + pw, r.y, (r.x + r.w) - (placement_rect.x + pw), r.h))
                                    else:
                                        new_free.append(r)
                                
                                next_free = prune_rects(tuple(new_free))
                                sub_req, sub_area, sub_placements = dfs(next_free, ())
                                
                                if sub_req != -1:
                                    total_area = pw * ph + sub_area
                                    if total_area > best_area:
                                        best_area = total_area
                                        best_placements = (current_placement,) + sub_placements
                                        
                return 0, best_area, best_placements

        req_placed, best_area, best_placements = dfs(initial_free, required_tuple)
        return best_area, list(best_placements)
