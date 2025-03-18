namespace Backend.Services
{
    public interface ISecureService
    {
        string GetSecureMessage();
    }

    public class SecureService : ISecureService
    {
        public string GetSecureMessage()
        {
            return "This is a secure message from the service!";
        }
    }

}
