import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [status, setStatus] = useState(null);
  const [populationData, setPopulationData] = useState([]);
  const [grid, setGrid] = useState([]);

  useEffect(() => {
    fetchStatus();
    fetchPopulationData();
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await axios.get('http://localhost:8000/status');
      setStatus(response.data);
      setGrid(response.data.grid);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  const fetchPopulationData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/population-data');
      setPopulationData(response.data.data);
    } catch (error) {
      console.error('Error fetching population data:', error);
    }
  };

  const handleStep = async () => {
    try {
      await axios.post('http://localhost:8000/step');
      fetchStatus();
      fetchPopulationData();
    } catch (error) {
      console.error('Error stepping simulation:', error);
    }
  };

  const handleReset = async () => {
    try {
      await axios.post('http://localhost:8000/reset');
      fetchStatus();
      fetchPopulationData();
    } catch (error) {
      console.error('Error resetting simulation:', error);
    }
  };

  const chartData = {
    labels: populationData.map(d => d.step),
    datasets: [
      {
        label: 'Australopithecus',
        data: populationData.map(d => d.Australopithecus),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Habilis',
        data: populationData.map(d => d.Habilis),
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
      },
      {
        label: 'Erectus',
        data: populationData.map(d => d.Erectus),
        borderColor: 'rgb(255, 205, 86)',
        backgroundColor: 'rgba(255, 205, 86, 0.5)',
      },
      {
        label: 'Heidelbergensis',
        data: populationData.map(d => d.Heidelbergensis),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: 'Neanderthal',
        data: populationData.map(d => d.Neanderthal),
        borderColor: 'rgb(153, 102, 255)',
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
      },
      {
        label: 'Denisovano',
        data: populationData.map(d => d.Denisovano),
        borderColor: 'rgb(255, 159, 64)',
        backgroundColor: 'rgba(255, 159, 64, 0.5)',
      },
      {
        label: 'Sapiens',
        data: populationData.map(d => d.Sapiens),
        borderColor: 'rgb(201, 203, 207)',
        backgroundColor: 'rgba(201, 203, 207, 0.5)',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Population Evolution',
      },
    },
  };

  return (
    <div className="App">
      <h1>PalVA - Paleo Simulation</h1>
      {status && (
        <div>
          <p>Year: {status.year}</p>
          <p>Total Population: {status.total_population}</p>
        </div>
      )}
      <button onClick={handleStep}>Step</button>
      <button onClick={handleReset}>Reset</button>
      <div>
        <h2>Grid</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(50, 10px)', gap: '1px' }}>
          {grid.flat().map((cell, index) => (
            <div
              key={index}
              style={{
                width: '10px',
                height: '10px',
                backgroundColor: cell ? 'black' : 'white',
                border: '1px solid #ccc'
              }}
            />
          ))}
        </div>
      </div>
      <div>
        <h2>Population Chart</h2>
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
}

export default App;