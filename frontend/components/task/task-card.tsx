'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskEdit } from '@/components/task/task-edit';
import { TaskView } from '@/components/task/task-view';
import { TaskDelete } from '@/components/task/task-delete';
import { Task } from '@/lib/types';

interface TaskCardProps {
  task: Task;
  onToggle?: (id: string) => void;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [taskData, setTaskData] = useState(task);

  const handleSave = (updatedTask: Task) => {
    setTaskData(updatedTask);
    setIsEditing(false);
    onEdit?.(updatedTask.id);
  };

  const handleDeleteConfirm = (taskId: string) => {
    onDelete?.(taskId);
    setIsDeleting(false);
  };

  if (isDeleting) {
    return (
      <Card className="bg-destructive/10 border-destructive">
        <CardContent className="pt-6">
          <TaskDelete
            taskId={taskData.id}
            onConfirm={handleDeleteConfirm}
            onCancel={() => setIsDeleting(false)}
          />
        </CardContent>
      </Card>
    );
  }

  if (isEditing) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Edit Task</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskEdit
            task={taskData}
            onSave={handleSave}
            onCancel={() => setIsEditing(false)}
          />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="transition-all hover:shadow-lg hover:border-primary/50 hover:-translate-y-0.5 duration-200">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardTitle className={`text-lg ${taskData.completed ? 'line-through text-muted-foreground' : ''}`}>
            {taskData.title}
          </CardTitle>
          <div className={`px-2 py-1 rounded-full text-xs ${
            taskData.completed
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
          }`}>
            {taskData.completed ? 'Done' : 'Pending'}
          </div>
        </div>
      </CardHeader>
      <CardContent className="pb-2">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {taskData.description}
        </p>
      </CardContent>
      <CardFooter className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onToggle?.(taskData.id)}
        >
          {taskData.completed ? 'Undo' : 'Complete'}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsEditing(true)}
        >
          Edit
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsDeleting(true)}
        >
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
}