import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="md:flex md:justify-between md:items-center md:px-10 py-3">
      <div className="px-8 py-3">
        <Link to="/" className="text-2xl font-bold text-gray-800 md:text-3xl">
          AppName
        </Link>
      </div>

      <nav className="md:mr-8">
        <Link to="/link1" className="block px-2 py-1 text-gray-800 hover:underline">
          Link 1
        </Link>
        <Link to="/link2" className="block px-2 py-1 text-gray-800 hover:underline">
          Link 2
        </Link>
        <Link to="/link3" className="block px-2 py-1 text-gray-800 hover:underline">
          Link 3
        </Link>
      </nav>
    </header>
  );
};

export default Header;