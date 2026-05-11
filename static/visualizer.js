const canvas = document.getElementById('cuttingCanvas');
const ctx = canvas.getContext('2d');

let binW = 500;
let binH = 500;
let products = [
    { id: 'P1', w: 100, h: 200, min_qty: 1 },
    { id: 'P2', w: 150, h: 150, min_qty: 1 },
    { id: 'P3', w: 200, h: 100, min_qty: 1 },
    { id: 'P4', w: 80, h: 80, min_qty: 1 },
    { id: 'P5', w: 120, h: 120, min_qty: 1 }
];
let defects = [];
let placements = [];

let isDrawing = false;
let startX = 0;
let startY = 0;
let currentDefect = null;

const colors = ['#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#06b6d4', '#3b82f6'];
const getProductColor = (id) => {
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
        hash = id.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
};

function init() {
    document.getElementById('updateBinBtn').addEventListener('click', updateBin);
    document.getElementById('addProdBtn').addEventListener('click', addProduct);
    document.getElementById('optimizeBtn').addEventListener('click', startOptimization);
    document.getElementById('exportBtn').addEventListener('click', exportCSV);
    
    canvas.addEventListener('mousedown', startDrawDefect);
    canvas.addEventListener('mousemove', drawDefect);
    canvas.addEventListener('mouseup', endDrawDefect);
    
    renderProductList();
    renderDefectList();
    updateCanvas();
}

function updateBin() {
    binW = parseInt(document.getElementById('binW').value);
    binH = parseInt(document.getElementById('binH').value);
    placements = [];
    defects = [];
    renderDefectList();
    updateCanvas();
}

function updateCanvas() {
    canvas.width = binW;
    canvas.height = binH;
    ctx.clearRect(0, 0, binW, binH);
    
    // Draw grid
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    for (let x = 0; x <= binW; x += 50) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, binH); ctx.stroke();
    }
    for (let y = 0; y <= binH; y += 50) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(binW, y); ctx.stroke();
    }
    
    // Draw defects
    ctx.fillStyle = 'rgba(239, 68, 68, 0.7)';
    defects.forEach(d => {
        ctx.fillRect(d.x, d.y, d.w, d.h);
        ctx.strokeRect(d.x, d.y, d.w, d.h);
    });
    
    // Draw placements
    placements.forEach(p => {
        ctx.fillStyle = getProductColor(p.product_id);
        ctx.globalAlpha = 0.85;
        ctx.fillRect(p.x, p.y, p.w, p.h);
        ctx.globalAlpha = 1.0;
        
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.strokeRect(p.x, p.y, p.w, p.h);
        
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 14px Inter';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(p.product_id, p.x + p.w/2, p.y + p.h/2);
    });
    
    if (currentDefect) {
        ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
        ctx.fillRect(currentDefect.x, currentDefect.y, currentDefect.w, currentDefect.h);
        ctx.strokeStyle = '#ef4444';
        ctx.strokeRect(currentDefect.x, currentDefect.y, currentDefect.w, currentDefect.h);
    }
    
    if (placements.length > 0) {
        document.getElementById('exportBtn').style.display = 'block';
        const usedArea = placements.reduce((acc, p) => acc + p.w * p.h, 0);
        const totalArea = binW * binH;
        const util = (usedArea / totalArea * 100).toFixed(2);
        document.getElementById('utilizationLabel').innerText = `${util}%`;
    } else {
        document.getElementById('exportBtn').style.display = 'none';
        document.getElementById('utilizationLabel').innerText = `0%`;
    }
}

function startDrawDefect(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    startX = (e.clientX - rect.left) * scaleX;
    startY = (e.clientY - rect.top) * scaleY;
    isDrawing = true;
    currentDefect = { x: startX, y: startY, w: 0, h: 0 };
}

function drawDefect(e) {
    if (!isDrawing) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const currX = (e.clientX - rect.left) * scaleX;
    const currY = (e.clientY - rect.top) * scaleY;
    
    currentDefect.x = Math.min(startX, currX);
    currentDefect.y = Math.min(startY, currY);
    currentDefect.w = Math.abs(currX - startX);
    currentDefect.h = Math.abs(currY - startY);
    
    updateCanvas();
}

function endDrawDefect() {
    if (!isDrawing) return;
    isDrawing = false;
    if (currentDefect.w > 5 && currentDefect.h > 5) {
        defects.push({
            x: Math.round(currentDefect.x),
            y: Math.round(currentDefect.y),
            w: Math.round(currentDefect.w),
            h: Math.round(currentDefect.h)
        });
        renderDefectList();
    }
    currentDefect = null;
    placements = [];
    updateCanvas();
}

function renderProductList() {
    const list = document.getElementById('productList');
    list.innerHTML = '';
    products.forEach((p, index) => {
        const div = document.createElement('div');
        div.className = 'item-row';
        div.innerHTML = `
            <span>${p.id} (${p.w}x${p.h})</span>
            <div style="display: flex; align-items: center; gap: 8px;">
                <button class="btn-qty" onclick="updateProductQty(${index}, -1)">-</button>
                <span style="min-width: 20px; text-align: center;">${p.min_qty}</span>
                <button class="btn-qty" onclick="updateProductQty(${index}, 1)">+</button>
                <span class="item-del" onclick="removeProduct(${index})" style="margin-left: 10px;">✕</span>
            </div>
        `;
        list.appendChild(div);
    });
}

window.updateProductQty = (index, delta) => {
    products[index].min_qty += delta;
    if (products[index].min_qty < 1) products[index].min_qty = 1;
    placements = [];
    renderProductList();
    updateCanvas();
};

function renderDefectList() {
    const list = document.getElementById('defectList');
    list.innerHTML = '';
    defects.forEach((d, index) => {
        const div = document.createElement('div');
        div.className = 'item-row';
        div.innerHTML = `
            <span>Defect (${d.x},${d.y}) ${d.w}x${d.h}</span>
            <span class="item-del" onclick="removeDefect(${index})">✕</span>
        `;
        list.appendChild(div);
    });
}

window.removeProduct = (index) => {
    products.splice(index, 1);
    placements = [];
    renderProductList();
    updateCanvas();
};

window.removeDefect = (index) => {
    defects.splice(index, 1);
    placements = [];
    renderDefectList();
    updateCanvas();
};

function addProduct() {
    const id = document.getElementById('newProdId').value;
    const w = parseInt(document.getElementById('newProdW').value);
    const h = parseInt(document.getElementById('newProdH').value);
    const min_qty = parseInt(document.getElementById('newProdQty').value) || 1;
    
    if (id && w && h) {
        products.push({ id, w, h, min_qty });
        document.getElementById('newProdId').value = '';
        document.getElementById('newProdW').value = '';
        document.getElementById('newProdH').value = '';
        document.getElementById('newProdQty').value = '1';
        placements = [];
        renderProductList();
        updateCanvas();
    }
}

async function startOptimization() {
    const statusMsg = document.getElementById('statusMsg');
    statusMsg.className = 'status-message pending';
    statusMsg.innerText = '提交中...';
    
    const allowInfinite = document.getElementById('allowInfinite').checked;
    const timeoutSec = parseFloat(document.getElementById('timeoutSec').value) || 5.0;
    
    const req = {
        bin_width: binW,
        bin_height: binH,
        products: products,
        defects: defects,
        timeout: timeoutSec,
        allow_infinite: allowInfinite
    };
    
    try {
        const res = await fetch('/api/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req)
        });
        const data = await res.json();
        
        pollStatus(data.task_id);
    } catch (e) {
        statusMsg.className = 'status-message failed';
        statusMsg.innerText = '提交失敗: ' + e;
    }
}

async function pollStatus(taskId) {
    const statusMsg = document.getElementById('statusMsg');
    try {
        const res = await fetch(`/api/tasks/${taskId}`);
        const task = await res.json();
        
        if (task.status === 'pending' || task.status === 'processing') {
            statusMsg.className = `status-message ${task.status}`;
            statusMsg.innerText = task.status === 'pending' ? '等待排隊中...' : '計算中...';
            setTimeout(() => pollStatus(taskId), 500);
        } else if (task.status === 'completed') {
            statusMsg.className = 'status-message completed';
            statusMsg.innerText = '計算完成！';
            placements = task.placements || [];
            updateCanvas();
        } else {
            statusMsg.className = 'status-message failed';
            statusMsg.innerText = '計算失敗: ' + task.error;
        }
    } catch (e) {
        statusMsg.className = 'status-message failed';
        statusMsg.innerText = '查詢失敗: ' + e;
    }
}

function exportCSV() {
    if (!placements || placements.length === 0) return;
    
    // 加入 BOM 以支援 Excel 正常顯示 UTF-8 中文
    let csvContent = "\uFEFF"; 
    csvContent += "產品名稱 (Product ID),寬度 (Width),長度 (Height),X座標,Y座標\n";
    
    placements.forEach(p => {
        csvContent += `${p.product_id},${p.w},${p.h},${p.x},${p.y}\n`;
    });
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "cutting_result.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

init();
