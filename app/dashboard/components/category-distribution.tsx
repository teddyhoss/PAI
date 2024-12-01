"use client";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { Radar } from "react-chartjs-2";
import { useEffect, useState } from "react";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

type StatsResponse = {
  total: number;
  high_urgency_count: number;
  top_category: string;
  top_zone: string;
  categories_distribution: { [key: string]: number };
  zones_distribution: { [key: string]: number };
  recent_issues: any[];
};

export function CategoryDistribution() {
  const [stats, setStats] = useState<StatsResponse | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/stats")
      .then((res) => res.json())
      .then((data: StatsResponse) => {
        setStats(data);
      });
  }, []);

  if (!stats) return <div>Caricamento...</div>;

  // Pulisce le chiavi delle categorie rimuovendo le virgolette
  const cleanCategories = Object.entries(stats.categories_distribution).reduce(
    (acc, [key, value]) => {
      const cleanKey = key.replace(/['"]+/g, '');
      acc[cleanKey] = value;
      return acc;
    },
    {} as { [key: string]: number }
  );

  const data = {
    labels: Object.keys(cleanCategories),
    datasets: [
      {
        label: "Distribuzione Categorie",
        data: Object.values(cleanCategories),
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      tooltip: {
        enabled: true,
      },
    },
    scales: {
      r: {
        angleLines: {
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: Math.max(...Object.values(cleanCategories)) + 1,
      },
    },
  };

  return <Radar data={data} options={options} />;
}
