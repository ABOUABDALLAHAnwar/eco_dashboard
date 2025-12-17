import React from 'react';

const DashboardCard = ({ carbonFootprintReduction }) => {
  return (
    <div className="flex flex-col items-center justify-center bg-white shadow-lg rounded-lg p-4 m-2 sm:m-4 md:m-6 lg:m-8">
      <h2 className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold text-gray-700">Carbon Footprint Reduction</h2>
      <div className="w-full mt-4">
        <div className="shadow w-full bg-gray-200">
          <div className="bg-green-500 text-xs leading-none py-1 text-center text-white" style={{ width: `${carbonFootprintReduction}%` }}>
            {carbonFootprintReduction}%
          </div>
        </div>
      </div>
      <p className="text-sm sm:text-base md:text-lg lg:text-xl text-gray-500 mt-4">
        You have reduced your carbon footprint by {carbonFootprintReduction}%
      </p>
    </div>
  );
};

export default DashboardCard;