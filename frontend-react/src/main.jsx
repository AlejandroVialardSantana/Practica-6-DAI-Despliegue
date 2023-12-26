// main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
// Bootstrap Bundle JS (opcional)
import 'bootstrap/dist/js/bootstrap.bundle.min';
import 'primereact/resources/themes/saga-blue/theme.css'; //tema
import 'primereact/resources/primereact.min.css'; //core css
import 'primeicons/primeicons.css'; //icons


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);