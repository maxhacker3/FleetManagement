import React, { useState, useEffect } from 'react';
import Stats from './Stats';
import Map from './Map';
import './App.css'; // Für das Layout

function App() {
  const useMockData = true; // Umschalter: true = Mock-Daten, false = API-Daten

  // Zentraler Zustand für Taxis und Kunden
  const [taxis, setTaxis] = useState([]);
  const [customers, setCustomers] = useState([]);

  // Mock-Daten
  const mockData = false
  /*{
    taxis: [
      { id: 1, position: [48.1351, 11.5820], target: [48.1401, 11.5900], distance: 100 },
      { id: 2, position: [48.1371, 11.5750], target: [48.1301, 11.5800], distance: 150 },
    ],
    customers: [
      { id: 101, position: [48.1371, 11.5750], destination: [48.1401, 11.5800] },
      { id: 102, position: [48.1401, 11.5800], destination: [48.1450, 11.5850] },
    ],
  };*/

  // Daten laden
  import Papa from "papaparse";

const MyComponent = () => {
    const useMockData = false; // Adjust this according to your logic

    useEffect(() => {
        if (useMockData) {
            // Use mock data
            setTaxis(mockData.taxis);
            setCustomers(mockData.customers);
        } else {
            // Read the CSV file to get the ID
            fetch("../id.csv") // Replace with the actual path to your CSV file
                .then((response) => response.text())
                .then((csvText) => {
                    // Parse the CSV data
                    const parsedData = Papa.parse(csvText, { header: true }); // `header: true` assumes CSV has headers
                    const rows = parsedData.data;

                    // Extract the ID (assuming the CSV has a column "id")
                    const id = rows[0]?.id; // Adjust index or key as per your CSV structure

                    if (id) {
                        // Fetch the scenario using the extracted ID
                        fetch(`http://localhost:8090/get_scenario/${id}`)
                            .then((response) => response.json())
                            .then((data) => {
                                setTaxis(data.taxis || []);
                                setCustomers(data.customers || []);
                            })
                            .catch((error) => {
                                console.error("Fehler beim Abrufen der Daten:", error);
                            });
                    } else {
                        console.error("ID not found in CSV.");
                    }
                })
                .catch((error) => {
                    console.error("Fehler beim Lesen der CSV:", error);
                });
        }
    }, [useMockData]);




  // Bewegung der Taxis simulieren
  useEffect(() => {
    const interval = setInterval(() => {
      setTaxis((prevTaxis) =>
        prevTaxis.map((taxi) => {
          const [lat, lon] = taxi.position;
          const [targetLat, targetLon] = taxi.target;

          const diffLat = targetLat - lat;
          const diffLon = targetLon - lon;

          if (Math.abs(diffLat) < 0.0001 && Math.abs(diffLon) < 0.0001) {
            return { ...taxi, position: [targetLat, targetLon] };
          }

          const newLat = lat + diffLat * 0.01;
          const newLon = lon + diffLon * 0.01;

          return {
            ...taxi,
            position: [newLat, newLon],
          };
        })
      );
    }, 1000);

    return () => clearInterval(interval); // Cleanup
  }, [taxis]);

  return (
    <div className="dashboard">
      {/* Kartenbereich */}
      <div className="map-container">
        <Map taxis={taxis} customers={customers} />
      </div>

      {/* Parameterbereich */}
      <div className="stats-container">
        <Stats taxis={taxis} customers={customers} />
      </div>
    </div>
  );
}

export default App;
