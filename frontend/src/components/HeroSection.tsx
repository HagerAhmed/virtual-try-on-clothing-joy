import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles } from "lucide-react";
import heroModel from "@/assets/hero-model.jpg";

const HeroSection = () => {
  return (
    <section className="relative min-h-screen bg-gradient-hero overflow-hidden pt-20">
      {/* Decorative elements */}
      <div className="absolute top-40 left-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
      
      <div className="container mx-auto px-6 py-20 lg:py-32">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left content */}
          <div className="order-2 lg:order-1 space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-muted rounded-full border border-border animate-fade-up">
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-muted-foreground">AI-Powered Virtual Fitting</span>
            </div>
            
            <h1 className="font-display text-5xl md:text-6xl lg:text-7xl font-medium leading-[1.1] tracking-tight animate-fade-up" style={{ animationDelay: "0.1s" }}>
              Try Before You
              <span className="block text-gradient">Buy, Virtually</span>
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground max-w-lg animate-fade-up" style={{ animationDelay: "0.2s" }}>
              Experience fashion like never before. Upload your photo and see how any piece looks on you — instantly.
            </p>
            
            <div className="flex flex-wrap items-center gap-4 animate-fade-up" style={{ animationDelay: "0.3s" }}>
              <Button variant="hero" size="xl">
                Start Trying On
                <ArrowRight className="w-5 h-5" />
              </Button>
              <Button variant="outline" size="xl">
                View Collection
              </Button>
            </div>
            
            {/* Stats */}
            <div className="flex items-center gap-8 pt-6 animate-fade-up" style={{ animationDelay: "0.4s" }}>
              <div>
                <div className="font-display text-3xl font-semibold text-foreground">50K+</div>
                <div className="text-sm text-muted-foreground">Try-ons daily</div>
              </div>
              <div className="w-px h-12 bg-border" />
              <div>
                <div className="font-display text-3xl font-semibold text-foreground">98%</div>
                <div className="text-sm text-muted-foreground">Accuracy rate</div>
              </div>
              <div className="w-px h-12 bg-border" />
              <div>
                <div className="font-display text-3xl font-semibold text-foreground">500+</div>
                <div className="text-sm text-muted-foreground">Fashion brands</div>
              </div>
            </div>
          </div>
          
          {/* Right image */}
          <div className="order-1 lg:order-2 relative animate-scale-in">
            <div className="relative aspect-[4/5] rounded-3xl overflow-hidden shadow-elevated">
              <img 
                src={heroModel} 
                alt="Fashion model showcasing virtual try-on" 
                className="w-full h-full object-cover"
              />
              
              {/* Floating UI overlay */}
              <div className="absolute bottom-6 left-6 right-6 bg-background/90 backdrop-blur-md rounded-2xl p-4 shadow-soft border border-border/50">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-primary" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-foreground">AI Fit Analysis</div>
                    <div className="text-xs text-muted-foreground">Perfect fit detected • Size M recommended</div>
                  </div>
                  <div className="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">
                    98% Match
                  </div>
                </div>
              </div>
            </div>
            
            {/* Decorative badge */}
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-primary rounded-full flex items-center justify-center shadow-glow animate-float">
              <span className="text-primary-foreground font-display text-sm font-semibold text-center leading-tight">
                Try It<br />Free
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
