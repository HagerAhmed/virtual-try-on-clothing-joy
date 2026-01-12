import { useState } from "react";
import { Upload, Camera, RefreshCw, Download, Share2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import heroModel from "@/assets/hero-model.jpg";
import clothing1 from "@/assets/clothing-1.jpg";
import clothing2 from "@/assets/clothing-2.jpg";
import clothing3 from "@/assets/clothing-3.jpg";

const TryOnSection = () => {
  const [selectedClothing, setSelectedClothing] = useState(0);
  
  const clothingOptions = [
    { id: 0, image: clothing1, name: "Silk Blouse" },
    { id: 1, image: clothing2, name: "Camel Blazer" },
    { id: 2, image: clothing3, name: "Midi Dress" },
  ];
  
  return (
    <section id="try-on" className="py-24 lg:py-32 bg-card">
      <div className="container mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="inline-block px-4 py-1.5 bg-primary/10 text-primary text-sm font-medium rounded-full mb-4">
            Virtual Try-On
          </span>
          <h2 className="font-display text-4xl md:text-5xl font-medium tracking-tight mb-4">
            See It On <span className="text-gradient">You</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            Upload your photo and watch our AI work magic. Experience clothes before buying.
          </p>
        </div>
        
        <div className="max-w-5xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-8 lg:gap-12">
            {/* Upload / Preview area */}
            <div className="space-y-6">
              <div className="relative aspect-[3/4] rounded-3xl overflow-hidden bg-muted border-2 border-dashed border-border hover:border-primary/50 transition-smooth group">
                {/* Placeholder / Upload state */}
                <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-center cursor-pointer">
                  <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-smooth">
                    <Upload className="w-10 h-10 text-primary" />
                  </div>
                  <h3 className="font-display text-xl font-medium text-foreground mb-2">
                    Upload Your Photo
                  </h3>
                  <p className="text-muted-foreground mb-6 max-w-xs">
                    Take a full-body photo or drag and drop an existing one
                  </p>
                  <div className="flex gap-3">
                    <Button variant="hero">
                      <Upload className="w-4 h-4" />
                      Upload Photo
                    </Button>
                    <Button variant="outline">
                      <Camera className="w-4 h-4" />
                      Take Photo
                    </Button>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Result preview */}
            <div className="space-y-6">
              <div className="relative aspect-[3/4] rounded-3xl overflow-hidden bg-muted shadow-elevated">
                <img 
                  src={heroModel} 
                  alt="Virtual try-on result"
                  className="w-full h-full object-cover"
                />
                
                {/* Overlay indicator */}
                <div className="absolute top-4 left-4 px-4 py-2 bg-background/90 backdrop-blur-sm rounded-full flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                  <span className="text-sm font-medium text-foreground">AI Preview</span>
                </div>
                
                {/* Action buttons */}
                <div className="absolute bottom-4 left-4 right-4 flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1 bg-background/90 backdrop-blur-sm">
                    <RefreshCw className="w-4 h-4" />
                    Regenerate
                  </Button>
                  <Button variant="outline" size="sm" className="bg-background/90 backdrop-blur-sm">
                    <Download className="w-4 h-4" />
                  </Button>
                  <Button variant="outline" size="sm" className="bg-background/90 backdrop-blur-sm">
                    <Share2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              
              {/* Clothing selector */}
              <div className="space-y-4">
                <h4 className="font-medium text-foreground">Select an item to try on:</h4>
                <div className="flex gap-4">
                  {clothingOptions.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => setSelectedClothing(item.id)}
                      className={`relative w-20 h-24 rounded-xl overflow-hidden transition-smooth ${
                        selectedClothing === item.id 
                          ? "ring-2 ring-primary ring-offset-2 ring-offset-card scale-105" 
                          : "opacity-70 hover:opacity-100"
                      }`}
                    >
                      <img 
                        src={item.image} 
                        alt={item.name}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                  <button className="w-20 h-24 rounded-xl border-2 border-dashed border-border hover:border-primary/50 flex items-center justify-center transition-smooth">
                    <span className="text-2xl text-muted-foreground">+</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TryOnSection;
