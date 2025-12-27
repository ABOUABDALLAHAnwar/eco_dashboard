import React from 'react';

function Header({ onAddAction, onUpdateProfile, onLogout }) {
  return (
    <header className="flex justify-between items-center p-4 bg-gray-900/80 backdrop-blur-sm text-white rounded-b-lg shadow-lg">
      <h1 className="text-2xl font-bold">Dashboard Éco</h1>
      <div className="flex gap-3">
        <button onClick={onAddAction} className="px-5 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition">
          Ajouter Action
        </button>
        <button onClick={onUpdateProfile} className="px-5 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition">
          Update Profile
        </button>
        <button onClick={onLogout} className="px-5 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition">
          Logout
        </button>
      </div>
    </header>
  );
}

export default Header;
