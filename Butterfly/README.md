# Butterfly 🦋

A stunning, production-quality frontend for **Butterfly** — helping VCs determine, spot, and trace market trends before they become big. Surfacing resources and insights VCs can rely on. Built with React, TypeScript, and modern web technologies for optimal performance and user experience.

## ✨ Features

### Core Functionality
- **🔥 Top 3 Trends Dashboard**: View the hottest trending technologies with momentum scores and 30-day changes
- **📊 Subtrends Explorer**: Dive deep into subsectors with momentum metrics and trend indicators  
- **🏢 Startup Discovery**: Explore the most promising startups in each subtrend
- **⚙️ Settings Panel**: Configure API endpoints or use local mock data

### Design & UX
- **🎨 Premium Dark Theme**: Sleek glass-morphism UI with teal/blue gradient backgrounds
- **📱 Mobile-first**: Fully responsive design optimized for all screen sizes
- **♿ Accessibility**: WCAG AA compliant with keyboard navigation and screen reader support
- **🎭 Smooth Animations**: Framer Motion powered micro-interactions and page transitions
- **💨 Fast Performance**: Optimized for Lighthouse scores with lazy loading and efficient caching

### Technical Excellence
- **🔧 API-Ready Architecture**: Seamlessly switch between mock data and live GCP backend
- **🔄 Smart Caching**: In-memory caching with automatic expiration and retry logic
- **🛡️ Error Handling**: Graceful fallbacks with friendly error messages
- **🧪 Type Safety**: Full TypeScript coverage for robust development

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Modern web browser

### Development Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd butterfly

# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:8080
```

### Environment Configuration

Create a `.env` file (see `.env.example`):

```env
# Optional: Connect to your GCP backend
VITE_API_BASE_URL=https://your-api.cloudfunctions.net

# If not set, the app runs with local mock data
```

## 🏗️ Architecture

### Project Structure
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # shadcn/ui components
│   ├── butterfly-header.tsx # Butterfly branding header
│   ├── hero-section.tsx # Landing hero with top 3 trends
│   ├── subtrends-section.tsx # Subtrends grid
│   └── subtrend-detail-drawer.tsx # Startup details
├── lib/
│   ├── api.ts           # API layer with caching & retry
│   └── utils.ts         # Utility functions
├── mocks/               # Local JSON mock data
├── types/               # TypeScript definitions
└── pages/
    └── Index.tsx        # Main application page
```

### Data Flow
1. **API Layer**: Handles data fetching with retry logic and caching
2. **Mock Fallback**: Automatically uses local JSON when API unavailable
3. **State Management**: React hooks for lightweight state management
4. **Error Boundaries**: Graceful error handling throughout the app

## 🎯 Core Views

### 1. Hero Section (Top 3 Trends)
- Butterfly header with logo and tagline "Catch the breeze before it turns into a hurricane"
- Three trend cards with clear visual hierarchy (Top 1 > Top 2 > Top 3)
- Glass-morphism design with hover parallax effects
- Animated momentum meters and sparkle effects for top trends
- Moving background media per trend reflecting its industry

### 2. Subtrends Grid
- Responsive grid layout of subtrend tiles
- Momentum metrics without sparklines (numerical indicators only)
- Sortable by momentum score or alphabetical
- Smooth scroll reveal animations
- Butterfly branding: "Spotted early by Butterfly"

### 3. Subtrend Detail Drawer
- Slide-over drawer (desktop) / full-screen sheet (mobile)
- Detailed momentum analytics and trend visualization
- Top 3 startups with logos, descriptions, and external links
- Keyboard navigation (ESC to close)
- Microcopy: "These startups ride the wave spotted by Butterfly"

## 🔌 API Integration

### Endpoints
The app expects these RESTful endpoints:

```typescript
GET /trends?limit=3
// Returns: Trend[]

GET /trends/{id}/subtrends  
// Returns: Subtrend[]

GET /subtrends/{id}/startups?limit=3
// Returns: Startup[]
```

### Data Types
```typescript
interface Trend {
  id: string;
  name: string;
  summary: string;
  momentum_score: number;    // 0-100
  change_30d_pct: number;   // percentage
  image_url?: string;
  bg_media_url?: string;    // Optional moving background media
}

interface Subtrend {
  id: string;
  trend_id: string;
  name: string;
  description: string;
  momentum_score: number;
  change_30d_pct: number;   // 30-day percentage change
}

interface Startup {
  id: string;
  name: string;
  one_liner: string;
  logo_url?: string;
  tags: string[];
  website_url: string;
}
```

## 📱 Deployment

### Firebase Hosting

```bash
# Build for production
npm run build

# Install Firebase CLI (if not already installed)
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase Hosting
firebase init hosting
# ✅ Select "Use an existing project" or create new
# ✅ Set public directory to: dist
# ✅ Configure as single-page app: Yes
# ✅ Set up automatic builds with GitHub: Optional

# Deploy to Firebase
firebase deploy

# Your app is now live at: https://your-project.firebaseapp.com
```

### Environment Variables for Production

Set your production API URL:
```bash
# In your CI/CD or build environment
export VITE_API_BASE_URL=https://your-production-api.com

# Then build
npm run build
```

## 🧪 Testing

```bash
# Run unit tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run linting
npm run lint

# Type checking
npm run type-check
```

## 🎨 Design System

### Color Palette
- **Background**: Dark navy/slate/teal gradient for premium feel
- **Surfaces**: Glassy dark neutrals with teal-blue glow
- **Primary**: Electric Blue (#3B82F6) for highlights and CTAs
- **Signature**: Vivid Yellow (#FACC15) for emerging trends (sparingly)
- **Momentum Signals**: 
  - Up/Growth: Neon teal-green (#14B8A6)
  - Neutral: Soft amber (#F59E0B)
  - Down: Warm red (#EF4444)

### Components
- **ButterflyHeader**: Prominent header with logo and tagline
- **MomentumBadge**: Displays scores with trend indicators (no sparklines)
- **TrendCard**: Interactive cards with rank hierarchy and animated progress meters
- **SectionSeparator**: Animated dividers between major sections
- **LoadingSkeleton**: Shimmer loading states for all content types

### Animations
- Entrance animations with staggered delays
- Hover parallax effects on cards
- Smooth scroll-to-section navigation
- Reduced motion support for accessibility
- Moving background media for trend cards (low-bandwidth, optional)

## 🔧 Configuration

### Settings Panel Features
- **API URL Configuration**: Set/change backend endpoint at runtime
- **Connection Testing**: Test API connectivity with latency display
- **Mock Data Toggle**: Switch between live API and local mocks
- **Reduced Motion Toggle**: Enable/disable animated backgrounds

### Local Storage
Settings persist across sessions:
- `apiBaseUrl`: Backend API endpoint
- `useMocks`: Whether to use local mock data

## 🤝 Contributing

### Development Guidelines
1. **Design System First**: Use semantic tokens, never hardcode colors
2. **Mobile-first**: Design for mobile, enhance for desktop
3. **Accessibility**: Include proper ARIA labels and keyboard navigation
4. **Performance**: Optimize images, lazy load content, minimize bundle size
5. **Type Safety**: Maintain 100% TypeScript coverage

### Code Style
- ESLint + Prettier for formatting
- Conventional commit messages
- Component-driven architecture
- Responsive design utilities from Tailwind

## 🦋 Butterfly Brand Identity

### Mission & Values
Butterfly helps VCs **catch the breeze before it turns into a hurricane** by:
- Spotting early market shifts and emerging patterns
- Providing reliable signals for confident investment decisions
- Connecting emerging trends to startup opportunities
- Surfacing resources and insights VCs can trust

### Brand Elements
- **Logo**: Butterfly symbol (placeholder for uploaded SVG)
- **Tagline**: "Catch the breeze before it turns into a hurricane"
- **Colors**: Premium dark theme with teal/blue gradients
- **Voice**: Professional, trustworthy, forward-looking

### Microcopy Integration
Strategic placement of VC-focused messaging:
- Hero section: "Insights VCs can rely on"
- Subtrends: "Spotted early by Butterfly"
- Startup details: "These startups ride the wave spotted by Butterfly"

## 🚀 Performance

### Optimization Features
- **Tree Shaking**: Only used components included in bundle
- **Code Splitting**: Dynamic imports for route-based splitting
- **Media Optimization**: Lightweight video loops with fallbacks
- **Caching Strategy**: Intelligent cache invalidation
- **Reduced Motion**: Respects user accessibility preferences

### Lighthouse Scores Target
- **Performance**: >90
- **Accessibility**: >95  
- **Best Practices**: >90
- **SEO**: >90

## 📊 Analytics Ready

The app is prepared for analytics integration:
- Component tracking hooks
- User interaction events
- Performance monitoring
- Error tracking and reporting

## 🔐 Security

- **No Server Secrets**: Frontend-only, no API keys in client code
- **HTTPS Only**: Secure connections enforced
- **Content Security Policy**: XSS protection headers
- **Input Validation**: All user inputs sanitized

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting guide
2. Search existing GitHub issues
3. Create a new issue with detailed reproduction steps

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ by Butterfly using React, TypeScript, Tailwind CSS, and Framer Motion**

*Catch the breeze before it turns into a hurricane.* 🦋