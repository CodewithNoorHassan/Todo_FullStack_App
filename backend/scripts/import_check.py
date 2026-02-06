# quick import check
try:
    import models.task as m
    print('Imported models.task OK')
    print('TaskCreate.todo_id annotation:', getattr(m.TaskCreate, '__annotations__', {}).get('todo_id'))
except Exception as e:
    print('Import error:', e)
    import traceback; traceback.print_exc()
