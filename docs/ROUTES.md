# 路由與頁面設計 (API Design) - 任務管理系統

## 1. 路由總覽表格

下方表格總結了操作任務管理系統的各項行為與對應的 URL、方法與負責的樣板檔案：

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| ---- | --------- | -------- | -------- | ---- |
| 任務列表(首頁) | GET | `/` | `templates/index.html` | 讀取所有任務並呈現於首頁視圖 |
| 新增任務 | POST | `/tasks` | — | 接收輸入表單，將新任務寫入 DB，完成後重導向至 `/` |
| 編輯任務頁面 | GET | `/tasks/<id>/edit` | `templates/edit.html` | 讀取並顯示要編輯的單筆任務內容，呈現編輯專用表單 |
| 更新任務 | POST | `/tasks/<id>/update` | — | 接收編輯後的新表單資料，更新 DB，完成後重新導向至 `/` |
| 切換任務狀態 | POST | `/tasks/<id>/toggle` | — | 單純更改資料邏輯：反轉任務目前的待辦/完成狀態，結束後重導向至 `/` |
| 刪除任務 | POST | `/tasks/<id>/delete` | — | 刪除對應的 `<id>` 任務，結束後重新導向至 `/` |

## 2. 每個路由的詳細說明

### 任務列表 - `GET /`
- **輸入**：無
- **處理邏輯**：呼叫 `TaskModel.get_all()` 的方法調出所有的任務清單。
- **輸出**：透過 Flask 方法，攜帶查詢到的列表渲染並回傳 `index.html` 畫面。
- **錯誤處理**：若連線發生問題，應讓 Flask 跳出並傳回 `500 Internal Server Error` 環境頁。

### 新增任務 - `POST /tasks`
- **輸入**：HTML 原生 `<form>` 送出的物件表單，需含有 `title` 資訊。
- **處理邏輯**：檢查收到的 `title` 是否有值並濾除空白；確保不是空白字串後呼叫 `TaskModel.create(title)`。
- **輸出**：透過 `redirect` 重導向回 `/` 首頁。
- **錯誤處理**：如果驗證發現沒帶 `title` 或為空值，則視為 `400 Bad Request` 或是帶入錯誤訊息(flash message)回傳。

### 編輯任務頁面 - `GET /tasks/<id>/edit`
- **輸入**：網址列中的任務識別參數： `<id>`
- **處理邏輯**：透過 `TaskModel.get_by_id(id)` 將原任務從 DB 中調閱出。
- **輸出**：帶著取出的對應任務內容去渲染 `edit.html`，讓 `<input>` 將標題代入預設值中。
- **錯誤處理**：倘若該 `<id>` 並不存在於 DB 內，回傳 `404 Not Found`。

### 更新任務 - `POST /tasks/<id>/update`
- **輸入**：標籤為 `<id>` 以及表單攜帶過來的新版 `title`。
- **處理邏輯**：再次驗證字串是否過短/空白，然後呼叫 `TaskModel.update(task_id=id, title=title)` 強制覆寫 `title` 欄位。
- **輸出**：重定向 (Redirect) 返回到首頁列表 `/`。
- **錯誤處理**：如標題為空或未找到目標 `id`，則拋出對應的 400 或 404 狀態碼。

### 切換任務狀態(未完成/已完成) - `POST /tasks/<id>/toggle`
- **輸入**：網址列 `<id>`。
- **處理邏輯**：先取得任務的 `status` 現況，如果是未完成 (`0`) 則傳遞更新改為 (`1`)；如果是已完成則是改為 (`0`)，實作簡單切換功能 (Toggle)。
- **輸出**：重新整理回歸列表本身 (Redirect)。

### 刪除任務 - `POST /tasks/<id>/delete`
- **輸入**：網址列對象 `<id>`。
- **處理邏輯**：觸發 `TaskModel.delete(id)` 從 DB 將資料永存移出。
- **輸出**：重新整理首面與導向。

## 3. Jinja2 模板清單

- `templates/base.html`: 所有網頁共用的底層版型 (將放有共同的 `<head>`、全局性的 CSS 以及共通導覽列元件)。
- `templates/index.html`: 繼承自 `base.html`，顯示「任務清單列表」、「完成操作」與「新增的介面輸入框」。
- `templates/edit.html`: 繼承自 `base.html`，當點選編輯後跳轉於此用來取代內容的畫面。

## 4. 路由骨架程式碼
根據 Blueprint 框架模式，上述的功能已經撰寫了函式定義、簽名與 docstrings 於 `app/routes/task_routes.py` 當中，將能在實作階段被直接套用邏輯完成它。
