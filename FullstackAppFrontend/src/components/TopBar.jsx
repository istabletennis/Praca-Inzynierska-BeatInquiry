import React from 'react';
import PropTypes from 'prop-types';
import '../styles/TopBar.css';
import Logo from "../assets/logo.png"

const TopBar = ({ buttons }) => {
  return (
    <div className="top-bar">
      <div className="logo">
        <img src={Logo} alt="Logo" className="logo-image" />
      </div>
      <div className="nav-buttons">
        {buttons.map((button, index) => (
          <div key={index} className="nav-button">
            {button}
          </div>
        ))}
      </div>
    </div>
  );
};

TopBar.propTypes = {
  buttons: PropTypes.arrayOf(PropTypes.element).isRequired,
};

export default TopBar;