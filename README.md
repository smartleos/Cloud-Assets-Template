# ☁️ Cloud-Assets Template

<div align="center">

![Optimize Images to WebP](https://github.com/eric861129/Cloud-Assets-Template/actions/workflows/optimize-images.yml/badge.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/eric861129/Cloud-Assets-Template)
![GitHub last commit](https://img.shields.io/github/last-commit/eric861129/Cloud-Assets-Template)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**🚀 一鍵擁有個人自動化圖床！**
**支援 WebP 自動優化、jsDelivr CDN 加速、自動生成美觀圖庫頁面。**

[查看 Demo 演示](https://eric861129.github.io/Cloud-Assets-Template/) · [報告問題](https://github.com/eric861129/Cloud-Assets-Template/issues) · [提交建議](https://github.com/eric861129/Cloud-Assets-Template/pulls)

</div>

---

## 📸 介面預覽

### 自動生成的圖庫頁面
![Cloud-Assets-Template](https://github.com/user-attachments/assets/28ed5b5f-09a0-4e9d-b829-ebbda88d3010)


*圖：自動生成的靜態網頁，支援樹狀目錄與一鍵複製*

## ✨ 特色功能

- 🛠️ **開箱即用**：Fork 後即可使用，無需複雜設定。
- 🖼️ **自動圖片優化**：上傳 JPG/PNG 自動轉為 WebP 並刪除原圖，節省空間。
- 🚀 **CDN 加速**：整合 [jsDelivr](https://www.jsdelivr.com/)，全球高速存取。
- 📂 **自動圖庫索引**：自動生成 `index.html`，以資料夾結構展示圖片。
- 📋 **一鍵複製**：網頁版提供 CDN 連結與 Markdown 語法的一鍵複製功能。
- 🆓 **完全免費**：利用 GitHub Repo 與 GitHub Pages 託管。

## 🚀 快速開始 (How to Use)

### 1. 建立您的圖床
點擊右上角的 **[Use this template](https://github.com/new?template_name=Cloud-Assets-Template&template_owner=eric861129)** 按鈕 (或 Fork 本專案)，建立一個新的 Repository（例如命名為 `my-assets`）。

### 2. 開啟 GitHub Actions
進入您新建立的 Repo，點選上方的 **Actions** 頁籤，如果看到警告，請點擊 **"I understand my workflows, go ahead and enable them"**。

### 3. 設定 GitHub Pages
1. 進入 **Settings** > **Pages**。
2. 在 **Build and deployment** > **Source** 選擇 **Deploy from a branch**。
3. **Branch** 選擇 `main` (或 `master`)，資料夾選擇 `/ (root)`。
4. 按下 **Save**。

### 4. 上傳圖片
您可以直接在 GitHub 網頁上操作，或 Clone 到本地端操作：
- 將圖片 (JPG, PNG) 放入 `Share/`、`Blog/` 或任何您建立的資料夾中。
- **Push** 提交變更。

### 5. 等待自動處理
- GitHub Actions 會自動觸發 `Optimize Images to WebP` 流程。
- 圖片會被轉為 `.webp`。
- `index.html` 會被更新。

### 6. 使用圖片
等待 GitHub Pages 部署完成（約 1-2 分鐘）後，訪問：
`https://<您的帳號>.github.io/<Repo名稱>/`

您將看到所有圖片的預覽，並可直接複製連結。

---

## 🔗 連結格式範例

您的圖片連結將會是：
`https://cdn.jsdelivr.net/gh/<您的帳號>/<Repo名稱>@main/<圖片路徑>.webp`

例如：
`https://cdn.jsdelivr.net/gh/eric861129/my-assets@main/Share/example.webp`

## 📂 目錄結構說明

- `Blog/`、`Share/`：預設的分類資料夾，您可以自由新增、刪除或重新命名資料夾。
- `optimize.py`：核心自動化腳本 (Python)。
- `index.html`：自動生成的圖庫首頁 (請勿手動大量修改，因為會被腳本覆蓋)。
- `.github/workflows/`：自動化流程設定檔。

## 🛠️ 技術細節

- **Core**: Python (Pillow) 用於圖片處理與 HTML 生成。
- **Automation**: GitHub Actions 監聽 Push 事件。
- **Hosting**: GitHub Pages 託管靜態頁面。
- **CDN**: jsDelivr 提供內容傳遞網路。

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request 來改進這個模板！詳情請見 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 授權

本專案採用 [MIT License](LICENSE)。
