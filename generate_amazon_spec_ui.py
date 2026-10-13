import sys

site_html = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SmartCart — Prime Retail, High-Definition Gallery & Dijkstra Logistics</title>
  
  <!-- Fonts: Plus Jakarta Sans, Outfit (Clean Premium Heading), JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <!-- Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            display: ['"Outfit"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            amazon: {
              navy: '#131921',
              dark: '#232F3E',
              orange: '#FF9900',
              amber: '#F3A847',
              blue: '#007185',
              link: '#007185',
              green: '#067D62',
              red: '#B12704',
              bg: '#F7F8FA',
              border: '#E3E6E6',
              card: '#FFFFFF'
            }
          }
        }
      }
    }
  </script>

  <style>
    ::selection {
      background: #FF9900;
      color: #131921;
    }
    ::-webkit-scrollbar {
      width: 7px;
    }
    ::-webkit-scrollbar-track {
      background: #F1F2F4;
    }
    ::-webkit-scrollbar-thumb {
      background: #B5B9BD;
      border-radius: 9999px;
    }

    body {
      background-color: #F7F8FA;
      color: #0F1111;
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    /* Product Card Hover Dynamics */
    .product-card {
      background: #FFFFFF;
      border: 1px solid #E3E6E6;
      border-radius: 12px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .product-card:hover {
      border-color: #D5D9D9;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
      transform: translateY(-3px);
    }

    /* Badge Pills */
    .badge-prime {
      background: linear-gradient(135deg, #00A8E1 0%, #0073BB 100%);
      color: #FFFFFF;
      font-weight: 800;
      font-style: italic;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      letter-spacing: 0.02em;
    }

    .badge-deal {
      background: #CC0C39;
      color: #FFFFFF;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
    }

    /* Star Rating Gold */
    .star-gold {
      color: #FFA41C;
    }

    /* Modal Backdrop */
    .modal-backdrop-blur {
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Top Amazon-Grade Navigation Bar -->
  <header class="sticky top-0 z-40 bg-amazon-navy text-white shadow-md">
    
    <!-- Upper Strip -->
    <div class="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between gap-4 sm:gap-6">
      
      <!-- Brand Logo -->
      <div class="flex items-center gap-3">
        <a href="/" class="flex items-center gap-2 group">
          <div class="w-9 h-9 rounded-lg bg-amazon-orange text-amazon-navy flex items-center justify-center font-display font-black text-xl shadow-sm">
            S
          </div>
          <div>
            <span class="font-display font-extrabold text-xl tracking-tight text-white flex items-center gap-1.5">
              SmartCart
              <span class="text-amazon-orange text-xs font-mono font-bold tracking-widest uppercase">PRO</span>
            </span>
            <div class="text-[10px] text-gray-300 font-mono tracking-wider">DIRECT SQLITE & 5% GST</div>
          </div>
        </a>
      </div>

      <!-- Quick Delivery Pin -->
      <div class="hidden md:flex items-center gap-2 text-xs text-gray-300 cursor-pointer hover:text-white transition-colors" onclick="document.getElementById('routeSection').scrollIntoView({behavior: 'smooth'})">
        <i data-lucide="map-pin" class="w-4 h-4 text-amazon-orange"></i>
        <div>
          <div class="text-[10px] text-gray-400">Deliver to</div>
          <div id="navDeliverCity" class="font-bold text-white">Bengaluru (Base Hub)</div>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="flex-1 max-w-2xl relative">
        <div class="flex items-center rounded-lg bg-white overflow-hidden shadow-inner border border-transparent focus-within:border-amazon-orange focus-within:ring-2 focus-within:ring-amazon-orange/40">
          <select id="headerCategorySelect" onchange="syncCategoryFromSelect(this.value)" class="bg-gray-100 text-gray-700 text-xs font-medium px-3 py-2.5 border-r border-gray-300 focus:outline-none cursor-pointer">
            <option value="ALL">All Departments</option>
            <option value="Electronics">Electronics</option>
            <option value="Furniture">Furniture</option>
            <option value="Home & Kitchen">Home & Kitchen</option>
            <option value="Fashion">Fashion</option>
            <option value="Groceries">Groceries</option>
          </select>
          <input type="text" id="searchInput" oninput="filterProducts()" placeholder="Search products, brands, detailed specifications, keywords..." 
            class="w-full px-3.5 py-2 text-xs sm:text-sm text-gray-900 focus:outline-none">
          <button class="bg-amazon-amber hover:bg-amazon-orange text-amazon-navy px-4 py-2.5 transition-colors flex items-center justify-center">
            <i data-lucide="search" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Right Header Actions -->
      <div class="flex items-center gap-4 text-xs">
        
        <!-- Customer Pricing Tier Indicator -->
        <div class="hidden sm:block text-right">
          <div class="text-[10px] text-gray-400">Customer Tier</div>
          <button onclick="toggleCustomerTier()" id="navTierBadge" class="font-bold text-amazon-orange hover:underline cursor-pointer">
            Regular (2% Disc) ▾
          </button>
        </div>

        <!-- Cart Island Trigger -->
        <button onclick="toggleCartDrawer(true)" id="headerCartBtn" class="flex items-center gap-2.5 bg-amazon-dark hover:bg-black/40 border border-white/20 rounded-lg px-3.5 py-2 text-white font-bold transition-all">
          <div class="relative">
            <i data-lucide="shopping-cart" class="w-5 h-5 text-amazon-orange"></i>
            <span id="cartCountBadge" class="absolute -top-2 -right-2.5 bg-amazon-orange text-amazon-navy text-[11px] font-black w-4.5 h-4.5 rounded-full flex items-center justify-center font-mono">0</span>
          </div>
          <div class="text-left hidden sm:block">
            <div class="text-[10px] text-gray-300 font-normal">Subtotal</div>
            <div id="headerCartTotal" class="font-mono text-xs font-black">₹0.00</div>
          </div>
        </button>

      </div>

    </div>

    <!-- Sub-Navbar Category Strip -->
    <div class="bg-amazon-dark px-4 py-1.5 text-xs text-gray-200 border-t border-white/10 overflow-x-auto whitespace-nowrap flex items-center gap-5">
      <button onclick="setCategoryFilter('ALL')" class="category-pill active font-bold text-white hover:text-amazon-orange transition-colors flex items-center gap-1.5">
        <i data-lucide="menu" class="w-3.5 h-3.5"></i> All Catalog (16 Items)
      </button>
      <span class="text-white/20">|</span>
      <button onclick="setCategoryFilter('Electronics')" class="category-pill hover:text-amazon-orange transition-colors">Electronics & Gadgets</button>
      <button onclick="setCategoryFilter('Furniture')" class="category-pill hover:text-amazon-orange transition-colors">Home & Office Furniture</button>
      <button onclick="setCategoryFilter('Home & Kitchen')" class="category-pill hover:text-amazon-orange transition-colors">Kitchen & Dining</button>
      <button onclick="setCategoryFilter('Fashion')" class="category-pill hover:text-amazon-orange transition-colors">Fashion & Apparel</button>
      <button onclick="setCategoryFilter('Groceries')" class="category-pill hover:text-amazon-orange transition-colors">Organic Groceries</button>
      <span class="text-white/20">|</span>
      <span class="text-[11px] text-amazon-amber flex items-center gap-1 font-mono">
        <i data-lucide="shield-check" class="w-3.5 h-3.5"></i> 5% GST Statutory Compliant
      </span>
      <span class="text-[11px] text-emerald-400 flex items-center gap-1 font-mono ml-auto">
        <i data-lucide="route" class="w-3.5 h-3.5"></i> Dijkstra Shortest Highway Routing
      </span>
    </div>
  </header>

  <!-- Main Catalog Content Container -->
  <main class="max-w-7xl mx-auto px-4 py-6 flex-1 w-full space-y-8">
    
    <!-- Top Filter & Sorting Control Bar -->
    <div class="bg-white rounded-xl p-4 border border-amazon-border shadow-xs flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-display font-extrabold text-gray-900" id="currentSectionTitle">
          Featured Catalog & Prime Inventory
        </h1>
        <p class="text-xs text-gray-500 font-mono mt-0.5" id="productCountHeader">
          Showing 16 verified items with high-resolution 2D photography & Amazon-spec descriptions
        </p>
      </div>

      <!-- Sorting & View Controls -->
      <div class="flex items-center gap-3 text-xs">
        <label class="text-gray-600 font-medium hidden sm:inline">Sort by:</label>
        <select id="sortSelect" onchange="sortProducts(this.value)" class="bg-gray-50 border border-amazon-border rounded-lg px-3 py-2 text-xs font-semibold text-gray-800 focus:outline-none focus:border-amazon-orange">
          <option value="featured">Featured & Best Selling</option>
          <option value="price_low">Price: Low to High</option>
          <option value="price_high">Price: High to Low</option>
          <option value="rating">Customer Rating (High to Low)</option>
          <option value="name">Alphabetical (A - Z)</option>
        </select>

        <button onclick="toggleGroupByCategory()" id="groupByCategoryBtn" class="px-3 py-2 rounded-lg border border-amazon-border bg-gray-50 hover:bg-gray-100 text-gray-800 font-semibold text-xs transition-colors flex items-center gap-1.5">
          <i data-lucide="layers" class="w-3.5 h-3.5 text-amazon-blue"></i>
          <span id="groupByCategoryText">Group by Department</span>
        </button>
      </div>
    </div>

    <!-- Product Grid or Grouped Container -->
    <div id="catalogDisplayContainer" class="space-y-8">
      <!-- Injected via JavaScript (Either Unified Grid or Department Sections) -->
    </div>

    <!-- Live Dijkstra Delivery Route Console Section -->
    <section id="routeSection" class="bg-white rounded-2xl p-6 border border-amazon-border shadow-xs">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5 pb-4 border-b border-gray-100">
        <div>
          <div class="inline-flex items-center gap-1.5 text-xs font-mono font-bold text-amazon-blue uppercase">
            <i data-lucide="truck" class="w-3.5 h-3.5 text-amazon-orange"></i>
            Graph-Optimized Delivery Logistics (SciPy Dijkstra Engine)
          </div>
          <h2 class="text-xl font-display font-bold text-gray-900 mt-1">Shortest Road Transit Optimizer</h2>
        </div>
        <div class="flex items-center gap-3 text-xs font-mono">
          <span class="text-gray-500">Warehouse Origin: <strong class="text-gray-900">Bengaluru Base Hub</strong></span>
          <span class="text-gray-300">•</span>
          <select id="routeDestCity" onchange="calculateRoute()" class="bg-gray-50 border border-amazon-border rounded-lg px-3 py-1.5 text-xs font-bold text-gray-800 focus:outline-none focus:border-amazon-orange">
            <option value="Mumbai">Destination: Mumbai</option>
            <option value="Delhi">Destination: Delhi</option>
            <option value="Hyderabad">Destination: Hyderabad</option>
            <option value="Chennai" selected>Destination: Chennai</option>
            <option value="Kolkata">Destination: Kolkata</option>
            <option value="Pune">Destination: Pune</option>
            <option value="Ahmedabad">Destination: Ahmedabad</option>
          </select>
        </div>
      </div>

      <!-- Telemetry Output -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
        <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
          <div class="text-xs font-mono text-gray-500 uppercase">Shortest Highway Distance</div>
          <div id="routeDistanceText" class="text-3xl font-mono font-extrabold text-amazon-blue mt-1">346 km</div>
          <div class="text-[11px] font-mono text-gray-500 mt-1">Computed via <code class="text-amazon-orange font-bold">scipy.sparse.csgraph.dijkstra</code></div>
        </div>

        <div class="md:col-span-2 bg-gray-50 rounded-xl p-4 border border-gray-200 flex flex-col justify-between">
          <div>
            <div class="text-xs font-mono text-gray-500 uppercase mb-2">Transit Corridor Route Nodes:</div>
            <div id="routePathNodes" class="flex flex-wrap items-center gap-2">
              <span class="px-3 py-1 bg-white border border-gray-300 rounded-full text-xs font-mono font-bold text-gray-800 flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Bengaluru
              </span>
              <i data-lucide="arrow-right" class="w-3.5 h-3.5 text-amazon-orange"></i>
              <span class="px-3 py-1 bg-white border border-amazon-orange text-amazon-orange rounded-full text-xs font-mono font-bold">
                Chennai
              </span>
            </div>
          </div>
          <div class="text-xs font-mono text-gray-500 mt-3 pt-3 border-t border-gray-200 flex items-center justify-between">
            <span>Estimated Fleet Transit: <strong id="routeEtaText" class="text-gray-900 font-bold">~5.8 Hours</strong></span>
            <span class="text-emerald-700 font-bold flex items-center gap-1">
              <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> Prime Priority Highway Corridor
            </span>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Amazon-Style Product Detail Quick View Modal (Full 2D High-Res + Rich Spec) -->
  <div id="productDetailModalBackdrop" onclick="closeProductModal()" class="fixed inset-0 bg-black/60 modal-backdrop-blur z-50 opacity-0 pointer-events-none transition-opacity duration-200 flex items-center justify-center p-4">
    <div id="productDetailModal" onclick="event.stopPropagation()" class="bg-white rounded-2xl max-w-4xl w-full max-h-[92vh] flex flex-col shadow-2xl transform scale-95 transition-transform duration-200 overflow-hidden border border-gray-200">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50">
        <div class="flex items-center gap-2">
          <span class="badge-prime">PRIME SPEC</span>
          <span id="modalCategoryBadge" class="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-gray-200 text-gray-800">ELECTRONICS</span>
          <span id="modalSkuBadge" class="text-xs font-mono text-gray-500">SKU: SC-001</span>
        </div>
        <button onclick="closeProductModal()" class="w-8 h-8 rounded-full hover:bg-gray-200 text-gray-500 hover:text-gray-800 flex items-center justify-center transition-colors">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Modal Body (Two-Column Layout: Left High-Res 2D Photo, Right Rich Specs) -->
      <div class="p-6 overflow-y-auto grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        
        <!-- Left: Crisp 2D Product Photography -->
        <div class="md:col-span-5 space-y-3">
          <div class="w-full h-80 rounded-xl overflow-hidden border border-gray-200 bg-white flex items-center justify-center p-2 shadow-xs group">
            <img id="modalProductImage" src="/images/prod_1.jpg" alt="Product Image" class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300">
          </div>
          <div class="text-[11px] text-gray-400 text-center font-mono">
            Verified 100% authentic product photograph • Sealed original package
          </div>
        </div>

        <!-- Right: Amazon Specification Breakdown -->
        <div class="md:col-span-7 space-y-4">
          <div>
            <h2 id="modalProductTitle" class="text-xl sm:text-2xl font-display font-bold text-gray-900 leading-snug">
              Wireless Noise-Canceling Headphones
            </h2>
            
            <!-- Ratings Strip -->
            <div class="flex items-center gap-2 mt-2">
              <div class="flex items-center text-sm star-gold" id="modalStarsContainer">
                ★★★★★
              </div>
              <span id="modalRatingText" class="text-xs font-bold text-amazon-blue">4.8</span>
              <span class="text-xs text-gray-400">•</span>
              <span id="modalReviewCount" class="text-xs text-amazon-blue hover:underline cursor-pointer">1,420 ratings</span>
            </div>
          </div>

          <!-- Pricing & 5% GST Breakdown -->
          <div class="p-3.5 bg-gray-50 rounded-xl border border-gray-200 space-y-1">
            <div class="flex items-baseline gap-2">
              <span class="text-xs text-red-600 font-bold uppercase tracking-wider">Deal of the Day:</span>
              <span id="modalProductPrice" class="text-3xl font-mono font-black text-gray-900">₹3,499.00</span>
              <span class="text-xs text-gray-500 font-mono">(Inclusive of 5% Statutory GST)</span>
            </div>
            <div class="text-xs text-gray-600 flex justify-between font-mono pt-1 border-t border-gray-200">
              <span>Base Subtotal: <strong id="modalTaxableSubtotal" class="text-gray-900">₹3,332.38</strong></span>
              <span>5% GST: <strong id="modalGstAmount" class="text-amazon-green">₹166.62</strong></span>
            </div>
          </div>

          <!-- Description Section -->
          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-gray-900 mb-1.5 flex items-center gap-1.5">
              <i data-lucide="info" class="w-4 h-4 text-amazon-blue"></i>
              About this item (Detailed Specifications)
            </h4>
            <p id="modalProductDescription" class="text-sm text-gray-700 leading-relaxed bg-white border border-gray-100 p-3 rounded-lg shadow-xs">
              Hybrid Active Noise Cancellation (ANC) with 40mm dynamic drivers. Features 35-hour extended battery life, dual ambient pass-through mode, and plush protein leather earcups.
            </p>
          </div>

          <!-- Fast Add to Cart Button Strip -->
          <div class="pt-2 flex items-center gap-3">
            <div class="flex items-center border border-gray-300 rounded-lg bg-gray-50 px-2 py-1.5">
              <button onclick="adjustModalQty(-1)" class="w-6 h-6 text-gray-700 hover:text-black font-bold text-sm">-</button>
              <input type="number" id="modalQtyInput" min="1" max="99" value="1" class="w-10 bg-transparent text-center text-xs font-mono font-bold text-gray-900 focus:outline-none">
              <button onclick="adjustModalQty(1)" class="w-6 h-6 text-gray-700 hover:text-black font-bold text-sm">+</button>
            </div>

            <button onclick="addModalProductToCart()" class="flex-1 py-2.5 px-5 rounded-lg bg-amazon-amber hover:bg-amazon-orange text-amazon-navy font-bold text-xs tracking-wider uppercase transition-colors flex items-center justify-center gap-2 shadow-xs">
              <i data-lucide="shopping-cart" class="w-4 h-4"></i>
              <span id="modalAddBtnLabel">Add to Shopping Cart</span>
            </button>
          </div>

        </div>

      </div>

    </div>
  </div>

  <!-- Cart Slide-Over Drawer -->
  <div id="cartDrawerBackdrop" onclick="toggleCartDrawer(false)" class="fixed inset-0 bg-black/60 modal-backdrop-blur z-50 opacity-0 pointer-events-none transition-opacity duration-200"></div>

  <aside id="cartDrawer" class="fixed top-0 right-0 h-full w-full max-w-md bg-white border-l border-amazon-border shadow-2xl z-50 transform translate-x-full transition-transform duration-250 ease-out flex flex-col">
    <div class="p-4 border-b border-gray-200 flex items-center justify-between bg-amazon-navy text-white">
      <div class="flex items-center gap-2">
        <i data-lucide="shopping-cart" class="w-5 h-5 text-amazon-orange"></i>
        <div>
          <h3 class="font-display font-bold text-base">Your Shopping Cart</h3>
          <p class="text-[10px] text-gray-300 font-mono">SQLite Invoicing & Real-time Decrement</p>
        </div>
      </div>
      <button onclick="toggleCartDrawer(false)" class="w-8 h-8 rounded hover:bg-white/10 text-gray-300 hover:text-white flex items-center justify-center transition-colors">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
    </div>

    <!-- Customer Tier Toggle -->
    <div class="p-3.5 bg-gray-100 border-b border-gray-200 flex items-center justify-between text-xs">
      <span class="text-gray-600 font-medium">Customer Membership:</span>
      <div class="flex items-center gap-2">
        <button id="tierRegularBtn" onclick="setCustomerTier(false)" class="px-2.5 py-1 rounded border border-amazon-orange bg-amazon-orange text-amazon-navy font-bold text-xs transition-all">Regular (2%)</button>
        <button id="tierPremiumBtn" onclick="setCustomerTier(true)" class="px-2.5 py-1 rounded border border-gray-300 bg-white text-gray-700 font-bold text-xs hover:border-amazon-orange transition-all">Prime Member (10%)</button>
      </div>
    </div>

    <!-- Items list -->
    <div id="cartItemsList" class="flex-1 overflow-y-auto p-4 space-y-3">
      <!-- Injected via renderCart() -->
    </div>

    <!-- Footer Summary & Checkout -->
    <div class="p-4 border-t border-gray-200 bg-gray-50 space-y-3">
      <div class="space-y-1.5 text-xs font-mono">
        <div class="flex justify-between text-gray-600">
          <span>Subtotal:</span>
          <span id="cartSubtotal" class="font-bold text-gray-900">₹0.00</span>
        </div>
        <div class="flex justify-between text-emerald-700">
          <span id="cartDiscountLabel">Tier Discount (2%):</span>
          <span id="cartDiscountAmt" class="font-bold">-₹0.00</span>
        </div>
        <div class="flex justify-between text-gray-600">
          <span>5% Statutory GST:</span>
          <span id="cartTaxAmt" class="font-bold text-gray-900">₹0.00</span>
        </div>
        <div class="pt-2 border-t border-gray-200 flex justify-between items-baseline text-sm">
          <span class="font-bold text-gray-900">Total Payable:</span>
          <span id="cartGrandTotal" class="text-2xl font-mono font-black text-amazon-red">₹0.00</span>
        </div>
      </div>

      <!-- Destination Hub -->
      <div>
        <label class="block text-[11px] font-mono text-gray-600 mb-1">Dispatch Hub:</label>
        <select id="cartDestinationCity" class="w-full text-xs font-mono bg-white border border-gray-300 rounded px-2.5 py-1.5 focus:outline-none focus:border-amazon-orange">
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
      <div class="pt-1 flex gap-2">
        <button onclick="clearCart()" class="px-3 py-2 rounded bg-white border border-gray-300 text-gray-600 hover:text-black text-xs font-medium flex items-center justify-center gap-1">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Clear
        </button>
        <button onclick="triggerCheckout()" id="checkoutSubmitBtn" class="flex-1 py-2.5 px-4 rounded bg-amazon-amber hover:bg-amazon-orange text-amazon-navy font-bold text-xs tracking-wider uppercase transition-colors flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-40 disabled:cursor-not-allowed">
          <span>Place Order & Generate Invoice</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>
      </div>
    </div>
  </aside>

  <!-- Checkout Tax Invoice Modal -->
  <div id="receiptModalBackdrop" class="fixed inset-0 bg-black/60 modal-backdrop-blur z-50 opacity-0 pointer-events-none transition-opacity duration-200 flex items-center justify-center p-4">
    <div id="receiptModal" class="bg-white rounded-2xl max-w-xl w-full max-h-[90vh] flex flex-col shadow-2xl transform scale-95 transition-transform duration-200 border border-gray-200">
      <div class="p-4 border-b border-gray-200 flex items-center justify-between bg-amazon-navy text-white rounded-t-2xl">
        <div class="flex items-center gap-2">
          <i data-lucide="check-circle" class="w-5 h-5 text-emerald-400"></i>
          <div>
            <h3 class="font-display font-bold text-base">Order Placed & Invoiced</h3>
            <p id="receiptOrderIdTag" class="text-xs font-mono text-amazon-orange">ORDER #SC-0000</p>
          </div>
        </div>
        <button onclick="closeReceiptModal()" class="w-8 h-8 rounded hover:bg-white/10 text-gray-300 hover:text-white flex items-center justify-center transition-colors">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="p-4 flex-1 overflow-y-auto">
        <pre id="receiptContentPre" class="p-4 bg-gray-50 border border-gray-200 rounded-xl font-mono text-xs text-gray-900 leading-relaxed whitespace-pre-wrap select-all overflow-x-auto"></pre>
      </div>

      <div class="p-4 border-t border-gray-200 bg-gray-50 flex items-center justify-between rounded-b-2xl">
        <div class="text-xs font-mono text-emerald-700 flex items-center gap-1.5 font-bold">
          <i data-lucide="file-check" class="w-4 h-4"></i>
          Stored in SQLite & CSV ledger
        </div>
        <button onclick="closeReceiptModal()" class="px-5 py-2 rounded bg-amazon-navy hover:bg-gray-800 text-white font-bold text-xs uppercase tracking-wider transition-colors">
          Done & Continue
        </button>
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT APPLICATION CORE -->
  <script>
    let products = [];
    let currentCategoryFilter = 'ALL';
    let currentSort = 'featured';
    let isGroupedView = false;
    let cart = [];
    let isPremiumCustomer = false;
    let selectedModalProduct = null;

    // -------------------------------------------------------------
    // DATA FETCHING & RENDERING
    // -------------------------------------------------------------
    async function loadProducts() {
      try {
        const res = await fetch('/api/products');
        products = await res.json();
        renderCatalog();
      } catch (err) {
        console.error("Error loading products:", err);
      }
    }

    function renderCatalog() {
      const container = document.getElementById('catalogDisplayContainer');
      const filtered = getFilteredAndSortedProducts();

      document.getElementById('productCountHeader').textContent = 
        `Showing ${filtered.length} verified products with high-resolution 2D photography & Amazon-spec descriptions`;

      if (filtered.length === 0) {
        container.innerHTML = `
          <div class="py-16 text-center text-gray-500 bg-white rounded-2xl border border-amazon-border">
            <i data-lucide="package-search" class="w-12 h-12 mx-auto mb-3 opacity-30 text-gray-400"></i>
            <p class="text-base font-bold text-gray-800">No matching items found</p>
            <p class="text-xs text-gray-500 mt-1">Try resetting department filters or search keywords.</p>
          </div>
        `;
        lucide.createIcons();
        return;
      }

      if (isGroupedView && currentCategoryFilter === 'ALL') {
        // Grouped by Category View
        const categories = [...new Set(filtered.map(p => p.category))].sort();
        container.innerHTML = categories.map(cat => {
          const catProducts = filtered.filter(p => p.category === cat);
          return `
            <div class="space-y-4">
              <div class="flex items-center justify-between pb-2 border-b-2 border-amazon-navy">
                <h3 class="text-lg font-display font-extrabold text-gray-900 flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-amazon-orange"></span>
                  ${cat} (${catProducts.length} items)
                </h3>
                <button onclick="setCategoryFilter('${cat}')" class="text-xs font-bold text-amazon-blue hover:underline">
                  View department ↗
                </button>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                ${catProducts.map(renderProductCardHTML).join('')}
              </div>
            </div>
          `;
        }).join('');
      } else {
        // Flat Unified Grid
        container.innerHTML = `
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            ${filtered.map(renderProductCardHTML).join('')}
          </div>
        `;
      }

      lucide.createIcons();
    }

    function renderProductCardHTML(p) {
      const inStock = p.stock > 0;
      const lowStock = p.stock > 0 && p.stock <= 5;
      const photoUrl = `/images/prod_${p.product_id}.jpg`;
      const rating = p.rating || 4.5;
      const reviewCount = p.review_count || 120;
      const shortDesc = p.description ? p.description.substring(0, 85) + '...' : 'Premium high-durability build quality.';

      return `
        <div class="product-card p-4 flex flex-col justify-between h-full group">
          <div>
            <!-- 2D High-Res Product Image Box -->
            <div class="relative w-full h-48 rounded-lg overflow-hidden mb-3 bg-white border border-gray-100 flex items-center justify-center p-2 cursor-pointer" onclick="openProductModal(${p.product_id})">
              <img src="${photoUrl}" alt="${p.name}" class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300">
              
              <div class="absolute top-2 left-2 flex items-center gap-1">
                <span class="badge-prime">PRIME</span>
              </div>

              ${p.price > 2000 ? '<span class="absolute top-2 right-2 badge-deal">Limited Deal</span>' : ''}
            </div>

            <!-- Department Pill -->
            <div class="text-[10px] font-mono font-bold text-gray-500 uppercase tracking-wider mb-1">${p.category}</div>

            <!-- Product Title -->
            <h4 class="font-display font-bold text-sm text-gray-900 group-hover:text-amazon-blue leading-snug cursor-pointer line-clamp-2 mb-1.5" onclick="openProductModal(${p.product_id})">
              ${p.name}
            </h4>

            <!-- Ratings Strip -->
            <div class="flex items-center gap-1.5 text-xs mb-2">
              <span class="star-gold font-bold text-xs">★ ${rating.toFixed(1)}</span>
              <span class="text-gray-400">•</span>
              <span class="text-gray-500 text-[11px] font-mono">(${reviewCount.toLocaleString()})</span>
            </div>

            <!-- 2D Product Description Excerpt -->
            <p class="text-xs text-gray-600 line-clamp-2 leading-relaxed mb-3">
              ${shortDesc}
            </p>
          </div>

          <!-- Price & Actions Footer -->
          <div class="pt-3 border-t border-gray-100 space-y-2">
            <div class="flex items-baseline justify-between">
              <div>
                <span class="text-xs text-gray-500 font-mono">₹</span>
                <span class="text-xl font-mono font-black text-gray-900">${p.price.toLocaleString('en-IN', {minimumFractionDigits: 0})}</span>
              </div>
              <span class="text-[10px] font-mono ${inStock ? (lowStock ? 'text-amber-600 font-bold' : 'text-emerald-700') : 'text-red-600 font-bold'}">
                ${inStock ? (lowStock ? `Only ${p.stock} left` : 'In Stock') : 'Out of Stock'}
              </span>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <button onclick="openProductModal(${p.product_id})" class="px-2.5 py-1.5 rounded-lg border border-gray-300 hover:border-gray-400 text-gray-700 text-xs font-semibold hover:bg-gray-50 transition-colors flex items-center justify-center gap-1" title="View Full 2D Specs">
                <i data-lucide="eye" class="w-3.5 h-3.5"></i>
              </button>

              <button onclick="addToCartDirect(${p.product_id})" ${!inStock ? 'disabled' : ''} class="flex-1 py-1.5 px-3 rounded-lg bg-amazon-amber hover:bg-amazon-orange text-amazon-navy font-bold text-xs tracking-wider transition-colors flex items-center justify-center gap-1.5 shadow-xs disabled:opacity-40 disabled:cursor-not-allowed">
                <i data-lucide="shopping-cart" class="w-3.5 h-3.5"></i>
                <span>Add to Cart</span>
              </button>
            </div>
          </div>
        </div>
      `;
    }

    function getFilteredAndSortedProducts() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const cat = currentCategoryFilter;

      let list = products.filter(p => {
        const matchQuery = p.name.toLowerCase().includes(q) || 
                           p.category.toLowerCase().includes(q) ||
                           (p.description && p.description.toLowerCase().includes(q));
        const matchCategory = (cat === 'ALL' || p.category.toLowerCase() === cat.toLowerCase());
        return matchQuery && matchCategory;
      });

      if (currentSort === 'price_low') {
        list.sort((a, b) => a.price - b.price);
      } else if (currentSort === 'price_high') {
        list.sort((a, b) => b.price - a.price);
      } else if (currentSort === 'rating') {
        list.sort((a, b) => (b.rating || 0) - (a.rating || 0));
      } else if (currentSort === 'name') {
        list.sort((a, b) => a.name.localeCompare(b.name));
      }

      return list;
    }

    function sortProducts(val) {
      currentSort = val;
      renderCatalog();
    }

    function toggleGroupByCategory() {
      isGroupedView = !isGroupedView;
      const textElem = document.getElementById('groupByCategoryText');
      textElem.textContent = isGroupedView ? "Unified Grid View" : "Group by Department";
      renderCatalog();
    }

    function setCategoryFilter(cat) {
      currentCategoryFilter = cat;
      const select = document.getElementById('headerCategorySelect');
      if (select) select.value = cat;

      const title = document.getElementById('currentSectionTitle');
      title.textContent = cat === 'ALL' ? "Featured Catalog & Prime Inventory" : `${cat} Department`;

      document.querySelectorAll('.category-pill').forEach(btn => {
        if (btn.textContent.includes(cat) || (cat === 'ALL' && btn.textContent.includes('All Catalog'))) {
          btn.className = "category-pill active font-bold text-white hover:text-amazon-orange transition-colors flex items-center gap-1.5";
        } else {
          btn.className = "category-pill hover:text-amazon-orange transition-colors";
        }
      });
      renderCatalog();
    }

    function syncCategoryFromSelect(cat) {
      setCategoryFilter(cat);
    }

    function filterProducts() {
      renderCatalog();
    }

    // -------------------------------------------------------------
    // PRODUCT DETAIL QUICK-VIEW MODAL (2D + AMAZON SPEC)
    // -------------------------------------------------------------
    function openProductModal(productId) {
      const p = products.find(x => x.product_id === productId);
      if (!p) return;
      selectedModalProduct = p;

      document.getElementById('modalProductImage').src = `/images/prod_${p.product_id}.jpg`;
      document.getElementById('modalProductTitle').textContent = p.name;
      document.getElementById('modalCategoryBadge').textContent = p.category.toUpperCase();
      document.getElementById('modalSkuBadge').textContent = `SKU: SC-${p.product_id.toString().padStart(3, '0')}`;
      
      const rating = p.rating || 4.5;
      document.getElementById('modalRatingText').textContent = rating.toFixed(1);
      document.getElementById('modalReviewCount').textContent = `${(p.review_count || 128).toLocaleString()} ratings`;
      
      document.getElementById('modalProductPrice').textContent = `₹${p.price.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      
      // Compute 5% GST breakdown
      const taxable = p.price / 1.05;
      const gst = p.price - taxable;
      document.getElementById('modalTaxableSubtotal').textContent = `₹${taxable.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      document.getElementById('modalGstAmount').textContent = `₹${gst.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

      document.getElementById('modalProductDescription').textContent = p.description || 
        "Engineered with premium food-grade and commercial alloys. Fully verified for endurance, ergonomics, and longevity.";

      document.getElementById('modalQtyInput').value = 1;

      const backdrop = document.getElementById('productDetailModalBackdrop');
      const modal = document.getElementById('productDetailModal');

      backdrop.classList.remove('opacity-0', 'pointer-events-none');
      backdrop.classList.add('opacity-100');
      modal.classList.remove('scale-95');
      modal.classList.add('scale-100');
      lucide.createIcons();
    }

    function closeProductModal() {
      const backdrop = document.getElementById('productDetailModalBackdrop');
      const modal = document.getElementById('productDetailModal');

      backdrop.classList.add('opacity-0', 'pointer-events-none');
      backdrop.classList.remove('opacity-100');
      modal.classList.add('scale-95');
      modal.classList.remove('scale-100');
    }

    function adjustModalQty(delta) {
      const input = document.getElementById('modalQtyInput');
      let val = parseInt(input.value) || 1;
      val += delta;
      if (val < 1) val = 1;
      if (selectedModalProduct && val > selectedModalProduct.stock) val = selectedModalProduct.stock;
      input.value = val;
    }

    function addModalProductToCart() {
      if (!selectedModalProduct) return;
      const qty = parseInt(document.getElementById('modalQtyInput').value) || 1;
      addToCartWithQty(selectedModalProduct.product_id, qty);
      closeProductModal();
    }

    function addToCartDirect(productId) {
      addToCartWithQty(productId, 1);
    }

    // -------------------------------------------------------------
    // CART ENGINE & PRICING TIERS
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
      showToast("Item added to cart", `${quantity}x ${p.name}`);
    }

    function updateCartBadge() {
      const totalCount = cart.reduce((acc, it) => acc + it.quantity, 0);
      const subtotal = cart.reduce((acc, it) => acc + (it.price * it.quantity), 0);
      
      document.getElementById('cartCountBadge').textContent = totalCount;
      document.getElementById('headerCartTotal').textContent = `₹${subtotal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

      const submitBtn = document.getElementById('checkoutSubmitBtn');
      if (submitBtn) submitBtn.disabled = (cart.length === 0);
    }

    function renderCart() {
      const list = document.getElementById('cartItemsList');
      if (!list) return;

      if (cart.length === 0) {
        list.innerHTML = `
          <div class="py-16 text-center text-gray-500">
            <i data-lucide="shopping-cart" class="w-12 h-12 mx-auto mb-3 opacity-30 text-gray-400"></i>
            <p class="font-bold text-gray-800 text-sm">Your shopping cart is empty</p>
            <p class="text-xs text-gray-500 mt-1">Select items from the catalog to build your shipment.</p>
          </div>
        `;
        recalcCartTotals();
        lucide.createIcons();
        return;
      }

      list.innerHTML = cart.map(item => {
        const photoUrl = `/images/prod_${item.product_id}.jpg`;
        const lineTotal = item.price * item.quantity;
        return `
          <div class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 border border-gray-200">
            <img src="${photoUrl}" alt="${item.name}" class="w-14 h-14 rounded object-contain bg-white border border-gray-200 p-1">
            <div class="flex-1 min-w-0">
              <h5 class="text-xs font-bold text-gray-900 truncate">${item.name}</h5>
              <div class="text-[11px] font-mono text-gray-500 mt-0.5">₹${item.price.toLocaleString('en-IN')} × ${item.quantity} = <strong class="text-gray-900">₹${lineTotal.toLocaleString('en-IN')}</strong></div>
              <div class="flex items-center gap-2 mt-1.5">
                <button onclick="modifyCartItemQty(${item.product_id}, -1)" class="w-5 h-5 rounded bg-white border border-gray-300 flex items-center justify-center text-xs font-bold text-gray-800 hover:bg-gray-100">-</button>
                <span class="text-xs font-mono font-bold text-gray-900">${item.quantity}</span>
                <button onclick="modifyCartItemQty(${item.product_id}, 1)" class="w-5 h-5 rounded bg-white border border-gray-300 flex items-center justify-center text-xs font-bold text-gray-800 hover:bg-gray-100">+</button>
                <button onclick="removeCartItem(${item.product_id})" class="text-[10px] text-red-600 hover:underline ml-auto">Delete</button>
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
      const navBadge = document.getElementById('navTierBadge');

      if (isPrem) {
        premBtn.className = "px-2.5 py-1 rounded border border-amazon-orange bg-amazon-orange text-amazon-navy font-bold text-xs transition-all";
        regBtn.className = "px-2.5 py-1 rounded border border-gray-300 bg-white text-gray-700 font-bold text-xs hover:border-amazon-orange transition-all";
        navBadge.textContent = "Prime Member (10% Disc) ▾";
      } else {
        regBtn.className = "px-2.5 py-1 rounded border border-amazon-orange bg-amazon-orange text-amazon-navy font-bold text-xs transition-all";
        premBtn.className = "px-2.5 py-1 rounded border border-gray-300 bg-white text-gray-700 font-bold text-xs hover:border-amazon-orange transition-all";
        navBadge.textContent = "Regular (2% Disc) ▾";
      }
      recalcCartTotals();
    }

    function toggleCustomerTier() {
      setCustomerTier(!isPremiumCustomer);
    }

    function recalcCartTotals() {
      const subtotal = cart.reduce((acc, it) => acc + (it.price * it.quantity), 0);
      const discRate = isPremiumCustomer ? 0.10 : 0.02;
      const discAmt = subtotal * discRate;
      const taxable = subtotal - discAmt;
      const taxAmt = taxable * 0.05;
      const grandTotal = taxable + taxAmt;

      document.getElementById('cartSubtotal').textContent = `₹${subtotal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      document.getElementById('cartDiscountLabel').textContent = `Tier Discount (${(discRate * 100).toFixed(0)}%):`;
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
    // LIVE DIJKSTRA SHORT ROUTE (PYTHON SCIPY BACKEND)
    // -------------------------------------------------------------
    async function calculateRoute() {
      const city = document.getElementById('routeDestCity').value;
      document.getElementById('navDeliverCity').textContent = `${city} Hub`;
      try {
        const res = await fetch(`/api/route?city=${encodeURIComponent(city)}`);
        const data = await res.json();

        document.getElementById('routeDistanceText').textContent = `${data.distance_km} km`;
        document.getElementById('routeEtaText').textContent = data.eta;

        const pathContainer = document.getElementById('routePathNodes');
        pathContainer.innerHTML = data.path.map((node, i) => {
          const isLast = (i === data.path.length - 1);
          return `
            <span class="px-3 py-1 bg-white border border-gray-300 rounded-full text-xs font-mono font-bold ${isLast ? 'text-amazon-orange border-amazon-orange' : 'text-gray-800'} flex items-center gap-1.5">
              ${i === 0 ? '<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>' : ''}
              ${node}
            </span>
            ${!isLast ? '<i data-lucide="arrow-right" class="w-3.5 h-3.5 text-amazon-orange"></i>' : ''}
          `;
        }).join('');
        lucide.createIcons();
      } catch (err) {
        console.warn("Route API note:", err);
      }
    }

    // -------------------------------------------------------------
    // CHECKOUT & INVOICING
    // -------------------------------------------------------------
    async function triggerCheckout() {
      if (cart.length === 0) return;

      const destCity = document.getElementById('cartDestinationCity').value;
      const payload = {
        customer_name: "Valued Patron",
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
              particleCount: 110,
              spread: 70,
              origin: { y: 0.6 },
              colors: ['#FF9900', '#131921', '#067D62', '#CC0C39']
            });
          }

          clearCart();
          await loadProducts();
        } else {
          alert("Error processing order checkout.");
        }
      } catch (err) {
        console.error("Checkout error:", err);
        alert("Server communication error during checkout.");
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

    function showToast(title, message) {
      let toast = document.getElementById('toastNotification');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toastNotification';
        toast.className = 'fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-5 py-3 rounded-xl bg-amazon-navy text-white shadow-2xl border border-white/20 transition-all pointer-events-none';
        document.body.appendChild(toast);
      }

      toast.innerHTML = `
        <div class="w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
          ✓
        </div>
        <div>
          <div class="text-xs font-bold leading-tight">${title}</div>
          <div class="text-[11px] text-gray-300 font-mono">${message}</div>
        </div>
      `;

      toast.style.opacity = '1';
      toast.style.transform = 'translate(-50%, 0)';

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translate(-50%, 15px)';
      }, 2500);
    }

    async function init() {
      await loadProducts();
      calculateRoute();
      lucide.createIcons();
    }

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""

with open('/home/ik7/Online_Shopping_Billing_System/web/index.html', 'w') as f:
    f.write(site_html)

print("Amazon-Spec 2D Product Gallery UI successfully deployed to index.html!")
