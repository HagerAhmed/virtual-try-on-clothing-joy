import { Upload, Shirt, Wand2, ShoppingBag } from "lucide-react";

const steps = [
  {
    icon: Upload,
    step: "01",
    title: "Upload Your Photo",
    description: "Take a full-body photo or upload an existing one. Our AI works with any pose.",
  },
  {
    icon: Shirt,
    step: "02",
    title: "Browse & Select",
    description: "Explore our curated collection of clothing from top fashion brands.",
  },
  {
    icon: Wand2,
    step: "03",
    title: "AI Magic",
    description: "Watch as our AI instantly fits the clothing to your body with stunning accuracy.",
  },
  {
    icon: ShoppingBag,
    step: "04",
    title: "Shop with Confidence",
    description: "Love it? Add to cart knowing exactly how it will look on you.",
  },
];

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-24 lg:py-32 bg-card">
      <div className="container mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="inline-block px-4 py-1.5 bg-primary/10 text-primary text-sm font-medium rounded-full mb-4">
            How It Works
          </span>
          <h2 className="font-display text-4xl md:text-5xl font-medium tracking-tight mb-4">
            Your Perfect Fit in
            <span className="text-gradient"> Four Steps</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            Our AI-powered technology makes virtual try-on effortless and accurate.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div 
              key={index} 
              className="group relative bg-background rounded-2xl p-8 shadow-soft hover:shadow-elevated transition-smooth border border-border/50 hover:border-primary/20"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Step number */}
              <span className="absolute top-6 right-6 font-display text-5xl font-bold text-muted/30">
                {step.step}
              </span>
              
              {/* Icon */}
              <div className="relative z-10 w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:bg-primary group-hover:scale-110 transition-smooth">
                <step.icon className="w-7 h-7 text-primary group-hover:text-primary-foreground transition-smooth" />
              </div>
              
              {/* Content */}
              <h3 className="font-display text-xl font-medium mb-2 text-foreground">
                {step.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">
                {step.description}
              </p>
              
              {/* Connector line (hidden on last item) */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 w-8 h-0.5 bg-border" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
