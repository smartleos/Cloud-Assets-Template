import os
from PIL import Image

REPO_OWNER = "eric861129"
REPO_NAME = "Cloud-Assets"

# 嘗試從 GitHub Actions 環境變數獲取 owner/repo
github_repository = os.getenv("GITHUB_REPOSITORY")
if github_repository:
    parts = github_repository.split("/")
    if len(parts) == 2:
        REPO_OWNER = parts[0]
        REPO_NAME = parts[1]

BRANCH = "main"
CDN_BASE_URL = f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}@{BRANCH}"

def optimize_images(directory=".", quality=80):
    """
    遞迴掃描目錄，將圖片轉為 WebP 並刪除原圖。
    """
    for root, dirs, files in os.walk(directory):
        if ".git" in root:
            continue
            
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                filepath = os.path.join(root, filename)
                base = os.path.splitext(filename)[0]
                output_path = os.path.join(root, f"{base}.webp")
                
                try:
                    # 轉檔
                    with Image.open(filepath) as img:
                        img.save(output_path, "WEBP", quality=quality, method=6)
                    print(f"優化成功: {filepath} -> {output_path}")
                    
                    # 刪除原圖
                    os.remove(filepath)
                    print(f"已刪除原圖: {filepath}")
                    
                except Exception as e:
                    print(f"處理 {filepath} 時出錯: {e}")

def generate_index_html(gallery_data):
    """
    根據圖片資料生成一個美觀的 index.html 靜態頁面 (樹狀結構、預設折疊)。
    """
    print("正在生成 index.html ...")
    
    # 1. 建構樹狀結構
    tree = {'files': [], 'subdirs': {}}
    
    for folder_path, files in gallery_data.items():
        if folder_path == "Root (根目錄)":
            current = tree
            current['files'] = files
        else:
            parts = folder_path.split("/")
            current = tree
            for part in parts:
                if part not in current['subdirs']:
                    current['subdirs'][part] = {'files': [], 'subdirs': {}}
                current = current['subdirs'][part]
            current['files'] = files

    # 2. 遞迴計算每個節點(含子目錄)的圖片總數
    def count_total_images(node):
        count = len(node['files'])
        for sub in node['subdirs'].values():
            count += count_total_images(sub)
        return count

    # 3. 遞迴生成 HTML
    def render_tree(node, current_path=""):
        html_parts = []
        
        # 先顯示子目錄 (Folders)，按名稱排序
        for dirname in sorted(node['subdirs'].keys()):
            sub_node = node['subdirs'][dirname]
            new_path = f"{current_path}/{dirname}" if current_path else dirname
            
            inner_content = render_tree(sub_node, new_path)
            total_imgs = count_total_images(sub_node)
            
            # 只有當該目錄或子目錄有圖片時才顯示
            if total_imgs > 0:
                folder_html = f"""
                <details class="folder-section">
                    <summary>📁 {dirname} <span class="badge rounded-pill bg-secondary ms-1">{total_imgs}</span></summary>
                    <div class="nested-content">
                        {inner_content}
                    </div>
                </details>
                """
                html_parts.append(folder_html)
            
        # 再顯示當前目錄的圖片 (Files)
        if node['files']:
            cards = []
            for filename in node['files']:
                if current_path:
                    img_path = f"{current_path}/{filename}"
                else:
                    img_path = filename
                
                full_url = f"{CDN_BASE_URL}/{img_path}"
                md_code = f"![{filename}]({full_url})"
                
                card_html = f"""
                <div class="col-md-3 col-sm-6 col-12">
                    <div class="card h-100 shadow-sm">
                        <div class="img-container" onclick="window.open('{full_url}')">
                             <img src="{full_url}" class="card-img-top img-preview" alt="{filename}" loading="lazy">
                        </div>
                        <div class="card-body p-2">
                            <p class="card-text text-truncate small mb-2" title="{filename}">{filename}</p>
                            <div class="d-grid gap-1">
                                <button class="btn btn-xs btn-outline-primary copy-btn" onclick="copyToClipboard('{full_url}', this)">複製連結</button>
                                <button class="btn btn-xs btn-outline-secondary copy-btn" onclick="copyToClipboard('{md_code}', this)">複製 MD</button>
                            </div>
                        </div>
                    </div>
                </div>
                """
                cards.append(card_html)
            
            images_grid = f"""
            <div class="row g-2 mt-1 mb-3">
                {''.join(cards)}
            </div>
            """
            html_parts.append(images_grid)
            
        return "".join(html_parts)

    content_html = render_tree(tree, "")

    html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud-Assets 圖庫</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; padding-top: 30px; padding-bottom: 50px; font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
        
        /* 圖片卡片樣式 */
        .card { border: none; transition: transform 0.2s; }
        .card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important; }
        .img-container { height: 150px; overflow: hidden; background: #eee; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .img-preview { max-height: 100%; max-width: 100%; object-fit: contain; }
        .btn-xs { padding: 0.1rem 0.4rem; font-size: 0.75rem; }
        
        /* 樹狀結構與折疊樣式 */
        .folder-section { margin-bottom: 8px; }
        .nested-content { 
            margin-left: 18px; 
            padding-left: 12px; 
            border-left: 2px solid #e0e0e0; /* 樹狀連接線 */
            margin-top: 5px;
        }
        
        details > summary { 
            list-style: none; 
            cursor: pointer; 
            padding: 8px 12px; 
            background: #fff; 
            border-radius: 6px; 
            border: 1px solid #dee2e6;
            font-weight: 600;
            display: inline-block;
            min-width: 250px;
            user-select: none;
            position: relative;
        }
        details > summary:hover { background-color: #f1f3f5; border-color: #ced4da; }
        
        /* 自定義箭頭 */
        details > summary::marker { display: none; }
        details > summary::before {
            content: '▶';
            display: inline-block;
            margin-right: 8px;
            font-size: 0.75rem;
            color: #6c757d;
            transition: transform 0.2s ease;
        }
        details[open] > summary::before { transform: rotate(90deg); }
        details[open] > summary { margin-bottom: 5px; background-color: #e9ecef; border-color: #ced4da; }

        h1 { font-size: 1.8rem; color: #343a40; }
    </style>
</head>
<body>
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
            <h1 class="m-0">📂 Cloud-Assets</h1>
            <div>
                 <button class="btn btn-sm btn-outline-secondary me-2" onclick="toggleAll(true)">全部展開</button>
                 <button class="btn btn-sm btn-outline-secondary me-2" onclick="toggleAll(false)">全部折疊</button>
                 <a href="https://github.com/eric861129/Cloud-Assets" class="btn btn-sm btn-dark" target="_blank">GitHub</a>
            </div>
        </div>

        <div id="gallery">
            {content}
        </div>
        
        <footer class="mt-5 text-center text-muted small">
            Generated by Cloud-Assets | <a href="#" onclick="window.scrollTo(0,0); return false;">Top</a>
        </footer>
    </div>

    <script>
        function copyToClipboard(text, btn) {
            navigator.clipboard.writeText(text).then(() => {
                const originalText = btn.innerText;
                const originalClass = btn.className;
                
                btn.innerText = "已複製";
                btn.className = "btn btn-xs btn-success copy-btn";
                
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.className = originalClass;
                }, 1500);
            });
        }
        
        function toggleAll(expand) {
            document.querySelectorAll('details').forEach(d => {
                if(expand) d.setAttribute('open', '');
                else d.removeAttribute('open');
            });
        }
    </script>
</body>
</html>
"""
    
    final_html = html_template.replace("{content}", "".join(content_html))
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print("index.html 生成完畢。")

if __name__ == "__main__":
    optimize_images()
    # 重新掃描以獲取最新的 WebP 資訊
    current_gallery_data = {}
    for root, dirs, files in os.walk("."):
        if ".git" in root: continue
        webp_files = [f for f in files if f.lower().endswith(".webp")]
        if webp_files:
            rel_dir = os.path.relpath(root, ".").replace("\\", "/")
            if rel_dir == ".": rel_dir = "Root (根目錄)"
            current_gallery_data[rel_dir] = sorted(webp_files)
            
    generate_index_html(current_gallery_data)
