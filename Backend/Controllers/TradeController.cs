﻿using Backend.Services;
using Backend.Models;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace Backend.Controllers
{
    [Route("api/trade")]
    [ApiController]
    public class TradeController : ControllerBase
    {
        private readonly TradeService _tradeService;

        public TradeController(TradeService tradeService)
        {
            _tradeService = tradeService;
        }

        [HttpPost("buy")]
        [ProducesResponseType(200)]
        [ProducesResponseType(400)]
        public async Task<IActionResult> BuyStock([FromBody] TradeRequest request)
        {
            if (request == null || string.IsNullOrEmpty(request.Symbol) || request.Quantity <= 0)
                return BadRequest("Invalid request parameters.");

            var success = await _tradeService.BuyStockAsync(request.Email,request.Symbol, request.Quantity);
            Console.WriteLine(success);
            return success ? Ok("Stock purchased successfully.") : BadRequest("Transaction failed.");
        }

        [HttpPost("sell")]
        [ProducesResponseType(200)]
        [ProducesResponseType(400)]
        public async Task<IActionResult> SellStock([FromBody] TradeRequest request)
        {
            if (request == null || string.IsNullOrEmpty(request.Symbol) || request.Quantity <= 0)
                return BadRequest("Invalid request parameters.");

            var success = await _tradeService.SellStockAsync(request.Email,request.Symbol, request.Quantity);
            Console.WriteLine(success);
            return success ? Ok("Stock sold successfully.") : BadRequest("Transaction failed.");
        }

        [HttpGet("trades/{email}")]
        [ProducesResponseType(200)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> GetTradesByUser(string email)
        {
            if (string.IsNullOrEmpty(email))
                return BadRequest("Email is required.");

            var trades = await _tradeService.GetUserTradesAsync(email);
            if (trades == null || !trades.Any())
                return NotFound("No trades found for the specified user.");

            return Ok(trades);
        }

    }

    public class TradeRequest
    {
        public string Email { get; set; }
        public string Symbol { get; set; }
        public int Quantity { get; set; }
    }
}
