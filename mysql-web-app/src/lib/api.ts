import { db } from "./cloudbase";

// 任务接口定义
export interface Todo {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
  _openid?: string;
}

// 创建任务
export async function createTodo(title: string): Promise<Todo> {
  const { data, error } = await db
    .from("todos")
    .insert({
      title,
      completed: false,
      created_at: new Date().toISOString(),
    })
    .select()
    .single();

  if (error) {
    throw new Error(`创建任务失败: ${error.message}`);
  }

  return data as unknown as Todo;
}

// 获取所有任务
export async function getTodos(): Promise<Todo[]> {
  const { data, error } = await db
    .from("todos")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    throw new Error(`获取任务失败: ${error.message}`);
  }

  return (data as unknown as Todo[]) || [];
}

// 更新任务状态
export async function updateTodo(
  id: number,
  updates: Partial<Pick<Todo, "title" | "completed">>
): Promise<Todo> {
  const { data, error } = await db
    .from("todos")
    .update(updates)
    .eq("id", id)
    .select()
    .single();

  if (error) {
    throw new Error(`更新任务失败: ${error.message}`);
  }

  return data as unknown as Todo;
}

// 删除任务
export async function deleteTodo(id: number): Promise<void> {
  const { error } = await db.from("todos").delete().eq("id", id);

  if (error) {
    throw new Error(`删除任务失败: ${error.message}`);
  }
}

// 切换任务完成状态
export async function toggleTodo(id: number, completed: boolean): Promise<Todo> {
  return updateTodo(id, { completed: !completed });
}
