from abc import ABC , abstractmethod


class EmailServiceInterface(ABC):
    
    @abstractmethod
    async def send_email_verification(self , email : str , verification_link : str)-> None:
        raise NotImplementedError
    @abstractmethod
    async def send_password_reset_email(self,email: str,reset_link: str) -> None:
        raise NotImplementedError