import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

const getItemById = (id) => listProducts.find((item) => item.itemId === id);

const reserveStockById = async (itemId, stock) => {
  await setAsync(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
};

app.get('/list_products', (req, res) => {
  res.json(listProducts.map((product) => ({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity,
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }

  const currentQuantity = item.initialAvailableQuantity - await getCurrentReservedStockById(itemId);

  res.json({
    itemId: item.itemId,
    itemName: item.itemName,
    price: item.price,
    initialAvailableQuantity: item.initialAvailableQuantity,
    currentQuantity,
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }

  const currentReservedStock = await getCurrentReservedStockById(itemId);

  if (currentReservedStock >= item.initialAvailableQuantity) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  await reserveStockById(itemId, currentReservedStock + 1);

  res.json({ status: 'Reservation confirmed', itemId });
});

const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
