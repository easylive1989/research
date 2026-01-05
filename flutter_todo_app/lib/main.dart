import 'package:flutter/material.dart';

void main() {
  runApp(const TodoApp());
}

class TodoApp extends StatelessWidget {
  const TodoApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Todo List',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const TodoListPage(),
    );
  }
}

class TodoListPage extends StatefulWidget {
  const TodoListPage({Key? key}) : super(key: key);

  @override
  State<TodoListPage> createState() => _TodoListPageState();
}

class _TodoListPageState extends State<TodoListPage> {
  final List<TodoItem> _todos = [];
  final TextEditingController _textController = TextEditingController();

  void _addTodo() {
    if (_textController.text.isNotEmpty) {
      setState(() {
        _todos.add(TodoItem(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          title: _textController.text,
          isCompleted: false,
        ));
        _textController.clear();
      });
    }
  }

  void _toggleTodo(int index) {
    setState(() {
      _todos[index].isCompleted = !_todos[index].isCompleted;
    });
  }

  void _deleteTodo(int index) {
    setState(() {
      _todos.removeAt(index);
    });
  }

  int get _completedCount => _todos.where((todo) => todo.isCompleted).length;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Todo List'),
        elevation: 2,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    key: const Key('todoInput'),
                    controller: _textController,
                    decoration: const InputDecoration(
                      hintText: '輸入待辦事項...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _addTodo(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  key: const Key('addButton'),
                  onPressed: _addTodo,
                  child: const Text('新增'),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '總計: ${_todos.length}',
                  key: const Key('totalCount'),
                  style: const TextStyle(fontSize: 16),
                ),
                Text(
                  '已完成: $_completedCount',
                  key: const Key('completedCount'),
                  style: const TextStyle(fontSize: 16),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: _todos.isEmpty
                ? const Center(
                    child: Text(
                      '沒有待辦事項',
                      style: TextStyle(fontSize: 16, color: Colors.grey),
                    ),
                  )
                : ListView.builder(
                    key: const Key('todoList'),
                    itemCount: _todos.length,
                    itemBuilder: (context, index) {
                      final todo = _todos[index];
                      return ListTile(
                        key: Key('todoItem_$index'),
                        leading: Checkbox(
                          key: Key('checkbox_$index'),
                          value: todo.isCompleted,
                          onChanged: (_) => _toggleTodo(index),
                        ),
                        title: Text(
                          todo.title,
                          key: Key('todoText_$index'),
                          style: TextStyle(
                            decoration: todo.isCompleted
                                ? TextDecoration.lineThrough
                                : null,
                            color: todo.isCompleted ? Colors.grey : null,
                          ),
                        ),
                        trailing: IconButton(
                          key: Key('deleteButton_$index'),
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => _deleteTodo(index),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }
}

class TodoItem {
  String id;
  String title;
  bool isCompleted;

  TodoItem({
    required this.id,
    required this.title,
    required this.isCompleted,
  });
}
