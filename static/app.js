const statusEl = document.getElementById('status');

const request = async (url, options = {}) => {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const data = await response.json();
      if (data.message) {
        message = data.message;
      }
    } catch (error) {
      // ignore json parsing errors
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
};

const setStatus = (message, tone = 'info') => {
  statusEl.textContent = message;
  statusEl.className = `status ${tone}`;
};

const clearStatus = () => {
  statusEl.textContent = '';
  statusEl.className = 'status';
};

const renderList = (listEl, items, formatter, onDelete) => {
  listEl.innerHTML = '';
  if (!items.length) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'empty';
    emptyItem.textContent = 'No entries yet.';
    listEl.appendChild(emptyItem);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = formatter(item);
    if (onDelete) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'danger';
      button.textContent = 'Delete';
      button.addEventListener('click', () => onDelete(item));
      li.appendChild(button);
    }
    listEl.appendChild(li);
  });
};

const loadCustomers = async () => {
  const listEl = document.getElementById('customer-list');
  const customers = await request('/customers');
  renderList(
    listEl,
    customers,
    (customer) => `${customer.id}. ${customer.first_name} ${customer.last_name} (${customer.email})`,
    async (customer) => {
      await request(`/customers/${customer.id}`, { method: 'DELETE' });
      setStatus('Customer deleted.', 'success');
      await loadCustomers();
    }
  );
};

const loadProducts = async () => {
  const listEl = document.getElementById('product-list');
  const products = await request('/products');
  renderList(
    listEl,
    products,
    (product) => `${product.id}. ${product.name} - $${Number(product.price).toFixed(2)}`,
    async (product) => {
      await request(`/products/${product.id}`, { method: 'DELETE' });
      setStatus('Product deleted.', 'success');
      await loadProducts();
    }
  );
};

const loadOrders = async () => {
  const listEl = document.getElementById('order-list');
  const orders = await request('/orders');
  renderList(
    listEl,
    orders,
    (order) =>
      `#${order.id} customer ${order.costumer_id} · product ${order.product_id} · qty ${order.quantity}`,
    async (order) => {
      await request(`/orders/${order.id}`, { method: 'DELETE' });
      setStatus('Order deleted.', 'success');
      await loadOrders();
    }
  );
};

const initForms = () => {
  const customerForm = document.getElementById('customer-form');
  customerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearStatus();
    const formData = new FormData(customerForm);
    const payload = Object.fromEntries(formData.entries());
    await request('/customers', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    customerForm.reset();
    setStatus('Customer created.', 'success');
    await loadCustomers();
  });

  const productForm = document.getElementById('product-form');
  productForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearStatus();
    const formData = new FormData(productForm);
    const payload = Object.fromEntries(formData.entries());
    payload.price = Number(payload.price);
    if (Number.isNaN(payload.price)) {
      setStatus('Price must be a number.', 'error');
      return;
    }
    await request('/products', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    productForm.reset();
    setStatus('Product created.', 'success');
    await loadProducts();
  });

  const orderForm = document.getElementById('order-form');
  orderForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearStatus();
    const formData = new FormData(orderForm);
    const payload = Object.fromEntries(formData.entries());
    payload.costumer_id = Number(payload.costumer_id);
    payload.product_id = Number(payload.product_id);
    payload.quantity = Number(payload.quantity);
    if ([payload.costumer_id, payload.product_id, payload.quantity].some(Number.isNaN)) {
      setStatus('Order fields must be numbers.', 'error');
      return;
    }
    await request('/orders', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    orderForm.reset();
    setStatus('Order created.', 'success');
    await loadOrders();
  });
};

const initRefreshButtons = () => {
  document.getElementById('refresh-customers').addEventListener('click', loadCustomers);
  document.getElementById('refresh-products').addEventListener('click', loadProducts);
  document.getElementById('refresh-orders').addEventListener('click', loadOrders);
};

const init = async () => {
  try {
    initForms();
    initRefreshButtons();
    await Promise.all([loadCustomers(), loadProducts(), loadOrders()]);
    clearStatus();
  } catch (error) {
    setStatus(error.message, 'error');
  }
};

document.addEventListener('DOMContentLoaded', init);
