# Data Layer Spec

All events are pushed to `window.dataLayer`. Clear the previous ecommerce object first:

```js
window.dataLayer = window.dataLayer || [];
dataLayer.push({ ecommerce: null });
dataLayer.push({ event: "add_to_cart", ecommerce: { /* ... */ } });
```

## Shared objects

### Item

| Field | Type | Required | Notes |
|---|---|---|---|
| `item_id` | string | yes | SKU. Must match across all events |
| `item_name` | string | yes | |
| `price` | number | yes | Unit price after item-level discounts |
| `quantity` | integer ≥ 1 | yes | |
| `item_brand` | string | no | |
| `item_category` | string | no | Top-level category |
| `item_variant` | string | no | Color, size, etc. |
| `discount` | number | no | Unit discount amount |

### Ecommerce

| Field | Type | Required | Notes |
|---|---|---|---|
| `currency` | string (ISO 4217) | yes | e.g. `USD` |
| `value` | number | yes | Sum of `price * quantity` |
| `items` | Item[] | yes | At least one |

## Events

### `view_item`
Fires on product detail page load, once per page view.

### `add_to_cart`
Fires after the cart API confirms the add, not on button click.

### `begin_checkout`
Fires on first load of the checkout flow.

### `purchase`
Fires once on order confirmation. Guard against reloads (e.g. store fired `transaction_id`s in `sessionStorage`).

Additional required fields:

| Field | Type | Notes |
|---|---|---|
| `transaction_id` | string | Unique order ID |
| `tax` | number | |
| `shipping` | number | |
| `new_customer` | `"true"` \| `"false"` \| `"not_specified"` | Backend-determined. See README |

Optional: `coupon` (string), `payment_type` (string).

```js
dataLayer.push({
  event: "purchase",
  ecommerce: {
    transaction_id: "T-100245",
    currency: "USD",
    value: 349.98,
    tax: 31.50,
    shipping: 0,
    new_customer: "true",
    items: [
      { item_id: "SKU-1001", item_name: "Example Product", price: 174.99, quantity: 2 }
    ]
  }
});
```
