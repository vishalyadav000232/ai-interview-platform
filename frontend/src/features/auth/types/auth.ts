export type UserRole = "STUDENT" | "ADMIN";

export type AuthUser = {
    id: string
    first_name : string,
    last_name : string
    email: string
    role: UserRole
    is_email_verified: boolean
    is_active: boolean
    created_at: string

}

export type LoginPayload = {
    email: string
    password: string
}

export type RegisterPayload = {
    first_name:string,
    last_name : string,
    email: string
    password: string
}

type DataRespone = {
    user : AuthUser,
    access_token : string
    verification_link : string
}

export type RegisterResponse = {
    success : boolean,
    message: string
    data: DataRespone
}

export type CurrentUserResponse = {
    user: AuthUser
}

export type LoginResponse = {
    success: boolean;
    message: string;
    access_token: string;
    token_type: "bearer";
    data: {
        user: AuthUser;
        access_token: string;
        token_type: "bearer";
    };
};


export type AuthState = {
    user: AuthUser | null;

    isAuthenticated: boolean;

    isLoading: boolean;

    setUser(user: AuthUser): void;

    clearUser(): void;

    setLoading(value: boolean): void;
}
