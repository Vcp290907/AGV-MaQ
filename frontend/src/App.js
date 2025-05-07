import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [temperatures, setTemperatures] = useState([]);
  const [status, setStatus] = useState('');
  const API_URL = 'http://<IP_DO_RASPBERRY>:5000'; // Substitua pelo IP do Raspberry

  // Busca temperaturas a cada 5 segundos
  useEffect(() => {
    const fetchTemperatures = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/temperatures`);
        setTemperatures(response.data);
      } catch (error) {
        console.error('Erro ao buscar temperaturas:', error);
      }
    };

    fetchTemperatures();
    const interval = setInterval(fetchTemperatures, 5000);
    return () => clearInterval(interval);
  }, []);

  // Função para acionar o buzzer
  const activateBuzzer = async () => {
    try {
      setStatus('Acionando...');
      const response = await axios.post(`${API_URL}/api/buzzer`);
      setStatus(response.data.message || response.data.error);
      setTimeout(() => setStatus(''), 3000);
    } catch (error) {
      setStatus('Erro ao acionar o buzzer');
      setTimeout(() => setStatus(''), 3000);
    }
  };

  return (
    <div className="container">
      <h1>Monitor de Temperatura</h1>
      <div className="control-section">
        <h2>Controle</h2>
        <button onClick={activateBuzzer}>Tocar Buzzer</button>
        {status && <p className="status">{status}</p>}
      </div>
      <div className="temperatures-section">
        <h2>Leituras de Temperatura</h2>
        {temperatures.length === 0 ? (
          <p>Nenhuma leitura ainda.</p>
        ) : (
          temperatures.map((temp) => (
            <div key={temp.id} className="temperature-card">
              <p>{temp.value.toFixed(1)} °C</p>
              <p className="timestamp">{new Date(temp.timestamp).toLocaleString()}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;