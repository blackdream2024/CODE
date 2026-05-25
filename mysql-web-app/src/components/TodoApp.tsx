import { useState, useEffect, useCallback } from "react";
import {
  getTodos,
  createTodo,
  deleteTodo,
  toggleTodo,
  type Todo,
} from "../lib/api";

export function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTitle, setNewTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 加载任务列表
  const loadTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getTodos();
      setTodos(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "加载失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  // 添加任务
  const handleAdd = async () => {
    if (!newTitle.trim()) return;

    try {
      setError(null);
      await createTodo(newTitle.trim());
      setNewTitle("");
      await loadTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "添加失败");
    }
  };

  // 切换完成状态
  const handleToggle = async (todo: Todo) => {
    try {
      setError(null);
      await toggleTodo(todo.id, todo.completed);
      await loadTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "更新失败");
    }
  };

  // 删除任务
  const handleDelete = async (id: number) => {
    try {
      setError(null);
      await deleteTodo(id);
      await loadTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "删除失败");
    }
  };

  // 回车提交
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleAdd();
    }
  };

  return (
    <div className="todo-app">
      <header className="todo-header">
        <h1>CloudBase MySQL 任务管理</h1>
        <p className="subtitle">使用 CloudBase 关系型数据库的 Web 应用示例</p>
      </header>

      {/* 错误提示 */}
      {error && (
        <div className="error-message">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* 添加任务 */}
      <div className="add-todo">
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入新任务..."
          disabled={loading}
        />
        <button onClick={handleAdd} disabled={loading || !newTitle.trim()}>
          添加
        </button>
      </div>

      {/* 任务列表 */}
      <div className="todo-list">
        {loading && todos.length === 0 ? (
          <div className="loading">加载中...</div>
        ) : todos.length === 0 ? (
          <div className="empty">暂无任务，添加一个吧！</div>
        ) : (
          todos.map((todo) => (
            <div key={todo.id} className={`todo-item ${todo.completed ? "completed" : ""}`}>
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggle(todo)}
              />
              <span className="todo-title">{todo.title}</span>
              <span className="todo-date">
                {new Date(todo.created_at).toLocaleDateString("zh-CN")}
              </span>
              <button
                className="delete-btn"
                onClick={() => handleDelete(todo.id)}
                title="删除"
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>

      {/* 统计信息 */}
      {todos.length > 0 && (
        <div className="todo-stats">
          <span>总计: {todos.length}</span>
          <span>已完成: {todos.filter((t) => t.completed).length}</span>
          <span>未完成: {todos.filter((t) => !t.completed).length}</span>
        </div>
      )}
    </div>
  );
}
