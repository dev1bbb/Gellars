# Gellar's Snack Bar website

A Streamlit site for Gellar's Snack Bar in Manomet, MA: menu with prices, an order builder, hours with a live open/closed sign, a map, and links to the shop's own Toast page for online checkout.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repo. Keep `app.py`, `menu_data.py`, `requirements.txt` and the `.streamlit` folder at the top level.
2. Go to share.streamlit.io, sign in with GitHub, and click **Create app**.
3. Pick the repo and branch, set the main file to `app.py`, and deploy.

Every push to the branch redeploys the site automatically.

## Updating the menu

Everything lives in `menu_data.py`. Change a price, add an item or edit the hours there, push, and the site updates. `app.py` never needs to change for menu edits.

- `price=None` shows "Ask at the window" and can't be added to an order.
- `out_of_stock=True` greys the item out and hides its Add button.

## Before launch

- [ ] Get ice cream prices (cones, cups, toppings, sundaes, floats, shakes) from the menu board and fill them in.
- [ ] Get Friday seafood prices.
- [ ] Replace `FLAVORS_SPOTTED` with the real flavor list.
- [ ] Confirm hours for each season.
- [ ] Confirm the Toast online ordering page is switched on.
- [ ] Ask the owner for real photos of the stand and food.

## How ordering works

Customers build an order on the site and see a running total. Checkout goes through Gellar's existing Toast page, so payment lands in the shop's own register with no new payment system to maintain. For phone orders, the "Read your order over the phone" panel gives a copyable summary.

The order on this site doesn't transfer into Toast. Customers re-add items there. Deep integration would need Toast's partner API.
