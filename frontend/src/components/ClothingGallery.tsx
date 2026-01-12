import { useState } from "react";
import { Link } from "react-router-dom";
import { Heart, Eye, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { categories } from "@/data/products";
import { useProducts } from "@/hooks/useProducts";

const ClothingGallery = () => {
  const [activeCategory, setActiveCategory] = useState("All");
  const { data: products, isLoading, error } = useProducts(activeCategory);

  if (isLoading) {
    return (
      <section id="collection" className="py-24 lg:py-32 bg-background">
        <div className="container mx-auto px-6 flex justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </section>
    );
  }

  if (error) {
    return <div className="text-center py-24 text-red-500">Failed to load products</div>
  }

  return (
    <section id="collection" className="py-24 lg:py-32 bg-background">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <span className="inline-block px-4 py-1.5 bg-primary/10 text-primary text-sm font-medium rounded-full mb-4">
              Collection
            </span>
            <h2 className="font-display text-4xl md:text-5xl font-medium tracking-tight">
              Curated <span className="text-gradient">Pieces</span>
            </h2>
          </div>

          {/* Category filters */}
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <Button
                key={category}
                variant={activeCategory === category ? "default" : "pill"}
                size="sm"
                onClick={() => setActiveCategory(category)}
              >
                {category}
              </Button>
            ))}
          </div>
        </div>

        {/* Gallery grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products?.map((item, index) => (
            <Link
              to={`/product/${item.id}`}
              key={item.id}
              className="group relative animate-fade-up block"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Image container */}
              <div className="relative aspect-[3/4] rounded-2xl overflow-hidden bg-card mb-4">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-full object-cover transition-smooth group-hover:scale-105"
                />

                {/* Overlay on hover */}
                <div className="absolute inset-0 bg-foreground/0 group-hover:bg-foreground/20 transition-smooth" />

                {/* Quick actions */}
                <div className="absolute top-4 right-4 flex flex-col gap-2 opacity-0 translate-x-4 group-hover:opacity-100 group-hover:translate-x-0 transition-smooth">
                  <button
                    onClick={(e) => e.preventDefault()}
                    className="w-10 h-10 rounded-full bg-background/90 backdrop-blur-sm flex items-center justify-center shadow-soft hover:bg-background transition-smooth"
                  >
                    <Heart className="w-5 h-5 text-foreground" />
                  </button>
                  <button
                    onClick={(e) => e.preventDefault()}
                    className="w-10 h-10 rounded-full bg-background/90 backdrop-blur-sm flex items-center justify-center shadow-soft hover:bg-background transition-smooth"
                  >
                    <Eye className="w-5 h-5 text-foreground" />
                  </button>
                </div>

                {/* Try-on button */}
                <div className="absolute bottom-4 left-4 right-4 opacity-0 translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-smooth">
                  <Button variant="hero" className="w-full">
                    Try On Virtually
                  </Button>
                </div>

                {/* Category badge */}
                <div className="absolute top-4 left-4">
                  <span className="px-3 py-1 bg-background/90 backdrop-blur-sm text-foreground text-xs font-medium rounded-full">
                    {item.category}
                  </span>
                </div>
              </div>

              {/* Product info */}
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">{item.brand}</p>
                <h3 className="font-display text-lg font-medium text-foreground">{item.name}</h3>
                <p className="text-lg font-semibold text-foreground">${item.price}</p>
              </div>
            </Link>
          ))}
        </div>

        {/* View all button */}
        <div className="text-center mt-12">
          <Button variant="outline" size="lg">
            View All Collection
          </Button>
        </div>
      </div>
    </section>
  );
};

export default ClothingGallery;
