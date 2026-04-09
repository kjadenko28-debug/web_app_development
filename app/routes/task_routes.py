from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

# 建立名為 'tasks' 的 Blueprint，以供 app.py 初始化註冊使用
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def index():
    """
    [任務列表]
    輸入：無
    處理邏輯：取得所有待辦事項 (呼叫 TaskModel.get_all)
    輸出：渲染 templates/index.html
    """
    pass

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    """
    [新增任務]
    輸入：表單資料 (title)
    處理邏輯：驗證 title 欄位輸入、呼叫 TaskModel.create
    輸出：重導向至 index (首頁)
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    """
    [編輯任務頁面]
    輸入：URL 參數 task_id
    處理邏輯：依據 ID 取得特定任務 (TaskModel.get_by_id)
    輸出：若找到則渲染 templates/edit.html；找不到則觸發 404
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    [更新任務]
    輸入：URL 參數 task_id、表單資料 (title)
    處理邏輯：驗證參數、呼叫 TaskModel.update 更新文字
    輸出：成功後重導向至 index (首頁) 回列表
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    [切換任務狀態]
    輸入：URL 參數 task_id
    處理邏輯：查詢是否已完成，並傳送新狀態到 TaskModel.update(status=...) 
    輸出：重導向至 index (首頁) 更新任務清單呈現
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    [刪除任務]
    輸入：URL 參數 task_id
    處理邏輯：呼叫 TaskModel.delete 強制抹除任務資料
    輸出：畫面重整導向回 index 列點
    """
    pass
