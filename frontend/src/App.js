import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import item1Img from './assets/item1.png';
import item2Img from './assets/item2.png';

function App() {
  const [item1, setItem1] = useState(false);
  const [item2, setItem2] = useState(false);
  const [status, setStatus] = useState('');
  const API_URL = 'http://localhost:5000';

  const handleSend = async () => {
    try {
      setStatus('Enviando...');
      const response = await axios.post(`${API_URL}/api/comando`, {
        item1,
        item2,
      });
      setStatus(response.data.message || response.data.error);
      setTimeout(() => setStatus(''), 3000);
    } catch (error) {
      setStatus('Erro ao enviar comando');
      setTimeout(() => setStatus(''), 3000);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Seleção de Itens</h1>
      <div className="selection-row">
        <div
          className={`selectable-item${item1 ? ' selected' : ''}`}
          onClick={() => setItem1(!item1)}
        >
          <img src={item1Img} alt="Item 1" className="item-img-large" />
          <span>Item 1</span>
        </div>
        <div
          className={`selectable-item${item2 ? ' selected' : ''}`}
          onClick={() => setItem2(!item2)}
        >
          <img src={item2Img} alt="Item 2" className="item-img-large" />
          <span>Item 2</span>
        </div>
      </div>
      <button className="send-btn" onClick={handleSend}>Enviar Comando</button>
      {status && <p className="status">{status}</p>}
    </div>
  );
}

export default App;