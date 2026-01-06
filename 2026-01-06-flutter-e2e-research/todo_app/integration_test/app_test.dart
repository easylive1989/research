import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:todo_app/main.dart'; // Adjust import based on your package name if needed

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('add todo test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const TodoApp());

    // Verify that the list is empty initially.
    expect(find.byType(ListTile), findsNothing);

    // Enter a todo item.
    await tester.enterText(find.byKey(const Key('todoInput')), 'Buy Milk');
    await tester.pump();

    // Tap the add button.
    await tester.tap(find.byKey(const Key('addTodoButton')));
    await tester.pumpAndSettle();

    // Verify that the item has been added.
    expect(find.text('Buy Milk'), findsOneWidget);
    expect(find.byType(ListTile), findsOneWidget);

    // Add another item
    await tester.enterText(find.byKey(const Key('todoInput')), 'Walk Dog');
    await tester.pump();
    await tester.tap(find.byKey(const Key('addTodoButton')));
    await tester.pumpAndSettle();

    // Verify total items
    expect(find.text('Walk Dog'), findsOneWidget);
    expect(find.byType(ListTile), findsNWidgets(2));
  });
}
