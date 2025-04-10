using System.ComponentModel.DataAnnotations;

namespace Backend.Models
{
    public class Trade
    {
        public string UserEmail { get; set; } // מזהה המשתמש שמבצע את הפעולה
        public string Symbol { get; set; } // סימבול של המניה
        public int Quantity { get; set; } // כמות מניות
        public decimal Price { get; set; } // מחיר בזמן הביצוע
        public TradeType Type { get; set; } // קנייה/מכירה
        [Key]
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }

    public enum TradeType
    {
        Buy,
        Sell
    }

}
