using Backend.Data;
using Backend.Models;
using Microsoft.EntityFrameworkCore;



namespace Backend.Services
{
    public class TradeService
    {
        private readonly AppDbContext _context;
        private readonly StockService _stockService;

        public TradeService(AppDbContext context, StockService stockService)
        {
            _context = context;
            _stockService = stockService;
        }

        public async Task<bool> BuyStockAsync(string userEmail, string symbol, int quantity)
        {
            var user = await _context.Users.Include(u => u.Portfolio).FirstOrDefaultAsync(u => u.Email == userEmail);
            var stock = new Stock { Id = 0, Name = "Eitan", Symbol = symbol, Price = 3 };//await _stockService.GetStockBySymbolAsync(symbol); // קריאה ל-Yahoo Finance

            if (user == null || stock == null || quantity <= 0) return false;

            decimal totalCost = stock.Price * quantity;
            if (user.Balance < totalCost) return false;

            // עדכון יתרה ופורטפוליו
            user.Balance -= totalCost;
            var userStock = user.Portfolio.FirstOrDefault(us => us.Symbol == stock.Symbol);
            if (userStock == null)
            {
                user.Portfolio.Add(new UserStock {UserEmail = user.Email, Symbol = stock.Symbol, Quantity = quantity, BuyPrice = stock.Price });
            }
            else
            {
                userStock.Quantity += quantity;
            }

            // יצירת עסקה
            _context.Add(new Trade { UserEmail = userEmail, Symbol = symbol, Quantity = quantity, Price = stock.Price, Type = TradeType.Buy });
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> SellStockAsync(string userEmail, string symbol, int quantity)
        {
            var user = await _context.Users.Include(u => u.Portfolio).FirstOrDefaultAsync(u => u.Email == userEmail);
            var stock = new Stock { Id = 0, Name = "Eitan", Symbol = symbol, Price = 3 };//await _stockService.GetStockBySymbolAsync(symbol); // קריאה ל-Yahoo Finance

            if (user == null || stock == null || quantity <= 0) return false;

            var userStock = user.Portfolio.FirstOrDefault(us => us.Symbol == stock.Symbol);
            if (userStock == null || userStock.Quantity < quantity) return false;

            decimal totalRevenue = stock.Price * quantity;
            user.Balance += totalRevenue;

            userStock.Quantity -= quantity;
            if (userStock.Quantity == 0)
            {
                user.Portfolio.Remove(userStock);
            }

            // יצירת עסקה
            _context.Add(new Trade { UserEmail = userEmail, Symbol = symbol, Quantity = quantity, Price = stock.Price, Type = TradeType.Sell });
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<List<Trade>> GetUserTradesAsync(string userEmail)
        {
            return await _context.Set<Trade>().Where(t => t.UserEmail == userEmail).OrderByDescending(t => t.Timestamp).ToListAsync();
        }
    }

}
