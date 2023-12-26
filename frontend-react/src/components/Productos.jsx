import React, { useState, useEffect } from 'react';
import '../App.css';
import { Card, Pagination } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Rating } from 'primereact/rating';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';


function ProductView({ category, searchKeyword }) {
  const [allProducts, setAllProducts] = useState([]);
  const [displayProducts, setDisplayProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [errorMessage, setErrorMessage] = useState('');
  const [rating, setRating] = useState({});
  const pageSize = 4;
  const token = 'testtoken';
  const serverUrl = 'http://localhost:8000/';

  useEffect(() => {
    let url;
    if (searchKeyword) {
      url = `${serverUrl}api/products/by-title?keyword=${encodeURIComponent(searchKeyword)}`;
    } else {
      url = category === 'all' ? `${serverUrl}api/products` : `${serverUrl}api/products/by-category?category=${encodeURIComponent(category)}`;
    }

    fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.ok === "yes" && Array.isArray(data.data) && data.data.length > 0) {
          setAllProducts(data.data);
          setDisplayProducts(data.data.slice(0, pageSize));
          setErrorMessage('');
        } else {
          setAllProducts([]);
          setDisplayProducts([]);
          setErrorMessage('No products found');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setErrorMessage('Error loading products');
      });
  }, [category, searchKeyword, serverUrl, token, pageSize, currentPage]);

  useEffect(() => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    setDisplayProducts(allProducts.slice(startIndex, endIndex));
  }, [currentPage, allProducts]);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const renderPagination = () => {
    const totalPages = Math.ceil(allProducts.length / pageSize);
    let items = [];
    for (let number = 1; number <= totalPages; number++) {
      items.push(
        <Pagination.Item key={number} active={number === currentPage} onClick={() => handlePageChange(number)}>
          {number}
        </Pagination.Item>,
      );
    }
    return <Pagination>{items}</Pagination>;
  };

  const handleRatingChange = (productId, newRating) => {
    setRating(prevRatings => ({
      ...prevRatings,
      [productId]: newRating
    }));
  };

  return (
    <div className="product-view">
      <h1>Products</h1>
      <div className="card-container">
        {displayProducts.length > 0 ? (
          displayProducts.map(product => (
            <Card key={product.id} className="card">
              <div className="card-img-container">
                <Card.Img variant="left" src={serverUrl + product.image} className="card-img" />
              </div>
              <Card.Body className="card-body">
                <Card.Title>{product.title}</Card.Title>
                <Card.Text>
                  {product.description}
                </Card.Text>
                <Card.Text>
                  Precio: ${product.price}
                </Card.Text>
                <div>
                <Rating value={rating[product.id] || product.rating.rate} 
                        onChange={(e) => handleRatingChange(product.id, e.value)} 
                        stars={5} 
                        cancel={false} />
                <span>({product.rating.count} reviews)</span>
              </div>
              </Card.Body>
            </Card>
          ))) : (
          <p>{errorMessage}</p>
        )}
      </div>
      {displayProducts.length > 0 && renderPagination()}
    </div>
  );
}

export default ProductView;