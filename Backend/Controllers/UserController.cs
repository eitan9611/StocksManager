using Backend.Models;
using Microsoft.AspNetCore.Mvc;

[Route("api/[controller]")]
[ApiController]
public class UserController : ControllerBase
{
    private readonly UserService _userService;

    public UserController(UserService userService)
    {
        _userService = userService;
    }

    [HttpGet("{email}")]
    public async Task<IActionResult> GetUser(string email)
    {
        var user = await _userService.GetUserByIdAsync(email);
        return user != null ? Ok(user) : NotFound("User not found.");
    }

    [HttpPost("create/{userEmail}")]
    public async Task<IActionResult> CreateUser(string userEmail)
    {
        var success = await _userService.AddUserAsync(userEmail);
        return success ? Ok("User created.") : BadRequest("Failed to create user.");
    }

    [HttpPut("balance/{userEmail}")]
    public async Task<IActionResult> UpdateBalance(string userEmail, [FromBody] decimal amount)
    {
        var success = await _userService.UpdateBalanceAsync(userEmail, amount);
        return success ? Ok("Balance updated.") : BadRequest("Failed to update balance.");
    }
    [HttpGet("get_all_users")]
    public async Task<ActionResult<List<User>>> GetAllUsers()
    {
        var users = await _userService.GetAllUsersAsync();
        return Ok(users);
    }
}
