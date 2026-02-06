'use client';

import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface TaskDeleteProps {
  taskId: string;
  onConfirm: (taskId: string) => void;
  onCancel: () => void;
}

export function TaskDelete({ taskId, onConfirm, onCancel }: TaskDeleteProps) {
  const [isConfirmed, setIsConfirmed] = useState(false);

  const handleConfirmClick = () => {
    if (isConfirmed) {
      onConfirm(taskId);
    } else {
      setIsConfirmed(true);
    }
  };

  return (
    <div className="bg-destructive/10 border border-destructive rounded-lg p-4">
      <h3 className="text-lg font-medium text-destructive">Delete Task</h3>
      <p className="text-destructive mt-2">
        {isConfirmed
          ? 'Are you absolutely sure you want to delete this task? This action cannot be undone.'
          : 'Are you sure you want to delete this task? This action cannot be undone.'}
      </p>
      <div className="mt-4 flex gap-2">
        <Button
          variant="destructive"
          onClick={handleConfirmClick}
        >
          {isConfirmed ? 'Confirm Delete' : 'Delete'}
        </Button>
        <Button
          variant="outline"
          onClick={onCancel}
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}