import { Task } from '@/lib/types';

interface TaskViewProps {
  task: Task;
}

export function TaskView({ task }: TaskViewProps) {
  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-semibold">{task.title}</h3>
          <p className="text-muted-foreground mt-2">{task.description}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${
          task.completed
            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
        }`}>
          {task.completed ? 'Completed' : 'Pending'}
        </div>
      </div>

      <div className="mt-4 text-sm text-muted-foreground">
        <p>Created: {new Date(task.createdAt).toLocaleDateString()}</p>
        <p>Updated: {new Date(task.updatedAt).toLocaleDateString()}</p>
      </div>
    </div>
  );
}