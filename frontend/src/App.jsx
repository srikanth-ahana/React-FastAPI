import React from 'react';
import './App.css';
import FruitList from './components/Fruits';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>FastAPI React App</h1>
      </header>
      <main>
        <FruitList />
      </main>
    </div>
  );
};

export default App;