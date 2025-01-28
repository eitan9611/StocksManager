using Backend.Models;
using Backend.Services;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class StocksController : ControllerBase
    {
        private readonly StockService _stockService;

        public StocksController(StockService stockService)
        {
            _stockService = stockService;
        }

        [HttpGet]
        public async Task<IActionResult> GetStocks()
        {
            return Ok(await _stockService.GetAllStocks());
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetStock(int id)
        {
            var stock = await _stockService.GetStockById(id);
            if (stock == null) return NotFound();
            return Ok(stock);
        }

        [HttpPost]
        public async Task<IActionResult> AddStock([FromBody] Stock stock)
        {
            return Ok(await _stockService.AddStock(stock));
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateStock(int id, [FromBody] Stock stock)
        {
            stock.Id = id;
            var success = await _stockService.UpdateStock(stock);
            if (!success) return NotFound();
            return Ok();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteStock(int id)
        {
            var success = await _stockService.DeleteStock(id);
            if (!success) return NotFound();
            return Ok();
        }
    }
}
