using System.ComponentModel.DataAnnotations;

namespace Backend.Models
{
    public class UserStock
    {
        public string UserEmail { get; set; }
        public string Symbol { get; set; } = string.Empty;
        public int Quantity { get; set; }
        public decimal BuyPrice { get; set; }
    }
    public class User
    {
        [Key]
        public string Email { get; set; } = string.Empty;
        public decimal Balance { get; set; } = 10000; // יתרה ראשונית ברירת מחדל

        public List<UserStock> Portfolio { get; set; } = new List<UserStock>();
    }
}