# Tailwind CSS Production Setup

## Installation Steps

1. **Install Node.js** (if not already installed)
   ```bash
   # Download from https://nodejs.org/
   ```

2. **Install Tailwind CSS**
   ```bash
   npm install
   ```

3. **Build CSS for Development**
   ```bash
   npm run build-css
   ```

4. **Build CSS for Production**
   ```bash
   npm run build-css-prod
   ```

## Benefits of Local Tailwind

✅ **Smaller Bundle Size**: Only includes used classes (~10-50KB vs 3MB)
✅ **Better Performance**: No external CDN dependency
✅ **Offline Support**: Works without internet
✅ **Custom Configuration**: Full control over theme and plugins
✅ **Production Optimization**: Minified and purged CSS
✅ **Better Caching**: Can be cached with your static files

## Development Workflow

1. Run `npm run build-css` during development (watches for changes)
2. Make HTML/template changes
3. Tailwind automatically rebuilds CSS
4. For production: `npm run build-css-prod`

## File Structure
```
static/
├── css/
│   ├── input.css      # Source file with @tailwind directives
│   ├── output.css     # Generated file (don't edit)
│   └── hero-animations.css
└── js/
    └── hero-interactions.js

tailwind.config.js     # Tailwind configuration
package.json          # Node.js dependencies
```

## Production Deployment

Add to your deployment script:
```bash
npm install
npm run build-css-prod
python manage.py collectstatic --noinput
```