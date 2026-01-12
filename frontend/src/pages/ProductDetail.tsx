import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { ArrowLeft, Heart, Share2, Check, Sparkles, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useProduct, useProducts } from "@/hooks/useProducts";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const ProductDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: product, isLoading: productLoading } = useProduct(id ?? "");

  // Use products hook to get related products
  // In a real app, this should be a dedicated endpoint
  const { data: allProducts } = useProducts(product?.category);

  const [selectedColor, setSelectedColor] = useState(0);
  const [selectedSize, setSelectedSize] = useState<string | null>(null);
  const [isWishlisted, setIsWishlisted] = useState(false);

  if (productLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="font-display text-3xl mb-4">Product not found</h1>
          <Button onClick={() => navigate("/")}>Back to Home</Button>
        </div>
      </div>
    );
  }

  const relatedProducts = allProducts
    ?.filter(p => p.id !== product.id)
    .slice(0, 3) || [];

  // Helper to get hex color
  const getColorHex = (colorName: string) => {
    const map: Record<string, string> = {
      'ivory': '#FFFFF0',
      'blush': '#FFB6C1',
      'navy': '#000080',
      'camel': '#C19A6B',
      'black': '#000000',
      'charcoal': '#36454F',
      'terracotta': '#E2725B',
      'sage': '#9CAF88',
      'cream': '#FFFDD0',
      'oatmeal': '#D7C4A7',
      'heather grey': '#9E9E9E',
      'champagne': '#F7E7CE',
      'dusty rose': '#DCAE96',
      'tan': '#D2B48C',
      'burgundy': '#722F37',
      'gold': '#FFD700',
      'silver': '#C0C0C0',
      'rose gold': '#B76E79',
    };
    return map[colorName.toLowerCase()] || '#E5E5E5';
  };

  // Helper to get image based on color choice (Mock implementation for Product 1)
  const getProductImage = () => {
    if (!product) return "";

    // Demo logic for Silk Button Blouse (ID 1)
    if (product.id === 1) {
      const color = product.colors[selectedColor].toLowerCase();
      if (color === 'navy') return '/assets/clothing-1-navy.png';
      if (color === 'blush') return '/assets/clothing-1-blush.png';
    }

    // Demo logic for Flowing Midi Dress (ID 3)
    if (product.id === 3) {
      const color = product.colors[selectedColor].toLowerCase();
      if (color === 'sage') return '/assets/clothing-3-sage.png';
      if (color === 'terracotta') return '/assets/clothing-3-terracotta.png';
      if (color === 'cream') return '/assets/clothing-3-cream.png';
    }

    return product.image;
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="pt-24 pb-16">
        <div className="container mx-auto px-6">
          {/* Breadcrumb */}
          <nav className="mb-8">
            <button
              onClick={() => navigate(-1)}
              className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-smooth"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Collection</span>
            </button>
          </nav>

          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16">
            {/* Product Image */}
            <div className="relative">
              <div className="aspect-[3/4] rounded-3xl overflow-hidden bg-card relative">
                <img
                  src={getProductImage()}
                  alt={product.name}
                  className="w-full h-full object-cover transition-opacity duration-300"
                />
              </div>

              {/* Category badge */}
              <div className="absolute top-6 left-6">
                <span className="px-4 py-2 bg-background/90 backdrop-blur-sm text-foreground text-sm font-medium rounded-full">
                  {product.category}
                </span>
              </div>

              {/* Action buttons */}
              <div className="absolute top-6 right-6 flex gap-2">
                <button
                  onClick={() => setIsWishlisted(!isWishlisted)}
                  className={`w-12 h-12 rounded-full backdrop-blur-sm flex items-center justify-center shadow-soft transition-smooth ${isWishlisted ? 'bg-primary text-primary-foreground' : 'bg-background/90 hover:bg-background'
                    }`}
                >
                  <Heart className={`w-5 h-5 ${isWishlisted ? 'fill-current' : ''}`} />
                </button>
                <button className="w-12 h-12 rounded-full bg-background/90 backdrop-blur-sm flex items-center justify-center shadow-soft hover:bg-background transition-smooth">
                  <Share2 className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Product Info */}
            <div className="flex flex-col">
              <div className="mb-6">
                <p className="text-muted-foreground text-lg mb-2">{product.brand}</p>
                <h1 className="font-display text-4xl md:text-5xl font-medium mb-4">{product.name}</h1>
                <p className="text-3xl font-semibold text-foreground">${product.price}</p>
              </div>

              <p className="text-muted-foreground leading-relaxed mb-8">
                {product.description}
              </p>

              {/* Color Selection */}
              <div className="mb-8">
                <h3 className="font-medium mb-4">Color: <span className="text-muted-foreground">{product.colors[selectedColor]}</span></h3>
                <div className="flex gap-3">
                  {product.colors.map((color, index) => (
                    <button
                      key={color}
                      onClick={() => setSelectedColor(index)}
                      className={`w-12 h-12 rounded-full border-2 flex items-center justify-center transition-smooth ${selectedColor === index
                        ? 'border-primary'
                        : 'border-border hover:border-muted-foreground'
                        }`}
                      style={{
                        backgroundColor: getColorHex(color)
                      }}
                    >
                      {selectedColor === index && (
                        <Check className={`w-5 h-5 ${['black', 'navy', 'charcoal', 'burgundy'].includes(color.toLowerCase()) ? 'text-white' : 'text-foreground'}`} />
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* Size Selection */}
              <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-medium">Size</h3>
                  <button className="text-sm text-primary hover:underline">Size Guide</button>
                </div>
                <div className="flex flex-wrap gap-3">
                  {product.sizes.map((size) => (
                    <button
                      key={size}
                      onClick={() => setSelectedSize(size)}
                      className={`min-w-[3rem] px-4 py-3 rounded-xl border-2 font-medium transition-smooth ${selectedSize === size
                        ? 'border-primary bg-primary/10 text-primary'
                        : 'border-border hover:border-muted-foreground'
                        }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-4 mb-8">
                <Button variant="hero" size="lg" className="w-full gap-2">
                  <Sparkles className="w-5 h-5" />
                  Try It On Virtually
                </Button>
                <Button variant="default" size="lg" className="w-full">
                  Add to Bag
                </Button>
              </div>

              {/* Product Details */}
              <div className="border-t border-border pt-8">
                <h3 className="font-medium mb-4">Product Details</h3>
                <ul className="space-y-2">
                  {product.details.map((detail, index) => (
                    <li key={index} className="flex items-start gap-2 text-muted-foreground">
                      <Check className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                      <span>{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Related Products */}
          {relatedProducts.length > 0 && (
            <section className="mt-24">
              <h2 className="font-display text-3xl font-medium mb-8">You May Also Like</h2>
              <div className="grid md:grid-cols-3 gap-8">
                {relatedProducts.map((item) => (
                  <Link
                    key={item.id}
                    to={`/product/${item.id}`}
                    className="group"
                  >
                    <div className="relative aspect-[3/4] rounded-2xl overflow-hidden bg-card mb-4">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-full h-full object-cover transition-smooth group-hover:scale-105"
                      />
                      <div className="absolute inset-0 bg-foreground/0 group-hover:bg-foreground/10 transition-smooth" />
                    </div>
                    <p className="text-sm text-muted-foreground">{item.brand}</p>
                    <h3 className="font-display text-lg font-medium">{item.name}</h3>
                    <p className="text-lg font-semibold">${item.price}</p>
                  </Link>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ProductDetail;
