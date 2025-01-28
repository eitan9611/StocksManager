namespace Backend.Models
{
    public class Stock
    {
        public int Id { get; set; }
        public string Name { get; set; }  // שם המניה
        public string Symbol { get; set; } // סימול (למשל: AAPL)
        public decimal Price { get; set; } // מחיר נוכחי
        public DateTime LastUpdated { get; set; } = DateTime.UtcNow;
    }
}
