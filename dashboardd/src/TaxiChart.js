import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Registrierung der ChartJS-Komponenten
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function TaxiChart() {
  const useMockData = true; // Umschalter: Mock-Daten oder Backend-Daten
  const [taxis, setTaxis] = useState([]);

  // Mock-Daten
  const mockData =false/*[
    { id: 1, distance: 100 },
    { id: 2, distance: 150 },
    { id: 3, distance: 200 },
  ];*/

  // Daten laden
  useEffect(() => {
    if (useMockData) {
      setTaxis(mockData);
    } else {
      fetch('http://localhost:8090/get_scenario/${id}') // Beispiel-Endpoint
        .then((response) => response.json())
        .then((data) => setTaxis(data.taxis || []))
        .catch((error) => console.error('Fehler beim Abrufen der Daten:', error));
    }
  }, [useMockData]);

  // Datenaufbereitung für das Chart
  const data = {
    labels: taxis.map((taxi) => `Taxi ${taxi.id || 'Unbekannt'}`),
    datasets: [
      {
        label: 'Gefahrene Kilometer',
        data: taxis.map((taxi) => taxi.distance || 0), // Fallback auf 0
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Optionen für das Chart
  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      title: {
        display: true,
        text: 'Gefahrene Kilometer pro Taxi',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Taxis',
        },
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Gefahrene Kilometer',
        },
      },
    },
  };

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default TaxiChart;
