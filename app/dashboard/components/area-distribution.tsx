"use client";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from "react-leaflet";

type Issue = {
  id: number;
  text: string;
  cap: string;
  category: string;
  urgency: string;
  explanation: string;
  city: string | null;
  coordinates: number[] | null;
  timestamp: string;
};

type StatsResponse = {
  total: number;
  high_urgency_count: number;
  top_category: string;
  top_zone: string;
  categories_distribution: { [key: string]: number };
  zones_distribution: { [key: string]: number };
  recent_issues: Issue[];
};

export function AreaDistribution() {
  const [geoData, setGeoData] = useState(null);
  const [issues, setIssues] = useState<Issue[]>([]);

  useEffect(() => {
    const getData = async () => {
      fetch("/ITA.geo.json")
        .then((res) => res.json())
        .then((data) => {
          setGeoData(data);
        });

      fetch("http://localhost:8000/api/stats")
        .then((res) => res.json())
        .then((data: StatsResponse) => {
          setIssues(
            data.recent_issues.filter((issue) => issue.coordinates !== null),
          );
        });
    };

    getData();
  }, []);

  const getIcon = (urgency: string) => {
    const color =
      urgency === "high" ? "red" : urgency === "medium" ? "orange" : "green";

    return new L.DivIcon({
      className: "custom-icon",
      html: `<div style="width: 20px; height: 20px; background-color: ${color}; border-radius: 50%; border: 2px solid black;"></div>`,
      iconSize: [20, 20],
      iconAnchor: [10, 10],
    });
  };

  return (
    <MapContainer
      center={[41.9028, 12.4964]}
      zoom={5}
      style={{ width: "100%", height: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {geoData && <GeoJSON data={geoData} />}

      {issues.map(
        (issue) =>
          issue.coordinates && (
            <Marker
              position={issue.coordinates as L.LatLngExpression}
              key={issue.id}
              icon={getIcon(issue.urgency)}>
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold">{issue.city}</h3>
                  <p className="text-sm">{issue.text}</p>
                  <div className="mt-2">
                    <span className="font-semibold">Categoria:</span>{" "}
                    {issue.category}
                  </div>
                  <div>
                    <span className="font-semibold">Urgenza:</span>{" "}
                    {issue.urgency}
                  </div>
                  <div className="mt-1 text-xs text-gray-600">
                    {new Date(issue.timestamp).toLocaleString()}
                  </div>
                </div>
              </Popup>
            </Marker>
          ),
      )}
    </MapContainer>
  );
}
