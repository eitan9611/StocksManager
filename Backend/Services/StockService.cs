﻿using Backend.Data;
using Backend.Models;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json.Linq;
using YahooFinanceApi;


namespace Backend.Services
{
    public class StockService
    {
        private readonly AppDbContext _context;

        public StockService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<List<Stock>> GetAllStocks()
        {
            return await _context.Stocks.ToListAsync();
        }

        public async Task<Stock?> GetStockById(int id)
        {
            return await _context.Stocks.FindAsync(id);
        }

        public async Task<Stock> AddStock(Stock stock)
        {
            stock.Id = 0; // Ensure that ID is not explicitly set
            _context.Stocks.Add(stock);
            await _context.SaveChangesAsync();
            return stock;
        }

        public async Task<bool> UpdateStock(Stock stock)
        {
            var existingStock = await _context.Stocks.FindAsync(stock.Id);
            if (existingStock == null) return false;

            existingStock.Price = stock.Price;
            existingStock.LastUpdated = DateTime.UtcNow;
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> DeleteStock(int id)
        {
            var stock = await _context.Stocks.FindAsync(id);
            if (stock == null) return false;

            _context.Stocks.Remove(stock);
            await _context.SaveChangesAsync();
            return true;
        }
        public async Task<decimal> GetStockPriceAsync(string symbol)
        {
            try
            {
                Console.WriteLine("im here1");
                var securities = await Yahoo.Symbols(symbol).Fields(Field.RegularMarketPrice).QueryAsync();
                foreach (var kvp in securities)
                {
                    Console.WriteLine($"Symbol: {kvp.Key}, Price: {kvp.Value.RegularMarketPrice}");
                    return Convert.ToDecimal(kvp.Value.RegularMarketPrice);
                }
                return 0;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error fetching stock price: {ex.Message}");
                return -1; // Handle errors appropriately
            }
        }

    }
}
