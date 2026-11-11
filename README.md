# Avern — Nocturne without the 3D bottle

This project publishes the original [Nocturne website](https://github.com/ProPanda32/Nocturne) at a separate GitHub Pages address. Its build starts from a pinned original commit and removes only the 3D bottle model and its loader. The original page layout, background image, particles, navigation, text, and other scene elements come from the original site.

The original repository is not modified. `scripts/remove-bottle.py` contains the small build change; `.github/workflows/deploy-pages.yml` builds and publishes it. The build also sets the Pages base path to `/Avern/` so the original assets load at the new address.
