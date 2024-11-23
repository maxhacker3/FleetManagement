import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ReverseGeocoding({ coords }) {
  const useMockData = false; // Umschalter: Mock-Daten oder API-Daten
  const [address, setAddress] = useState('Lade Adresse...');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!coords || coords.length !== 2) {
      setAddress('Ungültige Koordinaten');
      return;
    }

    if (useMockData) {
      // Verwende Mock-Daten
      setAddress(`Mock-Adresse für [${coords[0]}, ${coords[1]}]`);
    } else {
      const apiKey = process.env.REACT_APP_OPENCAGE_KEY;
      const url = `https://api.opencagedata.com/geocode/v1/json?q=${coords[0]}+${coords[1]}&key=${apiKey}`;

      const fetchAddress = async () => {
        try {
          console.log('API-Aufruf gestartet:', url); // Debugging: URL überprüfen
          const response = await axios.get(url);

          console.log('API-Antwort:', response.data); // Debugging: Ganze API-Antwort anzeigen
          const results = response.data.results;

          if (results && results.length > 0) {
            console.log('Extrahierte Adresse:', results[0].formatted); // Debugging: Adresse überprüfen
            setAddress(results[0].formatted); // Adresse aus API-Ergebnis setzen
          } else {
            console.warn('Keine Ergebnisse gefunden in API-Antwort');
            setAddress('Keine Adresse gefunden');
          }
        } catch (error) {
          console.error('Fehler beim Reverse Geocoding:', error); // Fehler-Details ausgeben
          setError('Fehler beim Abrufen der Adresse');
          setAddress(null); // Leere Adresse bei Fehler
        }
      };

      fetchAddress();
    }
  }, [coords, useMockData]);

  if (error) {
    return <span style={{ color: 'red' }}>{error}</span>;
  }

  return <span>{address}</span>;
}

export default ReverseGeocoding;
