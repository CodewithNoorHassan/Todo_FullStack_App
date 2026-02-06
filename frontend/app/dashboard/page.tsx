import { TaskOverview } from '@/components/dashboard/task-overview';
import { DashboardLayout } from '@/components/dashboard/layout';

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <TaskOverview />
    </DashboardLayout>
  );
}
