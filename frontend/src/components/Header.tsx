import { Button } from "@/components/ui/button";

const Header = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border/50">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <a href="/" className="font-display text-2xl font-semibold tracking-tight text-foreground">
          Moda<span className="text-primary">.</span>
        </a>
        
        <nav className="hidden md:flex items-center gap-8">
          <a href="#how-it-works" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth">
            How It Works
          </a>
          <a href="#collection" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth">
            Collection
          </a>
          <a href="#try-on" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth">
            Virtual Try-On
          </a>
        </nav>
        
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm">
            Sign In
          </Button>
          <Button variant="hero" size="sm">
            Get Started
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
