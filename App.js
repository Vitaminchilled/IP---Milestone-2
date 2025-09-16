/*import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <a href="http://localhost:5000/api/top-films" target="_blank" rel="noopener noreferrer">
          <button>View Top 5 Films (JSON)</button>
        </a>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

function MyButton() {
  return (
    <button>I'm a button</button>
  );
}

export default App;
*/

import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [films, setFilms] = useState([]);

  useEffect(() => {
    fetch("/api/top-films")
      .then(response => response.json())
      .then(data => setFilms(data))
      .catch(error => console.error("Error fetching films:", error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sakila Movie Store</h1>
        <h2>Top 5 Rented Films</h2>

        {films.length > 0 ? (
          <ul>
            {films.map((film) => (
              <li key={film.film_id}>
                {film.title} — rented {film.rental_count} times
              </li>
            ))}
          </ul>
        ) : (
          <p>Loading films...</p>
        )}
      </header>
    </div>
  );
}

export default App;
