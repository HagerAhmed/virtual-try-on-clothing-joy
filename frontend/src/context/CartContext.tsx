import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import api from "@/lib/api";
import { useAuth } from "./AuthContext";
import { toast } from "sonner";

export interface CartItem {
    id: number;
    product: {
        id: number;
        name: string;
        price: number;
        image: string;
        brand: string;
    };
    quantity: number;
    size: string;
    color: string;
}

interface Cart {
    id: number;
    items: CartItem[];
    total: number;
}

interface CartContextType {
    cart: Cart | null;
    isLoading: boolean;
    isOpen: boolean;
    setIsOpen: (open: boolean) => void;
    addToCart: (productId: number, size: string, color: string, quantity?: number) => Promise<void>;
    removeFromCart: (itemId: number) => Promise<void>;
    itemCount: number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider = ({ children }: { children: ReactNode }) => {
    const [cart, setCart] = useState<Cart | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const { isAuthenticated } = useAuth();

    // Fetch cart when authenticated
    useEffect(() => {
        if (isAuthenticated) {
            fetchCart();
        } else {
            setCart(null);
        }
    }, [isAuthenticated]);

    const fetchCart = async () => {
        setIsLoading(true);
        try {
            const response = await api.get("/cart");
            setCart(response.data);
        } catch (error) {
            console.error("Failed to fetch cart:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const addToCart = async (productId: number, size: string, color: string, quantity: number = 1) => {
        if (!isAuthenticated) {
            toast.error("Please sign in to add items to cart");
            return;
        }

        try {
            setIsLoading(true);
            const response = await api.post("/cart/items", {
                product_id: productId,
                quantity,
                size,
                color
            });
            setCart(response.data);
            setIsOpen(true); // Open drawer on success
            toast.success("Added to cart");
        } catch (error) {
            console.error("Failed to add to cart:", error);
            toast.error("Failed to add item to cart");
        } finally {
            setIsLoading(false);
        }
    };

    const removeFromCart = async (itemId: number) => {
        try {
            setIsLoading(true);
            const response = await api.delete(`/cart/items/${itemId}`);
            setCart(response.data);
            toast.success("Item removed");
        } catch (error) {
            console.error("Failed to remove from cart:", error);
            toast.error("Failed to remove item");
        } finally {
            setIsLoading(false);
        }
    };

    const itemCount = cart?.items.reduce((acc, item) => acc + item.quantity, 0) || 0;

    return (
        <CartContext.Provider
            value={{
                cart,
                isLoading,
                isOpen,
                setIsOpen,
                addToCart,
                removeFromCart,
                itemCount
            }}
        >
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (context === undefined) {
        throw new Error("useCart must be used within a CartProvider");
    }
    return context;
};
