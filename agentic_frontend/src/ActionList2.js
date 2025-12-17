import React from 'react';
import PropTypes from 'prop-types';

const EcoActionList = ({ actions }) => (
  <div className="flex flex-col md:flex-row md:flex-wrap justify-center items-center">
    {actions.map((action, index) => (
      <div key={index} className="flex items-center m-2 bg-green-200 p-2 rounded-lg shadow-md">
        <img src={action.icon} alt={action.name} className="w-10 h-10 md:w-16 md:h-16 mr-2" />
        <span className="text-sm md:text-lg">{action.name}</span>
      </div>
    ))}
  </div>
);

EcoActionList.propTypes = {
  actions: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      icon: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default EcoActionList;