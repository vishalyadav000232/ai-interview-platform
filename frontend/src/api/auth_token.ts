let accessToken: string | null = null;

export const setAccessToken = (token: string) => {
    accessToken = token;
    console.log("Token saved:", accessToken);
};

export const getAccessToken = () => {
    console.log("Token returned:", accessToken);
    return accessToken;
};

export const clearAccessToken = () => {
    accessToken = null;
};
