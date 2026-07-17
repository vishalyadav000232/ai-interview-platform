import type { PropsWithChildren } from "react";

import { useCurrentUser } from "../features/auth/hooks/useCurrentUser";

export function AuthBootstrap({
    children,
}: PropsWithChildren) {

    useCurrentUser();

    return <>{children}</>;
}
