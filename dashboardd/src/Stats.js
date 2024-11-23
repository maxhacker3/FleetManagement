import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TaxiChart from './TaxiChart';

function Stats() {
  const useMockData = true; // Umschalter: true = Mock-Daten, false = Backend-Daten
  const [data, setData] = useState({ taxis: [], customers: [], co2Savings: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock-Daten
  const mockData = false/*{
    taxis: [
      { id: 1, position: [48.1351, 11.5820], distance: 100 },
      { id: 2, position: [48.1371, 11.5750], distance: 150 },
    ],
    customers: [
      { id: 101, start: [48.1371, 11.5750], destination: [48.1401, 11.5800] },
      { id: 102, start: [48.1401, 11.5800], destination: [48.1450, 11.5850] },
    ],
    co2Savings: 123.45,
  };*/

  // Daten laden
  useEffect(() => {
    if (useMockData) {
      // Mock-Daten verwenden
      setData(mockData);
      setLoading(false);
    } else {
      // Backend-Daten abrufen
      axios
        .get('http://localhost:8090/get_scenario/${id}') // Beispiel-Endpoint
        .then((response) => {
          setData(response.data);
          setLoading(false);
        })
        .catch((error) => {
          console.error('Fehler beim Laden der Daten:', error);
          setError('Daten konnten nicht geladen werden');
          setLoading(false);
        });
    }
  }, [useMockData]);

  if (loading) {
    return <div className="stats-container">Daten werden geladen...</div>;
  }

  if (error) {
    return <div className="stats-container">{error}</div>;
  }

  return (
    <div className="stats-container">
      {/* Flottenstatus */}
      <div className="card">
        <h2>Flottenstatus</h2>
        <p><strong>Anzahl Taxis:</strong> {data.taxis?.length || 0}</p>
        <p><strong>Wartende Kunden:</strong> {data.customers?.filter((c) => c.waiting)?.length || 0}</p>
        <p><strong>CO₂ Einsparungen:</strong> {data.co2Savings?.toLocaleString() || 0} kg</p>
      </div>

      {/* Diagramm für gefahrene Kilometer */}
      <div className="card">
        <h2>Gefahrene Kilometer</h2>
        {data.taxis && data.taxis.length > 0 ? (
          <TaxiChart taxis={data.taxis} />
        ) : (
          <p>Keine Daten zu gefahrenen Kilometern verfügbar.</p>
        )}
      </div>

      {/* Taxi-Koordinaten */}
      <div className="card">
        <h2>Taxi-Koordinaten</h2>
        <ul>
          {data.taxis?.map((taxi) => (
            <li key={taxi.id}>
              Taxi {taxi.id}: [{taxi.position?.[0]?.toFixed(4)}, {taxi.position?.[1]?.toFixed(4)}]
            </li>
          ))}
        </ul>
      </div>

      {/* Kunden-Koordinaten */}
      <div className="card">
        <h2>Kunden-Koordinaten</h2>
        <ul>
          {data.customers?.map((customer) => (
            <li key={customer.id}>
              Kunde {customer.id} wartet bei [{customer.start?.[0]?.toFixed(4)}, {customer.start?.[1]?.toFixed(4)}] 
              und möchte nach [{customer.destination?.[0]?.toFixed(4)}, {customer.destination?.[1]?.toFixed(4)}]
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Stats;
