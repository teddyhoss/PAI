// @components
import { Dashboard } from "./components/dashboard";

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
    <Dashboard
      totalReports={stats.total}
      highUrgency={stats.high_urgency_count}
      mostReportedAreas="Roma"
      mostFrequencyCategory={stats.top_category
        .toUpperCase()
        .replaceAll('"', "")}
      data={stats.recent_issues}
    />
  );
}
