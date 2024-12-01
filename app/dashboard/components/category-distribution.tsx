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
  Legend,
);

type StatsResponse = {
  total: number;
  high_urgency_count: number;
  top_category: string;
  top_zone: string;
  categories_distribution: { [key: string]: number };
  zones_distribution: { [key: string]: number };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  recent_issues: any[];
};

export function CategoryDistribution() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/stats");
      if (!response.ok) throw new Error("Errore nel caricamento dei dati");
      const data: StatsResponse = await response.json();
      setStats(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Errore sconosciuto");
      console.error("Errore nel fetch dei dati:", err);
    }
  };

  useEffect(() => {
    // Carica i dati iniziali
    fetchData();

    // Imposta il polling ogni 30 secondi
    const interval = setInterval(fetchData, 30000);

    // Cleanup dell'intervallo quando il componente viene smontato
    return () => clearInterval(interval);
  }, []);

  if (error) return <div className="text-red-500">Errore: {error}</div>;
  if (!stats) return <div className="text-gray-500">Caricamento...</div>;

  // Pulisce le chiavi delle categorie rimuovendo le virgolette
  const cleanCategories = Object.entries(stats.categories_distribution).reduce(
    (acc, [key, value]) => {
      const cleanKey = key.replace(/['"]+/g, "");
      acc[cleanKey] = value;
      return acc;
    },
    {} as { [key: string]: number },
  );

  const data = {
    labels: Object.keys(cleanCategories),
    datasets: [
      {
        label: "Distribuzione Categorie",
        data: Object.values(cleanCategories),
        backgroundColor: "rgba(45, 98, 200, 0.5)",
        borderColor: "#2d62c8",
        borderWidth: 2,
        pointBackgroundColor: "rgba(45, 98, 200, 0.9)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
      tooltip: {
        enabled: true,
        callbacks: {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          label: (context: any) => {
            return `Segnalazioni: ${context.raw}`;
          },
        },
      },
    },
    scales: {
      r: {
        angleLines: {
          display: true,
        },
        suggestedMin: 0,
        suggestedMax: Math.max(...Object.values(cleanCategories)) + 1,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="w-full h-full min-h-[400px]">
      <Radar data={data} options={options} />
    </div>
  );
}
