const express = require('express');
const app = express();
const port = 3001;

app.get('/products', (req, res) => {
  res.json({
    products: [
      { id: 1, name: 'Notebook', price: 3000 },
      { id: 2, name: 'Mouse', price: 100 },
      { id: 3, name: 'Teclado Mecânico', price: 450 },
      { id: 4, name: 'Monitor 24"', price: 1200 },
      { id: 5, name: 'Cadeira Gamer', price: 1500 }
    ]
  });
});

app.listen(port, () => {
  console.log(`Products API running on port ${port}`);
});
