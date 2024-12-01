// @components
import { Dashboard } from "./components/dashboard";
import { ChatBot } from './components/chat-bot';

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
      <div className="col-span-12 lg:col-span-6 h-[600px]">
        <ChatBot />
      </div>
    </div>
  );
}
