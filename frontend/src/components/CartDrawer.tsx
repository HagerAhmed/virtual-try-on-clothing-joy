import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { ShoppingBag, Minus, Plus, X, Trash2 } from "lucide-react";
import { useCart } from "@/context/CartContext";
import { useNavigate } from "react-router-dom";

export function CartDrawer() {
    const { cart, isOpen, setIsOpen, removeFromCart, isLoading } = useCart();
    const navigate = useNavigate();

    const handleCheckout = () => {
        setIsOpen(false);
        navigate("/checkout");
    };

    return (
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetContent className="flex flex-col w-full sm:max-w-lg">
                <SheetHeader>
                    <SheetTitle className="flex items-center gap-2 font-display text-2xl">
                        <ShoppingBag className="w-5 h-5" />
                        Your Bag ({cart?.items.length || 0})
                    </SheetTitle>
                </SheetHeader>

                {!cart?.items.length ? (
                    <div className="flex-1 flex flex-col items-center justify-center space-y-4">
                        <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center">
                            <ShoppingBag className="w-8 h-8 text-muted-foreground" />
                        </div>
                        <div className="text-center">
                            <h3 className="font-medium text-lg">Your bag is empty</h3>
                            <p className="text-muted-foreground">Looks like you haven't added anything yet.</p>
                        </div>
                        <Button variant="outline" onClick={() => setIsOpen(false)}>
                            Continue Shopping
                        </Button>
                    </div>
                ) : (
                    <>
                        <ScrollArea className="flex-1 pr-4 -mr-4">
                            <div className="space-y-6 py-6">
                                {cart.items.map((item) => (
                                    <div key={item.id} className="flex gap-4">
                                        <div className="w-24 h-32 rounded-lg overflow-hidden bg-muted flex-shrink-0">
                                            <img
                                                src={item.product.image}
                                                alt={item.product.name}
                                                className="w-full h-full object-cover"
                                            />
                                        </div>
                                        <div className="flex-1 flex flex-col">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <h4 className="font-medium line-clamp-1">{item.product.name}</h4>
                                                    <p className="text-sm text-muted-foreground">{item.product.brand}</p>
                                                </div>
                                                <button
                                                    onClick={() => removeFromCart(item.id)}
                                                    className="text-muted-foreground hover:text-destructive transition-colors"
                                                    disabled={isLoading}
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>

                                            <div className="mt-2 space-y-1">
                                                <p className="text-sm text-muted-foreground">Size: {item.size}</p>
                                                <p className="text-sm text-muted-foreground">Color: {item.color}</p>
                                            </div>

                                            <div className="flex-1 flex items-end justify-between mt-2">
                                                <div className="flex items-center border rounded-md h-8">
                                                    {/* Quantity controls could be added here later */}
                                                    <span className="px-3 text-sm font-medium">{item.quantity}</span>
                                                </div>
                                                <p className="font-medium">${(item.product.price * item.quantity).toFixed(2)}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </ScrollArea>

                        <div className="space-y-4 pt-6 border-t bg-background">
                            <div className="space-y-2">
                                <div className="flex justify-between text-base font-medium">
                                    <p>Subtotal</p>
                                    <p>${cart.total.toFixed(2)}</p>
                                </div>
                                <p className="text-xs text-muted-foreground">
                                    Shipping and taxes calculated at checkout.
                                </p>
                            </div>
                            <Button className="w-full h-12 text-lg" onClick={handleCheckout}>
                                Checkout
                            </Button>
                        </div>
                    </>
                )}
            </SheetContent>
        </Sheet>
    );
}
