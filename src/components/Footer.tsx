import { Instagram, Twitter, Facebook, Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-foreground text-background py-16">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
          {/* Brand */}
          <div className="space-y-4">
            <a href="/" className="font-display text-2xl font-semibold tracking-tight">
              Moda<span className="text-primary">.</span>
            </a>
            <p className="text-background/70 leading-relaxed">
              Revolutionizing the way you shop for fashion with AI-powered virtual try-on technology.
            </p>
            <div className="flex gap-4">
              <a href="#" className="w-10 h-10 rounded-full bg-background/10 flex items-center justify-center hover:bg-background/20 transition-smooth">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-background/10 flex items-center justify-center hover:bg-background/20 transition-smooth">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-background/10 flex items-center justify-center hover:bg-background/20 transition-smooth">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-background/10 flex items-center justify-center hover:bg-background/20 transition-smooth">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h4 className="font-display font-medium text-lg mb-4">Quick Links</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Home</a></li>
              <li><a href="#how-it-works" className="text-background/70 hover:text-background transition-smooth">How It Works</a></li>
              <li><a href="#collection" className="text-background/70 hover:text-background transition-smooth">Collection</a></li>
              <li><a href="#try-on" className="text-background/70 hover:text-background transition-smooth">Virtual Try-On</a></li>
            </ul>
          </div>
          
          {/* Company */}
          <div>
            <h4 className="font-display font-medium text-lg mb-4">Company</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">About Us</a></li>
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Careers</a></li>
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Press</a></li>
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Contact</a></li>
            </ul>
          </div>
          
          {/* Legal */}
          <div>
            <h4 className="font-display font-medium text-lg mb-4">Legal</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Privacy Policy</a></li>
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Terms of Service</a></li>
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">Cookie Policy</a></li>
              <li><a href="#" className="text-background/70 hover:text-background transition-smooth">GDPR</a></li>
            </ul>
          </div>
        </div>
        
        {/* Bottom bar */}
        <div className="pt-8 border-t border-background/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-background/50 text-sm">
            © 2025 Moda. All rights reserved.
          </p>
          <p className="text-background/50 text-sm">
            Made with AI-powered fashion technology
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
