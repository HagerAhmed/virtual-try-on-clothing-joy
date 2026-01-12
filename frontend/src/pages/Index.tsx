import Header from "@/components/Header";
import HeroSection from "@/components/HeroSection";
import HowItWorks from "@/components/HowItWorks";
import ClothingGallery from "@/components/ClothingGallery";
import TryOnSection from "@/components/TryOnSection";
import Footer from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <HowItWorks />
        <ClothingGallery />
        <TryOnSection />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
