import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { Product } from "@/data/products";

export const useProducts = (category?: string) => {
    return useQuery({
        queryKey: ["products", category],
        queryFn: async () => {
            const params = category && category !== "All" ? { category } : {};
            const response = await api.get<Product[]>("/products", { params });
            return response.data;
        },
    });
};

export const useProduct = (id?: number | string) => {
    return useQuery({
        queryKey: ["product", id],
        queryFn: async () => {
            if (!id) return null;
            const response = await api.get<Product>(`/products/${id}`);
            return response.data;
        },
        enabled: !!id,
    });
};
