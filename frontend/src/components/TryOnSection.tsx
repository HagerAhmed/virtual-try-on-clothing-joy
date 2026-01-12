import { useState, useRef } from "react";
import { Upload, Camera, RefreshCw, Download, Share2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import heroModel from "@/assets/hero-model.jpg";
import clothing1 from "@/assets/clothing-1.jpg";
import clothing2 from "@/assets/clothing-2.jpg";
import clothing3 from "@/assets/clothing-3.jpg";
import api from "@/lib/api";
import { toast } from "sonner";

const TryOnSection = () => {
  const [selectedClothing, setSelectedClothing] = useState(0);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const clothingOptions = [
    { id: 0, image: clothing1, name: "Silk Blouse" },
    { id: 1, image: clothing2, name: "Camel Blazer" },
    { id: 2, image: clothing3, name: "Midi Dress" },
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      // Reset result when new image is uploaded
      setResultImage(null);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleTryOn = async () => {
    if (!selectedImage) {
      toast.error("Please upload an image first");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("userImage", selectedImage);
    formData.append("productId", selectedClothing.toString());

    try {
      const response = await api.post("/try-on/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResultImage(response.data.result_image);
      toast.success("Virtual try-on complete!");
    } catch (error) {
      console.error(error);
      toast.error("Failed to generate try-on result");
    } finally {
      setLoading(false);
    }
  };

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
              <div
                className="relative aspect-[3/4] rounded-3xl overflow-hidden bg-muted border-2 border-dashed border-border hover:border-primary/50 transition-smooth group"
                onClick={!previewUrl ? handleUploadClick : undefined}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  accept="image/*"
                  onChange={handleFileChange}
                />

                {previewUrl ? (
                  <img src={previewUrl} alt="User upload" className="w-full h-full object-cover" />
                ) : (
                  /* Placeholder / Upload state */
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
                      <Button variant="hero" onClick={handleUploadClick}>
                        <Upload className="w-4 h-4 mr-2" />
                        Upload Photo
                      </Button>
                    </div>
                  </div>
                )}

                {previewUrl && (
                  <div className="absolute top-4 right-4">
                    <Button variant="outline" size="sm" onClick={handleUploadClick}>Change</Button>
                  </div>
                )}
              </div>

              <Button
                variant="hero"
                size="lg"
                className="w-full"
                onClick={handleTryOn}
                disabled={!selectedImage || loading}
              >
                {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <RefreshCw className="w-4 h-4 mr-2" />}
                Generate Try-On
              </Button>
            </div>

            {/* Result preview */}
            <div className="space-y-6">
              <div className="relative aspect-[3/4] rounded-3xl overflow-hidden bg-muted shadow-elevated">
                <img
                  src={resultImage || heroModel}
                  alt="Virtual try-on result"
                  className="w-full h-full object-cover"
                />

                {/* Overlay indicator */}
                <div className="absolute top-4 left-4 px-4 py-2 bg-background/90 backdrop-blur-sm rounded-full flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                  <span className="text-sm font-medium text-foreground">
                    {resultImage ? "AI Generated" : "AI Preview"}
                  </span>
                </div>

                {/* Action buttons */}
                <div className="absolute bottom-4 left-4 right-4 flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1 bg-background/90 backdrop-blur-sm" onClick={handleTryOn} disabled={loading || !selectedImage}>
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
                      className={`relative w-20 h-24 rounded-xl overflow-hidden transition-smooth ${selectedClothing === item.id
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
