import React, { useState } from 'react';
import NavScrollExample from './components/Navegacion';
import ProductView from './components/Productos';

function App() {
  const [category, setCategory] = useState('all');
  const [searchKeyword, setSearchKeyword] = useState('');

  const handleCategoryChange = (newCategory) => {
    setCategory(newCategory);
  };

  const handleSearch = (keyword) => {
    setSearchKeyword(keyword);
  };

  return (
    <div className="App">
      <NavScrollExample onCategoryChange={handleCategoryChange} onSearch={handleSearch} />
      <ProductView category={category} searchKeyword={searchKeyword} />
    </div>
  );
}

export default App;
