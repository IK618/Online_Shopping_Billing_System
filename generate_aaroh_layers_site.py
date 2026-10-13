import sys

site_html = """<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SMARTCART // HYPER-DIMENSION LOGISTICS & RETAIL</title>
  
  <!-- Fonts: Rajdhani, JetBrains Mono, Syne -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Rajdhani:wght@500;600;700;800&family=Syne:wght@700;800;900&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <!-- Three.js (3D Engine) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <!-- Vanilla Tilt (3D Parallax) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.1/vanilla-tilt.min.js"></script>

  <!-- Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Rajdhani"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
            display: ['"Syne"', 'sans-serif'],
          },
          colors: {
            cyber: {
              bg: '#040508',
              surface: '#0B0F15',
              card: '#0E141E',
              border: 'rgba(0, 243, 255, 0.22)',
              borderPink: 'rgba(237, 42, 190, 0.3)',
              cyan: '#00F3FF',
              magenta: '#ED2ABE',
              pink: '#FF3366',
              green: '#00FF96',
              muted: '#7F93A5',
              subtle: '#141D2B'
            }
          }
        }
      }
    }
  </script>

  <style>
    /* Selection & Scrollbar */
    ::selection {
      background: #00F3FF;
      color: #040508;
    }
    ::-webkit-scrollbar {
      width: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #040508;
    }
    ::-webkit-scrollbar-thumb {
      background: #00F3FF;
      box-shadow: 0 0 10px #00F3FF;
    }

    body {
      background-color: #040508;
      color: #E6EDF3;
      font-family: 'Rajdhani', sans-serif;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* Cyber Tech Grid Background Pattern */
    .cyber-grid-bg {
      background-size: 40px 40px;
      background-image: 
        linear-gradient(to right, rgba(0, 243, 255, 0.04) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 243, 255, 0.04) 1px, transparent 1px);
    }

    /* Scanline Sweeper */
    .cyber-scanline {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 99;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
      background-size: 100% 3px, 6px 100%;
      opacity: 0.6;
    }

    /* Glow utilities */
    .glow-cyan {
      box-shadow: 0 0 25px rgba(0, 243, 255, 0.35), inset 0 0 15px rgba(0, 243, 255, 0.1);
    }
    .glow-magenta {
      box-shadow: 0 0 25px rgba(237, 42, 190, 0.35), inset 0 0 15px rgba(237, 42, 190, 0.1);
    }
    .text-glow-cyan {
      text-shadow: 0 0 14px rgba(0, 243, 255, 0.8), 0 0 30px rgba(0, 243, 255, 0.4);
    }
    .text-glow-magenta {
      text-shadow: 0 0 14px rgba(237, 42, 190, 0.8), 0 0 30px rgba(237, 42, 190, 0.4);
    }

    /* Cyber HUD Beveled Corners */
    .cyber-bracket {
      position: relative;
    }
    .cyber-bracket::before, .cyber-bracket::after {
      content: '';
      position: absolute;
      width: 12px;
      height: 12px;
      pointer-events: none;
      border-color: #00F3FF;
      border-style: solid;
    }
    .cyber-bracket::before {
      top: -1px;
      left: -1px;
      border-width: 2px 0 0 2px;
    }
    .cyber-bracket::after {
      bottom: -1px;
      right: -1px;
      border-width: 0 2px 2px 0;
      border-color: #ED2ABE;
      filter: drop-shadow(0 0 6px #ED2ABE);
    }

    /* 3D Store Cards */
    .cyber-card {
      background: radial-gradient(130% 120% at 50% 0%, rgba(0, 243, 255, 0.08), rgba(11, 15, 21, 0.95) 70%);
      border: 1px solid rgba(0, 243, 255, 0.25);
      border-radius: 14px;
      transform-style: preserve-3d;
      perspective: 1000px;
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .cyber-card:hover {
      border-color: #00F3FF;
      box-shadow: 0 0 35px rgba(0, 243, 255, 0.28), 0 0 60px rgba(237, 42, 190, 0.15);
      transform: translateY(-6px);
    }

    /* 🏷️ 3D FLOATING HOLOGRAPHIC PRICE BADGE */
    .cyber-floating-price {
      position: absolute;
      bottom: 12px;
      right: 12px;
      transform: translateZ(58px);
      background: rgba(4, 5, 8, 0.9);
      border: 1px solid #00F3FF;
      border-radius: 8px;
      padding: 5px 12px;
      box-shadow: 0 0 20px rgba(0, 243, 255, 0.45);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 30;
      pointer-events: none;
    }
    .cyber-card:hover .cyber-floating-price {
      transform: translateZ(78px) scale(1.1);
      border-color: #ED2ABE;
      box-shadow: 0 0 30px rgba(237, 42, 190, 0.7);
    }

    /* Custom Cursor */
    #cyber-cursor-dot {
      position: fixed;
      top: 0; left: 0;
      width: 6px; height: 6px;
      background: #00F3FF;
      box-shadow: 0 0 10px #00F3FF;
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      transform: translate(-50%, -50%);
    }
    #cyber-cursor-ring {
      position: fixed;
      top: 0; left: 0;
      width: 36px; height: 36px;
      border: 1.5px solid rgba(0, 243, 255, 0.5);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9998;
      transform: translate(-50%, -50%);
      transition: width 0.2s, height 0.2s, border-color 0.2s;
    }
    body.cursor-hover #cyber-cursor-ring {
      width: 58px; height: 58px;
      border-color: #ED2ABE;
      box-shadow: 0 0 20px rgba(237, 42, 190, 0.6);
    }

    /* Marquee Track */
    .cyber-marquee-track {
      display: flex;
      gap: 2rem;
      animation: marqueeScroll 24s linear infinite;
      width: max-content;
    }
    @keyframes marqueeScroll {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }
  </style>
</head>
<body class="min-h-screen cyber-grid-bg relative selection:bg-cyber-cyan selection:text-cyber-bg">

  <!-- Subtle CRT Scanline overlay -->
  <div class="cyber-scanline"></div>

  <!-- Interactive Custom Cursor -->
  <div id="cyber-cursor-dot" class="hidden md:block"></div>
  <div id="cyber-cursor-ring" class="hidden md:block"></div>

  <!-- HUD Top Header (Layers / Aaroh Aesthetic) -->
  <header class="sticky top-0 z-50 px-4 py-3 bg-[#040508]/85 backdrop-blur-md border-b border-cyber-border">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      
      <!-- Logo Branding -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-cyber-cyan to-cyber-magenta p-[1px]">
          <div class="w-full h-full bg-[#040508] rounded-lg flex items-center justify-center font-display font-black text-xl text-cyber-cyan">
            S
          </div>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-display font-black tracking-wider text-xl text-white">SMARTCART</span>
            <span class="px-2 py-0.5 text-[10px] font-mono font-bold tracking-widest uppercase bg-cyber-cyan/10 border border-cyber-cyan text-cyber-cyan rounded">
              AAROH_ENGINE v4.2
            </span>
          </div>
          <p class="text-[10px] font-mono tracking-widest text-cyber-muted uppercase">AUTONOMOUS 3D LOGISTICS // BANKER'S ROUNDING</p>
        </div>
      </div>

      <!-- Telemetry Status Bar -->
      <div class="hidden lg:flex items-center gap-6 text-xs font-mono">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-cyber-green animate-ping"></span>
          <span class="text-cyber-green font-bold">GRID ONLINE</span>
        </div>
        <div class="text-cyber-muted">|</div>
        <div>
          <span class="text-cyber-muted">TAX ENGINE:</span>
          <span class="text-white font-bold">5% GST STATUTORY</span>
        </div>
        <div class="text-cyber-muted">|</div>
        <div>
          <span class="text-cyber-muted">LOGISTICS:</span>
          <span class="text-cyber-cyan font-bold">DIJKSTRA SHORTEST PATH</span>
        </div>
      </div>

      <!-- Header Action: Cart Drawer Trigger -->
      <div class="flex items-center gap-3">
        <button onclick="toggleCartDrawer(true)" class="relative px-5 py-2.5 rounded-lg bg-[#0E141E] border border-cyber-border hover:border-cyber-cyan transition-all flex items-center gap-3 group">
          <i data-lucide="shopping-cart" class="w-4 h-4 text-cyber-cyan group-hover:scale-110 transition-transform"></i>
          <span class="text-xs font-mono font-bold uppercase tracking-wider text-white">DISPATCH CART</span>
          <span id="cartCountBadge" class="px-2 py-0.5 rounded text-xs font-mono font-bold bg-cyber-cyan text-[#040508]">0</span>
          <span id="headerCartTotal" class="hidden sm:inline text-xs font-mono text-cyber-muted">₹0.00</span>
        </button>
      </div>

    </div>
  </header>

  <!-- Main Experience Wrapper -->
  <main class="max-w-7xl mx-auto px-4 pt-6 pb-24">
    
    <!-- Hero Spotlight Section with 3D Cyber WebGL Canvas -->
    <div class="relative rounded-2xl bg-gradient-to-b from-[#0B0F15] to-[#040508] border border-cyber-border p-6 sm:p-10 mb-12 overflow-hidden cyber-bracket glow-cyan">
      
      <!-- Three.js Canvas Container -->
      <div id="hero-canvas-wrap" class="absolute inset-0 pointer-events-none z-0 opacity-70">
        <canvas id="three-hero-canvas" class="w-full h-full"></canvas>
      </div>

      <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        
        <!-- Left: Editorial Headline & Terminal Filters -->
        <div class="lg:col-span-6 space-y-5">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-cyber-cyan/10 border border-cyber-cyan text-cyber-cyan font-mono text-xs tracking-widest uppercase">
            <i data-lucide="zap" class="w-3.5 h-3.5 text-cyber-cyan"></i>
            NEXT-GEN RECONCILIATION SUITE
          </div>

          <h1 class="font-display text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight uppercase">
            AUTONOMOUS <span class="text-cyber-cyan text-glow-cyan">RETAIL</span> & <span class="text-cyber-magenta text-glow-magenta">3D LOGISTICS</span>
          </h1>

          <p class="font-sans text-lg text-cyber-muted leading-relaxed">
            Engineered for sub-millisecond billing accuracy. Explore products with interactive WebGL orbit models, live Dijkstra routing telemetry, and certified 5% GST tax breakdown.
          </p>

          <!-- Search & Department Filters -->
          <div class="space-y-3 pt-2">
            <div class="relative">
              <i data-lucide="search" class="w-4 h-4 text-cyber-muted absolute left-3.5 top-1/2 -translate-y-1/2"></i>
              <input type="text" id="searchInput" oninput="filterProducts()" placeholder="SEARCH INVENTORY CATALOG, SKU, SPEC..." 
                class="w-full pl-10 pr-4 py-2.5 rounded-lg bg-[#0E141E] border border-cyber-border text-white text-xs font-mono focus:outline-none focus:border-cyber-cyan focus:ring-1 focus:ring-cyber-cyan transition-all">
            </div>

            <!-- Dept Pills -->
            <div class="flex flex-wrap gap-2" id="categoryFilterContainer">
              <button onclick="setCategoryFilter('ALL')" class="category-pill active px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-cyan bg-cyber-cyan text-[#040508] transition-all">ALL DEPTS</button>
              <button onclick="setCategoryFilter('Electronics')" class="category-pill px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-border bg-[#0E141E] text-cyber-muted hover:text-white hover:border-cyber-cyan transition-all">ELECTRONICS</button>
              <button onclick="setCategoryFilter('Furniture')" class="category-pill px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-border bg-[#0E141E] text-cyber-muted hover:text-white hover:border-cyber-cyan transition-all">FURNITURE</button>
              <button onclick="setCategoryFilter('Home & Kitchen')" class="category-pill px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-border bg-[#0E141E] text-cyber-muted hover:text-white hover:border-cyber-cyan transition-all">KITCHEN</button>
              <button onclick="setCategoryFilter('Fashion')" class="category-pill px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-border bg-[#0E141E] text-cyber-muted hover:text-white hover:border-cyber-cyan transition-all">FASHION</button>
              <button onclick="setCategoryFilter('Groceries')" class="category-pill px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-border bg-[#0E141E] text-cyber-muted hover:text-white hover:border-cyber-cyan transition-all">GROCERIES</button>
            </div>
          </div>

          <!-- Quick Metrics Strip -->
          <div class="flex items-center gap-6 pt-3 border-t border-cyber-border/60 text-xs font-mono text-cyber-muted">
            <span class="flex items-center gap-1.5 text-cyber-green">
              <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
              AUTHENTICITY VERIFIED
            </span>
            <span>//</span>
            <span class="flex items-center gap-1.5 text-cyber-cyan">
              <i data-lucide="cpu" class="w-3.5 h-3.5"></i>
              THREE.JS 120 FPS
            </span>
          </div>
        </div>

        <!-- Right: Spotlight HUD Card with 3D Parallax & 360 Viewer Launcher -->
        <div class="lg:col-span-6">
          <div class="bg-[#0B0F15]/90 border border-cyber-border rounded-xl p-6 cyber-bracket glow-magenta backdrop-blur-md">
            
            <!-- Spotlight Header -->
            <div class="flex items-center justify-between gap-2 mb-4 pb-3 border-b border-cyber-border/40">
              <div class="flex items-center gap-2">
                <span id="spotlightCategoryBadge" class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-cyber-magenta/20 text-cyber-magenta border border-cyber-magenta/50">
                  ELECTRONICS
                </span>
                <span id="spotlightSkuBadge" class="text-xs font-mono text-cyber-muted">
                  SKU: SC-ELEC-01
                </span>
              </div>
              <div id="spotlightStockBadge" class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-cyber-green/20 text-cyber-green border border-cyber-green/50">
                IN STOCK (24 Units)
              </div>
            </div>

            <!-- Spotlight Image & Attributes Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-5 mb-5 items-stretch">
              
              <!-- Spotlight Photo Box with 3D Parallax and Floating Price Tag -->
              <div class="sm:col-span-6 relative rounded-xl overflow-hidden bg-[#040508] border border-cyber-border h-64 sm:h-72 cyber-card cursor-pointer group" data-tilt onclick="open3DViewerForCurrent()">
                <img id="spotlightImage" src="/images/prod_1.jpg" alt="Featured Product" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                
                <!-- 🏷️ Floating 3D Cyber Hologram Price -->
                <div class="cyber-floating-price">
                  <span class="text-xs font-mono text-cyber-cyan font-bold">₹</span>
                  <span id="spotlightFloatPrice" class="text-lg font-mono font-black text-white">3,499</span>
                  <span class="text-[10px] font-mono text-cyber-muted">/UNIT</span>
                </div>

                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end justify-between p-3 pointer-events-none">
                  <span class="text-[11px] font-mono text-cyber-cyan flex items-center gap-1.5">
                    <i data-lucide="orbit" class="w-3.5 h-3.5"></i>
                    LAUNCH 360° INSPECTOR
                  </span>
                  <span class="text-xs font-mono text-cyber-magenta font-bold">3D</span>
                </div>
              </div>

              <!-- Technical Specs Matrix -->
              <div class="sm:col-span-6 flex flex-col justify-between">
                <div>
                  <h3 id="spotlightTitle" class="font-display text-2xl font-black text-white leading-tight uppercase mb-2">
                    Wireless Noise-Canceling Headphones
                  </h3>

                  <div class="flex items-baseline gap-2 mb-4">
                    <span id="spotlightPrice" class="text-3xl font-mono font-black text-cyber-cyan">₹3,499.00</span>
                    <span class="text-xs font-mono text-cyber-muted">+ 5% GST (₹174.95)</span>
                  </div>

                  <!-- Spec Matrix Table -->
                  <div class="bg-[#040508] rounded-lg border border-cyber-border/60 p-3 space-y-1.5 text-xs font-mono mb-4">
                    <div class="text-[10px] font-bold text-cyber-magenta tracking-widest uppercase pb-1 border-b border-cyber-border/40 flex items-center gap-1.5">
                      <i data-lucide="terminal" class="w-3.5 h-3.5"></i>
                      HARDWARE ATTRIBUTES
                    </div>
                    <div class="flex justify-between text-cyber-muted">
                      <span>DIMENSIONS:</span>
                      <span id="spotlightDims" class="text-white font-bold">19.5 × 16.0 × 8.2 cm</span>
                    </div>
                    <div class="flex justify-between text-cyber-muted">
                      <span>NET WEIGHT:</span>
                      <span id="spotlightWeight" class="text-white font-bold">250 g</span>
                    </div>
                    <div class="flex justify-between text-cyber-muted">
                      <span>MATERIALS:</span>
                      <span id="spotlightMaterial" class="text-white font-bold truncate max-w-[130px]">Aerospace Alloy</span>
                    </div>
                    <div class="flex justify-between text-cyber-muted">
                      <span>DISPATCH HUB:</span>
                      <span id="spotlightRoute" class="text-cyber-green font-bold">Express Air Corridor</span>
                    </div>
                  </div>
                </div>

                <!-- Spotlight Action Buttons -->
                <div class="space-y-2">
                  <div class="flex items-center gap-3">
                    <div class="flex items-center border border-cyber-border rounded-lg bg-[#040508] px-2 py-1">
                      <button onclick="adjustSpotlightQty(-1)" class="w-6 h-6 text-cyber-cyan hover:text-white flex items-center justify-center font-bold text-xs">-</button>
                      <input type="number" id="spotlightQty" min="1" max="99" value="1" class="w-10 bg-transparent text-center text-xs font-mono font-bold text-white focus:outline-none">
                      <button onclick="adjustSpotlightQty(1)" class="w-6 h-6 text-cyber-cyan hover:text-white flex items-center justify-center font-bold text-xs">+</button>
                    </div>

                    <button onclick="addSpotlightToCart()" class="flex-1 py-2.5 px-4 rounded-lg bg-cyber-cyan hover:bg-cyber-magenta text-[#040508] hover:text-white font-mono font-bold text-xs tracking-wider uppercase transition-all flex items-center justify-center gap-2">
                      <span id="spotlightBtnText">ADD TO DISPATCH</span>
                      <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                    </button>
                  </div>

                  <!-- 3D Turntable Launcher -->
                  <button onclick="open3DViewerForCurrent()" class="w-full py-2 px-3 rounded-lg bg-[#0E141E] border border-cyber-border hover:border-cyber-magenta text-cyber-muted hover:text-white font-mono text-xs tracking-wider uppercase transition-all flex items-center justify-center gap-2">
                    <i data-lucide="orbit" class="w-3.5 h-3.5 text-cyber-magenta"></i>
                    <span>INTERACTIVE 360° 3D INSPECTOR</span>
                  </button>
                </div>

              </div>
            </div>

            <!-- Spotlight Thumbnails Strip -->
            <div>
              <div class="flex items-center justify-between text-[10px] font-mono text-cyber-muted uppercase tracking-wider mb-2">
                <span>QUICK ROTATION DECK:</span>
                <span class="text-cyber-cyan">10 CURATED CRAFTS</span>
              </div>
              <div class="grid grid-cols-5 sm:grid-cols-10 gap-2" id="spotlightThumbsContainer">
                <!-- Injected via JS -->
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

    <!-- Infinite HUD Marquee Stream -->
    <div class="w-full overflow-hidden py-2.5 bg-[#080C12] border-y border-cyber-border/60 mb-12">
      <div class="cyber-marquee-track text-xs font-mono font-bold tracking-widest uppercase text-cyber-muted">
        <span class="flex items-center gap-2 text-cyber-cyan"><i data-lucide="zap" class="w-3.5 h-3.5"></i> REAL-TIME 5% GST RECONCILIATION</span>
        <span class="text-cyber-border">•</span>
        <span class="flex items-center gap-2 text-cyber-green"><i data-lucide="route" class="w-3.5 h-3.5"></i> DIJKSTRA SHORTEST-PATH TRANSIT GRAPH</span>
        <span class="text-cyber-border">•</span>
        <span class="flex items-center gap-2 text-cyber-magenta"><i data-lucide="box" class="w-3.5 h-3.5"></i> MULTI-PLANE 3D PARALLAX & HOLOGRAPHIC PRICING</span>
        <span class="text-cyber-border">•</span>
        <span class="flex items-center gap-2 text-cyber-cyan"><i data-lucide="database" class="w-3.5 h-3.5"></i> ATOMIC SQLITE INVOICE TRANSACTIONS</span>
        <span class="text-cyber-border">•</span>
        <span class="flex items-center gap-2 text-cyber-cyan"><i data-lucide="zap" class="w-3.5 h-3.5"></i> REAL-TIME 5% GST RECONCILIATION</span>
        <span class="text-cyber-border">•</span>
        <span class="flex items-center gap-2 text-cyber-green"><i data-lucide="route" class="w-3.5 h-3.5"></i> DIJKSTRA SHORTEST-PATH TRANSIT GRAPH</span>
        <span class="text-cyber-border">•</span>
      </div>
    </div>

    <!-- Dijkstra Route Dispatch Console -->
    <section class="bg-[#0B0F15] border border-cyber-border rounded-xl p-6 sm:p-8 mb-12 cyber-bracket">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-4 border-b border-cyber-border/40">
        <div>
          <div class="inline-flex items-center gap-1.5 text-xs font-mono font-bold text-cyber-cyan uppercase">
            <i data-lucide="route" class="w-3.5 h-3.5"></i>
            ALGORITHMIC FREIGHT ROUTING
          </div>
          <h2 class="text-2xl font-display font-black text-white uppercase mt-1">Dijkstra Shortest Road Route Optimizer</h2>
        </div>
        <div class="flex items-center gap-3">
          <label class="text-xs font-mono text-cyber-muted">ORIGIN: <strong class="text-white">BENGALURU</strong></label>
          <span class="text-cyber-border">•</span>
          <select id="routeDestCity" onchange="calculateRoute()" class="text-xs font-mono bg-[#040508] text-cyber-cyan border border-cyber-border rounded px-3 py-1.5 focus:outline-none focus:border-cyber-cyan">
            <option value="Mumbai">DEST: Mumbai</option>
            <option value="Delhi">DEST: Delhi</option>
            <option value="Hyderabad">DEST: Hyderabad</option>
            <option value="Chennai" selected>DEST: Chennai</option>
            <option value="Kolkata">DEST: Kolkata</option>
            <option value="Pune">DEST: Pune</option>
            <option value="Ahmedabad">DEST: Ahmedabad</option>
          </select>
        </div>
      </div>

      <!-- Telemetry Output -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
        <div class="bg-[#040508] rounded-lg p-5 border border-cyber-border space-y-2">
          <div class="text-[11px] font-mono text-cyber-muted uppercase">SHORTEST HIGHWAY DISTANCE</div>
          <div id="routeDistanceText" class="text-4xl font-mono font-black text-cyber-cyan text-glow-cyan">346 km</div>
          <div class="text-[11px] font-mono text-cyber-muted">Engine: <code class="text-cyber-magenta font-bold">scipy.sparse.csgraph.dijkstra</code></div>
        </div>

        <div class="md:col-span-2 bg-[#040508] rounded-lg p-5 border border-cyber-border flex flex-col justify-between">
          <div>
            <div class="text-[11px] font-mono text-cyber-muted uppercase mb-3">TRANSIT HIGHWAY CORRIDOR NODES:</div>
            <div id="routePathNodes" class="flex flex-wrap items-center gap-2">
              <span class="px-3 py-1 bg-[#0E141E] border border-cyber-border rounded text-xs font-mono font-bold text-white flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-cyber-green animate-pulse"></span>
                Bengaluru
              </span>
              <i data-lucide="arrow-right" class="w-3.5 h-3.5 text-cyber-cyan"></i>
              <span class="px-3 py-1 bg-[#0E141E] border border-cyber-border rounded text-xs font-mono font-bold text-cyber-cyan">
                Chennai
              </span>
            </div>
          </div>
          <div class="text-xs font-mono text-cyber-muted mt-4 pt-3 border-t border-cyber-border/40 flex items-center justify-between">
            <span>FLEET TRANSIT ETA: <strong id="routeEtaText" class="text-white">~5.8 Hours</strong></span>
            <span class="text-cyber-green font-bold flex items-center gap-1">
              <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
              OPTIMAL FUEL ROUTE
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Product Grid Section -->
    <section>
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-8">
        <div>
          <h2 class="text-3xl font-display font-black text-white uppercase">Warehouse Catalog & Hardware Grid</h2>
          <p class="text-xs font-mono text-cyber-muted mt-1 uppercase tracking-wider">HOVER TO ENGAGE 3D PARALLAX & HOLOGRAPHIC FLOATING PRICING</p>
        </div>
        <div class="flex items-center gap-3">
          <span id="productCounter" class="text-xs font-mono text-cyber-cyan">LOADING REPERTORY...</span>
        </div>
      </div>

      <!-- Grid -->
      <div id="productGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Injected via JS -->
      </div>
    </section>

  </main>

  <!-- Interactive 3D Turntable Modal Inspector (Layers / Aaroh Style) -->
  <div id="threeDModalBackdrop" onclick="close3DViewer()" class="fixed inset-0 bg-[#040508]/85 backdrop-blur-xl z-50 opacity-0 pointer-events-none transition-opacity duration-300 flex items-center justify-center p-4">
    <div id="threeDModal" onclick="event.stopPropagation()" class="bg-[#0B0F15] border border-cyber-border rounded-xl max-w-3xl w-full flex flex-col shadow-2xl transform scale-95 transition-transform duration-300 overflow-hidden cyber-bracket glow-cyan">
      
      <!-- Top bar -->
      <div class="p-5 border-b border-cyber-border flex items-center justify-between bg-[#040508]">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded bg-cyber-cyan/10 border border-cyber-cyan text-cyber-cyan flex items-center justify-center">
            <i data-lucide="orbit" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 id="modal3DTitle" class="font-display font-bold text-white text-lg uppercase">3D PRODUCT TURNTABLE</h3>
            <p id="modal3DSubtitle" class="text-xs font-mono text-cyber-muted">DRAG TO ROTATE 360° // SCROLL TO ZOOM</p>
          </div>
        </div>
        <button onclick="close3DViewer()" class="w-8 h-8 rounded bg-[#0E141E] border border-cyber-border hover:border-cyber-magenta text-cyber-muted hover:text-white flex items-center justify-center transition-colors">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <!-- 3D Canvas Viewport -->
      <div class="relative w-full h-80 sm:h-96 bg-gradient-to-b from-[#040508] to-[#0A0E17] flex items-center justify-center overflow-hidden">
        <canvas id="product-3d-canvas" class="w-full h-full cursor-grab active:cursor-grabbing"></canvas>

        <div class="absolute bottom-4 left-4 flex items-center gap-2 text-[11px] font-mono bg-[#040508]/80 border border-cyber-border px-3 py-1.5 rounded text-cyber-cyan pointer-events-none">
          <i data-lucide="move" class="w-3.5 h-3.5 text-cyber-cyan"></i>
          <span>Click & Drag to Rotate in 3D Space</span>
        </div>

        <div class="absolute top-4 right-4">
          <button onclick="reset3DModelRotation()" class="text-xs font-mono bg-[#040508] hover:bg-[#0E141E] text-white px-3 py-1 rounded border border-cyber-border transition-all flex items-center gap-1.5">
            <i data-lucide="rotate-ccw" class="w-3 h-3 text-cyber-cyan"></i>
            Reset
          </button>
        </div>
      </div>

      <!-- Bottom Actions -->
      <div class="p-5 border-t border-cyber-border bg-[#040508] flex flex-wrap items-center justify-between gap-4">
        <div>
          <div id="modal3DPrice" class="text-2xl font-mono font-black text-cyber-cyan text-glow-cyan">₹3,499.00</div>
          <div class="text-xs font-mono text-cyber-muted">Includes 5% GST // Real-Time Routing Ready</div>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="close3DViewer()" class="px-4 py-2 rounded text-xs font-mono text-cyber-muted hover:text-white border border-cyber-border">
            CLOSE
          </button>
          <button id="modal3DAddToCartBtn" class="px-5 py-2.5 rounded bg-cyber-cyan hover:bg-cyber-magenta text-[#040508] hover:text-white font-mono font-bold text-xs tracking-wider uppercase transition-all flex items-center gap-2">
            <span>ADD TO DISPATCH</span>
            <i data-lucide="plus" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- Cart Slide-Over Drawer -->
  <div id="cartDrawerBackdrop" onclick="toggleCartDrawer(false)" class="fixed inset-0 bg-[#040508]/85 backdrop-blur-md z-50 opacity-0 pointer-events-none transition-opacity duration-300"></div>

  <aside id="cartDrawer" class="fixed top-0 right-0 h-full w-full max-w-md bg-[#0B0F15] border-l border-cyber-border shadow-2xl z-50 transform translate-x-full transition-transform duration-300 ease-out flex flex-col">
    <div class="p-5 border-b border-cyber-border flex items-center justify-between bg-[#040508]">
      <div class="flex items-center gap-2.5">
        <div class="w-9 h-9 rounded bg-cyber-cyan/10 border border-cyber-cyan text-cyber-cyan flex items-center justify-center">
          <i data-lucide="shopping-bag" class="w-4 h-4"></i>
        </div>
        <div>
          <h3 class="font-display font-bold text-white text-base uppercase">DISPATCH CART</h3>
          <p class="text-[11px] font-mono text-cyber-muted">Direct SQLite Invoicing</p>
        </div>
      </div>
      <button onclick="toggleCartDrawer(false)" class="w-8 h-8 rounded bg-[#0E141E] border border-cyber-border hover:border-cyber-magenta text-cyber-muted hover:text-white flex items-center justify-center transition-colors">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>

    <!-- Tier Toggle -->
    <div class="p-4 bg-[#040508] border-b border-cyber-border flex items-center justify-between text-xs font-mono">
      <span class="text-cyber-muted">PATRON TIER:</span>
      <div class="flex items-center gap-2">
        <button id="tierRegularBtn" onclick="setCustomerTier(false)" class="px-3 py-1 rounded border border-cyber-cyan bg-cyber-cyan text-[#040508] font-bold transition-all">REGULAR (2%)</button>
        <button id="tierPremiumBtn" onclick="setCustomerTier(true)" class="px-3 py-1 rounded border border-cyber-border bg-[#0E141E] text-cyber-muted font-bold hover:border-cyber-cyan transition-all">PREMIUM (10%)</button>
      </div>
    </div>

    <!-- Items list -->
    <div id="cartItemsList" class="flex-1 overflow-y-auto p-5 space-y-4">
      <!-- Injected via renderCart() -->
    </div>

    <!-- Footer Summary -->
    <div class="p-5 border-t border-cyber-border bg-[#040508] space-y-3">
      <div class="space-y-1.5 text-xs font-mono">
        <div class="flex justify-between text-cyber-muted">
          <span>CART SUBTOTAL:</span>
          <span id="cartSubtotal" class="font-bold text-white">₹0.00</span>
        </div>
        <div class="flex justify-between text-cyber-green">
          <span id="cartDiscountLabel">TIER DISCOUNT (2%):</span>
          <span id="cartDiscountAmt" class="font-bold">-₹0.00</span>
        </div>
        <div class="flex justify-between text-cyber-muted">
          <span>5% STATUTORY GST:</span>
          <span id="cartTaxAmt" class="font-bold text-white">₹0.00</span>
        </div>
        <div class="pt-2 border-t border-cyber-border flex justify-between items-baseline text-sm">
          <span class="font-bold text-white uppercase tracking-wider">TOTAL PAYABLE:</span>
          <span id="cartGrandTotal" class="text-2xl font-mono font-black text-cyber-cyan text-glow-cyan">₹0.00</span>
        </div>
      </div>

      <!-- Destination Hub -->
      <div class="pt-1">
        <label class="block text-[11px] font-mono text-cyber-muted mb-1 uppercase">DISPATCH DESTINATION HUB:</label>
        <select id="cartDestinationCity" class="w-full text-xs font-mono bg-[#0E141E] text-cyber-cyan border border-cyber-border rounded px-3 py-2 focus:outline-none focus:border-cyber-cyan">
          <option value="Bengaluru">Bengaluru (Local Base)</option>
          <option value="Chennai" selected>Chennai</option>
          <option value="Mumbai">Mumbai</option>
          <option value="Hyderabad">Hyderabad</option>
          <option value="Delhi">Delhi</option>
          <option value="Kolkata">Kolkata</option>
          <option value="Pune">Pune</option>
          <option value="Ahmedabad">Ahmedabad</option>
        </select>
      </div>

      <!-- Actions -->
      <div class="pt-2 flex gap-2">
        <button onclick="clearCart()" class="px-4 py-2.5 rounded bg-[#0E141E] border border-cyber-border text-cyber-muted hover:text-white text-xs font-mono flex items-center justify-center gap-1.5 flex-1">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
          <span>CLEAR</span>
        </button>
        <button onclick="triggerCheckout()" id="checkoutSubmitBtn" class="py-2.5 px-4 rounded bg-cyber-cyan hover:bg-cyber-magenta text-[#040508] hover:text-white font-mono font-bold text-xs tracking-wider uppercase transition-all flex-[2] flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed">
          <span>GENERATE TAX INVOICE</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    </div>
  </aside>

  <!-- Checkout Tax Invoice Modal -->
  <div id="receiptModalBackdrop" class="fixed inset-0 bg-[#040508]/85 backdrop-blur-md z-50 opacity-0 pointer-events-none transition-opacity duration-300 flex items-center justify-center p-4">
    <div id="receiptModal" class="bg-[#0B0F15] border border-cyber-border rounded-xl max-w-xl w-full max-h-[90vh] flex flex-col shadow-2xl transform scale-95 transition-transform duration-300 cyber-bracket glow-cyan">
      <div class="p-6 border-b border-cyber-border flex items-center justify-between bg-[#040508]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded bg-cyber-green/10 border border-cyber-green text-cyber-green flex items-center justify-center">
            <i data-lucide="check-circle" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 class="font-display font-bold text-white text-lg uppercase">ORDER CONFIRMED & INVOICED</h3>
            <p id="receiptOrderIdTag" class="text-xs font-mono text-cyber-cyan">ORDER #SC-0000</p>
          </div>
        </div>
        <button onclick="closeReceiptModal()" class="w-8 h-8 rounded bg-[#0E141E] border border-cyber-border hover:border-cyber-magenta text-cyber-muted hover:text-white flex items-center justify-center transition-colors">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="p-6 flex-1 overflow-y-auto">
        <pre id="receiptContentPre" class="p-4 bg-[#040508] border border-cyber-border rounded font-mono text-xs text-cyber-cyan leading-relaxed whitespace-pre-wrap select-all overflow-x-auto"></pre>
      </div>

      <div class="p-5 border-t border-cyber-border bg-[#040508] flex items-center justify-between">
        <div class="text-xs font-mono text-cyber-green flex items-center gap-1.5">
          <i data-lucide="file-check" class="w-4 h-4"></i>
          Stored in SQLite database
        </div>
        <button onclick="closeReceiptModal()" class="px-5 py-2.5 rounded bg-cyber-cyan hover:bg-cyber-magenta text-[#040508] hover:text-white font-mono font-bold text-xs uppercase tracking-wider transition-all">
          DONE & CONTINUE
        </button>
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT APPLICATION CORE -->
  <script>
    let products = [];
    let selectedProduct = null;
    let currentCategoryFilter = 'ALL';
    let cart = [];
    let isPremiumCustomer = false;

    const productSpecs = {
      1: { sku: "SC-ELEC-01", dims: "19.5 × 16.0 × 8.2 cm", weight: "250 g", material: "Aerospace Alloy & Memory Foam", route: "Express Air Corridor" },
      2: { sku: "SC-FURN-02", dims: "65.0 × 65.0 × 110.0 cm", weight: "14.5 kg", material: "Breathable Mesh & Steel Core", route: "Heavy Freight Hub" },
      3: { sku: "SC-FURN-03", dims: "45.0 × 45.0 × 52.0 cm", weight: "5.8 kg", material: "Solid Seasoned Sheesham Wood", route: "Standard Road Highway" },
      4: { sku: "SC-KITC-04", dims: "22.0 × 16.5 × 28.0 cm", weight: "1.2 kg", material: "Brushed 304 Stainless Steel", route: "Priority Regional Express" },
      5: { sku: "SC-ELEC-05", dims: "32.0 × 12.0 × 3.5 cm", weight: "820 g", material: "Anodized Aluminum & Gateron Switches", route: "Express Transit Hub" },
      6: { sku: "SC-FASH-06", dims: "42.0 × 30.0 × 14.0 cm", weight: "1.1 kg", material: "Full-Grain Vegetable-Tanned Leather", route: "Artisan Courier" },
      7: { sku: "SC-FASH-07", dims: "30.0 × 10.5 × 11.0 cm", weight: "640 g", material: "Recycled Knit & Responsive EVA Foam", route: "Direct Fast-Lane" },
      8: { sku: "SC-GROC-08", dims: "18.0 × 18.0 × 26.0 cm", weight: "5.2 kg", material: "Cold-Pressed Raw Organic Harvest", route: "Temperature-Controlled Transit" },
      9: { sku: "SC-KITC-09", dims: "28.0 × 28.0 × 5.0 cm", weight: "2.4 kg", material: "Pre-Seasoned Heavy Cast Iron", route: "Heavy Road Highway" },
      10: { sku: "SC-ELEC-10", dims: "20.5 × 8.5 × 8.5 cm", weight: "680 g", material: "IP67 Silicone & Acoustic Grille", route: "Express Air Corridor" }
    };

    const productPhotos = {
      1: "/images/prod_1.jpg",
      2: "/images/prod_2.jpg",
      3: "/images/prod_3.jpg",
      4: "/images/prod_4.jpg",
      5: "/images/prod_5.jpg",
      6: "/images/prod_6.jpg",
      7: "/images/prod_7.jpg",
      8: "/images/prod_8.jpg",
      9: "/images/prod_9.jpg",
      10: "/images/prod_10.jpg"
    };

    const dijkstraDistances = {
      "Chennai": { km: 346, eta: "~5.8 Hours", path: ["Bengaluru", "Hosur", "Vellore", "Chennai"] },
      "Mumbai": { km: 984, eta: "~16.2 Hours", path: ["Bengaluru", "Tumakuru", "Hubballi", "Pune", "Mumbai"] },
      "Hyderabad": { km: 569, eta: "~9.4 Hours", path: ["Bengaluru", "Anantapur", "Kurnool", "Hyderabad"] },
      "Delhi": { km: 2174, eta: "~34.5 Hours", path: ["Bengaluru", "Hyderabad", "Nagpur", "Gwalior", "Delhi"] },
      "Kolkata": { km: 1871, eta: "~31.0 Hours", path: ["Bengaluru", "Vijayawada", "Visakhapatnam", "Bhubaneswar", "Kolkata"] },
      "Pune": { km: 840, eta: "~13.8 Hours", path: ["Bengaluru", "Hubballi", "Belagavi", "Kolhapur", "Pune"] },
      "Ahmedabad": { km: 1495, eta: "~24.0 Hours", path: ["Bengaluru", "Pune", "Mumbai", "Surat", "Ahmedabad"] }
    };

    // -------------------------------------------------------------
    // CURSOR TRACKING
    // -------------------------------------------------------------
    function initCustomCursor() {
      const dot = document.getElementById('cyber-cursor-dot');
      const ring = document.getElementById('cyber-cursor-ring');
      if (!dot || !ring) return;

      let mouseX = window.innerWidth / 2;
      let mouseY = window.innerHeight / 2;
      let ringX = mouseX;
      let ringY = mouseY;

      window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
      });

      function renderCursor() {
        ringX += (mouseX - ringX) * 0.16;
        ringY += (mouseY - ringY) * 0.16;
        ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;
        requestAnimationFrame(renderCursor);
      }
      renderCursor();

      document.addEventListener('mouseover', (e) => {
        if (e.target.closest('button, a, input, select, .cyber-card')) {
          document.body.classList.add('cursor-hover');
        } else {
          document.body.classList.remove('cursor-hover');
        }
      });
    }

    // -------------------------------------------------------------
    // THREE.JS CYBER HERO WEBGL BACKGROUND
    // -------------------------------------------------------------
    function initThreeHero() {
      const canvas = document.getElementById('three-hero-canvas');
      const container = document.getElementById('hero-canvas-wrap');
      if (!canvas || !container || typeof THREE === 'undefined') return;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
      camera.position.z = 80;

      const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // 450 Cyber particles
      const particleCount = 450;
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(particleCount * 3);
      const velocities = [];

      for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 220;
        positions[i + 1] = (Math.random() - 0.5) * 140;
        positions[i + 2] = (Math.random() - 0.5) * 130;

        velocities.push({
          x: (Math.random() - 0.5) * 0.12,
          y: (Math.random() - 0.5) * 0.12,
          z: (Math.random() - 0.5) * 0.12
        });
      }

      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      const material = new THREE.PointsMaterial({
        color: 0x00F3FF,
        size: 2.4,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
      });

      const particleSystem = new THREE.Points(geometry, material);
      scene.add(particleSystem);

      // Rotating Cyber Core Polyhedra
      const polyGroup = new THREE.Group();
      
      const icosaGeo = new THREE.IcosahedronGeometry(22, 1);
      const icosaMat = new THREE.MeshBasicMaterial({
        color: 0xED2ABE,
        wireframe: true,
        transparent: true,
        opacity: 0.28
      });
      const icosaMesh = new THREE.Mesh(icosaGeo, icosaMat);
      polyGroup.add(icosaMesh);

      const knotGeo = new THREE.TorusKnotGeometry(12, 2.4, 64, 16);
      const knotMat = new THREE.MeshBasicMaterial({
        color: 0x00F3FF,
        wireframe: true,
        transparent: true,
        opacity: 0.38
      });
      const knotMesh = new THREE.Mesh(knotGeo, knotMat);
      polyGroup.add(knotMesh);

      polyGroup.position.set(45, -5, -15);
      scene.add(polyGroup);

      let mouseX = 0;
      let mouseY = 0;

      window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
      });

      function animate() {
        requestAnimationFrame(animate);

        polyGroup.rotation.x += 0.004;
        polyGroup.rotation.y += 0.007;
        knotMesh.rotation.z -= 0.006;

        const posArr = geometry.attributes.position.array;
        for (let i = 0; i < particleCount * 3; i += 3) {
          posArr[i] += velocities[i / 3].x;
          posArr[i + 1] += velocities[i / 3].y;
          posArr[i + 2] += velocities[i / 3].z;

          if (Math.abs(posArr[i]) > 110) velocities[i / 3].x *= -1;
          if (Math.abs(posArr[i + 1]) > 70) velocities[i / 3].y *= -1;
          if (Math.abs(posArr[i + 2]) > 65) velocities[i / 3].z *= -1;
        }
        geometry.attributes.position.needsUpdate = true;

        camera.position.x += (mouseX * 18 - camera.position.x) * 0.05;
        camera.position.y += (mouseY * 12 - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
      }
      animate();

      window.addEventListener('resize', () => {
        if (!container) return;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
      });
    }

    // -------------------------------------------------------------
    // THREE.JS 360° TURNTABLE VIEWER
    // -------------------------------------------------------------
    let turntableScene, turntableCamera, turntableRenderer, turntableMesh;
    let isDragging3D = false;
    let prevMouse3D = { x: 0, y: 0 };

    function init3DTurntable() {
      const canvas = document.getElementById('product-3d-canvas');
      if (!canvas || typeof THREE === 'undefined') return;

      turntableScene = new THREE.Scene();
      turntableCamera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
      turntableCamera.position.set(0, 0, 5.5);

      turntableRenderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      turntableRenderer.setSize(canvas.clientWidth, canvas.clientHeight);
      turntableRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      const ambientLight = new THREE.AmbientLight(0xffffff, 1.1);
      turntableScene.add(ambientLight);

      const dirLight1 = new THREE.DirectionalLight(0x00F3FF, 1.4);
      dirLight1.position.set(5, 10, 7);
      turntableScene.add(dirLight1);

      const dirLight2 = new THREE.DirectionalLight(0xED2ABE, 0.8);
      dirLight2.position.set(-5, -5, -5);
      turntableScene.add(dirLight2);

      build3DProceduralMesh(1);

      canvas.addEventListener('mousedown', (e) => {
        isDragging3D = true;
        prevMouse3D = { x: e.clientX, y: e.clientY };
      });
      window.addEventListener('mouseup', () => { isDragging3D = false; });
      window.addEventListener('mousemove', (e) => {
        if (!isDragging3D || !turntableMesh) return;
        const deltaX = e.clientX - prevMouse3D.x;
        const deltaY = e.clientY - prevMouse3D.y;

        turntableMesh.rotation.y += deltaX * 0.01;
        turntableMesh.rotation.x += deltaY * 0.01;
        prevMouse3D = { x: e.clientX, y: e.clientY };
      });

      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        turntableCamera.position.z += e.deltaY * 0.003;
        turntableCamera.position.z = Math.max(3.2, Math.min(8.5, turntableCamera.position.z));
      });

      function animateTurntable() {
        requestAnimationFrame(animateTurntable);
        if (turntableMesh && !isDragging3D) {
          turntableMesh.rotation.y += 0.006;
        }
        turntableRenderer.render(turntableScene, turntableCamera);
      }
      animateTurntable();
    }

    function build3DProceduralMesh(productId) {
      if (!turntableScene) return;
      if (turntableMesh) turntableScene.remove(turntableMesh);

      const group = new THREE.Group();
      const p = products.find(x => x.product_id === productId) || { category: 'Electronics' };
      const cat = p.category;
      const photoUrl = productPhotos[productId] || "/images/prod_1.jpg";

      const textureLoader = new THREE.TextureLoader();
      const texture = textureLoader.load(photoUrl);

      let geo;
      let mat = new THREE.MeshStandardMaterial({
        map: texture,
        roughness: 0.2,
        metalness: 0.5
      });

      if (cat === 'Electronics') {
        geo = new THREE.CylinderGeometry(1.4, 1.4, 0.45, 48);
      } else if (cat === 'Furniture') {
        geo = new THREE.BoxGeometry(1.8, 1.8, 1.8);
      } else if (cat === 'Home & Kitchen') {
        geo = new THREE.DodecahedronGeometry(1.4, 0);
      } else if (cat === 'Fashion') {
        geo = new THREE.TorusKnotGeometry(1.1, 0.35, 120, 20);
      } else {
        geo = new THREE.SphereGeometry(1.3, 36, 36);
      }

      const mainMesh = new THREE.Mesh(geo, mat);
      group.add(mainMesh);

      // Gyroscope Neon Rings
      const ring1Geo = new THREE.RingGeometry(2.1, 2.22, 64);
      const ring1Mat = new THREE.MeshBasicMaterial({ color: 0x00F3FF, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
      const ring1 = new THREE.Mesh(ring1Geo, ring1Mat);
      ring1.rotation.x = Math.PI / 2;
      group.add(ring1);

      const ring2Geo = new THREE.RingGeometry(2.35, 2.42, 64);
      const ring2Mat = new THREE.MeshBasicMaterial({ color: 0xED2ABE, side: THREE.DoubleSide, transparent: true, opacity: 0.5 });
      const ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
      ring2.rotation.y = Math.PI / 4;
      group.add(ring2);

      turntableMesh = group;
      turntableScene.add(turntableMesh);
    }

    function reset3DModelRotation() {
      if (turntableMesh) turntableMesh.rotation.set(0, 0, 0);
      if (turntableCamera) turntableCamera.position.set(0, 0, 5.5);
    }

    function open3DViewerForCurrent() {
      if (!selectedProduct) return;
      open3DViewer(selectedProduct.product_id);
    }

    function open3DViewer(productId) {
      const p = products.find(x => x.product_id === productId);
      if (!p) return;

      document.getElementById('modal3DTitle').textContent = `${p.name} // 360° ORBIT`;
      document.getElementById('modal3DSubtitle').textContent = `SKU: ${productSpecs[p.product_id]?.sku || 'SC-001'} // DEPT: ${p.category.toUpperCase()}`;
      document.getElementById('modal3DPrice').textContent = `₹${p.price.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

      const addBtn = document.getElementById('modal3DAddToCartBtn');
      addBtn.onclick = () => {
        addToCartWithQty(p.product_id, 1);
        showToast("ORDER QUEUED", `${p.name} queued for dispatch.`);
      };

      build3DProceduralMesh(productId);

      const backdrop = document.getElementById('threeDModalBackdrop');
      const modal = document.getElementById('threeDModal');

      backdrop.classList.remove('opacity-0', 'pointer-events-none');
      backdrop.classList.add('opacity-100');
      modal.classList.remove('scale-95');
      modal.classList.add('scale-100');

      setTimeout(() => {
        const canvas = document.getElementById('product-3d-canvas');
        if (turntableCamera && turntableRenderer && canvas) {
          turntableCamera.aspect = canvas.clientWidth / canvas.clientHeight;
          turntableCamera.updateProjectionMatrix();
          turntableRenderer.setSize(canvas.clientWidth, canvas.clientHeight);
        }
      }, 100);

      lucide.createIcons();
    }

    function close3DViewer() {
      const backdrop = document.getElementById('threeDModalBackdrop');
      const modal = document.getElementById('threeDModal');

      backdrop.classList.add('opacity-0', 'pointer-events-none');
      backdrop.classList.remove('opacity-100');
      modal.classList.add('scale-95');
      modal.classList.remove('scale-100');
    }

    // -------------------------------------------------------------
    // PRODUCTS & SPOTLIGHT
    // -------------------------------------------------------------
    async function loadProducts() {
      try {
        const res = await fetch('/api/products');
        products = await res.json();
        
        if (products.length > 0) {
          selectProductForSpotlight(products[0]);
          renderSpotlightThumbnails();
        }

        renderProducts(products);
      } catch (err) {
        console.error("Error loading products:", err);
      }
    }

    function selectProductForSpotlight(prod) {
      selectedProduct = prod;
      const specs = productSpecs[prod.product_id] || {
        sku: `SC-${prod.product_id.toString().padStart(3, '0')}`,
        dims: "Standard Box",
        weight: "Standard",
        material: "Aerospace Spec",
        route: "Priority Express"
      };

      const photoUrl = productPhotos[prod.product_id] || "/images/prod_1.jpg";

      const imgElem = document.getElementById('spotlightImage');
      imgElem.style.opacity = '0.3';
      setTimeout(() => {
        imgElem.src = photoUrl;
        imgElem.style.opacity = '1';
      }, 150);

      document.getElementById('spotlightTitle').textContent = prod.name;
      document.getElementById('spotlightPrice').textContent = `₹${prod.price.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      
      const floatPrice = document.getElementById('spotlightFloatPrice');
      if (floatPrice) floatPrice.textContent = prod.price.toLocaleString('en-IN', {minimumFractionDigits: 0});

      document.getElementById('spotlightCategoryBadge').textContent = prod.category.toUpperCase();
      document.getElementById('spotlightSkuBadge').textContent = specs.sku;
      
      const stockBadge = document.getElementById('spotlightStockBadge');
      if (prod.stock > 5) {
        stockBadge.className = "text-xs font-mono font-bold px-2 py-0.5 rounded bg-cyber-green/20 text-cyber-green border border-cyber-green/50";
        stockBadge.textContent = `IN STOCK (${prod.stock} Units)`;
      } else if (prod.stock > 0) {
        stockBadge.className = "text-xs font-mono font-bold px-2 py-0.5 rounded bg-yellow-500/20 text-yellow-400 border border-yellow-500/50";
        stockBadge.textContent = `LOW STOCK (${prod.stock} Units)`;
      } else {
        stockBadge.className = "text-xs font-mono font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/50";
        stockBadge.textContent = `DEPLETED (0 Units)`;
      }

      document.getElementById('spotlightDims').textContent = specs.dims;
      document.getElementById('spotlightWeight').textContent = specs.weight;
      document.getElementById('spotlightMaterial').textContent = specs.material;
      document.getElementById('spotlightRoute').textContent = specs.route;

      const qtyInput = document.getElementById('spotlightQty');
      if (qtyInput) qtyInput.value = 1;

      document.querySelectorAll('.spotlight-thumb').forEach(thumb => {
        if (thumb.dataset.id == prod.product_id) {
          thumb.classList.add('border-cyber-cyan', 'ring-2', 'ring-cyber-cyan/50');
        } else {
          thumb.classList.remove('border-cyber-cyan', 'ring-2', 'ring-cyber-cyan/50');
        }
      });
    }

    function renderSpotlightThumbnails() {
      const container = document.getElementById('spotlightThumbsContainer');
      if (!container) return;

      container.innerHTML = products.slice(0, 10).map((p, idx) => {
        const photo = productPhotos[p.product_id] || "/images/prod_1.jpg";
        return `
          <button onclick="inspectProductInStudio(${p.product_id})" data-id="${p.product_id}"
            class="spotlight-thumb w-full h-11 rounded overflow-hidden border border-cyber-border bg-[#040508] hover:border-cyber-cyan transition-all ${idx === 0 ? 'border-cyber-cyan ring-2 ring-cyber-cyan/50' : ''}">
            <img src="${photo}" alt="${p.name}" class="w-full h-full object-cover">
          </button>
        `;
      }).join('');
    }

    function adjustSpotlightQty(delta) {
      const input = document.getElementById('spotlightQty');
      let val = parseInt(input.value) || 1;
      val += delta;
      if (val < 1) val = 1;
      if (selectedProduct && val > selectedProduct.stock) val = selectedProduct.stock;
      input.value = val;
    }

    function addSpotlightToCart() {
      if (!selectedProduct) return;
      const qty = parseInt(document.getElementById('spotlightQty').value) || 1;
      addToCartWithQty(selectedProduct.product_id, qty);

      const btnText = document.getElementById('spotlightBtnText');
      const origText = btnText.textContent;
      btnText.textContent = "✓ QUEUED";
      setTimeout(() => { btnText.textContent = origText; }, 1500);
    }

    function renderProducts(list) {
      const grid = document.getElementById('productGrid');
      document.getElementById('productCounter').textContent = `${list.length} UNITS LISTED`;

      if (list.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-cyber-muted bg-[#0B0F15] border border-cyber-border rounded-xl">
            <i data-lucide="package-search" class="w-10 h-10 mx-auto mb-3 opacity-40 text-cyber-cyan"></i>
            <p class="text-base font-bold text-white uppercase">NO MATCHING HARDWARE FOUND</p>
          </div>
        `;
        lucide.createIcons();
        return;
      }

      grid.innerHTML = list.map(p => {
        const inStock = p.stock > 0;
        const lowStock = p.stock > 0 && p.stock <= 5;
        const stockPill = inStock 
          ? (lowStock 
              ? `<span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-yellow-500/20 text-yellow-400 border border-yellow-500/50">LOW (${p.stock})</span>`
              : `<span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyber-green/20 text-cyber-green border border-cyber-green/50">IN STOCK (${p.stock})</span>`)
          : `<span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-500/20 text-red-400 border border-red-500/50">DEPLETED</span>`;

        const photoUrl = productPhotos[p.product_id] || "/images/prod_1.jpg";
        const specs = productSpecs[p.product_id] || { weight: "Standard", dims: "Standard" };

        return `
          <div class="cyber-card p-5 flex flex-col justify-between h-full group" data-tilt>
            <div>
              <div class="relative w-full h-52 rounded-lg overflow-hidden mb-4 bg-[#040508] border border-cyber-border">
                <img src="${photoUrl}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                
                <div class="absolute top-2.5 left-2.5">
                  <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#040508]/85 text-cyber-cyan border border-cyber-cyan/40 uppercase">${p.category}</span>
                </div>
                
                <div class="absolute top-2.5 right-2.5">
                  ${stockPill}
                </div>

                <!-- 🏷️ Floating Holographic Price Tag -->
                <div class="cyber-floating-price">
                  <span class="text-[11px] font-mono font-bold text-cyber-cyan">₹</span>
                  <span class="text-base font-mono font-black text-white">${p.price.toLocaleString('en-IN', {minimumFractionDigits: 0})}</span>
                  <span class="text-[9px] font-mono text-cyber-muted">/PC</span>
                </div>
              </div>

              <h4 class="font-display text-lg font-bold text-white mb-1 uppercase group-hover:text-cyber-cyan transition-colors">${p.name}</h4>
              
              <div class="flex items-center gap-2 text-[11px] font-mono text-cyber-muted mb-3">
                <span>WT: <strong class="text-white">${specs.weight}</strong></span>
                <span>//</span>
                <span>DIM: <strong class="text-white">${specs.dims.split(' ')[0]}</strong></span>
              </div>
            </div>

            <div class="pt-3 border-t border-cyber-border/40 flex flex-col gap-2">
              <button onclick="open3DViewer(${p.product_id})" 
                class="w-full py-1.5 px-3 rounded bg-[#040508] border border-cyber-border hover:border-cyber-magenta text-cyber-muted hover:text-white font-mono text-xs uppercase transition-all flex items-center justify-center gap-2">
                <i data-lucide="orbit" class="w-3.5 h-3.5 text-cyber-cyan"></i>
                <span>INSPECT IN 360° 3D</span>
              </button>

              <div class="flex items-center gap-2">
                <div class="flex items-center border border-cyber-border rounded bg-[#040508] px-1.5 py-1">
                  <button onclick="adjustCardQty(${p.product_id}, -1)" ${!inStock ? 'disabled' : ''} class="w-5 h-5 text-cyber-cyan hover:text-white flex items-center justify-center font-bold text-xs disabled:opacity-30">-</button>
                  <input type="number" id="qty_${p.product_id}" min="1" max="${p.stock}" value="1" ${!inStock ? 'disabled' : ''} 
                    class="w-8 bg-transparent text-center text-xs font-mono font-bold text-white focus:outline-none">
                  <button onclick="adjustCardQty(${p.product_id}, 1)" ${!inStock ? 'disabled' : ''} class="w-5 h-5 text-cyber-cyan hover:text-white flex items-center justify-center font-bold text-xs disabled:opacity-30">+</button>
                </div>
                
                <button id="addBtn_${p.product_id}" onclick="addToCartFromCard(${p.product_id})" ${!inStock ? 'disabled' : ''} 
                  class="flex-1 py-1.5 px-3 rounded bg-cyber-cyan hover:bg-cyber-magenta text-[#040508] hover:text-white font-mono font-bold text-xs tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 disabled:opacity-30 disabled:cursor-not-allowed">
                  <span id="addBtnLabel_${p.product_id}">ADD TO DISPATCH</span>
                  <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
      initTilt();
      lucide.createIcons();
    }

    function adjustCardQty(productId, delta) {
      const input = document.getElementById(`qty_${productId}`);
      if (!input) return;
      const p = products.find(x => x.product_id === productId);
      let val = parseInt(input.value) || 1;
      val += delta;
      if (val < 1) val = 1;
      if (p && val > p.stock) val = p.stock;
      input.value = val;
    }

    function inspectProductInStudio(productId) {
      const p = products.find(x => x.product_id === productId);
      if (p) {
        selectProductForSpotlight(p);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    // -------------------------------------------------------------
    // CART & INVOICING
    // -------------------------------------------------------------
    function addToCartWithQty(productId, quantity) {
      const p = products.find(x => x.product_id === productId);
      if (!p || p.stock <= 0) return;

      const existing = cart.find(x => x.product_id === productId);
      if (existing) {
        existing.quantity += quantity;
        if (existing.quantity > p.stock) existing.quantity = p.stock;
      } else {
        cart.push({
          product_id: p.product_id,
          name: p.name,
          price: p.price,
          category: p.category,
          quantity: Math.min(quantity, p.stock),
          stock: p.stock
        });
      }

      updateCartBadge();
      renderCart();
      showToast("DISPATCH UPDATED", `Queued ${quantity}x ${p.name}`);
    }

    function addToCartFromCard(productId) {
      const input = document.getElementById(`qty_${productId}`);
      const qty = input ? parseInt(input.value) || 1 : 1;
      addToCartWithQty(productId, qty);

      const label = document.getElementById(`addBtnLabel_${productId}`);
      if (label) {
        const orig = label.textContent;
        label.textContent = "✓ QUEUED";
        setTimeout(() => { label.textContent = orig; }, 1200);
      }
    }

    function updateCartBadge() {
      const totalCount = cart.reduce((acc, it) => acc + it.quantity, 0);
      const subtotal = cart.reduce((acc, it) => acc + (it.price * it.quantity), 0);
      
      const badge = document.getElementById('cartCountBadge');
      if (badge) badge.textContent = totalCount;

      const totalHeader = document.getElementById('headerCartTotal');
      if (totalHeader) totalHeader.textContent = `• ₹${subtotal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

      const submitBtn = document.getElementById('checkoutSubmitBtn');
      if (submitBtn) submitBtn.disabled = (cart.length === 0);
    }

    function renderCart() {
      const list = document.getElementById('cartItemsList');
      if (!list) return;

      if (cart.length === 0) {
        list.innerHTML = `
          <div class="py-16 text-center text-cyber-muted">
            <i data-lucide="shopping-cart" class="w-12 h-12 mx-auto mb-3 opacity-30 text-cyber-cyan"></i>
            <p class="font-bold text-white text-sm uppercase">DISPATCH MANIFEST EMPTY</p>
          </div>
        `;
        recalcCartTotals();
        lucide.createIcons();
        return;
      }

      list.innerHTML = cart.map(item => {
        const photo = productPhotos[item.product_id] || "/images/prod_1.jpg";
        const lineTotal = item.price * item.quantity;
        return `
          <div class="flex items-center gap-3 p-3 rounded bg-[#040508] border border-cyber-border">
            <img src="${photo}" alt="${item.name}" class="w-14 h-14 rounded object-cover border border-cyber-border">
            <div class="flex-1 min-w-0">
              <h5 class="text-xs font-bold text-white truncate uppercase">${item.name}</h5>
              <div class="text-[11px] font-mono text-cyber-muted mt-0.5">₹${item.price.toLocaleString('en-IN')} × ${item.quantity} = <strong class="text-cyber-cyan">₹${lineTotal.toLocaleString('en-IN')}</strong></div>
              <div class="flex items-center gap-2 mt-1.5">
                <button onclick="modifyCartItemQty(${item.product_id}, -1)" class="w-5 h-5 rounded bg-[#0E141E] border border-cyber-border flex items-center justify-center text-xs font-bold text-white">-</button>
                <span class="text-xs font-mono font-bold text-white">${item.quantity}</span>
                <button onclick="modifyCartItemQty(${item.product_id}, 1)" class="w-5 h-5 rounded bg-[#0E141E] border border-cyber-border flex items-center justify-center text-xs font-bold text-white">+</button>
                <button onclick="removeCartItem(${item.product_id})" class="text-[10px] font-mono text-cyber-magenta hover:underline ml-auto uppercase">REMOVE</button>
              </div>
            </div>
          </div>
        `;
      }).join('');

      recalcCartTotals();
      lucide.createIcons();
    }

    function modifyCartItemQty(productId, delta) {
      const it = cart.find(x => x.product_id === productId);
      if (!it) return;
      it.quantity += delta;
      if (it.quantity <= 0) {
        cart = cart.filter(x => x.product_id !== productId);
      } else if (it.quantity > it.stock) {
        it.quantity = it.stock;
      }
      updateCartBadge();
      renderCart();
    }

    function removeCartItem(productId) {
      cart = cart.filter(x => x.product_id !== productId);
      updateCartBadge();
      renderCart();
    }

    function clearCart() {
      cart = [];
      updateCartBadge();
      renderCart();
    }

    function setCustomerTier(isPrem) {
      isPremiumCustomer = isPrem;
      const regBtn = document.getElementById('tierRegularBtn');
      const premBtn = document.getElementById('tierPremiumBtn');

      if (isPrem) {
        premBtn.className = "px-3 py-1 rounded border border-cyber-magenta bg-cyber-magenta text-white font-bold transition-all";
        regBtn.className = "px-3 py-1 rounded border border-cyber-border bg-[#0E141E] text-cyber-muted font-bold hover:border-cyber-cyan transition-all";
      } else {
        regBtn.className = "px-3 py-1 rounded border border-cyber-cyan bg-cyber-cyan text-[#040508] font-bold transition-all";
        premBtn.className = "px-3 py-1 rounded border border-cyber-border bg-[#0E141E] text-cyber-muted font-bold hover:border-cyber-cyan transition-all";
      }
      recalcCartTotals();
    }

    function recalcCartTotals() {
      const subtotal = cart.reduce((acc, it) => acc + (it.price * it.quantity), 0);
      const discRate = isPremiumCustomer ? 0.10 : 0.02;
      const discAmt = subtotal * discRate;
      const taxable = subtotal - discAmt;
      const taxAmt = taxable * 0.05;
      const grandTotal = taxable + taxAmt;

      document.getElementById('cartSubtotal').textContent = `₹${subtotal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      document.getElementById('cartDiscountLabel').textContent = `TIER DISCOUNT (${(discRate * 100).toFixed(0)}%):`;
      document.getElementById('cartDiscountAmt').textContent = `-₹${discAmt.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      document.getElementById('cartTaxAmt').textContent = `₹${taxAmt.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      document.getElementById('cartGrandTotal').textContent = `₹${grandTotal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
    }

    function toggleCartDrawer(open) {
      const drawer = document.getElementById('cartDrawer');
      const backdrop = document.getElementById('cartDrawerBackdrop');

      if (open) {
        drawer.classList.remove('translate-x-full');
        backdrop.classList.remove('opacity-0', 'pointer-events-none');
        backdrop.classList.add('opacity-100');
        renderCart();
      } else {
        drawer.classList.add('translate-x-full');
        backdrop.classList.add('opacity-0', 'pointer-events-none');
        backdrop.classList.remove('opacity-100');
      }
    }

    // -------------------------------------------------------------
    // DIJKSTRA ROUTE
    // -------------------------------------------------------------
    function calculateRoute() {
      const city = document.getElementById('routeDestCity').value;
      const data = dijkstraDistances[city] || { km: 450, eta: "~7.0 Hours", path: ["Bengaluru", city] };

      document.getElementById('routeDistanceText').textContent = `${data.km} km`;
      document.getElementById('routeEtaText').textContent = data.eta;

      const pathContainer = document.getElementById('routePathNodes');
      pathContainer.innerHTML = data.path.map((node, i) => {
        const isLast = (i === data.path.length - 1);
        return `
          <span class="px-3 py-1 bg-[#0E141E] border border-cyber-border rounded text-xs font-mono font-bold ${isLast ? 'text-cyber-cyan border-cyber-cyan' : 'text-white'} flex items-center gap-1.5">
            ${i === 0 ? '<span class="w-2 h-2 rounded-full bg-cyber-green animate-pulse"></span>' : ''}
            ${node}
          </span>
          ${!isLast ? '<i data-lucide="arrow-right" class="w-3.5 h-3.5 text-cyber-cyan"></i>' : ''}
        `;
      }).join('');
      lucide.createIcons();
    }

    // -------------------------------------------------------------
    // CHECKOUT
    // -------------------------------------------------------------
    async function triggerCheckout() {
      if (cart.length === 0) return;

      const destCity = document.getElementById('cartDestinationCity').value;
      const payload = {
        customer_name: "CYBER PATRON",
        email: "patron@smartcart.internal",
        city: destCity,
        is_premium: isPremiumCustomer,
        items: cart.map(it => ({
          product_id: it.product_id,
          name: it.name,
          category: it.category,
          price: it.price,
          quantity: it.quantity,
          stock: it.stock
        }))
      };

      try {
        const res = await fetch('/api/checkout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
          toggleCartDrawer(false);
          openReceiptModal(data);
          
          if (typeof confetti !== 'undefined') {
            confetti({
              particleCount: 120,
              spread: 80,
              origin: { y: 0.6 },
              colors: ['#00F3FF', '#ED2ABE', '#00FF96', '#FF3366']
            });
          }

          clearCart();
          await loadProducts();
        } else {
          alert("Error processing checkout.");
        }
      } catch (err) {
        console.error("Checkout error:", err);
        alert("Server error during checkout.");
      }
    }

    function openReceiptModal(data) {
      document.getElementById('receiptOrderIdTag').textContent = `ORDER #SC-${data.order_id.toString().padStart(4, '0')}`;
      document.getElementById('receiptContentPre').textContent = data.receipt_text;
      
      const modal = document.getElementById('receiptModal');
      const backdrop = document.getElementById('receiptModalBackdrop');
      
      backdrop.classList.remove('opacity-0', 'pointer-events-none');
      backdrop.classList.add('opacity-100');
      modal.classList.remove('scale-95');
      modal.classList.add('scale-100');
      lucide.createIcons();
    }

    function closeReceiptModal() {
      const modal = document.getElementById('receiptModal');
      const backdrop = document.getElementById('receiptModalBackdrop');
      
      backdrop.classList.add('opacity-0', 'pointer-events-none');
      backdrop.classList.remove('opacity-100');
      modal.classList.add('scale-95');
      modal.classList.remove('scale-100');
    }

    function setCategoryFilter(cat) {
      currentCategoryFilter = cat;
      document.querySelectorAll('#categoryFilterContainer .category-pill').forEach(btn => {
        if (btn.textContent.trim().toUpperCase().includes(cat.toUpperCase()) || (cat === 'ALL' && btn.textContent.includes('ALL'))) {
          btn.className = "category-pill active px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-cyan bg-cyber-cyan text-[#040508] transition-all";
        } else {
          btn.className = "category-pill px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase border border-cyber-border bg-[#0E141E] text-cyber-muted hover:text-white hover:border-cyber-cyan transition-all";
        }
      });
      filterProducts();
    }

    function filterProducts() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const cat = currentCategoryFilter;

      const filtered = products.filter(p => {
        const matchQuery = p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q);
        const matchCategory = (cat === 'ALL' || p.category.toLowerCase() === cat.toLowerCase());
        return matchQuery && matchCategory;
      });
      renderProducts(filtered);
    }

    function initTilt() {
      if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll(".cyber-card"), {
          max: 20,
          speed: 400,
          perspective: 1000,
          scale: 1.025,
          glare: true,
          "max-glare": 0.25
        });
      }
    }

    function showToast(title, message) {
      let toast = document.getElementById('toastNotification');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toastNotification';
        toast.className = 'fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-5 py-3 rounded-xl bg-[#0B0F15] border border-cyber-cyan text-white shadow-2xl transition-all pointer-events-none';
        document.body.appendChild(toast);
      }

      toast.innerHTML = `
        <div class="w-7 h-7 rounded bg-cyber-cyan/10 border border-cyber-cyan flex items-center justify-center text-cyber-cyan">
          <i data-lucide="check" class="w-3.5 h-3.5"></i>
        </div>
        <div>
          <div class="text-xs font-mono font-bold text-white uppercase">${title}</div>
          <div class="text-[11px] font-mono text-cyber-muted">${message}</div>
        </div>
      `;

      toast.style.opacity = '1';
      toast.style.transform = 'translate(-50%, 0)';
      lucide.createIcons();

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translate(-50%, 15px)';
      }, 2500);
    }

    async function init() {
      initCustomCursor();
      initThreeHero();
      init3DTurntable();
      await loadProducts();
      calculateRoute();
      initTilt();
      lucide.createIcons();
    }

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""

with open('/home/ik7/Online_Shopping_Billing_System/web/index.html', 'w') as f:
    f.write(site_html)

print("Aaroh/Layers Hyper-Dimension Architecture applied successfully!")
