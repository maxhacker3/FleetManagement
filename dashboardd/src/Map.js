import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const taxiIcon = L.icon({
  iconUrl: process.env.PUBLIC_URL + '/icons/Taxi.png',
  iconSize: [40, 40],
  iconAnchor: [20, 40],
  popupAnchor: [0, -40]
});

const customerIcon = L.icon({
  iconUrl: process.env.PUBLIC_URL + '/icons/Customer.png',
  iconSize: [40, 40],
  iconAnchor: [20, 40],
  popupAnchor: [0, -40]
});

function Map() {
  const useMockData = true; // Umschalter: Mock-Daten oder Backend-Daten

  // Dynamische Taxi-Daten
  const [taxis, setTaxis] = useState([]);
  const [customers, setCustomers] = useState([]);

  // Mock-Daten
  const mockTaxis =false /* [
    { id: 1, position: [48.1351, 11.5820], target: [48.1401, 11.5900] },
    { id: 2, position: [48.1371, 11.5750], target: [48.1301, 11.5800] }
  ];

  const mockCustomers = [
    { id: 101, position: [48.1371, 11.5750] },
    { id: 102, position: [48.1401, 11.5800] }
  ];*/

  useEffect(() => {
    if (useMockData) {
      setTaxis(mockTaxis);
      setCustomers(mockCustomers);
    } else {
      // Backend-Daten laden
      fetch('http://localhost:8090/get_scenario/${id}') // Beispiel-Endpoint
        .then((response) => response.json())
        .then((data) => setTaxis(data.taxis || []))
        .catch((error) => console.error('Fehler beim Laden der Taxi-Daten:', error));

      fetch('http://localhost:8090/get_scenario/${id}') // Beispiel-Endpoint
        .then((response) => response.json())
        .then((data) => setCustomers(data.customers || []))
        .catch((error) => console.error('Fehler beim Laden der Kunden-Daten:', error));
    }
  }, [useMockData]);

  // Effekt zur Simulation der Taxi-Bewegung
  useEffect(() => {
    const interval = setInterval(() => {
      setTaxis((prevTaxis) =>
        prevTaxis.map((taxi) => {
          const [lat, lon] = taxi.position;
          const [targetLat, targetLon] = taxi.target;

          // Berechnung der neuen Position (schrittweise Annäherung an das Ziel)
          const newLat = lat + (targetLat - lat) * 0.01; // 1% Annäherung
          const newLon = lon + (targetLon - lon) * 0.01;

          return {
            ...taxi,
            position: [newLat, newLon]
          };
        })
      );
    }, 1000); // Aktualisiere jede Sekunde

    return () => clearInterval(interval); // Cleanup bei Komponentendeaktivierung
  }, []);

  return (
    <MapContainer
      center={[48.1351, 11.5820]}
      zoom={13}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />

      {/* Dynamisch bewegende Taxis */}
      {taxis.map((taxi) => (
        <Marker position={taxi.position} key={taxi.id} icon={taxiIcon}>
          <Popup>
            <strong>Taxi {taxi.id}</strong>
            <br />
            Aktuelle Position: {taxi.position.join(', ')}
          </Popup>
        </Marker>
      ))}

      {/* Statische Kunden-Positionen */}
      {customers.map((customer) => (
        <Marker position={customer.position} key={customer.id} icon={customerIcon}>
          <Popup>
            <strong>Kunde {customer.id}</strong>
            <br />
            Wartet auf Abholung
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default Map;
