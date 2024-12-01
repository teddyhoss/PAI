"use client";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from "react-leaflet";

type City = {
  name: string;
  population: number;
  position: Array<number>;
};

export function AreaDistribution() {
  const [geoData, setGeoData] = useState(null);
  const [cityPoints, setCityPoints] = useState<Array<City>>([]);

  useEffect(() => {
    fetch("/ITA.geo.json")
      .then((res) => res.json())
      .then((data) => {
        setGeoData(data);
      });

    const cities = [
      { name: "Bologna", population: 200, position: [44.4949, 11.3426] },
      { name: "Roma", population: 3000000, position: [41.9028, 12.4964] },
      { name: "Milano", population: 1500000, position: [45.4642, 9.19] },
    ];

    setCityPoints(cities);
  }, []);

  const getStyle = () => {
    return {
      weight: 1,
      opacity: 1,
      color: "black",
      dashArray: "3",
      fillOpacity: 0.7,
    };
  };

  const redIcon = new L.DivIcon({
    className: "custom-icon",
    html: '<div style="width: 20px; height: 20px; background-color: red; border-radius: 50%; border: 2px solid black;"></div>',
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  });

  return (
    <MapContainer
      center={[41.9028, 12.4964]}
      zoom={6}
      style={{ width: "100%", height: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {geoData && <GeoJSON data={geoData} style={getStyle} />}

      {cityPoints.map((city, index) => (
        <Marker
          position={city.position as L.LatLngExpression}
          key={index}
          icon={redIcon}>
          <Popup>
            <b>{city.name}</b>
            <br />
            Población: {city.population}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
