import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axiosConfig';
import { useAuth } from '../context/AuthContext';
import TopBar from './TopBar';
import '../styles/TopBar.css';
import '../styles/Dashboard.css';

function Dashboard() {
  const auth = useAuth();
  const navigate = useNavigate();

  const [inputText, setInputText] = useState('');
  const [responseText, setResponseText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [selectedModel, setSelectedModel] = useState('');
  const [selectedDecade, setSelectedDecade] = useState('');

  const modelOptions = [
    { label: 'Beat Inquiry', value: 'ft:gpt-3.5-turbo-0125:personal:bi-0125-v2:9MLSGTSp' },
    { label: 'GPT4', value: 'gpt-4' },
    { label: 'GPT3.5', value: 'gpt-3.5-turbo' },
  ];

  const decadeOptions = [
    { label: '50s', value: '50s' },
    { label: '60s', value: '60s' },
    { label: '70s', value: '70s' },
    { label: '80s', value: '80s' },
    { label: '90s', value: '90s' },
    { label: '00s', value: '00s' },
    { label: '10s', value: '10s' },
    { label: '20s', value: '20s' },
  ];

  const handleModelChange = (event) => {
    setSelectedModel(event.target.value);
  };

  const handleDecadeChange = (event) => {
    setSelectedDecade(event.target.value);
  };

  useEffect(() => {
    if (!auth.user) {
      navigate('/');
    }
  }, [auth.user, navigate]);

  function handleLogout() {
    auth.logout();
    navigate('/');
  }

  function handleAnalysisNav() {
    navigate('/analysis');
  }

  const handleButtonClick = () => {
    setLoading(true);
    setError(null);
    setResponseText('');

    axios.post('/lyrics', {
        decade: selectedDecade,
        model: selectedModel
    })
      .then(response => {
        setResponseText(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  };

  const handleSaveLyrics = () => {
    axios.put('/save-lyrics', {
      "lyrics": responseText,
      "model": selectedModel,
      "decade": selectedDecade
    })
      .then(response => {
        alert('Lyrics saved successfully!');
      })
      .catch(error => {
        setError(error.message);
      });
  };

  if (!auth.user) {
    return null;
  }

  const buttons = [
      <button onClick={handleAnalysisNav} className="nav-link">Analysis</button>,
      <button onClick={handleLogout} className="nav-link">Logout</button>
  ];

  return (
    <div>
      <TopBar buttons={buttons} />
      <div class="split left">
        <div class="centered">
          <div class="description">
            <h2>Welcome to your BeatInquiry, {auth.user.username}!</h2>

            <p>
              Have you ever wondered if a song's lyrics can serve as a telltale sign
              of the decade they were written in,
            </p>
            <p>much like the sound of the music itself?</p>
            <br></br>
            <p>Or perhaps you've noticed the recurring themes in </p>
            <p>
              top radio love songs and wondered if there's more to it than just
              coincidence?
            </p>
            <br></br>
            <p>So did we!</p>
            <br></br>
            <p>
              Our goal was to determine whether we could accurately estimate the
              decade of production of these{" "}
            </p>
            <p>
              heart-wrenching love songs based solely on the lyrics — the phrases,
              words, and sentiments we can see and hear.
            </p>
            <p>
              After all, love comes in different shapes, sizes, and sets of nouns.
            </p>
            <br></br>
            <p>And without further ado, let's delve into our findings...</p>
            <br></br>
          </div>
          <div class="select-box">
            <select
              class="select"
              id="decade"
              value={selectedDecade}
              onChange={handleDecadeChange}
            >
              <option class="option" value="" disabled>
                Select Decade
              </option>
              {decadeOptions.map((decadeOption) => (
                <option
                  class="option"
                  key={decadeOption.value}
                  value={decadeOption.value}
                >
                  {decadeOption.label}
                </option>
              ))}
            </select>
          </div>
          <div class="select-box">
            <select
              class="select"
              id="model"
              value={selectedModel}
              onChange={handleModelChange}
            >
              <option class="option" value="" disabled>
                Select Model
              </option>
              {modelOptions.map((modelOption) => (
                <option
                  class="option"
                  key={modelOption.value}
                  value={modelOption.value}
                >
                  {modelOption.label}
                </option>
              ))}
            </select>
          </div>
          <div
            style={{
              paddingTop: "1px",
              paddingBottom: "5px",
            }}
          >
            <button class="inquire-button" onClick={handleButtonClick}>
              Inquire
            </button>
          </div>
          <div
            style={{
              paddingTop: "5px",
              paddingBottom: "5px",
            }}
          >
            <button class="inquire-button" onClick={handleSaveLyrics}>
              Save
            </button>
          </div>
        </div>
      </div>
      <div class="split right">
        <div class="centered">
          <table>
            <div>
              {loading && (
                <p
                  style={{
                    whiteSpace: "pre-wrap",
                    paddingTop: "100px",
                    paddingBottom: "100px",
                  }}
                >
                  Loading...
                </p>
              )}
              {error && <p>Error: {error.message}</p>}
              {responseText && (
                <p
                  style={{
                    whiteSpace: "pre-wrap",
                    paddingTop: "100px",
                    paddingBottom: "100px",
                  }}
                >
                  {responseText}
                </p>
              )}
            </div>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
