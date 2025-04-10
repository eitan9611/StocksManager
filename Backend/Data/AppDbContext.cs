using Microsoft.EntityFrameworkCore;
using Backend.Models;

namespace Backend.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Stock> Stocks { get; set; }
        public DbSet<User> Users { get; set; }
        public DbSet<UserStock> UserStocks { get; set; }
        public DbSet<Trade> Trades { get; set; }



        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // קשר בין משתמש למניות שהוא מחזיק
            modelBuilder.Entity<UserStock>()
                .HasOne<User>()
                .WithMany(u => u.Portfolio)
                .HasForeignKey(us => us.UserEmail);
        }
    }
}
