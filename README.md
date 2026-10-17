# # Hartwell's Creamery website (sample)

A one-page website for a 100-year-old ice cream shop. Free to host on GitHub Pages.

## Files
| File | What it is |
|---|---|
| `build_site.py` | All the words, flavors, prices, hours and history. **Edit this file.** |
| `template.html` | The design (layout, colors, fonts). Only edit if you want to change the look. |
| `index.html` | The finished website, created by `build_site.py`. This is what gets published. |

## Make it yours
1. Open `build_site.py` and replace everything marked **SAMPLE**: shop name, town, address, phone,
   email, the history timeline, flavors, prices, reviews and hours.
2. Run `python3 build_site.py` in Terminal. It rewrites `index.html`.
3. Open `index.html` in your browser to check it.

The flavor of the day, the "Open now / Closed now" badge and today's row in the hours table update
automatically. Hours use the shop's time zone (`SHOP_TZ` in `template.html`, set to New York).

## Put it online free with GitHub Pages
1. Create a new public GitHub repo, e.g. `hartwells-creamery`.
2. Upload `index.html` (and the other files if you want to keep them together).
3. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   choose `main` and `/ (root)`, then **Save**.
4. After a minute or two the site is live at `https://your-username.github.io/hartwells-creamery/`.
5. To use a real address like `hartwellscreamery.com`, buy the domain and add it under
   **Settings → Pages → Custom domain**.

## Before launch
- Add real photos (shop front, the marble counter, the old crank, scoops). Put them in the repo and
  add `<img>` tags, or ask for help adding a photo gallery.
- Pints, catering, gift cards and the flavor list currently open the customer's phone or email app.
  When the shop is ready, these can link to an online ordering service (Toast, Square, Shopify) and
  an email-list service (Mailchimp, Square Marketing).
- Claim the shop's Google Business Profile so hours and photos match the website.
