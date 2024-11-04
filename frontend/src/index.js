import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // Optional: add any global styles here
import App from './App';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// Optional: measure and log performance, useful during development
reportWebVitals();
