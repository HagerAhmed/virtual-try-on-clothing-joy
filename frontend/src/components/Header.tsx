import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ShoppingBag } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useCart } from "@/context/CartContext";
import { CartDrawer } from "./CartDrawer";

const Header = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  const { itemCount, setIsOpen } = useCart();

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border/50">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <a href="/" className="font-display text-2xl font-semibold tracking-tight text-foreground">
            Moda<span className="text-primary">.</span>
          </a>

          <nav className="hidden md:flex items-center gap-8">
            <a href="/#how-it-works" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth">
              How It Works
            </a>
            <a href="/#collection" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth">
              Collection
            </a>
            <a href="/#try-on" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth">
              Virtual Try-On
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="relative"
              onClick={() => setIsOpen(true)}
            >
              <ShoppingBag className="w-5 h-5" />
              {itemCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-primary text-primary-foreground text-[10px] font-bold w-4 h-4 flex items-center justify-center rounded-full">
                  {itemCount}
                </span>
              )}
            </Button>

            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium hidden sm:inline-block">
                  Hi, {user?.full_name?.split(' ')[0] || 'User'}
                </span>
                <Button variant="outline" size="sm" onClick={logout}>
                  Sign Out
                </Button>
              </div>
            ) : (
              <>
                <Button variant="ghost" size="sm" onClick={() => navigate("/login")}>
                  Sign In
                </Button>
                <Button variant="hero" size="sm" onClick={() => navigate("/signup")}>
                  Get Started
                </Button>
              </>
            )}
          </div>
        </div>
      </header>
      <CartDrawer />
    </>
  );
};

export default Header;
