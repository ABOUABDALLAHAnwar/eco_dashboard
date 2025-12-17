import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 p-6 mt-8">
      <div className="container mx-auto flex flex-wrap justify-between items-center">
        <div className="w-full sm:w-auto self-center">
          <div className="text-xl font-semibold text-white">Company Name</div>
          <div className="text-gray-400 mt-2">1234 Street, City, Country</div>
          <div className="text-gray-400 mt-2">Email: info@company.com</div>
          <div className="text-gray-400 mt-2">Phone: +1234567890</div>
        </div>
        <div className="flex items-center mt-4 sm:mt-0">
          <a href="https://facebook.com" className="text-gray-400 hover:text-white ml-4">
            <i className="fab fa-facebook-f"></i>
          </a>
          <a href="https://twitter.com" className="text-gray-400 hover:text-white ml-4">
            <i className="fab fa-twitter"></i>
          </a>
          <a href="https://linkedin.com" className="text-gray-400 hover:text-white ml-4">
            <i className="fab fa-linkedin-in"></i>
          </a>
          <a href="https://instagram.com" className="text-gray-400 hover:text-white ml-4">
            <i className="fab fa-instagram"></i>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

