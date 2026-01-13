import { useState } from "react";
import { X, Upload, Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { toast } from "sonner";

interface VirtualTryOnModalProps {
    isOpen: boolean;
    onClose: () => void;
    productImage: string;
    productName: string;
    productId: number;
    selectedColor?: string;
    selectedSize?: string;
}

export const VirtualTryOnModal = ({
    isOpen,
    onClose,
    productImage,
    productName,
    productId,
    selectedColor,
    selectedSize,
}: VirtualTryOnModalProps) => {
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [resultImage, setResultImage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setSelectedImage(file);
            setPreviewUrl(URL.createObjectURL(file));
            setResultImage(null);
        }
    };

    const handleTryOn = async () => {
        if (!selectedImage) {
            toast.error("Please upload your photo first");
            return;
        }

        setLoading(true);
        setProgress(0);

        // Simulate progress for better UX
        const progressInterval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 90) {
                    clearInterval(progressInterval);
                    return 90;
                }
                return prev + 10;
            });
        }, 500);

        const formData = new FormData();
        formData.append("userImage", selectedImage);
        formData.append("productId", productId.toString());

        try {
            const response = await api.post("/try-on/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            clearInterval(progressInterval);
            setProgress(100);
            setResultImage(response.data.result_image);
            toast.success("Virtual try-on complete!");
        } catch (error) {
            clearInterval(progressInterval);
            console.error(error);
            toast.error("Failed to generate try-on result");
        } finally {
            setLoading(false);
            setTimeout(() => setProgress(0), 1000);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-background rounded-3xl shadow-elevated m-4">
                {/* Header */}
                <div className="sticky top-0 z-10 flex items-center justify-between p-6 bg-background border-b border-border">
                    <div>
                        <h2 className="font-display text-2xl font-medium">Virtual Try-On</h2>
                        <p className="text-sm text-muted-foreground mt-1">
                            {productName}
                            {selectedColor && ` • ${selectedColor}`}
                            {selectedSize && ` • Size ${selectedSize}`}
                        </p>
                    </div>
                    <button
                        onClick={onClose}
                        className="w-10 h-10 rounded-full hover:bg-muted flex items-center justify-center transition-smooth"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6">
                    <div className="grid md:grid-cols-2 gap-6">
                        {/* Upload Section */}
                        <div className="space-y-4">
                            <h3 className="font-medium text-lg">1. Upload Your Photo</h3>
                            <div
                                className={`relative aspect-[3/4] rounded-2xl overflow-hidden border-2 border-dashed transition-smooth ${previewUrl ? "border-primary" : "border-border hover:border-primary/50"
                                    }`}
                            >
                                <input
                                    type="file"
                                    id="photo-upload"
                                    className="hidden"
                                    accept="image/*"
                                    onChange={handleFileChange}
                                />

                                {previewUrl ? (
                                    <>
                                        <img src={previewUrl} alt="Your photo" className="w-full h-full object-cover" />
                                        <div className="absolute top-4 right-4">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => document.getElementById("photo-upload")?.click()}
                                            >
                                                Change
                                            </Button>
                                        </div>
                                    </>
                                ) : (
                                    <label
                                        htmlFor="photo-upload"
                                        className="absolute inset-0 flex flex-col items-center justify-center cursor-pointer p-8 text-center"
                                    >
                                        <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                                            <Upload className="w-8 h-8 text-primary" />
                                        </div>
                                        <h4 className="font-medium text-lg mb-2">Upload Your Photo</h4>
                                        <p className="text-sm text-muted-foreground">
                                            Take a full-body photo or upload an existing one
                                        </p>
                                    </label>
                                )}
                            </div>

                            {/* Product Preview */}
                            <div className="p-4 bg-muted rounded-xl">
                                <p className="text-sm font-medium mb-2">Trying On:</p>
                                <div className="flex items-center gap-3">
                                    <img src={productImage} alt={productName} className="w-16 h-20 object-cover rounded-lg" />
                                    <div>
                                        <p className="font-medium">{productName}</p>
                                        {selectedColor && <p className="text-sm text-muted-foreground">Color: {selectedColor}</p>}
                                        {selectedSize && <p className="text-sm text-muted-foreground">Size: {selectedSize}</p>}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Result Section */}
                        <div className="space-y-4">
                            <h3 className="font-medium text-lg">2. See the Result</h3>
                            <div className="relative aspect-[3/4] rounded-2xl overflow-hidden bg-muted">
                                {resultImage ? (
                                    <img src={resultImage} alt="Try-on result" className="w-full h-full object-cover" />
                                ) : (
                                    <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-center">
                                        <Sparkles className="w-12 h-12 text-muted-foreground mb-4" />
                                        <p className="text-muted-foreground">
                                            {loading ? "Generating your try-on..." : "Your result will appear here"}
                                        </p>
                                    </div>
                                )}

                                {/* Progress Bar */}
                                {loading && (
                                    <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/50 to-transparent">
                                        <div className="space-y-2">
                                            <div className="flex items-center justify-between text-white text-sm">
                                                <span>Processing...</span>
                                                <span>{progress}%</span>
                                            </div>
                                            <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-primary transition-all duration-300"
                                                    style={{ width: `${progress}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Action Button */}
                    <div className="mt-6">
                        <Button
                            variant="hero"
                            size="lg"
                            className="w-full"
                            onClick={handleTryOn}
                            disabled={!selectedImage || loading}
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                    Generating...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5 mr-2" />
                                    Generate Virtual Try-On
                                </>
                            )}
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};
