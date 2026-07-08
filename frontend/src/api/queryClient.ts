import { QueryClient } from "@tanstack/react-query";


export const queryClient = new QueryClient(
    {
        defaultOptions:{
            queries:{
                retry:1,
                refetchOnWindowFocus:false,
                refetchOnReconnect: true,
                staleTime:1000*60,
                gcTime:5 * 60 * 1000,

            },
            mutations:{
                retry:0,
            
            }
        }
    }
)