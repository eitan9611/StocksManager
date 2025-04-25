using Backend.Data;
using Backend.Models;
using Microsoft.EntityFrameworkCore;


public class UserService
{
    private readonly AppDbContext _context;

    public UserService(AppDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetUserByIdAsync(string userEmail)
    {
        return await _context.Users.Include(u => u.Portfolio).FirstOrDefaultAsync(u => u.Email == userEmail);
    }

    public async Task<bool> UpdateBalanceAsync(string userEmail, decimal amount)
    {
        var user = await _context.Users.FindAsync(userEmail);
        if (user == null) return false;

        user.Balance += amount;
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> AddUserAsync(string userEmail)
    {
        var user = await _context.Users.FindAsync(userEmail);
        if (user != null) return false;

        User new_user = new User { Email = userEmail, Balance = 10000};

        _context.Users.Add(new_user);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<List<User>> GetAllUsersAsync()
    {
        return await _context.Users.ToListAsync();
    }
    public async Task ShowAllUsersAsync()
    {
        var users = await _context.Users.ToListAsync();
        if (users.Count == 0)
        {
            Console.WriteLine("No users found.");
            return;
        }

        foreach (var user in users)
        {
            Console.WriteLine($"User: {user.Email}, Balance: {user.Balance}");
        }
    }

}
