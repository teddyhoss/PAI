// @components
import { Dashboard } from "./components/dashboard";
import { ChatBot } from "./components/chat-bot";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Circle } from "./components/circle";

const getStats = async () => {
  const response = await fetch("http://localhost:8000/api/stats");

  const data = await response.json();

  if (data.error) {
    throw new data.error();
  }

  return data;
};

export default async function DashboardPage() {
  const stats = await getStats();

  return (
    <Dialog>
      <div className="grid grid-cols-12 gap-4">
        <Dashboard
          totalReports={stats.total}
          highUrgency={stats.high_urgency_count}
          mostReportedAreas="Roma"
          mostFrequencyCategory={stats.top_category
            .toUpperCase()
            .replaceAll('"', "")}
          data={stats.recent_issues}
        />
      </div>
      <DialogTrigger asChild>
        <Circle />
      </DialogTrigger>
      <DialogContent>
        <DialogTitle>ChatBot</DialogTitle>
        <div className="min-h-96 max-h-96">
          <ChatBot />
        </div>
      </DialogContent>
    </Dialog>
  );
}
